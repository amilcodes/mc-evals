#!/usr/bin/env python3
"""Boot the bench server, run console commands (one per line on stdin), print each reply.

Usage: mc_cmds.py <java> <server.jar> <run_dir> < commands.txt
A line starting with "#sleep N" waits N seconds.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bench_server import boot, strip  # noqa: E402


def main():
    java, jar, run_dir = sys.argv[1:4]
    cmds = [l.strip() for l in sys.stdin if l.strip()]
    srv, boot_s = boot(java, jar, run_dir)
    print(f"[booted in {boot_s}s]")
    srv.drain(0.5)
    for c in cmds:
        if c.startswith("#sleep"):
            time.sleep(float(c.split()[1]))
            continue
        out = srv.cmd(c, settle=0.35)
        print(f"> {c}")
        for l in out:
            print("   ", strip(l)[:600])
    srv.stop()


if __name__ == "__main__":
    main()
