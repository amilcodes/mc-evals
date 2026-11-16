"""Speed census: greedy timing descent on every valid benchmark door.

    python3 speed_census.py [workers]

For each door (runs.json, status "door"), under the physics it was built for:
  round:   grade every timing edit of every signal component (dev grade, 3 cycles)
  combine: apply the improving edits one at a time, best first, keeping each only if the door
           stays valid, no larger, and strictly faster (open + close ticks)
  repeat from the combined design while it keeps improving, at most MAX_ROUNDS rounds.
Faster designs are then confirmed with the final grade, the 11 placement shifts and the 180° turn.
Output: speed_census.jsonl (one line per door) and speed_designs/<run>.json.
"""
import copy
import json
import multiprocessing as mp
import sys
import tempfile as _tf
import time
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BENCH = ROOT / "runs/bench"
SCRATCH = Path("/private/tmp/claude-501/census_k")
MAX_ROUNDS = 3
H4 = ["north", "south", "east", "west"]
D6 = H4 + ["up", "down"]

_K = None


def _init(physics):
    global _K
    sys.path.insert(0, str(ROOT / "grader"))
    import pdgrader.kernel as K
    SCRATCH.mkdir(parents=True, exist_ok=True)
    K.tempfile = types.SimpleNamespace(mkdtemp=lambda prefix="", dir=None: _tf.mkdtemp(prefix=prefix, dir=str(SCRATCH)))
    _K = K.Kernel(heap="800M", physics=physics or None)
    mp.util.Finalize(_K, _K.close, exitpriority=10)


def short(bid):
    return bid.split(":")[-1]


def timing_options(b):
    """Timing-relevant replacements for one signal component."""
    bid, p = short(b["id"]), b.get("props") or {}
    f = p.get("facing", "north")
    out = []
    if bid == "repeater":
        d = p.get("delay", "1")
        out += [("repeater", {"facing": f, "delay": str(x)}) for x in range(1, 5) if str(x) != d]
        out += [("observer", {"facing": f}), ("comparator", {"facing": f}), ("redstone_wire", {})]
    elif bid == "observer":
        out += [("observer", {"facing": x}) for x in D6 if x != f]
        if f in H4:
            out += [("repeater", {"facing": f, "delay": str(x)}) for x in range(1, 5)]
    elif bid == "comparator":
        out += [("repeater", {"facing": f, "delay": str(x)}) for x in range(1, 5)] + [("observer", {"facing": f}), ("redstone_wire", {})]
    elif bid == "redstone_wire":
        out += [("repeater", {"facing": x, "delay": "1"}) for x in H4]
    return out


def edits_for(design):
    out = []
    for b in design["blocks"]:
        for bid, props in timing_options(b):
            out.append({"pos": b["pos"], "from": [short(b["id"]), b.get("props") or {}], "to": [bid, props]})
    return out


def apply(design, e):
    s = copy.deepcopy(design)
    s["blocks"] = [b for b in s["blocks"] if b["pos"] != e["pos"]]
    bid, props = e["to"]
    if bid != "air":
        s["blocks"].append({"pos": list(e["pos"]), "id": bid, **({"props": dict(props)} if props else {})})
    return s


def brief(r):
    return {k: r.get(k) for k in ("valid", "volume", "open_ticks", "close_ticks")} | {"fail": r["failures"][0]["code"] if r["failures"] else None}


def task_grade(args):
    run, n, design, edits = args
    from pdgrader.grade import grade
    out = []
    for e in edits:
        try:
            r = brief(grade(_K, apply(design, e), n, "seamless", "dev"))
        except Exception as ex:
            r = {"valid": False, "fail": "error:" + repr(ex)[:80]}
        out.append((e, r))
    return run, out


def faster(r, best, vol0):
    return r.get("valid") and r["volume"] <= vol0 and r["open_ticks"] + r["close_ticks"] < best["open_ticks"] + best["close_ticks"]


def task_combine(args):
    run, n, design, cur, improving, vol0 = args
    from pdgrader.grade import grade
    applied = []
    for e, _ in improving:
        if any(a["pos"] == e["pos"] for a in applied):
            continue
        cand = apply(design, e)
        r = brief(grade(_K, cand, n, "seamless", "dev"))
        if faster(r, cur, vol0):
            design, cur = cand, r
            applied.append(e)
    return run, design, cur, applied


def task_confirm(args):
    run, n, design = args
    from pdgrader.grade import grade, translation_pass_rate, rotated_180
    f = brief(grade(_K, design, n, "seamless", "final"))
    tr = translation_pass_rate(_K, design, n, "seamless", "final")
    rot = brief(grade(_K, rotated_180(design, n), n, "seamless", "final"))
    return run, {"final": f, "placements_passed": tr["passed"], "rot180": rot}


def run_group(doors, physics, workers):
    """doors: run -> {n, design, base(brief)} ; all built for the same physics."""
    pool = mp.Pool(workers, initializer=_init, initargs=(physics,))
    state = {r: {"design": d["design"], "cur": d["base"], "n": d["n"], "vol0": d["base"]["volume"], "applied": [], "rounds": 0, "graded": 0}
             for r, d in doors.items()}
    active = [r for r in state]
    for rnd in range(1, MAX_ROUNDS + 1):
        if not active:
            break
        jobs = []
        for r in active:
            s = state[r]
            es = edits_for(s["design"])
            s["graded"] += len(es)
            for i in range(0, len(es), 12):
                jobs.append((r, s["n"], s["design"], es[i:i + 12]))
        t0 = time.monotonic()
        found = {r: [] for r in active}
        for k, (r, res) in enumerate(pool.imap_unordered(task_grade, jobs)):
            found[r] += [(e, x) for e, x in res if faster(x, state[r]["cur"], state[r]["vol0"])]
        print(f"  round {rnd}: {len(active)} doors, {sum(len(j[3]) for j in jobs)} edits, {time.monotonic() - t0:.0f}s, "
              f"{sum(1 for r in active if found[r])} doors with a faster neighbour", flush=True)
        combine = []
        for r in active:
            imp = sorted(found[r], key=lambda ex: ex[1]["open_ticks"] + ex[1]["close_ticks"])
            if imp:
                s = state[r]
                combine.append((r, s["n"], s["design"], s["cur"], imp, s["vol0"]))
        nxt = []
        for r, design, cur, applied in pool.imap_unordered(task_combine, combine):
            s = state[r]
            if applied:
                s["design"], s["cur"], s["applied"] = design, cur, s["applied"] + applied
                s["rounds"] = rnd
                nxt.append(r)
        active = nxt
    conf = [(r, s["n"], s["design"]) for r, s in state.items() if s["applied"]]
    for r, c in pool.imap_unordered(task_confirm, conf):
        state[r]["confirm"] = c
    pool.close()
    pool.join()
    return state


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    sys.path.insert(0, str(ROOT / "grader"))
    import os
    only = set(filter(None, os.environ.get("ONLY", "").split(",")))
    runs = [r for r in json.load(open(BENCH / "dashboard/runs.json")) if r["status"] == "door" and (not only or r["run"] in only)]
    groups = {}
    for r in runs:
        j = json.load(open(BENCH / r["wave"] / r["run"] / "result.json"))
        phys = j.get("physics") or {}
        key = json.dumps(phys, sort_keys=True)
        groups.setdefault(key, {})[r["run"]] = {"n": j["n"], "design": j["candidate"], "task": r["task"], "model": r["model"]}
    out_path = HERE / os.environ.get("OUT", "speed_census.jsonl")
    done = {json.loads(l)["run"] for l in open(out_path)} if out_path.exists() else set()
    (HERE / "speed_designs").mkdir(exist_ok=True)
    for key, doors in groups.items():
        doors = {r: d for r, d in doors.items() if r not in done}
        if not doors:
            continue
        physics = json.loads(key)
        print(f"physics {key}: {len(doors)} doors", flush=True)
        # baselines (dev) for every door in the group, graded on one pool
        pool = mp.Pool(workers, initializer=_init, initargs=(physics,))
        base = dict((r, res[0][1]) for r, res in pool.imap_unordered(task_grade, [(r, d["n"], d["design"], [{"pos": [9999, 0, 0], "from": [], "to": ["air", {}]}]) for r, d in doors.items()]))
        pool.close()
        pool.join()
        good = {r: {**d, "base": base[r]} for r, d in doors.items() if base[r].get("valid")}
        for r in doors:
            if r not in good:
                print(f"  {r}: baseline not valid under dev grade ({base[r].get('fail')}), skipped", flush=True)
        t0 = time.monotonic()
        # one door at a time (smallest first), saved as soon as it finishes, so a stop loses little
        order = sorted(doors, key=lambda r: len(doors[r]["design"]["blocks"]))
        for r in order:
            d = doors[r]
            while True:  # disk guard: macOS swap shares this volume
                free = os.statvfs("/private/tmp")
                if free.f_bavail * free.f_frsize > 400e6:
                    break
                print(f"  waiting for disk space ({free.f_bavail * free.f_frsize / 1e6:.0f} MB free)", flush=True)
                time.sleep(60)
            s = run_group({r: good[r]}, physics, workers).get(r) if r in good else None
            rec = {"run": r, "task": d["task"], "model": d["model"], "physics": physics, "base": base[r]}
            if s:
                rec |= {"edits_graded": s["graded"], "best_dev": s["cur"], "applied": s["applied"], "confirm": s.get("confirm")}
                if s["applied"]:
                    json.dump(s["design"], open(HERE / "speed_designs" / f"{r}.json", "w"), indent=1)
            with open(out_path, "a") as f:
                f.write(json.dumps(rec) + "\n")
            b, c = base[r], (s or {}).get("cur") or {}
            print(f"  {r}: {b.get('open_ticks')}/{b.get('close_ticks')} -> {c.get('open_ticks')}/{c.get('close_ticks')} "
                  f"({len((s or {}).get('applied') or [])} edits) {time.monotonic() - t0:.0f}s", flush=True)
        print(f"  group done in {time.monotonic() - t0:.0f}s", flush=True)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    main()
