"""Log-scale scoring and a variance / sample-size check, for choosing the next wave.

    python3 bench/log_stats.py ../runs/bench/dashboard/runs.json

Log score = log2(reference / volume): +1 is a door half the reference's volume, 0 matches it.
A run with no working door gets the log score of a door filling the whole test region
(48^3 = 110,592 blocks), the largest door the grader could accept. Doors-only statistics are
reported separately so the floor does not drive them.

Runs needed: two-sample, two-sided alpha 0.05, power 0.8, n = 2 (1.96 + 0.84)^2 (sd / gap)^2
with sd pooled from the two models. A planning estimate, not a test.
"""
import json
import math
import statistics as st
import sys
from collections import defaultdict
from itertools import combinations

FLOOR_VOLUME = 48 ** 3
Z = (1.96 + 0.84) ** 2


def log_score(r):
    vol = r["volume"] if r["status"] == "door" else FLOOR_VOLUME
    return math.log2(r["reference"] / vol)


def main():
    runs = json.load(open(sys.argv[1]))
    g = defaultdict(list)
    for r in runs:
        g[(r["task"], r["model"])].append(r)
    print(f"{'task':<14}{'model':<12}{'n':>3}{'doors':>6}{'mean ratio':>11}{'sd':>6}{'mean log2':>10}{'sd':>6}{'log2 doors':>11}{'sd':>6}")
    stats = {}
    for (task, model), rs in sorted(g.items()):
        ratio = [r["score"] for r in rs]
        logs = [log_score(r) for r in rs]
        dl = [log_score(r) for r in rs if r["status"] == "door"]
        sd = lambda xs: st.stdev(xs) if len(xs) > 1 else float("nan")
        stats[(task, model)] = (ratio, logs, dl)
        print(f"{task:<14}{model:<12}{len(rs):>3}{len(dl):>6}{st.mean(ratio):>11.2f}{sd(ratio):>6.2f}{st.mean(logs):>10.2f}{sd(logs):>6.2f}"
              f"{(st.mean(dl) if dl else float('nan')):>11.2f}{sd(dl):>6.2f}")
    print("\nruns per model to separate each pair (power 0.8):")
    for task in sorted({k[0] for k in stats}):
        models = [k[1] for k in stats if k[0] == task]
        for a, b in combinations(models, 2):
            out = []
            for name, idx in (("ratio", 0), ("log2", 1), ("log2 doors", 2)):
                xa, xb = stats[(task, a)][idx], stats[(task, b)][idx]
                if len(xa) < 2 or len(xb) < 2:
                    out.append(f"{name}: too few"); continue
                gap = abs(st.mean(xa) - st.mean(xb))
                sd = math.sqrt((st.variance(xa) + st.variance(xb)) / 2)
                if gap == 0:
                    out.append(f"{name}: no gap"); continue
                need = math.ceil(2 * Z * (sd / gap) ** 2) if sd > 0 else 2
                out.append(f"{name}: gap {gap:.2f} sd {sd:.2f} -> {need}")
            print(f"  {task} {a} vs {b}: " + "; ".join(out))


if __name__ == "__main__":
    main()
