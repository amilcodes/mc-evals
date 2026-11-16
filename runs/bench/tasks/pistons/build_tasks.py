"""Generates and verifies the piston-machine tasks. Every function takes a live kernel `k`
started with the physics it needs (one kernel at a time; see check.kernel_for).

Stages (each writes small JSON files next to this script):
  refs(k)                    vanilla: verify every reference machine            -> refs/<name>.json
  break_scan(k, name)        vanilla: grade natural single edits of a reference -> work/breaks_<name>.json
  neighbourhood(k, spec, blocks)  every single edit inside the task box; returns the passing ones
  physics_scan(k, physics)   grade every reference under changed physics        -> work/physics_<tag>.json
"""
import copy
import json
import time
from pathlib import Path

import check as C
import machines as M

HERE = Path(__file__).resolve().parent
REFS, TASKS, WORK = HERE / "refs", HERE / "tasks", HERE / "work"
for d in (REFS, TASKS, WORK):
    d.mkdir(exist_ok=True)

H4 = ["north", "south", "east", "west"]
D6 = H4 + ["up", "down"]


def S(bid, **props):
    return {"id": "minecraft:" + bid, **({"props": {k: str(v) for k, v in props.items()}} if props else {})}


def generic_palette():
    """The single-edit palette: every state a one-block edit may write (None = make the cell air)."""
    out = [None] + [S(x) for x in ("stone", "redstone_block", "slime_block", "honey_block", "obsidian", "glass",
                                   "redstone_wire", "redstone_torch", "target", "note_block")]
    out += [S(p, facing=f) for p in ("piston", "sticky_piston", "observer") for f in D6]
    out += [S("repeater", facing=f, delay=d) for f in H4 for d in range(1, 5)]
    out += [S("comparator", facing=f, mode=m) for f in H4 for m in ("compare", "subtract")]
    out += [S("redstone_wall_torch", facing=f) for f in H4]
    return out


def key(state):
    if state is None:
        return "air"
    return C.rules.state_string(state["id"], state.get("props") or {})


def palette_for(blocks):
    """Generic palette plus every exact (non-lever) block state used in the given build(s)."""
    pal = {key(p): p for p in generic_palette()}
    for bl in blocks:
        if bl["id"].endswith(":lever") or bl["id"].endswith(":piston_head"):
            continue
        if (bl.get("props") or {}).get("extended") == "true":
            continue
        st = {"id": bl["id"], **({"props": dict(bl["props"])} if bl.get("props") else {})}
        pal.setdefault(key(st), st)
    return list(pal.values())


def cell_map(blocks):
    return {tuple(b["pos"]): b for b in blocks}


def apply(blocks, edits):
    cells = cell_map(copy.deepcopy(blocks))
    for e in edits:
        p = tuple(e["pos"])
        cells.pop(p, None)
        if e["to"] is not None:
            cells[p] = {"pos": list(p), **copy.deepcopy(e["to"])}
    return [cells[p] for p in sorted(cells)]


def edit_str(e):
    return f"{e['pos']}: {e.get('from', '?')} -> {key(e['to'])}"


def graded(k, spec, blocks, screen=2):
    """Full check, but with a cheap screen (first `screen` toggles) to reject most failures early."""
    if screen:
        r = C.check(k, spec, blocks, n_toggles=screen)
        if not r["pass"]:
            return r
    return C.check(k, spec, blocks)


# ---------------------------------------------------------------- references

def refs(k, names=None):
    out = {}
    for name, f in M.MACHINES.items():
        if names and name not in names:
            continue
        m = f()
        r = C.check(k, m["spec"], m["blocks"])
        m["verified"] = {"physics": {}, "pass": r["pass"], "timings": r["timings"], "block_count": r["block_count"]}
        (REFS / f"{name}.json").write_text(json.dumps(m, indent=1))
        out[name] = C.brief(r)
    return out


def load_ref(name):
    return json.loads((REFS / f"{name}.json").read_text())


# ---------------------------------------------------------------- natural single-edit breaks

def natural_edits(m):
    """Plausible one-block mistakes on the reference's own blocks (and a few additions)."""
    spec = m["spec"]
    protect = {tuple(spec["lever"])} | {tuple(f[:3]) for f in spec.get("fixed", [])}
    conserve = set(spec.get("conserve", {}))
    cells = cell_map(m["blocks"])
    out = []
    for p, bl in cells.items():
        bid, props = bl["id"].split(":")[1], bl.get("props") or {}
        if p in protect or bl["id"] in conserve or bid == "piston_head" or props.get("extended") == "true":
            continue
        f = props.get("facing")
        alts = [None]
        if bid == "repeater":
            alts += [S("repeater", facing=f, delay=d) for d in range(1, 5) if str(d) != props.get("delay", "1")]
            alts += [S("repeater", facing=opp(f), delay=props.get("delay", "1")), S("redstone_wire")]
        elif bid == "observer":
            alts += [S("observer", facing=x) for x in D6 if x != f]
            alts += [S("repeater", facing=f, delay=1)] if f in H4 else []
        elif bid in ("piston", "sticky_piston"):
            alts += [S("sticky_piston" if bid == "piston" else "piston", facing=f), S(bid, facing=opp(f))]
        elif bid == "slime_block":
            alts += [S("honey_block"), S("stone")]
        elif bid == "honey_block":
            alts += [S("slime_block")]
        elif bid == "white_glazed_terracotta":
            alts += [S("stone")]
        elif bid in ("stone", "smooth_stone", "obsidian"):
            alts += [S("glass"), S("redstone_block")] + ([S("stone")] if bid == "obsidian" else [])
        elif bid == "redstone_wire":
            alts += [S("repeater", facing=x, delay=1) for x in H4]
        elif bid == "redstone_torch":
            alts += [S("redstone_block")]
        else:
            alts = alts
        for a in alts:
            out.append({"pos": list(p), "from": key({"id": bl["id"], "props": props}), "to": a})
    # additions: a stray stone next to a slime/honey block or on the free end of a pushed line
    occupied = set(cells)
    for p, bl in cells.items():
        if bl["id"].endswith(("slime_block", "honey_block")):
            for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                q = (p[0] + d[0], p[1] + d[1], p[2] + d[2])
                if q not in occupied and in_box(spec, q) and not in_clear(spec, q):
                    out.append({"pos": list(q), "from": "air", "to": S("stone")})
                    occupied.add(q)
    return out


def opp(f):
    return {"north": "south", "south": "north", "east": "west", "west": "east", "up": "down", "down": "up"}[f]


def in_box(spec, p):
    lo, hi = spec["box"]["min"], spec["box"]["max"]
    return all(lo[i] <= p[i] <= hi[i] for i in range(3))


def in_clear(spec, p):
    return p in C.expand([{"at": c, "is": "air"} for c in spec.get("keep_clear", [])])


def break_scan(k, name):
    m = load_ref(name)
    rows = []
    for e in natural_edits(m):
        r = graded(k, m["spec"], apply(m["blocks"], [e]), screen=0)
        rows.append({**e, "result": C.brief(r)})
    (WORK / f"breaks_{name}.json").write_text(json.dumps(rows))
    return {"edits": len(rows), "failing": sum(not r["result"]["pass"] for r in rows)}


# ---------------------------------------------------------------- single-edit neighbourhood

def neighbourhood_edits(spec, start, ref_blocks=()):
    pal = palette_for(list(start) + list(ref_blocks))
    cells = cell_map(start)
    lever = tuple(spec["lever"])
    skip = {lever} | {tuple(f[:3]) for f in spec.get("fixed", [])}
    clear = set(C.expand([{"at": c, "is": "air"} for c in spec.get("keep_clear", [])]))
    lo, hi = spec["box"]["min"], spec["box"]["max"]
    out = []
    for x in range(lo[0], hi[0] + 1):
        for y in range(lo[1], hi[1] + 1):
            for z in range(lo[2], hi[2] + 1):
                p = (x, y, z)
                if p in skip or p in clear:
                    continue
                cur = key({"id": cells[p]["id"], "props": cells[p].get("props") or {}}) if p in cells else "air"
                for st in pal:
                    if key(st) != cur:
                        out.append({"pos": list(p), "from": cur, "to": st})
    return out


def neighbourhood(k, spec, start, ref_blocks=(), stop_after=None, log=None):
    """Grades every single edit of `start` inside the box. Returns (n_edits, passing_edits, seconds)."""
    edits = neighbourhood_edits(spec, start, ref_blocks)
    t0, passing = time.monotonic(), []
    for i, e in enumerate(edits):
        r = graded(k, spec, apply(start, [e]))
        if r["pass"]:
            passing.append(e)
            if stop_after and len(passing) >= stop_after:
                break
        if log and i % 500 == 0:
            log(f"{i}/{len(edits)} {len(passing)} passing {time.monotonic() - t0:.0f}s")
    return len(edits), passing, round(time.monotonic() - t0, 1)


# ---------------------------------------------------------------- physics scan

def physics_tag(physics):
    return "_".join(f"{a}{b}" for a, b in sorted(physics.items())) or "vanilla"


def physics_scan(k, physics, extra=None):
    out = {}
    for name in M.MACHINES:
        m = load_ref(name)
        out[name] = C.brief(C.check(k, m["spec"], m["blocks"]))
    for label, (spec, blocks) in (extra or {}).items():
        out[label] = C.brief(C.check(k, spec, blocks))
    (WORK / f"physics_{physics_tag(physics)}.json").write_text(json.dumps(out, indent=1))
    return out


# ---------------------------------------------------------------- tasks

PHYS_TEXT = {
    "push_limit": "a piston can move at most {v} blocks (vanilla: 12)",
    "repeater_unit": "each repeater delay step lasts {v} game ticks (vanilla: 2, so delays 1-4 are 2/4/6/8 ticks)",
    "observer_delay": "an observer fires {v} game ticks after the change it watches (vanilla: 2)",
    "observer_pulse": "an observer's output pulse lasts {v} game ticks (vanilla: 2)",
}


def spec_text(spec):
    s = {**C.DEFAULTS, **spec}
    lines = [f"- Lever at {spec['lever']}; it starts off. The grader settles the build, then flips the lever "
             f"{len(spec['schedule'])} times (idle gaps {spec['schedule']} ticks before each flip).",
             f"- After each flip the build must come to rest within {s['time_cap']} ticks, then stay unchanged for {s['hold']} ticks.",
             f"- Lever off (start and after every even flip): " + "; ".join(req_text(r) for r in spec["states"]["off"]) + ".",
             f"- Lever on (after every odd flip): " + "; ".join(req_text(r) for r in spec["states"]["on"]) + ".",
             f"- The whole build must return to exactly the same resting state every two flips; no item drops; no block may leave the box.",
             f"- At most {spec['block_budget']} blocks (lever included), all inside the box {spec['box']['min']}..{spec['box']['max']}."]
    if spec.get("conserve"):
        lines.append("- Exactly " + ", ".join(f"{v} {k.split(':')[1]}" for k, v in spec["conserve"].items()) + " in the build, at all times.")
    if spec.get("keep_clear"):
        lines.append(f"- These cells must stay empty at every tick: {spec['keep_clear']}.")
    if spec.get("fixed"):
        lines.append(f"- {len(spec['fixed'])} fixed cells must keep their block at every tick: "
                     + ", ".join(f"{f[:3]}" for f in spec["fixed"][:16]) + (" ..." if len(spec["fixed"]) > 16 else "") + ".")
    return "\n".join(lines)


def req_text(r):
    at = r["at"]
    pos = "(" + ", ".join(f"{a[0]}..{a[1]}" if isinstance(a, list) else str(a) for a in at) + ")"
    ids = r["is"] if isinstance(r["is"], list) else [r["is"]]
    return f"{pos} is {' or '.join(i.replace('minecraft:', '') for i in ids)}"


def prompt_for(task, m):
    head = {
        "repair": f"This {m['title']} is broken: it does not do what it should. Repair it.",
        "port": f"This {m['title']} works in vanilla Minecraft Java 26.3, but this server runs with changed physics: "
                + "; ".join(PHYS_TEXT[a].format(v=v) for a, v in task["physics"].items()) + ". Adapt the build so it works here.",
        "hidden_rule": f"This {m['title']} works in vanilla Minecraft Java 26.3, but it fails on this server, which has one changed "
                       "game mechanic that is not disclosed. Work out what is different and adapt the build so it works here.",
    }[task["kind"]]
    return (f"{head}\n\nGoal: {m['goal']}\n\nSpec (checked in the game engine):\n{spec_text(task['spec'])}\n\n"
            "You may change, add or remove any blocks except the lever. Allowed blocks: the benchmark allow-list. "
            "Submit the complete build as a list of blocks.")


def task_spec(m, start, ref, box=None, slack=2):
    spec = copy.deepcopy(m["spec"])
    spec["block_budget"] = max(len(start), len(ref)) + slack
    if box:
        spec["box"] = box
    return spec


def make_task(k, tid, kind, name, start, ref, physics=None, edits=None, difficulty=None, hard_search=False, notes=None,
              box=None, log=None):
    """Verifies (start fails, reference passes) under the kernel's physics and writes tasks/<tid>.json.
    hard_search: brute-force the single-edit neighbourhood of `start`; 'hard' iff no edit passes."""
    m = load_ref(name)
    spec = task_spec(m, start, ref, box)
    rs, rr = C.check(k, spec, start), C.check(k, spec, ref)
    task = {"id": tid, "family": "pistons", "kind": kind, "machine": name, "physics": physics or {},
            "disclose_physics": kind != "hidden_rule", "difficulty": difficulty, "spec": spec,
            "start_build": start, "reference_solution": ref,
            "provenance": {"edits": [edit_str(e) for e in (edits or [])], "notes": notes or ""},
            "verification": {"start": C.brief(rs), "reference": C.brief(rr), "reference_timings": rr["timings"]}}
    ok = (not rs["pass"]) and rr["pass"]
    if ok and hard_search:
        n, passing, secs = neighbourhood(k, spec, start, ref, log=log)
        task["verification"]["single_edit_search"] = {"edits_tried": n, "passing": [edit_str(e) for e in passing[:20]],
                                                      "n_passing": len(passing), "seconds": secs}
        task["difficulty"] = "hard" if not passing else "medium"
    task["prompt"] = prompt_for(task, m)
    task["verified"] = ok
    if ok:
        (TASKS / f"{tid}.json").write_text(json.dumps(task, indent=1))
    return {"id": tid, "ok": ok, "difficulty": task["difficulty"], "start": C.brief(rs)["fail"], "ref": rr["pass"],
            "search": task["verification"].get("single_edit_search", {}).get("n_passing")}


def E(pos, to, frm=None):
    return {"pos": list(pos), "from": frm, "to": to}


def repair(k, tid, name, edits, difficulty="easy", hard_search=False, notes="", log=None):
    m = load_ref(name)
    cells = cell_map(m["blocks"])
    for e in edits:
        if e["from"] is None:
            c = cells.get(tuple(e["pos"]))
            e["from"] = key({"id": c["id"], "props": c.get("props") or {}}) if c else "air"
    start = apply(m["blocks"], edits)
    return make_task(k, tid, "repair", name, start, m["blocks"], edits=edits, difficulty=difficulty,
                     hard_search=hard_search, notes=notes, log=log)


def port(k, tid, name, physics, fix, kind="port", difficulty=None, notes="", start=None, edits=None):
    """Port / hidden_rule task: the vanilla reference is the start build; `fix` is the reference solution.
    The kernel `k` must be running `physics`."""
    m = load_ref(name)
    lo = [min([m["spec"]["box"]["min"][i]] + [bl["pos"][i] for bl in fix]) for i in range(3)]
    hi = [max([m["spec"]["box"]["max"][i]] + [bl["pos"][i] for bl in fix]) for i in range(3)]
    box = {"min": lo, "max": hi}
    start = start or m["blocks"]
    lo = [min([lo[i]] + [bl["pos"][i] for bl in start]) for i in range(3)]
    hi = [max([hi[i]] + [bl["pos"][i] for bl in start]) for i in range(3)]
    box = {"min": lo, "max": hi}
    return make_task(k, tid, kind, name, start, fix, physics=physics, difficulty=difficulty,
                     notes=notes, box=box, edits=edits)


def write_index():
    rows = []
    for f in sorted(TASKS.glob("*.json")):
        t = json.loads(f.read_text())
        rows.append({"id": t["id"], "kind": t["kind"], "difficulty": t["difficulty"], "machine": t["machine"],
                     "physics": t["physics"], "disclose_physics": t["disclose_physics"], "verified": t["verified"],
                     "start_fail": t["verification"]["start"]["fail"],
                     "single_edit_fixes": t["verification"].get("single_edit_search", {}).get("n_passing")})
    (HERE / "index.json").write_text(json.dumps(rows, indent=1))
    return rows
