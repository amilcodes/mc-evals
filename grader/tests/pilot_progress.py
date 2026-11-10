#!/usr/bin/env python3
"""Summarise agent runs from their server-side logs. Usage: pilot_progress.py <runs_dir>"""
import collections
import json
import pathlib
import sys

for d in sorted(pathlib.Path(sys.argv[1]).iterdir()):
    if not (d / "log.jsonl").exists():
        continue
    log = [json.loads(l) for l in (d / "log.jsonl").read_text().splitlines()]
    tests = [e for e in log if e["kind"] == "test"]
    sim = [e for e in tests if e.get("stage") != "validation"]
    valid = [e for e in tests if e.get("valid")]
    fails = collections.Counter(c for e in sim for c in e.get("failures", []))
    print(f"{d.name}: {log[-1]['t'] / 60:.1f} min, tests {len(sim)} (+{len(tests) - len(sim)} rejected), "
          f"trace/view {sum(e['kind'] in ('trace', 'view') for e in log)}, valid {len(valid)}, "
          f"best {min((e['volume'] for e in valid), default=None)}, submits {sum(e['kind'] == 'submit' for e in log)}")
    if fails:
        print("    failure codes:", dict(fails.most_common(6)))
    if sim and not valid:
        print("    furthest (partial):", max(e.get("partial", 0.0) for e in sim))
    prog = [(i + 1, e["volume"]) for i, e in enumerate(sim) if e.get("valid") and e["volume"] == e["best"]]
    if prog:
        print("    best-so-far by test #:", prog[-10:])
