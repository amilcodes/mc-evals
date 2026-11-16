"""Port and hidden-rule tasks from the physics matrix (data/physics_matrix.json).

    python3 gen_port.py <run> <target-physics-json> [--hidden] [--ref <run>|auto] [--full-limit N] [--sample N]
                        [--retime-search]

Under the target physics:
  1. the start door (as built, verified under its home physics) must fail the final grade;
  2. the reference must pass the final grade. --ref auto picks the smallest door of the same
     size that passed the target physics in the matrix; --retime-search additionally searches
     the start door's timing edits (every repeater delay/facing, observer facing, repeater <->
     observer swap, singly and in pairs) for a same-volume port, which becomes the reference
     if it passes the final grade and is no larger than the auto reference;
  3. single-edit brute force over the census neighbourhood of the start design (full if the
     neighbourhood is at most --full-limit, otherwise local to signal components + a sample).
Writes tasks/port-<size>-<run>-<tag>.json (or hidden-<...>.json with --hidden).
"""
import argparse
import itertools
import json
import random
import time

import lib
from lib import census

H4 = ["north", "south", "east", "west"]
D6 = H4 + ["up", "down"]
SIGNAL = {"repeater", "observer", "comparator", "redstone_wire", "redstone_torch", "redstone_wall_torch"}


def timing_edits(design):
    out = []
    for b in design["blocks"]:
        bid, p = lib.canon(b)
        f = p.get("facing")
        cur = (bid, p)
        alts = []
        if bid == "repeater":
            alts += [("repeater", {"facing": f, "delay": str(x)}) for x in range(1, 5) if str(x) != p["delay"]]
            alts += [("observer", {"facing": f})]
        elif bid == "observer":
            alts += [("observer", {"facing": x}) for x in D6 if x != f]
            if f in H4:
                alts += [("repeater", {"facing": f, "delay": str(x)}) for x in range(1, 5)]
        for a in alts:
            out.append({"pos": b["pos"], "from": [cur[0], cur[1]], "to": [a[0], a[1]]})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("target")
    ap.add_argument("--hidden", action="store_true")
    ap.add_argument("--ref", default="auto")
    ap.add_argument("--full-limit", type=int, default=4200)
    ap.add_argument("--sample", type=int, default=1200)
    ap.add_argument("--retime-search", action="store_true")
    ap.add_argument("--pairs-limit", type=int, default=1500)
    a = ap.parse_args()
    target = json.loads(a.target)
    tag = lib.phys_tag(target)
    d = lib.door(a.run)
    n, start, home = d["n"], d["candidate"], d["physics"]
    size = lib.size_label(n)
    mat = json.load(open(lib.HERE / "data/physics_matrix.json"))
    kind = "hidden_rule" if a.hidden else "port"
    tid = f"{'hidden' if a.hidden else 'port'}-{size}-{a.run}-{tag.replace(',', '+').replace('=', '')}"
    rng = random.Random(tid)

    # reference candidates: same size, passed the target physics in the matrix (dev), smallest first
    cands = sorted((x for x in lib.doors() if lib.rules.dims(x["n"]) == lib.rules.dims(n) and x["run"] != a.run
                    and mat.get(tag, {}).get(x["run"], {}).get("valid")), key=lambda x: x["volume"])
    if a.ref != "auto":
        cands = [lib.door(a.ref)]
    log = {"task": tid, "candidates": [x["run"] for x in cands]}

    with lib.kernel(target) as k:
        st, sb = lib.grade_ladder(k, start, n)
        assert st != "final_ok", f"{a.run} passes under {tag}; nothing to port"
        start_final = lib.brief(lib.grade(k, start, n, "seamless", "final"))
        ref = None
        for c in cands:
            s, b = lib.grade_ladder(k, c["candidate"], n)
            log.setdefault("ref_checks", []).append([c["run"], s])
            if s == "final_ok":
                ref = {"source": c["run"], "kind": "another agent's door", "design": c["candidate"], **{x: b[x] for x in ("volume", "open_ticks", "close_ticks")}}
                break
        same_volume = None
        if a.retime_search:
            t0 = time.monotonic()
            te = timing_edits(start)
            found = None
            for e in te:
                s, b = lib.grade_ladder(k, census.apply(start, e), n)
                if s == "final_ok" and b["volume"] <= d["volume"]:
                    found = ([e], b)
                    break
            pairs = list(itertools.combinations(range(len(te)), 2))
            pairs = [p for p in pairs if te[p[0]]["pos"] != te[p[1]]["pos"]]
            rng.shuffle(pairs)
            npairs = 0
            if not found:
                for i, j in pairs[: a.pairs_limit]:
                    npairs += 1
                    s_ = lib.apply_edits(start, [te[i], te[j]])
                    if lib.grade(k, s_, n, "seamless", "screen")["valid"]:
                        s, b = lib.grade_ladder(k, s_, n)
                        if s == "final_ok" and b["volume"] <= d["volume"]:
                            found = ([te[i], te[j]], b)
                            break
            log["retime_search"] = {"timing_edits": len(te), "pairs_graded": npairs, "pairs_total": len(pairs),
                                    "found": found[0] if found else None, "seconds": round(time.monotonic() - t0)}
            if found:
                same_volume = {"edits": found[0], **{x: found[1][x] for x in ("volume", "open_ticks", "close_ticks")}}
                if ref is None or found[1]["volume"] <= ref["volume"]:
                    ref = {"source": a.run + " + timing edits", "kind": "retimed start door", "design": lib.apply_edits(start, found[0]),
                           **{x: found[1][x] for x in ("volume", "open_ticks", "close_ticks")}}
        if ref is None:
            print(f"{tid}: no reference passes {tag}; skipped. {log}", flush=True)
            lib.write_json(lib.HERE / f"data/port_{tid}.json", log)
            return
        # single-edit brute force
        t0 = time.monotonic()
        neigh = lib.neighbours(start, n)
        total = len(neigh)
        full = total <= a.full_limit
        if full:
            todo = neigh
        else:
            sig = {tuple(b["pos"]) for b in start["blocks"] if lib.canon(b)[0] in SIGNAL}
            local = [e for e in neigh if tuple(e["pos"]) in sig]
            rest = [e for e in neigh if tuple(e["pos"]) not in sig]
            todo = local + rng.sample(rest, min(a.sample, len(rest)))
        fixes, graded = lib.single_edit_fixes(k, start, n, todo, stop_at_first=False, log_every=1000)
        fixes = [f for f in fixes if f["final"]["volume"] <= d["volume"]]
        log["brute_force"] = {"total": total, "graded": graded, "full": full, "fixes": fixes[:20], "seconds": round(time.monotonic() - t0)}
    lib.write_json(lib.HERE / f"data/port_{tid}.json", log)

    max_volume = max(d["volume"], ref["volume"])
    if fixes:
        same_volume = same_volume or {"edits": [fixes[0]], **{x: fixes[0]["final"][x] for x in ("volume", "open_ticks", "close_ticks")}}
    home_txt = "vanilla Minecraft 26.3" if not home else f"Minecraft 26.3 with changed physics {json.dumps(home)}"
    if a.hidden:
        told = (f"This {size} seamless piston door passes the grader under {home_txt}. The server it will be graded on has had "
                f"some of its game constants changed, and the door no longer works there. You are not told which. "
                f"Your test calls run on that server. Make a door that passes there, in a box of volume at most {max_volume}.")
    else:
        told = (f"This {size} seamless piston door passes the grader under {home_txt}. It will now be graded under Minecraft 26.3 "
                f"with these physics changes: {json.dumps(target)} (vanilla: repeater_unit 2, push_limit 12, observer_delay 2, "
                f"observer_pulse 2), and it fails there. Port it: produce a door that passes under the new physics, in a box of "
                f"volume at most {max_volume}. You may change as much as you like.")
    task = {
        "id": tid, "family": "piston_doors", "kind": kind, "n": n, "size": size, "track": "seamless",
        "physics": target, "physics_told": not a.hidden, "told": told, "start": start,
        "constraints": {"max_volume": max_volume, "max_blocks": None, "allowed_blocks": None, "edit_budget": None, "initial_state": None},
        "reference": {**ref, "edits_from_start": lib.edit_distance(start, ref["design"])},
        "provenance": {"start_run": a.run, "start_model": d["model"], "start_home_physics": home, "generator": "gen_port.py"},
        "difficulty": {
            "single_edit_fix": bool(fixes) if full else (True if fixes else "none found (partial search)"),
            "single_edit_fixes_found": len(fixes),
            "neighbourhood_size": total, "neighbours_graded": graded,
            "brute_force": "full" if full else "every state at every signal-component cell + random sample of the rest",
            "same_volume_port_known": bool(same_volume) or ref["volume"] <= d["volume"],
            "same_volume_port": same_volume if same_volume else ({"source": ref["source"], "note": "a different design of the same or smaller volume"} if ref["volume"] <= d["volume"] else None),
            "retime_search": log.get("retime_search"),
            "start_fail": start_final["fail"], "start_final_partial": start_final["partial"],
            "start_volume": d["volume"],
            "reference_volume": ref["volume"], "reference_open_ticks": ref["open_ticks"], "reference_close_ticks": ref["close_ticks"],
        },
    }
    lib.write_json(lib.TASKS / f"{tid}.json", task)
    print(f"{tid}: ref {ref['source']} vol {ref['volume']}; single-edit fixes {len(fixes)} of {graded} graded ({'full' if full else 'partial'})", flush=True)
    lib.cleanup()


if __name__ == "__main__":
    main()
