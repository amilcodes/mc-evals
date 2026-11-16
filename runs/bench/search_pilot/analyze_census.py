"""Summarises a census_<run>.jsonl file.   python3 analyze_census.py census_<run>.jsonl <seed_volume> <seed_open> <seed_close>"""
import collections
import json
import sys

path, vol0, open0, close0 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
R = [json.loads(l) for l in open(path)]
err = [r for r in R if "error" in r]
R = [r for r in R if "dev" in r]


def kind(r):
    a, b = r["from"][0], r["to"][0]
    if a == "air":
        return "fill empty cell"
    if b == "air":
        return "delete block"
    if a == b:
        return "re-orient/re-time same block"
    return "swap block type"


def ok(r):
    return bool(r.get("final", {}).get("valid"))


out = {"graded": len(R), "errors": len(err), "dev_valid": sum(r["dev"]["valid"] for r in R), "final_valid": sum(ok(r) for r in R)}
by = collections.defaultdict(lambda: [0, 0, 0])
for r in R:
    k = kind(r)
    by[k][0] += 1
    by[k][1] += r["dev"]["valid"]
    by[k][2] += ok(r)
out["by_kind"] = {k: {"n": v[0], "dev_valid": v[1], "final_valid": v[2], "final_rate": round(v[2] / v[0], 4)} for k, v in by.items()}

# functional cells = cells that hold a block in the seed
func = [r for r in R if r["from"][0] != "air"]
cells = collections.defaultdict(lambda: [0, 0, ""])
for r in func:
    c = cells[tuple(r["pos"])]
    c[0] += 1
    c[1] += ok(r)
    c[2] = r["from"][0]
crit = sorted(((v[1], k, v[2]) for k, v in cells.items()))
out["functional_cells"] = len(cells)
out["functional_cells_with_any_working_alternative"] = sum(1 for v in cells.values() if v[1])
out["functional_cells_rigid"] = [[list(k), b] for n, k, b in crit if n == 0]
out["functional_cells_flexible"] = [[list(k), b, n] for n, k, b in sorted(crit, reverse=True) if n][:15]

# nontrivial neutral moves: change an existing block and still pass final
neutral = [r for r in func if ok(r)]
out["nontrivial_working_neighbours"] = len(neutral)
out["nontrivial_examples"] = [[r["pos"], r["from"][0], r["from"][1], "->", r["to"][0], r["to"][1], r["final"]["volume"], r["final"]["open_ticks"], r["final"]["close_ticks"]] for r in neutral[:40]]

better = [r for r in R if ok(r) and (r["final"]["volume"] < vol0 or (r["final"]["volume"] <= vol0 and (r["final"]["open_ticks"] < open0 or r["final"]["close_ticks"] < close0)))]
out["improvements"] = [[r["pos"], r["from"][0], r["from"][1], "->", r["to"][0], r["to"][1], r["final"]["volume"], r["final"]["open_ticks"], r["final"]["close_ticks"]] for r in sorted(better, key=lambda r: (r["final"]["volume"], r["final"]["open_ticks"] + r["final"]["close_ticks"]))]
worse_bigger = [r for r in R if ok(r) and r["final"]["volume"] > vol0]
out["working_but_larger"] = len(worse_bigger)
out["dev_pass_final_fail"] = sum(1 for r in R if r["dev"]["valid"] and not ok(r))

bad = [r for r in R if not r["dev"]["valid"]]
out["failure_codes"] = collections.Counter(r["dev"]["fail"] for r in bad).most_common()
hist = collections.Counter(round(r["dev"]["partial"] * 6) / 6 for r in bad)
out["broken_partial_hist (flips passed of 6, incl. fractional cells)"] = sorted((round(k, 2), v) for k, v in hist.items())
out["broken_flips_passed"] = sorted(collections.Counter(r["dev"]["flips_passed"] for r in bad).items())
print(json.dumps(out, indent=1))
