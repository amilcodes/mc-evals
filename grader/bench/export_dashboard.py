"""Builds the dashboard's two data files from every wave's summary.json.

    python3 bench/export_dashboard.py ../runs/bench/w1/summary.json [more summaries...] --out <dir>

runs.json: one row per run. curve.json: one row per test call, with the best valid volume
so far, minutes since the agent's first tool call, and API-equivalent cost so far.
"""
import argparse
import json
from pathlib import Path

MODEL = {"fable": "Fable 5.2", "opus": "Opus 5.5", "sonnet": "Sonnet 5.5", "haiku": "Haiku 5.5"}


def task_name(n, track):
    w, h = (n, n) if isinstance(n, int) else n
    return f"{w}×{h} {track}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("summaries", nargs="+")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    runs, curve = [], []
    for path in a.summaries:
        s = json.loads(Path(path).read_text())
        for r in s["runs"]:
            n = r.get("n", s["n"])
            task = task_name(n, s["track"]) + (" (changed physics)" if r.get("physics") else "") + (" (kit 2)" if r.get("kit", 1) >= 2 else "")
            fin = r.get("final") or {}
            tr = fin.get("translations") or {}
            scored = "final" in r
            runs.append({
                "run": r["name"], "wave": s["wave"], "task": task, "model": MODEL[r["model_alias"]],
                "model_id": ",".join(r["model_ids"]), "status": ("door" if fin.get("valid") else "no door") if scored else "running",
                "volume": fin.get("volume") if scored else r["best_dev_volume"],
                "dims": "×".join(map(str, fin["dims"])) if fin.get("valid") and fin.get("dims") else None,
                "score": round(r.get("score") or 0.0, 3) if scored else None,
                "reference": r["reference"],
                "placements": f"{tr['passed']}/{tr['of']}" if tr else None,
                "first_door_min": r["first_valid_minutes"], "first_door_cost": r["first_valid_cost"],
                "minutes_limit": r.get("minutes_limit") or s.get("minutes"), "cost": r["cost"],
                "tests": r["test_calls"], "traces": r["sim_calls"], "lab_ticks": r["lab_ticks"],
                "rounds": r["rounds"], "model_calls": r["model_calls"],
                "output_tokens": r["tokens"]["out"], "best_partial": r["best_partial"],
            })
            for p in r["curve"]:
                curve.append({"run": r["name"], "task": task, "model": MODEL[r["model_alias"]], "test": p["test"],
                              "minutes": p["minutes"], "cost": p["cost"], "volume": p["volume"] if p["valid"] else None,
                              "best": p["best"], "score": p["score"]})
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "runs.json").write_text(json.dumps(runs, indent=0))
    (out / "curve.json").write_text(json.dumps(curve, indent=0))
    print(len(runs), "runs,", len(curve), "curve points ->", out)


if __name__ == "__main__":
    main()
