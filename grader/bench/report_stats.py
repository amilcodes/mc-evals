"""Aggregate statistics across benchmark waves, for the write-up.

    python3 bench/report_stats.py ../runs/bench/w1 ../runs/bench/w2 ../runs/bench/w3

Each folder holds manifest.json and summary.json. Only runs with a final verdict are counted.
"Volume before the loop" is the best volume when the run was first told to keep going (or
its final volume if it never was), so the gain shows what the continue messages bought.
"""
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

MODEL = {"fable": "Fable 5.2", "opus": "Opus 5.5", "sonnet": "Sonnet 5.5", "haiku": "Haiku 5.5"}
ORDER = list(MODEL.values())


def main():
    rows = []
    for folder in map(Path, sys.argv[1:]):
        man = json.loads((folder / "manifest.json").read_text())
        summ = {r["name"]: r for r in json.loads((folder / "summary.json").read_text())["runs"]}
        for run in man["runs"]:
            s = summ.get(run["name"])
            if not s or "final" not in s:
                continue
            fin = s["final"]
            first_reprompt = (run.get("reprompts") or [None])[0]
            before = first_reprompt["best"] if first_reprompt else (fin.get("volume") if fin.get("valid") else None)
            rows.append({
                "task": (lambda n: f"{n}x{n}" if isinstance(n, int) else f"{n[0]}x{n[1]}")(s.get("n", 3)), "model": MODEL[run["model"]], "run": run["name"],
                "door": bool(fin.get("valid")), "volume": fin.get("volume"), "score": s.get("score") or 0.0,
                "cost": s["cost"], "first": s["first_valid_minutes"], "tests": s["test_calls"],
                "before_loop": before, "reprompted": bool(first_reprompt), "rounds": s["rounds"],
                "placements": (fin.get("translations") or {}).get("passed"),
            })
    groups = defaultdict(list)
    for r in rows:
        groups[(r["task"], r["model"])].append(r)
    print(f"{'task':<5} {'model':<11} {'runs':>4} {'doors':>5} {'best':>5} {'median':>7} {'mean sc':>7} {'sd sc':>6} "
          f"{'first door':>10} {'cost':>7} {'tests':>5} {'loop gain':>9}")
    for task in sorted({k[0] for k in groups}):
        for model in ORDER:
            rs = groups.get((task, model))
            if not rs:
                continue
            doors = [r for r in rs if r["door"]]
            scores = [r["score"] for r in rs]
            gains = [r["before_loop"] / r["volume"] for r in doors if r["before_loop"] and r["volume"]]
            print(f"{task:<5} {model:<11} {len(rs):>4} {len(doors):>5} "
                  f"{(min(r['volume'] for r in doors) if doors else '-')!s:>5} "
                  f"{(statistics.median(r['volume'] for r in doors) if doors else '-')!s:>7} "
                  f"{statistics.mean(scores):>7.2f} {(statistics.stdev(scores) if len(scores) > 1 else 0):>6.2f} "
                  f"{(statistics.median(r['first'] for r in doors) if doors else float('nan')):>10.1f} "
                  f"{statistics.mean(r['cost'] for r in rs):>7.2f} {statistics.mean(r['tests'] for r in rs):>5.1f} "
                  f"{(statistics.mean(gains) if gains else float('nan')):>9.2f}")
    print()
    improved = [r for r in rows if r["door"] and r["reprompted"] and r["before_loop"] and r["volume"] < r["before_loop"]]
    with_door = [r for r in rows if r["door"] and r["reprompted"] and r["before_loop"]]
    print(f"runs with a door when first told to keep going: {len(with_door)}; improved afterwards: {len(improved)}")
    for r in improved:
        print(f"   {r['run']}: {r['before_loop']} -> {r['volume']}")
    late = [r for r in rows if r["door"] and r["reprompted"] and not r["before_loop"]]
    print(f"runs with no door when first told to keep going that then built one: {len(late)} {[r['run'] for r in late]}")


if __name__ == "__main__":
    main()
