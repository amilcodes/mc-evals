"""Exits (printing which runs) once any running run has passed its time limit by GRACE minutes.

    python3 watchdog.py w2/manifest.json w3/manifest.json

Time used is measured like the server does: wall time since the first tool call, less the
excluded windows recorded at resumes, and it is checked once a minute. A run whose time
is up but whose agent is still running needs to be stopped by hand (TaskStop).
"""
import json
import sys
import time

GRACE = 5


def used_minutes(run):
    try:
        log = [json.loads(line) for line in open(run["log"]) if line.strip()]
    except OSError:
        return None
    first = next((e for e in log if e["kind"] == "first_call"), None)
    if not first:
        return None
    windows = [w for e in log if e["kind"] == "resume" for w in e.get("excluded", [])]
    now = time.time()
    lost = sum(max(0.0, min(b, now) - max(a, first["unix"])) for a, b in windows)
    return (now - first["unix"] - lost) / 60


while True:
    over = []
    for path in sys.argv[1:]:
        for run in json.load(open(path))["runs"]:
            if run.get("status") != "running":
                continue
            used = used_minutes(run)
            if used is not None and used > run.get("minutes", 120) + GRACE:
                over.append(f"{run['name']} ({used:.0f} of {run.get('minutes')} min)")
    if over:
        print("time is up for: " + ", ".join(over))
        sys.exit(0)
    time.sleep(60)
