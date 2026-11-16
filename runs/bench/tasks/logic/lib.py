"""Core of the timing / sequential-logic task family: harness, kernel jobs, traces, spec checks.

A *case* is one build checked against one spec: the harness cells (lever, its support block, the
output cells) plus the agent's build, placed at an x offset so that several cases can share one
kernel job (`run_cases`). Every case gets the same lever schedule. Traces are rebuilt per tick
from the kernel's change log, so the result is identical to running each case alone as long as
the copies cannot reach each other (cases are spaced far apart, and any batch where a case left
its box or spawned an entity is re-run one case at a time).

Time convention: t = 0 is the end of settling. A lever event at t is applied after tick t has run,
and the sample at t is taken after every event at t. An edge (t, v) means the output was v at t
and not v at t - 1.
"""
import os
import shutil
import sys
import tempfile as _tf
import time
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "grader"))

import pdgrader.kernel as K  # noqa: E402
from pdgrader import rules  # noqa: E402
from pdgrader.validate import validate_part  # noqa: E402

SCRATCH = Path("/private/tmp/claude-501/tasks_logic_k")
MIN_FREE_MB = 300
ORIGIN = (0, 100, 0)
SPACING = 40           # x distance between copies in a batched job
SETTLE_MAX, SETTLE_QUIET = 80, 20
MAX_CHANGES = 20000

# ------------------------------------------------------------------ kernel


def wait_for_disk(min_mb=MIN_FREE_MB, tries=10):
    for i in range(tries + 1):
        free = shutil.disk_usage("/private/tmp").free // (1 << 20)
        if free >= min_mb:
            return free
        if i == tries:
            raise SystemExit(f"only {free} MB free in /private/tmp after waiting {tries} min; stopping")
        print(f"[disk] {free} MB free < {min_mb} MB, waiting 60 s ({i + 1}/{tries})", flush=True)
        time.sleep(60)


_KERNEL = {"k": None, "physics": None}


def kernel(physics=None):
    """One kernel at a time, heap 1G, scratch under SCRATCH. Re-boots when the physics changes."""
    key = K.physics_key(physics)
    if _KERNEL["k"] is not None and _KERNEL["physics"] == key:
        return _KERNEL["k"]
    close_kernel()
    wait_for_disk()
    SCRATCH.mkdir(parents=True, exist_ok=True)
    K.tempfile = types.SimpleNamespace(mkdtemp=lambda prefix="", dir=None: _tf.mkdtemp(prefix=prefix, dir=str(SCRATCH)))
    _KERNEL["k"] = K.Kernel(heap="1G", physics=key or None)
    _KERNEL["physics"] = key
    return _KERNEL["k"]


def close_kernel():
    if _KERNEL["k"] is not None:
        _KERNEL["k"].close()
        _KERNEL["k"] = None


def cleanup():
    close_kernel()
    shutil.rmtree(SCRATCH, ignore_errors=True)


# ------------------------------------------------------------------ blocks

def norm_id(bid):
    return bid if ":" in bid else "minecraft:" + bid


def block(pos, bid, **props):
    b = {"pos": list(pos), "id": bid.split(":")[-1]}
    if props:
        b["props"] = {k: str(v).lower() if isinstance(v, bool) else str(v) for k, v in props.items()}
    return b


def state_of(b):
    return rules.state_string(norm_id(b["id"]), {k: str(v) for k, v in (b.get("props") or {}).items()})


def harness_blocks(h):
    """Harness cells as (pos, state, frozen-block-id) triples."""
    out = []
    for name, inp in h["inputs"].items():
        out.append((tuple(inp["support"]), "minecraft:stone", "minecraft:stone"))
        f = inp.get("facing", "west")
        out.append((tuple(inp["lever"]), f"minecraft:lever[face=wall,facing={f},powered=false]", "minecraft:lever"))
    for name, o in h["outputs"].items():
        bid = norm_id(o.get("block", "note_block"))
        out.append((tuple(o["pos"]), bid, bid))
    return out


def output_on(state, kind):
    """Is an output cell 'on'? Works off the serialized block state."""
    if state is None:
        return False
    bid, p = rules.parse_state(state)
    if bid != norm_id(kind):
        return False
    if "powered" in p:
        return p["powered"] == "true"
    if "lit" in p:
        return p["lit"] == "true"
    if "extended" in p:
        return p["extended"] == "true"
    if "power" in p:
        return p["power"] != "0"
    return False


# ------------------------------------------------------------------ static checks

def static_check(task, build):
    """Allow-list, harness cells, bounding box and block budget. Returns a list of failures."""
    errors, cells = validate_part(build, 1, walls=False)
    fails = [{"code": e["code"], "message": e["message"], **({"pos": e["pos"]} if "pos" in e else {})} for e in errors]
    harness = {p for p, _, _ in harness_blocks(task["harness"])}
    lim = task["limits"]
    lo, hi = lim["bbox"]["min"], lim["bbox"]["max"]
    for p in cells:
        if p in harness:
            fails.append({"code": "on_harness_cell", "message": "this cell belongs to the harness (lever, its block, or an output)", "pos": list(p)})
        elif not all(lo[i] <= p[i] <= hi[i] for i in range(3)):
            fails.append({"code": "outside_bbox", "message": f"block outside the allowed box {lo}..{hi}", "pos": list(p)})
    if len(cells) > lim["max_blocks"]:
        fails.append({"code": "over_budget", "message": f"{len(cells)} blocks; the budget is {lim['max_blocks']}"})
    return fails[:30]


# ------------------------------------------------------------------ jobs

def schedule_events(spec):
    """Sorted [(t, lever_name)] from the spec's input schedule."""
    return sorted((int(e["t"]), e["lever"]) for e in spec["inputs"])


def _shift(p, dx):
    return (p[0] + dx, p[1], p[2])


def build_job(task, builds, spec=None):
    """One kernel job for several builds of the same task, copy i shifted by i * SPACING in x."""
    spec = spec or task["spec"]
    lo, hi = task["limits"]["bbox"]["min"], task["limits"]["bbox"]["max"]
    pad = 14
    n = len(builds)
    region = {"min": [lo[0] - pad, lo[1] - 6, lo[2] - pad], "max": [hi[0] + pad + (n - 1) * SPACING, hi[1] + 8, hi[2] + pad]}
    hb = harness_blocks(task["harness"])
    placed, frozen = [], []
    for i, b in enumerate(builds):
        dx = i * SPACING
        for p, st, fid in hb:
            placed.append([*_shift(p, dx), st])
            frozen.append([*_shift(p, dx), fid])
        for blk in b:
            if norm_id(blk["id"]) == "minecraft:air":
                continue
            placed.append([*_shift(blk["pos"], dx), state_of(blk)])
    steps = [{"op": "clear"}, {"op": "place", "blocks": placed},
             {"op": "run", "label": "settle", "max_ticks": SETTLE_MAX, "quiet": SETTLE_QUIET, "max_changes": MAX_CHANGES},
             {"op": "snapshot", "label": "start"}]
    now = 0
    levers = task["harness"]["inputs"]
    for t, name in schedule_events(spec):
        if t > now:
            steps.append({"op": "run", "label": f"run@{now}", "max_ticks": t - now, "min_ticks": t - now, "max_changes": MAX_CHANGES})
            now = t
        for i in range(n):
            steps.append({"op": "lever", "label": f"lever@{t}#{i}", "pos": list(_shift(levers[name]["lever"], i * SPACING))})
    end = int(spec["end"])
    if end > now:
        steps.append({"op": "run", "label": f"run@{now}", "max_ticks": end - now, "min_ticks": end - now, "max_changes": MAX_CHANGES})
    steps.append({"op": "snapshot", "label": "end"})
    return {"origin": list(ORIGIN), "region": region, "n": 1, "door_block": "minecraft:stone",
            "frozen": frozen, "steps": steps}


def _copy_of(x, n):
    i = round(x / SPACING)
    return i if 0 <= i < n else None


def read_job(task, n, res, spec=None):
    """Per-copy traces from a job result: {"settled", "outputs": {name: [initial, [[t, v], ...]]},
    "occupied_outside": [...], "levers_ok"}."""
    spec = spec or task["spec"]
    steps = res["steps"]
    outs = task["harness"]["outputs"]
    lo, hi = task["limits"]["bbox"]["min"], task["limits"]["bbox"]["max"]
    harness = {p for p, _, _ in harness_blocks(task["harness"])}
    per = [{"settled": True, "lever_errors": [], "outside": [], "harness_changed": [], "truncated": False,
            "state": {}, "trace": {k: [] for k in outs}} for _ in range(n)]

    def local(c):
        i = _copy_of(c[1], n)
        if i is None:
            return None, None
        return i, (c[1] - i * SPACING, c[2], c[3])

    def note(i, p, t, new):
        cs = per[i]
        if p not in harness and new != "minecraft:air" and not new.startswith("minecraft:moving_piston") \
                and not all(lo[k] <= p[k] <= hi[k] for k in range(3)):
            if len(cs["outside"]) < 10:
                cs["outside"].append([t, list(p), new])
        cs["state"][p] = new
        for name, o in outs.items():
            if tuple(o["pos"]) == p:
                v = output_on(new, o.get("block", "note_block"))
                tr = cs["trace"][name]
                last = tr[-1][1] if tr else cs["init"][name]
                if v != last:
                    if tr and tr[-1][0] == t:
                        tr.pop()        # changed back within the same sample
                    else:
                        tr.append([t, v])

    settle = next(s for s in steps if s.get("label") == "settle")
    start = next(s for s in steps if s.get("label") == "start")
    for cs in per:
        cs["init"] = {}
    for c in start["cells"]:
        i, p = local([0, *c])
        if i is None:
            continue
        per[i]["state"][p] = c[3]
        if p not in harness and not all(lo[k] <= p[k] <= hi[k] for k in range(3)) and len(per[i]["outside"]) < 10:
            per[i]["outside"].append([0, list(p), c[3]])
    for i in range(n):
        for name, o in outs.items():
            per[i]["init"][name] = output_on(per[i]["state"].get(tuple(o["pos"])), o.get("block", "note_block"))
    if not settle["quiescent"]:
        late = settle["ticks"] - SETTLE_QUIET
        moved = {local(c)[0] for c in settle["changes"] if c[0] > late}
        if len(settle["changes"]) >= MAX_CHANGES or not moved:
            moved = set(range(n))
        for i in moved:
            if i is not None:
                per[i]["settled"] = False
    now = 0
    for s in steps:
        lab = s.get("label", "")
        if lab.startswith("run@"):
            base = int(lab[4:])
            if len(s["changes"]) >= MAX_CHANGES:
                for cs in per:
                    cs["truncated"] = True
            for c in s["changes"]:
                i, p = local(c)
                if i is not None:
                    note(i, p, base + c[0], c[5])
            now = base + s["ticks"]
        elif lab.startswith("lever@"):
            t = int(lab[6:].split("#")[0])
            i = int(lab.split("#")[1])
            if "error" in s:
                per[i]["lever_errors"].append(s["error"])
            for c in s.get("changes", []):
                j, p = local(c)
                if j is not None:
                    note(j, p, t, c[5])
    fv = res.get("frozen_violation")
    if fv:
        i, p = local([0, *fv["pos"]])
        if i is not None:
            per[i]["harness_changed"].append(fv)
    out = []
    for cs in per:
        out.append({"settled": cs["settled"], "lever_errors": cs["lever_errors"][:3], "outside": cs["outside"],
                    "harness_changed": cs["harness_changed"], "truncated": cs["truncated"],
                    "outputs": {k: [cs["init"][k], cs["trace"][k]] for k in outs}})
    return out


# ------------------------------------------------------------------ spec comparison

def compare(spec, outputs):
    """Returns None if the traces meet the spec, else a failure dict."""
    tol = int(spec.get("tol", 0))
    lat = spec.get("latency", [0, 0])
    for name, want in spec["outputs"].items():
        init, edges = outputs[name]
        if bool(init) != bool(want["initial"]):
            return {"code": "wrong_initial", "message": f"output {name} starts {'on' if init else 'off'}, spec says {'on' if want['initial'] else 'off'}",
                    "output": name, "got": edges[:12]}
        exp = want["edges"]
        if len(edges) != len(exp):
            return {"code": "wrong_edge_count", "message": f"output {name} has {len(edges)} edges, spec has {len(exp)}",
                    "output": name, "got": edges[:24], "want": exp[:24]}
        best = None
        for s in range(int(lat[0]), int(lat[1]) + 1):
            bad = next((k for k, (a, e) in enumerate(zip(edges, exp)) if a[1] != e[1] or abs(a[0] - (e[0] + s)) > tol), None)
            if bad is None:
                best = None
                break
            if best is None or bad > best[0]:
                best = (bad, s)
        else:
            k = best[0]
            return {"code": "wrong_timing", "message": f"output {name} edge #{k}: got {'on' if edges[k][1] else 'off'} at t={edges[k][0]}, "
                    f"spec wants {'on' if exp[k][1] else 'off'} at t={exp[k][0]} (tolerance {tol}, latency shift {lat})",
                    "output": name, "edge": k, "got": edges[:24], "want": exp[:24]}
    return None


def verdict(task, static, trace, spec=None):
    spec = spec or task["spec"]
    fails = list(static)
    if trace is not None:
        if not trace["settled"]:
            fails.append({"code": "not_settled", "message": f"still changing {SETTLE_MAX} ticks after placement"})
        if trace["lever_errors"]:
            fails.append({"code": "lever_missing", "message": trace["lever_errors"][0]})
        if trace["harness_changed"]:
            fails.append({"code": "harness_changed", "message": "a harness cell (lever, its block, an output) was moved or replaced", **trace["harness_changed"][0]})
        if trace["outside"]:
            fails.append({"code": "left_bbox", "message": "a block appeared outside the allowed box during the run", "cells": trace["outside"][:5]})
        if trace.get("entity"):
            fails.append({"code": "entity", "message": f"an entity appeared ({trace['entity']['type']})"})
        if trace["truncated"]:
            fails.append({"code": "too_many_changes", "message": "change log overflowed; trace incomplete"})
        if not fails:
            f = compare(spec, trace["outputs"])
            if f:
                fails.append(f)
    return {"pass": not fails, "failures": fails, "outputs": trace["outputs"] if trace else None}


def run_cases(task, builds, physics=None, spec=None, batch=1):
    """Checks many builds against one task spec. Returns a list of verdicts (same order)."""
    spec = spec or task["spec"]
    physics = task.get("physics") if physics is None else physics
    results = [None] * len(builds)
    todo = []
    for i, b in enumerate(builds):
        st = static_check(task, b)
        if st:
            results[i] = verdict(task, st, None, spec)
        else:
            todo.append(i)
    k = kernel(physics)

    def run(idx):
        job = build_job(task, [builds[i] for i in idx], spec)
        res = k.run_job(job)
        traces = read_job(task, len(idx), res, spec)
        return res, traces

    for c in range(0, len(todo), batch):
        idx = todo[c:c + batch]
        res, traces = run(idx)
        dirty = bool(res.get("entity_seen")) or bool(res.get("escaped")) or any(t["outside"] or t["harness_changed"] for t in traces)
        if dirty and len(idx) > 1:
            for i in idx:
                r1, t1 = run([i])
                tr = t1[0]
                if r1.get("entity_seen"):
                    tr["entity"] = r1["entity_seen"]
                if r1.get("escaped"):
                    tr["outside"] = tr["outside"] or [["escaped test region"]]
                results[i] = verdict(task, [], tr, spec)
        else:
            for i, tr in zip(idx, traces):
                if res.get("entity_seen"):
                    tr["entity"] = res["entity_seen"]
                if res.get("escaped"):
                    tr["outside"] = tr["outside"] or [["escaped test region"]]
                results[i] = verdict(task, [], tr, spec)
    return results


def check(task, build, physics=None, spec=None):
    return run_cases(task, [build], physics, spec)[0]
