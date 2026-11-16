"""Generates and verifies the timing / sequential-logic task set.

    python3 make_tasks.py refs            # measure every reference circuit (vanilla) -> refs/
    python3 make_tasks.py repair [names]  # repair tasks (easy / medium / hard)    -> tasks/
    python3 make_tasks.py port            # port + hidden_rule tasks               -> tasks/
    python3 make_tasks.py verify          # re-check every task: start fails, reference passes

One kernel at a time (heap 1G); a kernel is re-booted only when the physics changes.
Sweep results are cached in work/cache.json so an interrupted run resumes cheaply.
"""
import hashlib
import json
import random
import sys
import time
from pathlib import Path

import edits
import lib
import tasklib
from circuits import CIRCUITS

HERE = Path(__file__).resolve().parent
TASKS, REFS, WORK = HERE / "tasks", HERE / "refs", HERE / "work"
CACHE = WORK / "cache.json"

KNOBS = {
    "repeater_unit": "game ticks per repeater delay step (vanilla 2, so delays 1-4 are 2/4/6/8 gt)",
    "observer_delay": "game ticks from a watched change to an observer's output (vanilla 2)",
    "observer_pulse": "game ticks an observer's output pulse lasts (vanilla 2)",
    "push_limit": "most blocks a piston can push (vanilla 12)",
}


def describe(physics):
    return "; ".join(f"{k} = {v} ({KNOBS[k]})" for k, v in sorted(physics.items()))


# ------------------------------------------------------------------ cache

def _load_cache():
    try:
        return json.loads(CACHE.read_text())
    except Exception:
        return {}


_cache = None


def cache():
    global _cache
    if _cache is None:
        _cache = _load_cache()
    return _cache


def save_cache():
    WORK.mkdir(exist_ok=True)
    CACHE.write_text(json.dumps(cache(), separators=(",", ":")))


def key(*parts):
    return hashlib.sha256(json.dumps(parts, sort_keys=True).encode()).hexdigest()[:20]


# ------------------------------------------------------------------ refs

def ref(name):
    return json.loads((REFS / f"{name}.json").read_text())


def make_refs(names):
    REFS.mkdir(exist_ok=True)
    for n in names:
        c = CIRCUITS[n]
        probe = tasklib.skeleton(c, [c["build"]], tasklib.spec_from(c, {"Q": [False, []]}), max_blocks=500)
        probe["limits"]["bbox"] = {"min": [-20, -10, -20], "max": [20, 10, 20]}
        r = lib.check(probe, c["build"], {})
        spec = tasklib.spec_from(c, r["outputs"])
        task = tasklib.skeleton(c, [c["build"]], spec)
        again = lib.check(task, c["build"], {})          # must reproduce exactly inside its own box
        assert again["pass"], (n, again["failures"])
        out = {"name": n, "title": c["title"], "notes": c["notes"], "harness": c["harness"], "build": c["build"],
               "block_count": len(c["build"]), "bbox": tasklib.bbox_of([c["build"]], c["harness"], 0, 0),
               "inputs": spec["inputs"], "end": spec["end"], "trace": spec["outputs"], "physics": {}}
        (REFS / f"{n}.json").write_text(json.dumps(out, indent=1))
        print(f"ref {n}: {len(c['build'])} blocks, Q edges {[e[0] for e in spec['outputs']['Q']['edges']]}", flush=True)


def ref_spec(r):
    return {"inputs": r["inputs"], "end": r["end"], "tol": 0, "latency": [0, 0], "outputs": r["trace"]}


# ------------------------------------------------------------------ sweeps

def sweep(task, build, physics, early_exit=False, chunk=200):
    """Single-edit neighbourhood of `build`. Returns {"neighbours", "checked", "passing": [edits]}."""
    k = key("sweep", task["limits"], task["spec"], task["harness"], physics, sorted(map(json.dumps, build)), early_exit)
    if k in cache():
        return cache()[k]
    nb = edits.neighbourhood(build, task)
    passing, checked = [], 0
    t0 = time.monotonic()
    for c in range(0, len(nb), chunk):
        part = nb[c:c + chunk]
        res = lib.run_cases(task, [edits.apply(build, e) for e in part], physics)
        checked += len(part)
        passing += [e for e, r in zip(part, res) if r["pass"]]
        if early_exit and passing:
            break
    out = {"neighbours": len(nb), "checked": checked, "passing": passing[:20], "n_passing": len(passing),
           "seconds": round(time.monotonic() - t0, 1)}
    cache()[k] = out
    save_cache()
    return out


# ------------------------------------------------------------------ task files

def first_failure(v):
    f = v["failures"][0] if v["failures"] else None
    return None if f is None else {"code": f["code"], "message": f["message"][:300]}


def write_task(t):
    TASKS.mkdir(exist_ok=True)
    (TASKS / f"{t['id']}.json").write_text(json.dumps(t, indent=1))


def brief(kind, r, physics, disclosed):
    head = (f"Circuit: {r['title']}. Input: lever A at {r['harness']['inputs']['A']['lever']} on the stone block "
            f"{r['harness']['inputs']['A']['support']}. Output: note block Q at {r['harness']['outputs']['Q']['pos']}; "
            "Q is on while the note block is powered. The lever, its block and Q belong to the harness: do not "
            "move, replace or build on them. ")
    rules_ = ("Your build is checked by toggling the lever on the spec's schedule and comparing Q's on/off edges, "
              "tick by tick, with the spec. Stay inside the bounding box and the block budget; allowed blocks are "
              "the benchmark allow-list. ")
    if kind == "repair":
        return head + ("This build is broken: Q does not follow the spec. Repair it (vanilla 26.3 physics) so "
                       "that Q matches the spec exactly. ") + rules_
    if disclosed:
        return head + (f"This build meets the spec in vanilla 26.3, but here the physics is changed: {describe(physics)}. "
                       "The spec is fixed in game ticks. Modify the build so that Q matches the spec under the "
                       "changed physics. ") + rules_
    return head + ("This build meets the spec in vanilla 26.3, but this world's physics differs from vanilla in one "
                   "undisclosed respect, and here Q misses the spec. The spec is fixed in game ticks. Modify the "
                   "build so that Q matches the spec in this world. ") + rules_


def assemble(tid, kind, difficulty, r, physics, disclosed, start, reference, task, provenance, hardness, v_start, v_ref):
    return {
        "id": tid, "family": "logic", "kind": kind, "difficulty": difficulty, "circuit": r["name"],
        "title": r["title"], "brief": brief(kind, r, physics, disclosed),
        "physics": physics, "physics_disclosed": disclosed,
        "harness": r["harness"], "limits": task["limits"], "spec": task["spec"],
        "start": {"blocks": start}, "reference": {"blocks": reference},
        "provenance": provenance, "hardness": hardness,
        "verified": {"start": {"pass": v_start["pass"], "first_failure": first_failure(v_start),
                               "Q": v_start["outputs"]["Q"] if v_start["outputs"] else None},
                     "reference": {"pass": v_ref["pass"]}},
    }


# ------------------------------------------------------------------ repair

PREFERRED = {"delay": 3, "mode": 3, "reversed": 2, "turned": 3, "swapped": 2, "missing": 1, "stray": 1}


def make_repair(name, rng, max_sweeps=3, want_medium=True):
    r = ref(name)
    spec = ref_spec(r)
    task = {"harness": r["harness"], "spec": spec, "physics": {},
            "limits": {"bbox": tasklib.bbox_of([r["build"]], r["harness"]), "max_blocks": r["block_count"] + 4}}
    base = r["build"]
    fl = edits.faults(base, task)
    res = lib.run_cases(task, [edits.apply(base, f) for f in fl], {})
    breaking = [f for f, v in zip(fl, res) if not v["pass"]]
    print(f"[{name}] {len(fl)} single faults, {len(breaking)} break the spec", flush=True)
    made = []

    # easy: one fault, weighted toward the interesting kinds
    weights = [PREFERRED.get(f["kind"], 1) for f in breaking]
    f = rng.choices(breaking, weights)[0]
    start = edits.apply(base, f)
    vs = lib.check(task, start, {})
    assert not vs["pass"]
    made.append(assemble(f"logic_repair_{name}_easy", "repair", "easy", r, {}, True, start, base, task,
                         {"faults": [f]}, {"note": "one fault; undoing it restores the spec"}, vs, lib.check(task, base, {})))

    # medium / hard: 2-3 faults at distinct cells
    got_hard = got_med = False
    sweeps = 0
    for attempt in range(40):
        if got_hard and (got_med or not want_medium):
            break
        k = 3 if attempt % 3 else 2
        combo = []
        for f in rng.sample(breaking, len(breaking)):
            if all(f["pos"] != g["pos"] for g in combo):
                combo.append(f)
            if len(combo) == k:
                break
        start = edits.apply_all(base, combo)
        vs = lib.check(task, start, {})
        if vs["pass"]:
            continue
        # cheap test first: does undoing one fault alone already pass?
        undo = [{"pos": f["pos"], "to": list(edits.norm(next((b for b in base if b["pos"] == f["pos"]), None)))} for f in combo]
        und = lib.run_cases(task, [edits.apply(start, u) for u in undo], {})
        one = [u for u, v in zip(undo, und) if v["pass"]]
        if one:
            if not got_med and want_medium:
                got_med = True
                made.append(assemble(f"logic_repair_{name}_medium", "repair", "medium", r, {}, True, start, base, task,
                                     {"faults": combo}, {"note": f"{len(combo)} faults, but one edit restores the spec",
                                                         "example_single_fix": one[0]}, vs, lib.check(task, base, {})))
                print(f"[{name}] medium: {len(combo)} faults, undo-one fixes", flush=True)
            continue
        if got_hard or sweeps >= max_sweeps:
            continue
        sweeps += 1
        sw = sweep(task, start, {}, early_exit=False)
        print(f"[{name}] sweep {sweeps}: {sw['neighbours']} neighbours, {sw['n_passing']} pass, {sw['seconds']}s", flush=True)
        if sw["n_passing"] == 0:
            got_hard = True
            made.append(assemble(f"logic_repair_{name}_hard", "repair", "hard", r, {}, True, start, base, task,
                                 {"faults": combo},
                                 {"note": "no single edit in the neighbourhood restores the spec",
                                  "single_edit_neighbours": sw["neighbours"], "passing": 0}, vs, lib.check(task, base, {})))
        elif not got_med and want_medium:
            got_med = True
            made.append(assemble(f"logic_repair_{name}_medium", "repair", "medium", r, {}, True, start, base, task,
                                 {"faults": combo},
                                 {"note": f"{len(combo)} faults; {sw['n_passing']} single edits restore the spec",
                                  "example_single_fix": sw["passing"][0], "single_edit_neighbours": sw["neighbours"]},
                                 vs, lib.check(task, base, {})))
    for t in made:
        write_task(t)
        print(f"  wrote {t['id']}", flush=True)
    return made


# ------------------------------------------------------------------ port / hidden

def E(pos, bid, **props):
    return {"pos": list(pos), "to": [bid, {k: str(v) for k, v in props.items()}]}


RU1, RU3 = {"repeater_unit": 1}, {"repeater_unit": 3}
OD1, OD3 = {"observer_delay": 1}, {"observer_delay": 3}
OP1 = {"observer_pulse": 1}

# (circuit, physics, disclosed, hand-made fix as edits on the reference build)
PORTS = [
    ("delay12", RU3, True, [E((2, 1, 0), "repeater", facing="west", delay=2)]),
    ("delay16", RU3, True, [E((1, 1, 0), "comparator", facing="west", mode="compare"),
                            E((2, 1, 0), "repeater", facing="west", delay=1),
                            E((6, 1, 0), "comparator", facing="west", mode="compare")]),
    ("delay16", RU1, True, [E((1, 1, 0), "repeater", facing="west", delay=4), E((3, 1, 0), "repeater", facing="west", delay=4)]),
    ("clock20", RU3, True, [E((4, 1, 1), "comparator", facing="north", mode="compare"),
                            E((3, 1, 1), "repeater", facing="south", delay=2)]),
    ("clock20", RU1, True, [E((4, 1, 1), "repeater", facing="north", delay=4)]),
    ("rise_mono", RU1, True, [E((2, 1, 1), "repeater", facing="west", delay=4)]),
    ("extender", RU3, True, [E((2, 1, 2), "repeater", facing="west", delay=2)]),
    ("obs_chain", OD3, True, [E((4, 1, 0), "stone")]),
    ("obs_chain", OD1, True, [E((2, 0, 0), "stone"), E((2, 1, 0), "repeater", facing="west", delay=2)]),
    ("tff", OD3, True, [E((2, 1, 0), "repeater", facing="west", delay=1), E((3, 1, 0), "observer", facing="west")]),
    # hidden rule
    ("delay12", RU1, False, [E((1, 1, 0), "repeater", facing="west", delay=4), E((3, 1, 0), "repeater", facing="west", delay=4)]),
    ("extender", RU1, False, [E((3, 1, 2), "repeater", facing="west", delay=4), E((1, 1, 1), "repeater", facing="north", delay=4)]),
    ("obs_chain", OP1, False, [E((4, 0, 0), "stone"), E((4, 1, 0), "repeater", facing="west", delay=1)]),
    ("tff", OD1, False, [E((3, 1, 0), "observer", facing="west")]),
]


def physics_tag(p):
    return "_".join(f"{k.replace('_', '')}{v}" for k, v in sorted(p.items()))


def make_ports(only_physics=None):
    made = []
    order = sorted(range(len(PORTS)), key=lambda i: json.dumps(PORTS[i][1], sort_keys=True))
    for i in order:
        name, physics, disclosed, fix_edits = PORTS[i]
        if only_physics is not None and physics != only_physics:
            continue
        r = ref(name)
        spec = ref_spec(r)
        fix = edits.apply_all(r["build"], fix_edits)
        task = {"harness": r["harness"], "spec": spec, "physics": physics,
                "limits": {"bbox": tasklib.bbox_of([r["build"], fix], r["harness"]),
                           "max_blocks": max(r["block_count"], len(fix)) + 4}}
        kind = "port" if disclosed else "hidden_rule"
        tid = f"logic_{kind}_{name}_{physics_tag(physics)}"
        vs = lib.check(task, r["build"], physics)
        vf = lib.check(task, fix, physics)
        print(f"[{tid}] start pass={vs['pass']} hand-fix pass={vf['pass']}", flush=True)
        if vs["pass"]:
            print("   vanilla build already meets the spec under this physics; skipped", flush=True)
            continue
        if not vf["pass"]:
            print("   hand fix FAILS:", first_failure(vf), vf["outputs"], flush=True)
            continue
        sw = sweep(task, r["build"], physics, early_exit=False)
        print(f"   sweep: {sw['neighbours']} neighbours, {sw['n_passing']} pass, {sw['seconds']}s", flush=True)
        if sw["n_passing"]:
            diff, hard = "easy", {"note": f"{sw['n_passing']} single edits meet the spec", "example_single_fix": sw["passing"][0],
                                  "single_edit_neighbours": sw["neighbours"]}
        else:
            diff, hard = "hard", {"note": "no single edit in the neighbourhood meets the spec under this physics",
                                  "single_edit_neighbours": sw["neighbours"], "passing": 0,
                                  "reference_fix_edits": len(fix_edits)}
        t = assemble(tid, kind, diff, r, physics, disclosed, r["build"], fix, task,
                     {"reference_fix": fix_edits, "vanilla_reference": True}, hard, vs, vf)
        write_task(t)
        made.append(t)
        print(f"   wrote {tid} ({diff})", flush=True)
    return made


# ------------------------------------------------------------------ verify

def verify():
    """Fresh re-check of every task file: start must fail, reference must pass (under the task physics)."""
    files = sorted(TASKS.glob("*.json"))
    by_phys = {}
    for f in files:
        t = json.loads(f.read_text())
        by_phys.setdefault(json.dumps(t["physics"], sort_keys=True), []).append((f, t))
    bad, rows = 0, []
    for ph, items in sorted(by_phys.items()):
        for f, t in items:
            vs = lib.check(t, t["start"]["blocks"], t["physics"])
            vr = lib.check(t, t["reference"]["blocks"], t["physics"])
            # hard-wire cheat: the reference plus a redstone block beside Q must fail
            q = t["harness"]["outputs"]["Q"]["pos"]
            cells = {tuple(b["pos"]) for b in t["reference"]["blocks"]}
            harn = {p for p, _, _ in lib.harness_blocks(t["harness"])}
            spot = next(p for p in [(q[0] + 1, q[1], q[2]), (q[0], q[1] + 1, q[2]), (q[0], q[1], q[2] + 1), (q[0], q[1], q[2] - 1)]
                        if p not in cells and p not in harn)
            vc = lib.check(t, t["reference"]["blocks"] + [lib.block(spot, "redstone_block")], t["physics"])
            ok = (not vs["pass"]) and vr["pass"] and not vc["pass"]
            bad += not ok
            rows.append((t["id"], t["kind"], t["difficulty"], ok))
            print(f"{'OK ' if ok else 'BAD'} {t['id']:<44} {t['kind']:<12} {t['difficulty']:<7} start={first_failure(vs)['code'] if vs['failures'] else 'PASS'}"
                  f" ref={'pass' if vr['pass'] else first_failure(vr)} cheat={'PASS' if vc['pass'] else first_failure(vc)['code']}", flush=True)
    print(f"{len(rows) - bad}/{len(rows)} tasks verified", flush=True)
    return bad == 0


if __name__ == "__main__":
    cmd = sys.argv[1]
    try:
        if cmd == "refs":
            make_refs(sys.argv[2:] or list(CIRCUITS))
        elif cmd == "repair":
            rng = random.Random(20261116)
            for n in sys.argv[2:] or list(CIRCUITS):
                make_repair(n, random.Random(f"{n}-20261116"))
        elif cmd == "port":
            make_ports()
        elif cmd == "verify":
            sys.exit(0 if verify() else 1)
    finally:
        lib.close_kernel()
