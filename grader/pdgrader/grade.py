"""Grades one submission against rulebook v0 using the simulation kernel."""
import time

from . import rules
from .validate import validate

_OTHER = {"open": "closed", "closed": "open"}


def _pattern(n, state):
    w, h = rules.dims(n)
    return ("." if state == "open" else "#") * (w * h)


def _rows(n, door):
    """Doorway string as rows, top row first, e.g. '##/..' for a 2x2 with the top row closed."""
    w, h = rules.dims(n)
    return "/".join(door[y * w:(y + 1) * w] for y in reversed(range(h)))


def _timeline(n, doors, limit=24):
    out, last = [], None
    for t, d in enumerate(doors):
        if d != last:
            out.append([t, _rows(n, d)])
            last = d
    return out[:limit]


def _fail(code, message, **detail):
    return {"code": code, "message": message, **detail}


def build_job(n, blocks, lever, mode, time_cap, origin=None, legacy_placement=False):
    lo, hi = rules.region(n)
    shell = rules.shell(n)
    lo_z, hi_z = lo[2], hi[2]
    hallway = [(x, y, z) for z in range(lo_z, hi_z + 1) if z != 0 for (x, y, _) in rules.doorway(n)]
    placed = [[*c, rules.WALL_BLOCK] for c in shell]
    placed += [[*pos, rules.state_string(bid, props)] for pos, (bid, props) in sorted(blocks.items())]
    steps = [
        {"op": "clear"},
        {"op": "place", "blocks": placed, "observers_fire_on_place": bool(legacy_placement)},
        {"op": "run", "label": "settle", "max_ticks": rules.SETTLE_CAP + rules.QUIET, "quiet": rules.QUIET},
        {"op": "snapshot", "label": "rest.start"},
    ]
    k = 0
    for c in range(rules.CYCLES[mode]):
        for h in (0, 1):
            tag = f"{c}.{h}"
            delay = rules.FINAL_DELAYS[k % len(rules.FINAL_DELAYS)] if mode == "final" else 0
            k += 1
            if delay:
                steps.append({"op": "run", "label": f"idle.{tag}", "max_ticks": delay, "min_ticks": delay})
            steps.append({"op": "lever", "label": f"lever.{tag}", "pos": list(lever)})
            steps.append({"op": "run", "label": f"move.{tag}", "max_ticks": time_cap + rules.QUIET, "quiet": rules.QUIET})
            steps.append({"op": "run", "label": f"hold.{tag}", "max_ticks": rules.HOLD, "min_ticks": rules.HOLD})
            steps.append({"op": "snapshot", "label": f"rest.{tag}"})
    return {
        "origin": list(origin or rules.ORIGIN),
        "region": {"min": list(lo), "max": list(hi)},
        "n": rules.dims(n)[0],
        "w": rules.dims(n)[0],
        "h": rules.dims(n)[1],
        "door_block": rules.DOOR_BLOCK,
        "ignore": [list(lever)],
        "frozen": [[*c, rules.WALL_BLOCK] for c in shell] + [[*c, "minecraft:air"] for c in hallway],
        "steps": steps,
    }


def _ring_violations(n, cells):
    """Open-state visibility check: every cell beside an empty doorway cell must be a plain block."""
    bad = []
    for d in rules.doorway(n):
        if d in cells:
            continue
        for nb in ((d[0] - 1, d[1], 0), (d[0] + 1, d[1], 0), (d[0], d[1] - 1, 0), (d[0], d[1] + 1, 0)):
            if rules.in_doorway(n, nb):
                continue
            found = cells.get(nb, "minecraft:air")
            if rules.parse_state(found)[0] not in rules.PLAIN and [list(nb), found] not in bad:
                bad.append([list(nb), found])
    return bad


def grade(kernel, sub, n, track="open", mode="dev", time_cap=None, reference=None, origin=None, legacy_placement=False):
    """Returns a result dict. `valid` is the verdict; `failures` lists every rule that was broken."""
    time_cap = rules.TIME_CAP if time_cap is None else time_cap
    result = {
        "valid": False, "n": n, "track": track, "mode": mode, "game_version": rules.GAME_VERSION,
        "stage": "validation", "failures": [], "warnings": [],
        "volume": None, "dims": None, "block_count": None, "timings": [],
        # Diagnostic only, never the score: how far the mechanism got. Flips completed, plus
        # the share of doorway cells that reached the target on the flip that failed.
        "flips_passed": 0, "flips_total": 2 * rules.CYCLES.get(mode, 0), "partial": 0.0,
    }
    if track not in rules.TRACKS:
        result["failures"].append(_fail("bad_track", f"track must be one of {rules.TRACKS}"))
        return result
    errors, blocks = validate(sub, n)
    if errors:
        result["failures"] = errors
        return result
    lever = next(p for p, (bid, _) in blocks.items() if bid == "minecraft:lever")
    initial = sub["initial_state"]

    t0 = time.monotonic()
    res = kernel.run_job(build_job(n, blocks, lever, mode, time_cap, origin, legacy_placement))
    result["sim_seconds"] = round(time.monotonic() - t0, 3)
    steps = {s["label"]: s for s in res["steps"] if "label" in s}
    fails = result["failures"]

    # ---- settle
    result["stage"] = "settle"
    settle = steps["settle"]
    rest = {tuple(c[:3]): c[3] for c in steps["rest.start"]["cells"]}
    lost = [list(p) for p, (bid, _) in sorted(blocks.items()) if rules.parse_state(rest.get(p, "minecraft:air"))[0] != bid]
    if lost:
        result["warnings"].append({
            "code": "changed_on_placement",
            "message": "these submitted blocks were gone or replaced once the build settled (unsupported, or moved by a piston)",
            "positions": lost[:20],
        })
    if not settle["quiescent"]:
        fails.append(_fail("not_settled", f"the build was still changing {rules.SETTLE_CAP} ticks after placement",
                           changes=settle["changes"][:40]))
    elif settle["door"][-1] != _pattern(n, initial):
        fails.append(_fail("wrong_initial_state", f"initial_state is {initial} but after settling the doorway is {_rows(n, settle['door'][-1])}",
                           doorway=_rows(n, settle["door"][-1]), changes=settle["changes"][:40]))

    # ---- cycles
    near = 0.0
    if not fails:
        result["stage"] = "cycles"
        state = initial
        for c in range(rules.CYCLES[mode]):
            for h in (0, 1):
                tag, target = f"{c}.{h}", _OTHER[state]
                where = {"cycle": c + 1, "to": target}
                idle = steps.get(f"idle.{tag}")
                if idle and idle["changes_total"]:
                    fails.append(_fail("not_at_rest", "the build changed while idle between flips", **where))
                    break
                if "error" in steps[f"lever.{tag}"]:
                    fails.append(_fail("lever_missing", steps[f"lever.{tag}"]["error"], **where))
                    break
                move, hold = steps[f"move.{tag}"], steps[f"hold.{tag}"]
                doors, want = move["door"], _pattern(n, target)
                reach = next((t for t in range(len(doors)) if all(d == want for d in doors[t:])), None)
                detail = {**where, "doorway_at_end": _rows(n, doors[-1]), "timeline": _timeline(n, doors),
                          "changes": move["changes"][:40], "changes_total": move["changes_total"]}
                if reach is None:
                    near = sum(a == b for a, b in zip(doors[-1], want)) / len(want)
                    # A door that never moves has every cell "wrong"; one cell right is real progress.
                    detail["cells_reached"] = round(near * len(want))
                    verb = "open" if target == "open" else "close"
                    fails.append(_fail(f"did_not_{verb}", f"cycle {c + 1}: the door did not {verb} within {time_cap} ticks "
                                       f"(doorway at end: {_rows(n, doors[-1])}; # door block, . air, m moving, ? other)", **detail))
                    break
                if not move["quiescent"] or move["last_change_tick"] > time_cap:
                    fails.append(_fail("too_slow", f"cycle {c + 1}: the doorway was {target} at tick {reach} but the build was "
                                       f"still changing after the {time_cap}-tick cap", reach_tick=reach, **detail))
                    break
                if hold["changes_total"] or any(d != want for d in hold["door"]):
                    fails.append(_fail("did_not_hold", f"cycle {c + 1}: the door reached {target} but changed again within {rules.HOLD} ticks",
                                       **where, timeline=_timeline(n, hold["door"]), changes=hold["changes"][:40]))
                    break
                result["timings"].append({**where, "reach_tick": reach, "reset_tick": move["last_change_tick"]})
                result["flips_passed"] += 1
                state = target
            else:
                continue
            break

    result["partial"] = round((result["flips_passed"] + near) / result["flips_total"], 4) if result["flips_total"] else 0.0

    # ---- whole-run rules
    if res["entity_seen"]:
        e = res["entity_seen"]
        fails.append(_fail("entity", f"an entity ({e['type']}) appeared at tick {e['job_tick']}; item drops and falling blocks count", **e))
    if res["frozen_violation"]:
        v = res["frozen_violation"]
        what = "hallway_blocked" if rules.in_hallway(n, v["pos"]) else "wall_changed"
        msg = "a block entered the hallway" if what == "hallway_blocked" else "a hallway wall block was moved or replaced"
        fails.append(_fail(what, f"{msg} at {v['pos']} (found {v['found']}) at tick {v['job_tick']}", **v))
    if res["escaped"]:
        fails.append(_fail("left_test_volume", "a block left the 48 x 48 x 48 test volume"))

    # ---- seamless track
    if track == "seamless" and not fails:
        for label, s in steps.items():
            if not label.startswith("rest."):
                continue
            bad = _ring_violations(n, {tuple(c[:3]): c[3] for c in s["cells"]})
            if bad:
                result["stage"] = "seamless"
                fails.append(_fail("not_seamless", "with the door open, these cells beside the doorway are visible from the hallway "
                                   "and are not plain blocks", cells=bad[:20]))
                break

    # ---- size
    if res["swept"]:
        lo = [min(res["swept"]["min"][i], 0) for i in range(3)]
        w, h = rules.dims(n)
        hi = [max(res["swept"]["max"][0], w - 1), max(res["swept"]["max"][1], h - 1), max(res["swept"]["max"][2], 0)]
        result["bbox"] = {"min": lo, "max": hi}
        result["dims"] = [hi[i] - lo[i] + 1 for i in range(3)]
        result["volume"] = result["dims"][0] * result["dims"][1] * result["dims"][2]
    shell = set(rules.shell(n))
    result["block_count"] = sum(1 for p in rest if p not in shell and p != lever)

    if not fails:
        result["stage"] = "complete"
        result["valid"] = True
        opens = [t["reach_tick"] for t in result["timings"] if t["to"] == "open"]
        closes = [t["reach_tick"] for t in result["timings"] if t["to"] == "closed"]
        result["open_ticks"], result["close_ticks"] = max(opens), max(closes)
        result["reset_ticks"] = max(t["reset_tick"] for t in result["timings"])
        if reference:
            result["reference_volume"] = reference
            result["score"] = round(reference / result["volume"], 4)
    else:
        result["score"] = 0.0 if reference else None
    return result


# Offsets from the pinned position used for the robustness tag: odd and even shifts on each
# axis, and shifts that move the doorway across chunk and chunk-section borders.
TRANSLATIONS = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (7, 3, 5), (16, 0, 16), (-9, -4, 23), (37, 12, -41), (-64, 8, 100)]
_TURN = {"east": "west", "west": "east", "north": "south", "south": "north"}


def rotated_180(sub, n):
    """The same build turned half a turn about the vertical axis through the doorway's centre.

    The hallway still runs along z, so the task is unchanged, but every block sits at a
    different position and faces the opposite way. Returns None if a block would leave the
    test volume.
    """
    out = []
    for b in sub["blocks"]:
        x, y, z = b["pos"]
        pos = [rules.dims(n)[0] - 1 - x, y, -z]
        if not rules.in_region(n, pos):
            return None
        props = dict(b.get("props") or {})
        if "facing" in props:
            props["facing"] = _TURN.get(str(props["facing"]), props["facing"])
        if any(k in props for k in _TURN):
            props = {**{k: v for k, v in props.items() if k not in _TURN}, **{_TURN[k]: v for k, v in props.items() if k in _TURN}}
        out.append({"pos": pos, "id": b["id"], **({"props": props} if props else {})})
    return {"initial_state": sub["initial_state"], "blocks": out}


def translation_pass_rate(kernel, sub, n, track="open", mode="dev", legacy_placement=False):
    """Robustness tag: how many shifted and turned placements of the same submission stay valid.

    Eight shifted positions, then the build turned 180 degrees at the pinned position and at
    two shifted ones. It does not change the verdict. Quarter turns are not covered.
    """
    cases = [("shift", d, sub) for d in TRANSLATIONS]
    turned = rotated_180(sub, n)
    if turned:
        cases += [("turned", d, turned) for d in [(0, 0, 0)] + TRANSLATIONS[3:5]]
    failed = []
    for kind, d, design in cases:
        origin = tuple(rules.ORIGIN[i] + d[i] for i in range(3))
        if not grade(kernel, design, n, track, mode, origin=origin, legacy_placement=legacy_placement)["valid"]:
            failed.append([kind, list(d)])
    return {"passed": len(cases) - len(failed), "of": len(cases), "failed": failed, "failed_offsets": [f[1] for f in failed]}
