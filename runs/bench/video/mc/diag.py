"""Cycles the door with the same-tick lever functions and lists every cell that differs from the
grader's start state (door open, lever off) after each full cycle. Never saves."""
import sys, time
exec(open("build_world.py").read().split('wait_for(r"Done \\(")')[0])
wait_for(r"Done \(")
print(cmd('datapack enable "file/pdcheck"', 2)[-1:])
cmd("forceload add -16 -16 40 32", 3); time.sleep(3); drain(0.3)
HOLD_ON, HOLD_OFF = (float(v) for v in (sys.argv[2:4] if len(sys.argv) > 3 else (7.5, 9)))
def diff(tag):
    out = cmd("function pdcheck:diff", 4)
    d = [l.split("DIFF ", 1)[1] for l in out if "DIFF " in l and "DIFFDONE" not in l]
    print(f"{tag}: {len(d)} cells differ", "(done)" if any("DIFFDONE" in l for l in out) else "(NO DONE LINE)")
    for l in d[:3]: print("   ", l)
diff("start")
for i in range(int(sys.argv[1]) if len(sys.argv) > 1 else 3):
    cmd("function pdcam:lever_on", HOLD_ON); cmd("function pdcam:lever_off", HOLD_OFF)
    diff(f"after cycle {i+1}")
p.kill(); p.wait()
