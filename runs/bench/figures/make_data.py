"""Builds figures/data.json from the dashboard export and the speed census.

    python3 grader/bench/export_dashboard.py ...   (refreshes dashboard/runs.json, curve.json)
    python3 runs/bench/figures/make_data.py
    python3 runs/bench/figures/build.py
"""
import datetime
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BENCH = HERE.parent
KEEP = ["run", "wave", "task", "model", "status", "volume", "dims", "cost", "tests", "first_door_min", "minutes_limit", "placements", "rounds"]

runs = [{k: r.get(k) for k in KEEP} for r in json.loads((BENCH / "dashboard/runs.json").read_text())]
curve = json.loads((BENCH / "dashboard/curve.json").read_text())
by_run = {r["run"]: r for r in runs}

# Figure 3: standard 3x3 and 4x4 runs at their full limits (120 / 150 minutes); wave 9's 50-minute runs are left out.
progress = []
for r in runs:
    if r["status"] != "door" or r["task"] not in ("3×3 seamless", "4×4 seamless") or (r["minutes_limit"] or 0) < 120:
        continue
    steps, best = [], None
    for p in sorted((p for p in curve if p["run"] == r["run"]), key=lambda p: p["minutes"]):
        if p.get("best") is not None and p["best"] != best:
            best = p["best"]
            steps.append([round(p["minutes"], 1), best])
    if not steps:
        continue
    if steps[-1][1] != r["volume"]:  # final regrade can be smaller than the last test seen
        steps.append([steps[-1][0], r["volume"]])
    progress.append({"run": r["run"], "task": r["task"], "model": r["model"], "steps": steps, "end": r["minutes_limit"], "final": r["volume"]})

# Figure 7: speed census, one row per valid door
speed = []
for line in (BENCH / "search_pilot/speed_census.jsonl").read_text().splitlines():
    s = json.loads(line)
    b, a = s["base"], s["best_dev"]
    if s["confirm"]:
        a = s["confirm"]["final"]
    speed.append({"run": s["run"], "task": s["task"], "model": s["model"], "volume": b["volume"],
                  "before": [b["open_ticks"], b["close_ticks"]], "after": [a["open_ticks"], a["close_ticks"]],
                  "edits": len(s["applied"]),
                  "placements": s["confirm"]["placements_passed"] if s["confirm"] else None,
                  "rot180": bool(s["confirm"] and s["confirm"]["rot180"]["valid"]) if s["confirm"] else None})

out = {"runs": runs, "progress": progress, "speed": speed, "generated": datetime.date.today().isoformat()}
(HERE / "data.json").write_text(json.dumps(out, ensure_ascii=False))
print(len(runs), "runs,", len(progress), "progress lines,", len(speed), "speed rows,", sum(s["after"] != s["before"] for s in speed), "faster")
