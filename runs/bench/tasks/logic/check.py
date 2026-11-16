"""Check a build against a timing / sequential-logic task.

    python3 check.py tasks/<id>.json [build.json | --start | --reference] [--physics '{"repeater_unit": 3}']

build.json is a list of blocks or an object with a "blocks" list, in the task's local coordinates
(same block format as the benchmark: {"pos": [x, y, z], "id": "repeater", "props": {...}}). With no
build argument the task's starting build is checked. The task's physics is used unless --physics
overrides it. Prints a JSON verdict: {"pass", "failures", "Q": [initial, [[t, on], ...]]}; exit
status 0 on pass, 1 on fail.

Runs one kernel (heap 1G) with its scratch folder under /private/tmp/claude-501/tasks_logic_k,
which is removed afterwards.
"""
import json
import sys

import lib


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    task = json.loads(open(argv[0]).read())
    physics = task.get("physics") or {}
    build = task["start"]["blocks"]
    rest = argv[1:]
    while rest:
        a = rest.pop(0)
        if a == "--physics":
            physics = json.loads(rest.pop(0))
        elif a == "--start":
            build = task["start"]["blocks"]
        elif a == "--reference":
            build = task["reference"]["blocks"]
        else:
            b = json.loads(open(a).read())
            build = b["blocks"] if isinstance(b, dict) else b
    try:
        v = lib.check(task, build, physics)
    finally:
        lib.cleanup()
    out = {"task": task["id"], "physics": physics, "pass": v["pass"], "failures": v["failures"],
           "outputs": v["outputs"]}
    print(json.dumps(out, indent=1))
    return 0 if v["pass"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
