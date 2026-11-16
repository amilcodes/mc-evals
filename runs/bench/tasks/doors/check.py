"""Grade a submitted design for one door task.

    python3 check.py tasks/<id>.json submission.json [--mode final|dev] [--json]

The submission is a design in the candidate format ({"initial_state", "blocks"}); a result.json
style wrapper with a "candidate" key is accepted too. The task's size, track ("seamless") and
grading physics are always used; anything the submission says about them is ignored, except
that a stated size different from the task's is refused.

Pass means: the task's constraints hold (checked before any simulation where possible) AND the
existing grader's verdict, grade(kernel, design, n, "seamless", mode), is valid under the task's
physics AND the measured volume is within max_volume. Exit code 0 on pass, 1 on fail.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib  # noqa: E402
from lib import rules  # noqa: E402
from pdgrader.validate import validate  # noqa: E402


def _fail(code, msg):
    return {"code": code, "message": msg}


def static_checks(task, sub):
    """Constraint checks that need no simulation. Returns a list of failures."""
    n, c = task["n"], task["constraints"]
    out = []
    if isinstance(sub, dict) and "candidate" in sub and "blocks" not in sub:
        sub = sub["candidate"]
    if not isinstance(sub, dict) or not isinstance(sub.get("blocks"), list):
        return [_fail("bad_format", 'submission must be {"initial_state": ..., "blocks": [...]}')]
    for key in ("n", "size"):
        if key in sub and rules.dims(sub[key]) != rules.dims(n):
            out.append(_fail("wrong_size", f"task is a {rules.label(n)} door; submission says {sub[key]!r}"))
    errors, blocks = validate(sub, n)
    if errors:
        out += [_fail("invalid_design", f"{e['code']}: {e['message']}" + (f" at {e['pos']}" if "pos" in e else "")) for e in errors[:10]]
        return out
    allowed = c.get("allowed_blocks")
    if allowed:
        allowed = {a if ":" in a else "minecraft:" + a for a in allowed}
        bad = sorted({bid for bid, _ in blocks.values() if bid not in allowed})
        if bad:
            out.append(_fail("block_not_allowed", f"blocks not allowed in this task: {bad}"))
    lever = next(p for p, (bid, _) in blocks.items() if bid == "minecraft:lever")
    body = [p for p in blocks if p != lever]
    if c.get("max_blocks") is not None:
        count = sum(1 for p in body if not rules.in_doorway(n, p))
        if count > c["max_blocks"]:
            out.append(_fail("over_block_budget", f"{count} blocks (doorway and lever excluded) > budget {c['max_blocks']}"))
    if c.get("max_volume") is not None:
        # The doorway is always inside the box, and the grader's swept box can only be larger
        # than the placed blocks' box, so this is a safe early refusal.
        w, h = rules.dims(n)
        lo = [min([p[i] for p in body] + [0]) for i in range(3)]
        hi = [max([p[i] for p in body] + [(w - 1, h - 1, 0)[i]]) for i in range(3)]
        vol = (hi[0] - lo[0] + 1) * (hi[1] - lo[1] + 1) * (hi[2] - lo[2] + 1)
        if vol > c["max_volume"]:
            out.append(_fail("box_too_big", f"placed blocks already span {vol} > max_volume {c['max_volume']}"))
    if c.get("initial_state") and sub.get("initial_state") != c["initial_state"]:
        out.append(_fail("initial_state_changed", f"initial_state must stay {c['initial_state']!r}"))
    if c.get("edit_budget") is not None:
        d = lib.edit_distance(task["start"], sub)
        if d > c["edit_budget"]:
            out.append(_fail("over_edit_budget", f"{d} cells differ from the starting design > edit budget {c['edit_budget']}"))
    return out


def check(task, sub, kernel=None, mode="final"):
    """Returns {"pass", "failures", "grade"}. `kernel` must have been started with the task's physics."""
    if isinstance(sub, dict) and "candidate" in sub and "blocks" not in sub:
        sub = sub["candidate"]
    fails = static_checks(task, sub)
    out = {"task": task["id"], "pass": False, "failures": fails, "grade": None}
    if fails:
        return out
    if kernel is not None and lib.physics_key(getattr(kernel, "physics", {})) != lib.physics_key(task["physics"]):
        raise ValueError(f"kernel physics {kernel.physics} != task physics {task['physics']}")
    own = kernel is None
    ctx = lib.kernel(task["physics"]) if own else None
    k = ctx.__enter__() if own else kernel
    try:
        r = lib.grade(k, sub, task["n"], "seamless", mode)
    finally:
        if own:
            ctx.__exit__(None, None, None)
    out["grade"] = {**lib.brief(r), "mode": mode, "failures": [f"{f['code']}: {f['message']}"[:300] for f in r["failures"][:3]]}
    if not r["valid"]:
        fails.append(_fail("grader_failed", out["grade"]["failures"][0] if out["grade"]["failures"] else "invalid"))
    elif task["constraints"].get("max_volume") is not None and r["volume"] > task["constraints"]["max_volume"]:
        fails.append(_fail("too_big", f"measured volume {r['volume']} > max_volume {task['constraints']['max_volume']}"))
    out["pass"] = not fails
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("task")
    ap.add_argument("submission")
    ap.add_argument("--mode", default="final", choices=["final", "dev"])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    task = json.load(open(a.task))
    sub = json.load(open(a.submission))
    try:
        res = check(task, sub, mode=a.mode)
    finally:
        lib.cleanup()
    if a.json:
        print(json.dumps(res, indent=1))
    else:
        print(("PASS" if res["pass"] else "FAIL") + f"  {task['id']}")
        if res["grade"]:
            g = res["grade"]
            print(f"  grade ({g['mode']}): valid={g['valid']} volume={g['volume']} open={g['open_ticks']} close={g['close_ticks']} partial={g['partial']}")
        for f in res["failures"]:
            print(f"  - {f['code']}: {f['message']}")
    sys.exit(0 if res["pass"] else 1)


if __name__ == "__main__":
    main()
