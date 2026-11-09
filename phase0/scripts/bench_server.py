#!/usr/bin/env python3
"""Phase 0 measurement: boot time and tick throughput of the vanilla dedicated server.

Usage: bench_server.py <java> <server.jar> <run_dir> [--fresh]

Drives the server over stdin/stdout. Prints a JSON summary at the end.
"""
import json
import queue
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

PROPS = """\
level-name=world
level-type=minecraft\\:flat
generate-structures=false
server-ip=127.0.0.1
server-port=25599
online-mode=false
spawn-protection=0
max-tick-time=-1
pause-when-empty-seconds=-1
view-distance=2
simulation-distance=2
sync-chunk-writes=false
enable-rcon=false
enable-query=false
white-list=true
"""


class Server:
    def __init__(self, java, jar, run_dir):
        self.lines = queue.Queue()
        self.log = []
        self.t0 = time.monotonic()
        self.proc = subprocess.Popen(
            [java, "-Xms1G", "-Xmx2G", "-jar", jar, "nogui"],
            cwd=run_dir,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        threading.Thread(target=self._pump, daemon=True).start()

    def _pump(self):
        for line in self.proc.stdout:
            line = line.rstrip("\n")
            self.log.append(line)
            self.lines.put((time.monotonic(), line))

    def wait_for(self, pattern, timeout=120):
        """Return (timestamp, match) for the first new line matching pattern."""
        rx = re.compile(pattern)
        deadline = time.monotonic() + timeout
        while True:
            left = deadline - time.monotonic()
            if left <= 0:
                raise TimeoutError(f"no line matching {pattern!r}; tail: {self.log[-8:]}")
            try:
                ts, line = self.lines.get(timeout=left)
            except queue.Empty:
                continue
            m = rx.search(line)
            if m:
                return ts, m

    def drain(self, settle=0.4):
        """Collect lines until output has been quiet for `settle` seconds."""
        out = []
        while True:
            try:
                _, line = self.lines.get(timeout=settle)
                out.append(line)
            except queue.Empty:
                return out

    def cmd(self, text, settle=0.4):
        self.proc.stdin.write(text + "\n")
        self.proc.stdin.flush()
        return self.drain(settle)

    def send(self, text):
        self.proc.stdin.write(text + "\n")
        self.proc.stdin.flush()

    def rss_mb(self):
        out = subprocess.run(["ps", "-o", "rss=", "-p", str(self.proc.pid)], capture_output=True, text=True)
        try:
            return round(int(out.stdout.strip()) / 1024, 1)
        except ValueError:
            return None

    def stop(self):
        t = time.monotonic()
        self.send("stop")
        self.proc.wait(timeout=120)
        return round(time.monotonic() - t, 2)


def strip(line):
    return re.sub(r"^\[[^\]]*\] \[[^\]]*\]: ", "", line)


def sprint(srv, n, timeout=900):
    t = time.monotonic()
    srv.send(f"tick sprint {n}")
    _, m = srv.wait_for(r"Sprint completed with ([\d.,]+) ticks per second, or ([\d.,]+) ms per tick", timeout)
    wall = time.monotonic() - t
    return {
        "ticks": n,
        "reported_tps": float(m.group(1).replace(",", "")),
        "reported_mspt": float(m.group(2).replace(",", "")),
        "wall_s": round(wall, 3),
    }


def boot(java, jar, run_dir):
    srv = Server(java, jar, run_dir)
    ts, _ = srv.wait_for(r"Done \(", timeout=300)
    return srv, round(ts - srv.t0, 2)


def main():
    java, jar, run_dir = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    fresh = "--fresh" in sys.argv
    if fresh and run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "eula.txt").write_text("eula=true\n")
    (run_dir / "server.properties").write_text(PROPS)

    res = {}

    # --- cold boot (creates the world) ---
    srv, res["cold_boot_s"] = boot(java, jar, str(run_dir))
    res["rss_after_boot_mb"] = srv.rss_mb()
    res["datapack_list"] = [strip(l) for l in srv.cmd("datapack list")]
    res["version"] = [strip(l) for l in srv.cmd("version")]
    res["stop_s"] = srv.stop()

    # --- warm boot (world exists) ---
    srv, res["warm_boot_s"] = boot(java, jar, str(run_dir))

    # --- tick control semantics ---
    sem = {}
    sem["query"] = [strip(l) for l in srv.cmd("tick query")]
    sem["gametime_cmd"] = [strip(l) for l in srv.cmd("time query gametime")]
    sem["freeze"] = [strip(l) for l in srv.cmd("tick freeze")]
    g0 = [strip(l) for l in srv.cmd("time query gametime")]
    sem["sprint_while_frozen"] = sprint(srv, 1000)
    g1 = [strip(l) for l in srv.cmd("time query gametime")]
    time.sleep(1.0)
    g2 = [strip(l) for l in srv.cmd("time query gametime")]
    sem["gametime_before_after_then_1s_later"] = [g0, g1, g2]
    sem["query_after_sprint"] = [strip(l) for l in srv.cmd("tick query")]
    t = time.monotonic()
    sem["step_100"] = [strip(l) for l in srv.cmd("tick step 100", settle=0.2)]
    time.sleep(6.0)
    g3 = [strip(l) for l in srv.cmd("time query gametime")]
    sem["gametime_6s_after_step_100"] = g3
    sem["unfreeze"] = [strip(l) for l in srv.cmd("tick unfreeze")]
    res["tick_semantics"] = sem

    # --- throughput: empty world ---
    res["forceload"] = [strip(l) for l in srv.cmd("forceload add 0 0 15 1023")]
    res["sprint_empty"] = sprint(srv, 20000)

    # --- throughput: piston workload ---
    # One unit = two observers facing each other (a 2-gametick clock) driving a
    # sticky piston that pushes a stone block. Units sit 2 blocks apart along z.
    def place_units(start, stop):
        for k in range(start, stop):
            z = 2 * k
            srv.send(f"setblock 0 -50 {z} minecraft:observer[facing=east]")
            srv.send(f"setblock 2 -50 {z} minecraft:sticky_piston[facing=up]")
            srv.send(f"setblock 2 -49 {z} minecraft:stone")
            srv.send(f"setblock 1 -50 {z} minecraft:observer[facing=west]")
        return len(srv.drain(1.0))

    res["workload"] = []
    placed = 0
    for target in (16, 64, 256, 512):
        acks = place_units(placed, target)
        placed = target
        # let clocks start, then confirm pistons are actually moving
        sprint(srv, 40)
        srv.cmd("tick freeze")
        seen = set()
        for _ in range(8):
            for state in ("true", "false"):
                out = srv.cmd(f"execute if block 2 -50 0 minecraft:sticky_piston[extended={state}]", settle=0.15)
                if any("Test passed" in l for l in out):
                    seen.add(state)
            out = srv.cmd("execute if block 2 -50 0 minecraft:moving_piston", settle=0.15)
            if any("Test passed" in l for l in out):
                seen.add("moving")
            sprint(srv, 1)
        srv.cmd("tick unfreeze")
        r = sprint(srv, 4000)
        r.update({"pistons": target, "setblock_acks": acks, "piston_states_seen": sorted(seen), "rss_mb": srv.rss_mb()})
        res["workload"].append(r)

    res["stop_s_2"] = srv.stop()
    (run_dir / "bench_log.txt").write_text("\n".join(srv.log))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
