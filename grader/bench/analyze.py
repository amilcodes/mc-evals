"""Per-run measurements for a benchmark wave: score over time, cost and test calls.

    python3 bench/analyze.py ../runs/bench/w1/manifest.json [--score]

Reads each run's server log (tool calls with wall-clock times) and its agent transcript
(every model call with token usage), and writes summary.json next to the manifest:

- curve: one point per test call, with minutes since the agent's first tool call, the
  API-equivalent cost so far, and the best valid volume so far;
- totals: tokens by kind, API-equivalent cost, calls by tool, lab ticks, rounds;
- final: the final-test verdict from `pdgrader score` (with --score; cached in result.json).

Costs use API list prices (see PRICES). They are what the same tokens would cost on the
Claude API, not what was billed in this session.
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pdgrader import references  # noqa: E402

# $ per million tokens: input, 5-minute cache write, 1-hour cache write, cache read, output.
# From the claude-api reference (cached 2026-11-03). Haiku 5.5: rates are five times higher above
# 100K-token prompts ($0.50 / $2.50); its cache-read rate is not published there, so 0.1x input
# is assumed.
PRICES = {
    "claude-fable-5-2": {"in": 8.0, "w5": 10.0, "w1h": 16.0, "read": 0.20, "out": 40.0},
    "claude-opus-5-5": {"in": 4.0, "w5": 5.0, "w1h": 8.0, "read": 0.20, "out": 20.0},
    "claude-sonnet-5-5": {"in": 2.0, "w5": 2.5, "w1h": 4.0, "read": 0.10, "out": 10.0},
    "claude-haiku-5-5": {"in": 0.10, "w5": 0.125, "w1h": 0.20, "read": 0.01, "out": 0.50},
}
HAIKU_LONG = {"in": 0.50, "w5": 0.625, "w1h": 1.0, "read": 0.05, "out": 2.50}


def _unix(ts):
    return datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()


def model_calls(transcript):
    """One record per model call (deduplicated by message id), in time order."""
    seen, calls = set(), []
    path = Path(transcript)
    if not path.exists():
        return calls
    for line in path.read_text(errors="replace").splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        m = e.get("message")
        if e.get("type") != "assistant" or not isinstance(m, dict) or not m.get("usage") or m.get("model") == "<synthetic>":
            continue
        key = m.get("id") or e.get("requestId") or e.get("uuid")
        if key in seen:
            continue
        seen.add(key)
        u = m["usage"]
        cc = u.get("cache_creation") or {}
        w1h = cc.get("ephemeral_1h_input_tokens", 0) or 0
        w5 = (u.get("cache_creation_input_tokens", 0) or 0) - w1h
        calls.append({"t": _unix(e["timestamp"]), "model": m.get("model"), "in": u.get("input_tokens", 0) or 0,
                      "w5": w5, "w1h": w1h, "read": u.get("cache_read_input_tokens", 0) or 0,
                      "out": u.get("output_tokens", 0) or 0})
    calls.sort(key=lambda c: c["t"])
    return calls


def call_cost(c):
    p = PRICES.get(c["model"])
    if p is None:
        return None
    if c["model"] == "claude-haiku-5-5" and c["in"] + c["w5"] + c["w1h"] + c["read"] > 100_000:
        p = HAIKU_LONG
    return (c["in"] * p["in"] + c["w5"] * p["w5"] + c["w1h"] * p["w1h"] + c["read"] * p["read"] + c["out"] * p["out"]) / 1e6


def analyze_run(run, n, track, do_score=False):
    log = [json.loads(line) for line in Path(run["log"]).read_text().splitlines() if line.strip()]
    first = next((e for e in log if e["kind"] == "first_call"), None)
    calls = model_calls(run["transcript"]) if run.get("transcript") else []
    t0 = first["unix"] if first and "unix" in first else (calls[0]["t"] if calls else None)
    # Windows that do not count as working time (the machine asleep), recorded at each resume.
    windows = [w for e in log if e["kind"] == "resume" for w in e.get("excluded", [])]

    def minutes(u):
        lost = sum(max(0.0, min(b, u) - max(a, t0)) for a, b in windows)
        return round((u - t0 - lost) / 60, 2)
    ref = references.reference(n, track, run.get("physics"))

    # Cumulative cost at any moment.
    cum, costs = 0.0, []
    for c in calls:
        cum += call_cost(c) or 0.0
        costs.append((c["t"], cum))

    def cost_at(t):
        out = 0.0
        for ct, cc in costs:
            if ct <= t:
                out = cc
            else:
                break
        return out

    curve, best, tests = [], None, 0
    for e in log:
        if e["kind"] != "test" or e.get("stage") == "validation":
            continue
        tests += 1
        if e.get("valid") and (best is None or e["volume"] < best):
            best = e["volume"]
        curve.append({"test": tests, "minutes": minutes(e["unix"]) if t0 else None,
                      "cost": round(cost_at(e["unix"]), 4), "valid": e.get("valid"), "volume": e.get("volume"),
                      "best": best, "score": round(ref / best, 4) if best and ref else 0.0,
                      "partial": e.get("partial", 0.0)})
    tokens = {k: sum(c[k] for c in calls) for k in ("in", "w5", "w1h", "read", "out")}
    models = sorted({c["model"] for c in calls})
    out = {
        "name": run["name"], "model_alias": run["model"], "model_ids": models, "n": n, "physics": run.get("physics") or {}, "kit": run.get("kit_version", 1),
        "minutes_limit": run.get("minutes"),
        "rounds": run.get("rounds", 1), "notes": run.get("notes", []),
        "minutes_active": minutes(max(e["unix"] for e in log if "unix" in e)) if t0 else None,
        "excluded_windows": windows,
        "agent_minutes": round((calls[-1]["t"] - calls[0]["t"]) / 60, 1) if calls else None,
        "model_calls": len(calls), "tokens": tokens, "cost": round(cum, 2),
        "test_calls": tests, "sim_calls": sum(1 for e in log if e["kind"] in ("trace", "view", "film")),
        "lab_worlds": sum(1 for e in log if e["kind"] == "lab" and e.get("op") == "new"),
        "lab_ticks": sum(e.get("ticks", 0) for e in log if e["kind"] == "lab"),
        "best_dev_volume": best, "best_partial": max((p["partial"] for p in curve), default=0.0),
        "first_valid_minutes": next((p["minutes"] for p in curve if p["valid"]), None),
        "first_valid_cost": next((p["cost"] for p in curve if p["valid"]), None),
        "reference": ref, "curve": curve,
    }
    result_path = Path(run["log"]).with_name("result.json")
    if do_score and not result_path.exists() and str(run.get("status", "")).startswith("finished"):
        from pdgrader import server
        r = server.score(run["log"])
        result_path.write_text(json.dumps(r, indent=1))
    if result_path.exists():
        r = json.loads(result_path.read_text())
        out["final"] = {k: r.get(k) for k in ("valid", "volume", "dims", "score", "translations", "final_failures", "candidate_source")}
        # Scored against today's reference table, so a reference added after the run still applies.
        out["score"] = round(ref / r["volume"], 4) if ref and r.get("valid") and r.get("volume") else 0.0
        out["final"]["score"] = out["score"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--score", action="store_true", help="run the final test for runs that have no result.json yet")
    a = ap.parse_args()
    man = json.loads(Path(a.manifest).read_text())
    n, track = man.get("n", 3), man.get("track", "seamless")
    # Runs cancelled before they produced anything, or never launched, are not results.
    kept = [r for r in man["runs"] if not str(r.get("status", "")).startswith(("cancelled", "held", "pending"))]
    runs = [analyze_run(r, r.get("n", n), track, a.score) for r in kept]
    summary = {"wave": man["wave"], "task": man["task"], "n": n, "track": track, "minutes": man.get("minutes"),
               "prices": PRICES, "runs": runs}
    Path(a.manifest).with_name("summary.json").write_text(json.dumps(summary, indent=1))
    for r in runs:
        fin = r.get("final") or {}
        print(f"{r['name']:<13} {','.join(r['model_ids']) or '?':<20} final {str(fin.get('volume')):>5} score {r.get('score', '-')!s:>6} "
              f"best-dev {str(r['best_dev_volume']):>5} first-valid {str(r['first_valid_minutes']):>6} min "
              f"tests {r['test_calls']:>3} sims {r['sim_calls']:>3} lab {r['lab_ticks']:>5} "
              f"calls {r['model_calls']:>4} ${r['cost']:>7} partial {r['best_partial']}")


if __name__ == "__main__":
    main()
