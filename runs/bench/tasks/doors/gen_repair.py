"""Repair tasks: perturb a verified door with k = 2..4 natural edits.

    python3 gen_repair.py <run> <k>[,<k>...] [--full-limit N] [--sample N] [--seed S]

For each requested k, under the door's own physics:
  1. draw k "natural" edits at distinct mechanism cells (wrong facing, wrong repeater delay,
     sticky <-> normal piston, slime <-> honey, a conducting block swapped for glass, a deleted
     block ...). Each edit must break the door on its own (1-cycle screen).
  2. the combined design must fail.
  3. local check: every census state at every perturbed cell (which includes each exact revert)
     must leave the door failing the final grade.
  4. brute force: every single edit in the census neighbourhood of the perturbed design (plus the
     exact reverts) is graded; if the neighbourhood is larger than --full-limit, the edits at and
     next to the perturbed cells plus a random --sample of the rest are graded instead. Any edit
     that passes the final grade rejects the perturbation (counted in the log).
Accepted perturbations are written as tasks/repair-<size>-<run>-k<k>.json.
Per-door bookkeeping (single-edit screens, rejections) goes to data/repair_<run>.json.
"""
import argparse
import json
import random
import time

import lib
from lib import census, rules

H4 = ["north", "south", "east", "west"]
D6 = H4 + ["up", "down"]


def natural_mutations(bid, p):
    """Plausible build mistakes for one block, as census-palette states."""
    out = [("air", {})]
    f = p.get("facing")
    if bid in ("piston", "sticky_piston"):
        out.append(("sticky_piston" if bid == "piston" else "piston", {"facing": f}))
        out += [(bid, {"facing": x}) for x in D6 if x != f]
    elif bid == "observer":
        out += [("observer", {"facing": x}) for x in D6 if x != f]
    elif bid == "repeater":
        d = p.get("delay", "1")
        out += [("repeater", {"facing": f, "delay": str(x)}) for x in range(1, 5) if str(x) != d]
        out += [("repeater", {"facing": x, "delay": d}) for x in H4 if x != f]
    elif bid == "comparator":
        out.append(("comparator", {"facing": f, "mode": "subtract" if p.get("mode") == "compare" else "compare"}))
        out += [("comparator", {"facing": x, "mode": p.get("mode", "compare")}) for x in H4 if x != f]
    elif bid == "redstone_wall_torch":
        out += [("redstone_wall_torch", {"facing": x}) for x in H4 if x != f] + [("redstone_torch", {})]
    elif bid == "redstone_torch":
        out += [("redstone_wire", {})]
    elif bid == "slime_block":
        out += [("honey_block", {}), ("stone", {})]
    elif bid == "honey_block":
        out += [("slime_block", {}), ("stone", {})]
    elif bid == "redstone_block":
        out += [("stone", {}), ("target", {})]
    elif bid == "redstone_wire":
        out += [("stone", {})]
    elif bid in ("obsidian", "target", "note_block", "glass"):
        out += [("stone", {})]
    elif "minecraft:" + bid in rules.PLAIN:
        out += [("glass", {}), ("slime_block", {}), ("obsidian", {})]
    return [m for m in out if m in census.PALETTE or m == ("air", {})]


def mutable_cells(design, n):
    out = []
    for b in design["blocks"]:
        bid, p = lib.canon(b)
        pos = tuple(b["pos"])
        if bid in ("lever", "piston_head") or rules.in_doorway(n, pos):
            continue
        if (b.get("props") or {}).get("extended") == "true":
            continue
        out.append((pos, (bid, p)))
    return out


def edit(pos, cur, to):
    return {"pos": list(pos), "from": [cur[0], cur[1]], "to": [to[0], to[1]]}


def local_edits(design, n, cells_):
    """Every palette state at the given cells, plus exact reverts handled by the caller."""
    cs = {tuple(b["pos"]): lib.canon(b) for b in design["blocks"]}
    out = []
    for pos in cells_:
        cur = cs.get(pos, ("air", {}))
        for st in census.PALETTE:
            if st != cur:
                out.append(edit(pos, cur, st))
    return out


def near(p, q, r=1):
    return sum(abs(a - b) for a, b in zip(p, q)) <= r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("ks")
    ap.add_argument("--full-limit", type=int, default=4200)
    ap.add_argument("--sample", type=int, default=1200)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--attempts", type=int, default=8)
    a = ap.parse_args()
    d = lib.door(a.run)
    n, seed, phys = d["n"], d["candidate"], d["physics"]
    size = lib.size_label(n)
    book_path = lib.HERE / f"data/repair_{a.run}.json"
    book = json.load(open(book_path)) if book_path.exists() else {"run": a.run, "single": {}, "attempts": []}
    rng = random.Random(f"{a.run}-{a.seed}")
    cells_ = mutable_cells(seed, n)

    with lib.kernel(phys) as k:
        st, ref = lib.grade_ladder(k, seed, n)
        assert st == "final_ok", f"seed does not pass final under its own physics: {st} {ref}"
        print(f"{a.run} {size} {lib.phys_tag(phys)}: seed ok {ref}", flush=True)

        def breaks(pos, cur, to):
            key = json.dumps([list(pos), list(to)], sort_keys=True)
            if key not in book["single"]:
                r = lib.grade(k, census.apply(seed, edit(pos, cur, to)), n, "seamless", "screen")
                book["single"][key] = not r["valid"]
            return book["single"][key]

        for kk in [int(x) for x in a.ks.split(",")]:
            tid = f"repair-{size}-{a.run}-k{kk}"
            if (lib.TASKS / f"{tid}.json").exists():
                print(f"  {tid} exists", flush=True)
                continue
            for attempt in range(a.attempts):
                t0 = time.monotonic()
                # 1. k breaking edits at distinct cells, at least 2 cells apart so they are separate faults
                picks, tries = [], 0
                while len(picks) < kk and tries < 400:
                    tries += 1
                    pos, cur = rng.choice(cells_)
                    if any(near(pos, q[0], 1) for q in picks):
                        continue
                    to = rng.choice([m for m in natural_mutations(*cur) if m != cur])
                    if breaks(pos, cur, to):
                        picks.append((pos, cur, to))
                if len(picks) < kk:
                    print("  could not find enough breaking edits", flush=True)
                    break
                pert = [edit(p, c, t) for p, c, t in picks]
                start = lib.apply_edits(seed, pert)
                rec = {"k": kk, "edits": pert}
                # 2. must fail
                s0 = lib.grade(k, start, n, "seamless", "screen")
                if s0["valid"]:
                    rec["rejected"] = "combined edits still pass the screen"
                    book["attempts"].append(rec)
                    continue
                # 3 + 4. single-edit search
                reverts = [edit(tuple(e["pos"]), tuple(e["to"]), tuple(e["from"])) for e in pert]
                for r_ in reverts:
                    r_["to"] = [r_["to"][0], r_["to"][1]]
                pcells = [tuple(e["pos"]) for e in pert]
                neigh = lib.neighbours(start, n)
                total = len(neigh)
                local = [e for e in neigh if any(near(tuple(e["pos"]), q, 1) for q in pcells)]
                rest = [e for e in neigh if not any(near(tuple(e["pos"]), q, 1) for q in pcells)]
                full = total <= a.full_limit
                todo, seen = [], set()
                for e in reverts + local + (rest if full else rng.sample(rest, min(a.sample, len(rest)))):
                    key = (tuple(e["pos"]), json.dumps(e["to"], sort_keys=True))
                    if key not in seen:
                        seen.add(key)
                        todo.append(e)
                fixes, graded = lib.single_edit_fixes(k, start, n, todo, stop_at_first=True, log_every=1000)
                rec.update({"neighbours_total": total, "graded": graded, "full": full, "seconds": round(time.monotonic() - t0)})
                if fixes:
                    rec["rejected"] = "a single edit fixes it"
                    rec["fix"] = fixes[0]
                    book["attempts"].append(rec)
                    lib.write_json(book_path, book)
                    print(f"  k={kk} attempt {attempt}: single-edit fix found after {graded} ({fixes[0]['pos']} -> {fixes[0]['to']})", flush=True)
                    continue
                fin = lib.grade(k, start, n, "seamless", "final")
                assert not fin["valid"]
                rec["accepted"] = tid
                book["attempts"].append(rec)
                lib.write_json(book_path, book)
                told = (f"This {size} seamless piston door used to pass the grader. {kk} of its blocks were then changed "
                        f"(each one a plausible build mistake: wrong facing, wrong repeater delay, wrong block type, or a "
                        f"missing block), and now it fails. Repair it. Grading physics: "
                        + ("vanilla Minecraft 26.3." if not phys else "Minecraft 26.3 with changed physics " + json.dumps(phys) + ".")
                        + f" Your fix may change at most {kk + 2} cells of the given design, the box may not grow beyond "
                        f"volume {ref['volume']}, and the initial state must stay '{seed['initial_state']}'.")
                task = {
                    "id": tid, "family": "piston_doors", "kind": "repair", "n": n, "size": size, "track": "seamless",
                    "physics": phys, "physics_told": True, "told": told, "start": start,
                    "constraints": {"max_volume": ref["volume"], "max_blocks": None, "allowed_blocks": None,
                                    "edit_budget": kk + 2, "initial_state": seed["initial_state"]},
                    "reference": {"source": a.run, "kind": "original door", "design": seed, "volume": ref["volume"],
                                  "open_ticks": ref["open_ticks"], "close_ticks": ref["close_ticks"],
                                  "edits_from_start": lib.edit_distance(start, seed)},
                    "provenance": {"seed_run": a.run, "seed_model": d["model"], "perturbation": pert, "generator": "gen_repair.py",
                                   "rng_seed": a.seed, "attempt": attempt},
                    "difficulty": {
                        "edits_made": kk,
                        "single_edit_fix": False if full else "none found (partial search)",
                        "neighbourhood_size": total, "neighbours_graded": graded,
                        "brute_force": "full" if full else f"local (cells within 1 of a perturbed cell) + exact reverts + random sample of {min(a.sample, len(rest))}",
                        "start_fail": lib.brief(fin)["fail"], "start_final_partial": fin["partial"],
                        "reference_volume": ref["volume"], "reference_open_ticks": ref["open_ticks"], "reference_close_ticks": ref["close_ticks"],
                    },
                }
                lib.write_json(lib.TASKS / f"{tid}.json", task)
                print(f"  {tid}: accepted after {graded} neighbours graded ({'full' if full else 'partial'}), {rec['seconds']}s", flush=True)
                break
        lib.write_json(book_path, book)
    lib.cleanup()


if __name__ == "__main__":
    main()
