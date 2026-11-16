"""Measure every reference circuit (or the named ones) under the given physics and print traces."""
import json, sys, time
import lib
from circuits import CIRCUITS

def loose_task(c):
    ev, end = c["schedule"]
    return {"harness": c["harness"], "limits": {"bbox": {"min": [-2, -1, -4], "max": [12, 4, 6]}, "max_blocks": 200},
            "spec": {"inputs": ev, "end": end, "outputs": {"Q": {"initial": False, "edges": []}}}}

if __name__ == "__main__":
    physics = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    names = sys.argv[2:] or list(CIRCUITS)
    try:
        for n in names:
            c = CIRCUITS[n]
            t = loose_task(c)
            t0 = time.monotonic()
            r = lib.check(t, c["build"], physics)
            print(n, round(time.monotonic() - t0, 2), "s inputs", [e["t"] for e in t["spec"]["inputs"]])
            print("   ", [f["code"] for f in r["failures"] if f["code"] != "wrong_edge_count"], "Q:", r["outputs"])
    finally:
        lib.cleanup()
