"""Spec checker for the piston-machine repair / port tasks (see README.md for the format).

    python3 check.py <task.json> [build.json]      # build defaults to the task's reference_solution
    python3 check.py <task.json> --start           # check the task's (broken) starting build

A build is a list of blocks [{"pos": [x, y, z], "id": str, "props": {...}}] (or an object with a
"blocks" list). check(kernel, spec, blocks) returns {"pass": bool, "failures": [...], ...}.
The kernel must have been started with the task's physics (see kernel_for()).
"""
import json
import sys
import tempfile as _tf
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "grader"))

from pdgrader import rules  # noqa: E402
from pdgrader.validate import validate_part  # noqa: E402

SCRATCH = Path("/private/tmp/claude-501/tasks_pistons_k")
ORIGIN = (0, 100, 0)
DEFAULTS = {"settle_cap": 40, "time_cap": 60, "quiet": 20, "hold": 40, "periodic": True, "forbid_entities": True}
MIN_TOGGLES = 4
MAX_CHANGES = 6000


# ---------------------------------------------------------------- kernel

def kernel_for(physics=None, heap="1G"):
    """A Kernel whose scratch dirs live under SCRATCH (never under grader/)."""
    import pdgrader.kernel as K
    SCRATCH.mkdir(parents=True, exist_ok=True)
    K.tempfile = types.SimpleNamespace(mkdtemp=lambda prefix="", dir=None: _tf.mkdtemp(prefix=prefix, dir=str(SCRATCH)))
    return K.Kernel(heap=heap, physics=physics or None)


# ---------------------------------------------------------------- spec helpers

def _span(v):
    if isinstance(v, int):
        return range(v, v + 1)
    lo, hi = v
    return range(lo, hi + 1)


def expand(reqs):
    """[{"at": [x|[lo,hi], y, z], "is": id|[ids]}] -> {(x,y,z): set(ids)}; "air" means empty."""
    out = {}
    for r in reqs:
        ids = r["is"] if isinstance(r["is"], list) else [r["is"]]
        ids = {i if i == "air" or ":" in i else "minecraft:" + i for i in ids}
        ids = {"minecraft:air" if i == "air" else i for i in ids}
        for x in _span(r["at"][0]):
            for y in _span(r["at"][1]):
                for z in _span(r["at"][2]):
                    out[(x, y, z)] = ids
    return out


def _cells(snapshot):
    return {tuple(c[:3]): c[3] for c in snapshot["cells"]}


def _bid(state):
    return rules.parse_state(state)[0]


def _mismatch(want, cells):
    bad = []
    for p, ids in sorted(want.items()):
        got = _bid(cells.get(p, "minecraft:air"))
        if got not in ids:
            bad.append({"pos": list(p), "want": sorted(ids), "found": got})
    return bad


def _fail(code, message, **detail):
    return {"code": code, "message": message, **detail}


def normalise(build):
    items = build["blocks"] if isinstance(build, dict) else build
    out = []
    for b in items:
        bid = b["id"] if ":" in b["id"] else "minecraft:" + b["id"]
        if bid == "minecraft:air":
            continue
        out.append({"pos": list(b["pos"]), "id": bid, **({"props": dict(b["props"])} if b.get("props") else {})})
    return out


def toggles(spec):
    return len(spec["schedule"])


def target_state(i):
    """State name required after toggle i (1-based); toggle 0 is the settled start."""
    return "on" if i % 2 else "off"


# ---------------------------------------------------------------- static checks

def static_check(spec, build):
    """Allow-list, piston-head consistency, lever, box, budget, fixed cells. Returns (errors, blocks)."""
    items = normalise(build)
    errors, blocks = validate_part(items, 1)
    if errors:
        return errors, blocks
    lever = tuple(spec["lever"])
    levers = [p for p, (bid, _) in blocks.items() if bid == "minecraft:lever"]
    if levers != [lever]:
        errors.append(_fail("lever", f"exactly one lever is required, at {list(lever)}; found {[list(p) for p in levers]}"))
    lo, hi = spec["box"]["min"], spec["box"]["max"]
    out = [list(p) for p in blocks if not all(lo[i] <= p[i] <= hi[i] for i in range(3))]
    if out:
        errors.append(_fail("outside_box", f"blocks outside the allowed box {lo}..{hi}", positions=out[:20]))
    if len(blocks) > spec["block_budget"]:
        errors.append(_fail("over_budget", f"{len(blocks)} blocks (lever included) is over the budget of {spec['block_budget']}"))
    for f in spec.get("fixed", []):
        got = blocks.get(tuple(f[:3]))
        if not got or got[0] != f[3]:
            errors.append(_fail("fixed_cell", f"cell {f[:3]} must hold {f[3]}", pos=f[:3]))
    for bid, k in spec.get("conserve", {}).items():
        have = sum(1 for (x, _) in blocks.values() if x == bid)
        if have != k:
            errors.append(_fail("conserve", f"the build must contain exactly {k} {bid}, found {have}"))
    for p in expand([{"at": c, "is": "air"} for c in spec.get("keep_clear", [])]):
        if p in blocks:
            errors.append(_fail("keep_clear", f"cell {list(p)} must stay empty", pos=list(p)))
    return errors, blocks


# ---------------------------------------------------------------- job

def build_job(spec, blocks, n_toggles=None):
    s = {**DEFAULTS, **spec}
    lever = list(spec["lever"])
    placed = [[*pos, rules.state_string(bid, props)] for pos, (bid, props) in sorted(blocks.items())]
    clear = sorted(expand([{"at": c, "is": "air"} for c in spec.get("keep_clear", [])]))
    frozen = [[*p, "minecraft:air"] for p in clear] + [list(f) for f in spec.get("fixed", [])]
    steps = [
        {"op": "clear"},
        {"op": "place", "blocks": placed},
        {"op": "run", "label": "settle", "max_ticks": s["settle_cap"] + s["quiet"], "quiet": s["quiet"], "max_changes": MAX_CHANGES},
        {"op": "snapshot", "label": "rest.0"},
    ]
    sched = spec["schedule"][: n_toggles or len(spec["schedule"])]
    for i, delay in enumerate(sched, 1):
        if delay:
            steps.append({"op": "run", "label": f"idle.{i}", "max_ticks": delay, "min_ticks": delay})
        steps.append({"op": "lever", "label": f"lever.{i}", "pos": lever})
        steps.append({"op": "run", "label": f"move.{i}", "max_ticks": s["time_cap"] + s["quiet"], "quiet": s["quiet"],
                      "max_changes": MAX_CHANGES})
        steps.append({"op": "run", "label": f"hold.{i}", "max_ticks": s["hold"], "min_ticks": s["hold"]})
        steps.append({"op": "snapshot", "label": f"rest.{i}"})
    lo, hi = spec["box"]["min"], spec["box"]["max"]
    return {
        "origin": list(ORIGIN),
        "region": {"min": list(lo), "max": list(hi)},
        # The kernel's doorway trace is not used here; point it at one cell.
        "n": 1, "w": 1, "h": 1, "door_block": "minecraft:stone",
        "ignore": [lever],
        "frozen": frozen,
        "steps": steps,
    }


def _reach_tick(before, lever_changes, move, want):
    """First tick of the move step from which every target cell matches and keeps matching.
    Reconstructed from the per-tick change log; None if the log was truncated."""
    if len(move["changes"]) >= MAX_CHANGES:
        return None
    cur = {p: _bid(before.get(p, "minecraft:air")) for p in want}
    for c in lever_changes:  # instant changes during the flip itself
        p = tuple(c[1:4])
        if p in cur:
            cur[p] = _bid(c[5])
    ok = [all(cur[p] in want[p] for p in want)]
    by_tick = {}
    for c in move["changes"]:
        by_tick.setdefault(c[0], []).append(c)
    for t in range(1, move["ticks"] + 1):
        for c in by_tick.get(t, []):
            p = tuple(c[1:4])
            if p in cur:
                cur[p] = _bid(c[5])
        ok.append(all(cur[p] in want[p] for p in want))
    reach = None
    for t in range(len(ok) - 1, -1, -1):
        if not ok[t]:
            break
        reach = t
    return reach


def check(kernel, spec, build, n_toggles=None):
    """Simulates the build against the spec. n_toggles < len(schedule) runs a cheaper screen."""
    s = {**DEFAULTS, **spec}
    res = {"pass": False, "stage": "static", "failures": [], "toggles_passed": 0, "timings": []}
    if len(spec["schedule"]) < MIN_TOGGLES:
        res["failures"].append(_fail("bad_spec", f"a spec needs at least {MIN_TOGGLES} toggles"))
        return res
    errors, blocks = static_check(spec, build)
    res["block_count"] = len(blocks)
    if errors:
        res["failures"] = errors
        return res
    want = {k: expand(v) for k, v in spec["states"].items()}
    out = kernel.run_job(build_job(spec, blocks, n_toggles))
    steps = {st["label"]: st for st in out["steps"] if "label" in st}
    fails = res["failures"]

    res["stage"] = "settle"
    rest = {0: _cells(steps["rest.0"])}
    if not steps["settle"]["quiescent"]:
        fails.append(_fail("not_settled", f"still changing {s['settle_cap']} ticks after placement",
                           changes=steps["settle"]["changes"][:20]))
    else:
        bad = _mismatch(want["off"], rest[0])
        if bad:
            fails.append(_fail("wrong_start", "after placement the target cells are not in the 'off' state", cells=bad[:20]))

    n = n_toggles or len(spec["schedule"])
    if not fails:
        res["stage"] = "toggles"
        for i in range(1, n + 1):
            where = {"toggle": i, "to": target_state(i)}
            idle = steps.get(f"idle.{i}")
            if idle and idle["changes_total"]:
                fails.append(_fail("not_at_rest", "the build changed while idle before the toggle", **where,
                                   changes=idle["changes"][:20]))
                break
            lv = steps[f"lever.{i}"]
            if "error" in lv:
                fails.append(_fail("lever_missing", lv["error"], **where))
                break
            move, hold = steps[f"move.{i}"], steps[f"hold.{i}"]
            rest[i] = _cells(steps[f"rest.{i}"])
            tgt = want[target_state(i)]
            bad = _mismatch(tgt, rest[i])
            if bad:
                fails.append(_fail("wrong_state", f"toggle {i}: target cells are not in the '{target_state(i)}' state at rest",
                                   **where, cells=bad[:20], changes=move["changes"][:30]))
                break
            if not move["quiescent"] or move["last_change_tick"] > s["time_cap"]:
                fails.append(_fail("too_slow", f"toggle {i}: the build was still changing after {s['time_cap']} ticks", **where,
                                   last_change_tick=move["last_change_tick"], quiescent=move["quiescent"]))
                break
            if hold["changes_total"]:
                fails.append(_fail("did_not_hold", f"toggle {i}: the build changed again within {s['hold']} ticks of coming to rest",
                                   **where, changes=hold["changes"][:20]))
                break
            reach = _reach_tick(rest[i - 1], lv.get("changes", []), move, tgt)
            if s.get("reach_cap") is not None and (reach is None or reach > s["reach_cap"]):
                fails.append(_fail("too_slow", f"toggle {i}: target cells reached at tick {reach}, cap {s['reach_cap']}", **where))
                break
            counts = {bid: sum(1 for v in rest[i].values() if _bid(v) == bid) for bid in spec.get("conserve", {})}
            if any(counts[bid] != k for bid, k in spec.get("conserve", {}).items()):
                fails.append(_fail("conserve", f"toggle {i}: block counts changed: {counts}, want {spec['conserve']}", **where))
                break
            if s["periodic"] and i >= 2 and rest[i] != rest[i - 2]:
                diff = sorted(set(rest[i].items()) ^ set(rest[i - 2].items()))
                fails.append(_fail("not_periodic", f"toggle {i}: the whole build at rest differs from its state two toggles earlier",
                                   **where, diff=[[list(d[0]), d[1]] for d in diff[:20]]))
                break
            res["timings"].append({**where, "reach_tick": reach, "last_change_tick": move["last_change_tick"]})
            res["toggles_passed"] = i

    if s["forbid_entities"] and out["entity_seen"]:
        e = out["entity_seen"]
        fails.append(_fail("entity", f"an entity ({e['type']}) appeared at tick {e['job_tick']} (item drop or falling block)", **e))
    if out["frozen_violation"]:
        v = out["frozen_violation"]
        fails.append(_fail("frozen_cell", f"a keep-clear or fixed cell changed at {v['pos']} (found {v['found']}) at tick {v['job_tick']}", **v))
    if out["escaped"]:
        fails.append(_fail("left_box", "a block left the allowed box during the run"))
    res["swept"] = out["swept"]
    if not fails:
        res["stage"] = "complete"
        res["pass"] = True
    return res


def brief(r):
    f = r["failures"][0] if r["failures"] else None
    return {"pass": r["pass"], "toggles_passed": r["toggles_passed"], "fail": f["code"] if f else None,
            "msg": f["message"][:160] if f else None}


def main(argv):
    task = json.loads(Path(argv[0]).read_text())
    if len(argv) > 1 and argv[1] == "--start":
        build = task["start_build"]
    elif len(argv) > 1:
        build = json.loads(Path(argv[1]).read_text())
    else:
        build = task["reference_solution"]
    with kernel_for(task.get("physics")) as k:
        r = check(k, task["spec"], build)
    print(json.dumps({k: v for k, v in r.items() if k != "swept"}, indent=1)[:4000])
    return 0 if r["pass"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
