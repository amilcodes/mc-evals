"""Confirm every task with check.py: the starting design must FAIL and the reference must PASS,
both with the final grade under the task's physics. Also runs the hack probes. Writes the
result into each task's "verified" field and prints a summary.

    python3 verify_tasks.py [task-id-substring]

Hack probes (all must be refused):
  bigger_box     reference plus a stone block placed just outside max_volume's reach
  no_door        reference with the doorway emptied and initial_state forced to "open"
                 (closed-start doors) or with every door-supplying piston removed (open-start)
  wrong_size     reference submitted with a different stated size
  over_budget    (repair) the reference with extra stone added beyond the edit budget
"""
import copy
import datetime
import json
import sys
from collections import defaultdict

import lib
from check import check
from lib import rules


def probes(task):
    ref = copy.deepcopy(task["reference"]["design"])
    n = task["n"]
    w, h = rules.dims(n)
    out = {}
    # bigger box: a block far enough out to blow max_volume
    big = copy.deepcopy(ref)
    big["blocks"].append({"pos": [w + 12, 0, 0], "id": "stone"})
    out["bigger_box"] = big
    # no door: drop every doorway block and every piston, keep the lever
    nod = copy.deepcopy(ref)
    nod["blocks"] = [b for b in nod["blocks"] if not rules.in_doorway(n, b["pos"]) and "piston" not in b["id"]]
    nod["initial_state"] = "open"
    out["no_door"] = nod
    ws = copy.deepcopy(ref)
    ws["n"] = [w + 1, h]
    out["wrong_size"] = ws
    if task["constraints"].get("edit_budget") is not None:
        # the reference repair plus filler stone in empty cells of its own box, one past the budget
        ob = copy.deepcopy(ref)
        taken = {tuple(b["pos"]) for b in ob["blocks"]}
        lo = [min(b["pos"][i] for b in ob["blocks"]) for i in range(3)]
        hi = [max(b["pos"][i] for b in ob["blocks"]) for i in range(3)]
        free = [(x, y, z) for x in range(lo[0], hi[0] + 1) for y in range(lo[1], hi[1] + 1) for z in range(lo[2], hi[2] + 1)
                if (x, y, z) not in taken and not rules.in_doorway(n, (x, y, z)) and not rules.in_hallway(n, (x, y, z))
                and not rules.in_shell(n, (x, y, z))]
        for p in free:
            if lib.edit_distance(task["start"], ob) > task["constraints"]["edit_budget"]:
                break
            ob["blocks"].append({"pos": list(p), "id": "stone"})
        if lib.edit_distance(task["start"], ob) > task["constraints"]["edit_budget"]:
            out["over_budget"] = ob
    return out


def main():
    sub = sys.argv[1] if len(sys.argv) > 1 else ""
    paths = sorted(p for p in lib.TASKS.glob("*.json") if sub in p.stem)
    groups = defaultdict(list)
    for p in paths:
        t = json.load(open(p))
        groups[lib.phys_tag(t["physics"])].append((p, t))
    bad = []
    for tag, items in groups.items():
        with lib.kernel(items[0][1]["physics"]) as k:
            for p, t in items:
                s = check(t, t["start"], k)
                r = check(t, t["reference"]["design"], k)
                hacks = {name: check(t, d, k)["pass"] for name, d in probes(t).items()}
                ok = (not s["pass"]) and r["pass"] and not any(hacks.values())
                t["verified"] = {
                    "date": datetime.date.today().isoformat(), "mode": "final", "physics": tag,
                    "start_passes": s["pass"], "start_grade": s["grade"],
                    "reference_passes": r["pass"], "reference_grade": r["grade"],
                    "hack_probes_refused": {h: not v for h, v in hacks.items()},
                    "ok": ok,
                }
                for key in ("failures",):
                    if t["verified"]["start_grade"]:
                        t["verified"]["start_grade"].pop(key, None)
                    if t["verified"]["reference_grade"]:
                        t["verified"]["reference_grade"].pop(key, None)
                t["verified"]["start_fail"] = (s["failures"] or [{}])[0].get("message", "")[:200]
                lib.write_json(p, t)
                print(f"{'OK ' if ok else 'BAD'} {t['id']}: start {'PASS' if s['pass'] else 'fail'}, ref {'PASS' if r['pass'] else 'fail'} "
                      f"(vol {r['grade'] and r['grade']['volume']}), hacks accepted: {[h for h, v in hacks.items() if v]}", flush=True)
                if not ok:
                    bad.append(t["id"])
    lib.cleanup()
    print(f"{len(paths) - len(bad)}/{len(paths)} tasks verified" + (f"; BAD: {bad}" if bad else ""))


if __name__ == "__main__":
    main()
