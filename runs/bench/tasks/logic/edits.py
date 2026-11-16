"""Single-block edits: the fault model used to break builds and the neighbourhood used to prove hardness.

An edit sets one cell to one block state ("air" deletes). The single-edit neighbourhood of a build
is every cell of the task's bounding box that is not a harness cell, set to every state of PALETTE
other than its current one. PALETTE is the census palette (runs/bench/search_pilot/census.py) plus
the lever-free states this family uses (wall torch facings are already in it).
"""
import copy
import random

H4 = ["north", "south", "east", "west"]
D6 = H4 + ["up", "down"]
OPP = {"north": "south", "south": "north", "east": "west", "west": "east", "up": "down", "down": "up"}


def palette():
    out = [("air", {}), ("stone", {}), ("redstone_block", {}), ("slime_block", {}), ("honey_block", {}),
           ("obsidian", {}), ("glass", {}), ("target", {}), ("note_block", {}), ("redstone_wire", {}),
           ("redstone_torch", {})]
    out += [("piston", {"facing": f}) for f in D6] + [("sticky_piston", {"facing": f}) for f in D6]
    out += [("observer", {"facing": f}) for f in D6]
    out += [("repeater", {"facing": f, "delay": str(d)}) for f in H4 for d in range(1, 5)]
    out += [("comparator", {"facing": f, "mode": m}) for f in H4 for m in ("compare", "subtract")]
    out += [("redstone_wall_torch", {"facing": f}) for f in H4]
    return out


PALETTE = palette()


def norm(b):
    """(id, props) with only the props an edit can set (shape/power/lit/powered are recomputed)."""
    if b is None:
        return ("air", {})
    bid = b["id"].split(":")[-1]
    p = {k: str(v) for k, v in (b.get("props") or {}).items()}
    if bid in ("redstone_wire", "redstone_torch", "redstone_block", "stone", "target", "note_block", "glass",
               "obsidian", "slime_block", "honey_block"):
        return (bid, {})
    if bid == "repeater":
        return (bid, {"facing": p.get("facing", "north"), "delay": p.get("delay", "1")})
    if bid == "comparator":
        return (bid, {"facing": p.get("facing", "north"), "mode": p.get("mode", "compare")})
    if bid in ("piston", "sticky_piston", "observer", "redstone_wall_torch"):
        return (bid, {"facing": p.get("facing", "north")})
    return (bid, p)


def cells_of(build):
    return {tuple(b["pos"]): b for b in build}


def apply(build, edit):
    """edit = {"pos": [x,y,z], "to": [id, props]}; returns a new build."""
    pos = list(edit["pos"])
    out = [copy.deepcopy(b) for b in build if list(b["pos"]) != pos]
    bid, props = edit["to"]
    if bid != "air":
        b = {"pos": pos, "id": bid}
        if props:
            b["props"] = dict(props)
        out.append(b)
    return sorted(out, key=lambda b: tuple(b["pos"]))


def apply_all(build, edits):
    for e in edits:
        build = apply(build, e)
    return build


def neighbourhood(build, task):
    """Every single edit inside the task box (harness cells excluded)."""
    from lib import harness_blocks
    harness = {p for p, _, _ in harness_blocks(task["harness"])}
    lo, hi = task["limits"]["bbox"]["min"], task["limits"]["bbox"]["max"]
    cells = cells_of(build)
    out = []
    for x in range(lo[0], hi[0] + 1):
        for y in range(lo[1], hi[1] + 1):
            for z in range(lo[2], hi[2] + 1):
                p = (x, y, z)
                if p in harness:
                    continue
                cur = norm(cells.get(p))
                for st in PALETTE:
                    if st != cur:
                        out.append({"pos": list(p), "to": [st[0], dict(st[1])]})
    return out


def faults(build, task, rng=None):
    """Plausible single faults: mis-set delays, turned or swapped components, missing or stray blocks."""
    from lib import harness_blocks
    harness = {p for p, _, _ in harness_blocks(task["harness"])}
    cells = cells_of(build)
    out = []
    for p, b in cells.items():
        bid, props = norm(b)
        f = props.get("facing")
        if bid == "repeater":
            out += [{"pos": list(p), "to": ["repeater", {**props, "delay": str(d)}], "kind": "delay"}
                    for d in range(1, 5) if str(d) != props["delay"]]
            out.append({"pos": list(p), "to": ["repeater", {**props, "facing": OPP[f]}], "kind": "reversed"})
            out.append({"pos": list(p), "to": ["comparator", {"facing": f, "mode": "compare"}], "kind": "swapped"})
        elif bid == "comparator":
            out.append({"pos": list(p), "to": ["comparator", {**props, "mode": "subtract" if props["mode"] == "compare" else "compare"}], "kind": "mode"})
            out.append({"pos": list(p), "to": ["comparator", {**props, "facing": OPP[f]}], "kind": "reversed"})
            out.append({"pos": list(p), "to": ["repeater", {"facing": f, "delay": "1"}], "kind": "swapped"})
        elif bid == "observer":
            out += [{"pos": list(p), "to": ["observer", {"facing": g}], "kind": "turned"} for g in D6 if g != f]
        elif bid in ("piston", "sticky_piston"):
            out.append({"pos": list(p), "to": ["piston" if bid == "sticky_piston" else "sticky_piston", props], "kind": "swapped"})
            out.append({"pos": list(p), "to": [bid, {"facing": OPP[f]}], "kind": "reversed"})
        elif bid == "redstone_wall_torch":
            out.append({"pos": list(p), "to": ["air", {}], "kind": "missing"})
        elif bid == "redstone_wire":
            out.append({"pos": list(p), "to": ["air", {}], "kind": "missing"})
            out.append({"pos": list(p), "to": ["stone", {}], "kind": "swapped"})
            out.append({"pos": list(p), "to": ["repeater", {"facing": "west", "delay": "1"}], "kind": "swapped"})
        elif bid == "redstone_block":
            out.append({"pos": list(p), "to": ["stone", {}], "kind": "swapped"})
        elif bid == "stone" and p[1] == 1:
            out.append({"pos": list(p), "to": ["glass", {}], "kind": "swapped"})
    # stray blocks next to signal components
    lo, hi = task["limits"]["bbox"]["min"], task["limits"]["bbox"]["max"]
    seen = set()
    for p, b in cells.items():
        if p[1] != 1:
            continue
        for d in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0)):
            q = (p[0] + d[0], p[1] + d[1], p[2] + d[2])
            if q in cells or q in harness or q in seen or not all(lo[i] <= q[i] <= hi[i] for i in range(3)):
                continue
            seen.add(q)
            out.append({"pos": list(q), "to": ["stone", {}], "kind": "stray"})
            out.append({"pos": list(q), "to": ["redstone_block", {}], "kind": "stray"})
    return out
