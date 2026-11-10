#!/usr/bin/env python3
"""Compares the kernel's tick-by-tick trace of a door with a real vanilla dedicated server.

The kernel advances the world by calling ServerLevel.tick itself. This script builds the same
door on an ordinary dedicated server with console commands, steps it with `/tick step 1`, and
probes a set of cells every tick, then checks the two traces match.

Usage: parity_dedicated.py <java> <server.jar> <dedicated_run_dir> [fixture] [n]
The run dir must already contain an accepted eula.txt (the operator's decision, not this script's).
"""
import copy
import queue
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "fixtures"))

from make_fixtures import FIXTURES  # noqa: E402
from pdgrader import rules  # noqa: E402
from pdgrader.grade import build_job  # noqa: E402
from pdgrader.kernel import Kernel  # noqa: E402
from pdgrader.validate import validate  # noqa: E402

TICKS = 8
CLASSES = ["air", "stone", "moving_piston", "piston_head", "sticky_piston[extended=true]", "sticky_piston[extended=false]"]


def classify(state):
    bid, props = rules.parse_state(state)
    bid = bid.replace("minecraft:", "")
    if bid == "sticky_piston":
        return f"sticky_piston[extended={props['extended']}]"
    return bid if bid in CLASSES else "other"


class Console:
    def __init__(self, java, jar, run_dir):
        self.q = queue.Queue()
        self.proc = subprocess.Popen([java, "-Xmx2G", "-jar", jar, "nogui"], cwd=run_dir, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        threading.Thread(target=lambda: [self.q.put(l.rstrip("\n")) for l in self.proc.stdout], daemon=True).start()
        self.wait(r"Done \(", 300)

    def wait(self, pattern, timeout=30):
        rx, end = re.compile(pattern), time.monotonic() + timeout
        while True:
            line = self.q.get(timeout=max(0.01, end - time.monotonic()))
            m = rx.search(line)
            if m:
                return m

    def ask(self, cmd, pattern, timeout=30):
        self.proc.stdin.write(cmd + "\n")
        self.proc.stdin.flush()
        return self.wait(pattern, timeout)

    def gametime(self):
        return int(self.ask("time query gametime", r"game time is (\d+)").group(1))

    def step(self):
        g = self.gametime()
        self.ask("tick step 1", r"Stepping 1 tick")
        while self.gametime() < g + 1:
            pass
        assert self.gametime() == g + 1

    def probe(self, w):
        for c in CLASSES:
            if self.ask(f"execute if block {w[0]} {w[1]} {w[2]} minecraft:{c}", r"Test (passed|failed)").group(1) == "passed":
                return c
        return "other"


def main():
    java, jar, run_dir = sys.argv[1:4]
    name = sys.argv[4] if len(sys.argv) > 4 else "good_2x2"
    n = int(sys.argv[5]) if len(sys.argv) > 5 else 2
    errors, blocks = validate(copy.deepcopy(FIXTURES[name]), n)
    assert not errors, errors
    lever = next(p for p, (bid, _) in blocks.items() if bid == "minecraft:lever")
    probes = set(rules.doorway(n)) | {p for p, (bid, _) in blocks.items() if "piston" in bid or bid == rules.DOOR_BLOCK}
    probes = sorted(probes | {rules.step(p, props["facing"], k) for p, (bid, props) in blocks.items() if "piston" in bid for k in (1, 2, 3)})
    W = lambda p: tuple(rules.ORIGIN[i] + p[i] for i in range(3))  # noqa: E731

    # ---- kernel trace
    with Kernel() as k:
        # The server side is built with /setblock, which runs a shape update on each placed block
        # and so makes observers fire on placement. The grader's own rule (0.3) skips that, so the
        # kernel is asked for the older placement here to compare like with like.
        res = k.run_job(build_job(n, blocks, lever, "dev", rules.TIME_CAP, legacy_placement=True))
    steps = {s["label"]: s for s in res["steps"] if "label" in s}
    kernel_trace = []
    state = {tuple(c[:3]): c[3] for c in steps["rest.start"]["cells"]}
    for tag in ("0.0", "0.1"):
        changes = steps[f"move.{tag}"]["changes"]
        for t in range(1, TICKS + 1):
            for c in changes:
                if c[0] == t:
                    state[tuple(c[1:4])] = c[5]
            kernel_trace.append([classify(state.get(p, "minecraft:air")) for p in probes])
        for c in changes:  # bring the state to the end of the move before the next flip
            state[tuple(c[1:4])] = c[5]

    # ---- dedicated server trace
    con = Console(java, jar, run_dir)
    lo, hi = rules.region(n)
    xs = [p[0] for p in blocks] ; ys = [p[1] for p in blocks] ; zs = [p[2] for p in blocks]
    a, b = W((min(xs) - 3, min(ys) - 3, min(zs) - 3)), W((max(xs) + 3, max(ys) + 3, max(zs) + 3))
    con.ask(f"forceload add {a[0] - 16} {a[2] - 40} {b[0] + 16} {b[2] + 40}", r"force loaded|No chunks|Marked")
    con.ask("tick rate 200", r"Set the target tick rate")
    con.ask("tick freeze", r"frozen")
    con.ask(f"fill {a[0]} {a[1]} {a[2]} {b[0]} {b[1]} {b[2]} minecraft:air", r"filled|No blocks")
    for cell in rules.shell(n):
        if min(zs) - 2 <= cell[2] <= max(zs) + 2:
            w = W(cell)
            con.ask(f"setblock {w[0]} {w[1]} {w[2]} {rules.WALL_BLOCK}", r"Changed the block|Could not set")
    for pos, (bid, props) in sorted(blocks.items()):
        w = W(pos)
        con.ask(f"setblock {w[0]} {w[1]} {w[2]} {rules.state_string(bid, props)}", r"Changed the block|Could not set")
    for _ in range(30):
        con.step()
    start = [con.probe(W(p)) for p in probes]
    kernel_start = [classify({tuple(c[:3]): c[3] for c in steps["rest.start"]["cells"]}.get(p, "minecraft:air")) for p in probes]
    server_trace = []
    lw = W(lever)
    lever_bid, lever_props = blocks[lever]
    for powered in ("true", "false"):
        con.ask(f"setblock {lw[0]} {lw[1]} {lw[2]} {rules.state_string(lever_bid, {**lever_props, 'powered': powered})}", r"Changed the block")
        for _ in range(TICKS):
            con.step()
            server_trace.append([con.probe(W(p)) for p in probes])
        for _ in range(40):
            con.step()
    con.proc.stdin.write("stop\n")
    con.proc.stdin.flush()
    con.proc.wait(timeout=60)

    # ---- compare
    print(f"fixture {name}, {len(probes)} probe cells, {2 * TICKS} ticks compared")
    print("rest state matches:", start == kernel_start)
    mismatches = 0
    for i, (kt, st) in enumerate(zip(kernel_trace, server_trace)):
        phase, t = ("after lever on ", i + 1) if i < TICKS else ("after lever off", i - TICKS + 1)
        same = kt == st
        mismatches += not same
        moving = sum(c == "moving_piston" for c in st)
        print(f"  {phase} tick {t}: {'match' if same else 'MISMATCH'}  (server: {moving} moving, doorway {''.join('#' if st[probes.index(d)] == 'stone' else '.' if st[probes.index(d)] == 'air' else 'm' for d in rules.doorway(n))})")
        if not same:
            for p, x, y in zip(probes, kt, st):
                if x != y:
                    print(f"      {p}: kernel {x}, server {y}")
    ok = start == kernel_start and mismatches == 0
    print("PARITY OK" if ok else f"PARITY FAILED ({mismatches} ticks differ)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
