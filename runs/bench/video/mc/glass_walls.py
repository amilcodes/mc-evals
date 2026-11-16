"""Turns the hallway walls (the grader's stone shell, every z except the doorway plane z=9) into glass,
except the wall cells listed in a keep file (ones the circuit sends power through), then cycles the
lever three times and checks the doorway closes fully and opens fully. Saves only if it works.

    python3 glass_walls.py keep_stone_min.json
"""
import json, re, sys, time
exec(open("build_world.py").read().split('wait_for(r"Done \\(")')[0])   # server boot + helpers
keep = {tuple(c) for c in json.load(open(sys.argv[1]))}
walls = [(x, y, z) for z in [*range(0, 9), *range(10, 16)]
         for (x, y) in [(15, y) for y in range(103, 107)] + [(20, y) for y in range(103, 107)]
                       + [(x, 102) for x in range(16, 20)] + [(x, 107) for x in range(16, 20)]]
wait_for(r"Done \(")
print("server up")
cmd('datapack enable "file/pdcheck"', 2)
WALLSET = {tuple(c) for c in walls}
def diff():
    out = cmd("function pdcheck:diff", 4)
    d = [l.split("DIFF ", 1)[1] for l in out if "DIFF " in l and "DIFFDONE" not in l]
    assert any("DIFFDONE" in l for l in out)
    return [l for l in d if tuple(map(int, l.split()[:3])) not in WALLSET]
cmd("forceload add -16 -16 40 32", 3)
time.sleep(3); drain(0.2)
glass = 0
for c in walls:
    if c in keep:
        continue
    r = cmd(f"execute if block {c[0]} {c[1]} {c[2]} minecraft:stone run setblock {c[0]} {c[1]} {c[2]} minecraft:glass", 0.03)
    glass += 1
drain(1.5)
cnt = cmd("execute store result score #g x run fill 15 102 0 20 107 15 minecraft:glass replace minecraft:glass", 1.0)
print("glass cells set:", glass, "| fill check:", cnt[-1:] )
def doorway():
    s = ""
    for y in range(3, -1, -1):
        for x in range(4):
            r = cmd(f"execute if block {16 + x} {103 + y} 9 minecraft:stone", 0.15)
            s += "#" if any("passed" in l for l in r) else "."
        s += "/"
    return s[:-1]
L = "setblock 0 109 11 minecraft:lever[face=wall,facing=west,powered={}]"
ON = ["function pdcam:lever_on"]
OFF = ["function pdcam:lever_off"]
time.sleep(4); print("after glass:", doorway())
ok = True
for i in range(int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 4):
    for c in ON: cmd(c, 0.1)
    time.sleep(7); d = doorway(); print(f"cycle {i+1} lever on :", d); ok &= d == "####/####/####/####"
    for c in OFF: cmd(c, 0.1)
    time.sleep(9); d = doorway(); print(f"cycle {i+1} lever off:", d); ok &= d == "..../..../..../...."
    bad = diff(); print(f"   cells off from the film (walls excluded): {len(bad)}", bad[:3]); ok &= not bad
print("WORKS" if ok else "FAILED")
if ok:
    if "--save" in sys.argv: print(cmd("save-all flush", 3))
    else: p.kill()
    if "--save" in sys.argv: cmd("stop", 0.5)
else:
    p.kill()          # do not save a broken world
p.wait(timeout=60)
print("stopped", p.returncode)
sys.exit(0 if ok else 1)
