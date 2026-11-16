"""Checker self-test: known hacks and broken builds must fail, references must pass (vanilla kernel).

    python3 selftest.py            # boots its own vanilla kernel
or, from a lab with a live kernel k:  import selftest; selftest.run(k)
"""
import json
import sys
from pathlib import Path

import check as C
import machines as M
from build_tasks import S, apply, cell_map

HERE = Path(__file__).resolve().parent


def hacks():
    """(name, machine, build, expected failure code)."""
    out = []
    dpe = M.dpe()
    lever = [bl for bl in dpe["blocks"] if bl["id"].endswith("lever")]
    floor = [M.b(-1, -2, 4, "stone")]
    # 1. A build that is always "extended": payload parked at the target, never moves.
    out.append(("static_extended", "dpe", lever + floor + [M.b(4, 0, 0, "lime_concrete")], "wrong_start"))
    # 2. Extends but never retracts: both pistons non-sticky. The 'on' state is reached; 'off' never again.
    nr = apply(dpe["blocks"], [{"pos": [0, 0, 0], "to": S("piston", facing="east")}, {"pos": [1, 0, 0], "to": S("piston", facing="east")}])
    out.append(("never_retracts", "dpe", nr, "wrong_state"))
    # 3. Bring a second payload up from below the target instead of extending: blocked by keep_clear + conserve.
    below = lever + floor + [M.b(2, 0, 0, "lime_concrete"), M.b(4, -1, 0, "lime_concrete"), M.b(4, -2, 0, "sticky_piston", facing="up"),
                             M.b(-1, -1, 3, "redstone_wire")]
    out.append(("from_below", "dpe", below, "conserve"))
    # 4. Works for the first cycle only (non-sticky bottom piston): blue is left in the slot's track.
    sw = M.swapper()
    out.append(("one_shot", "swapper", apply(sw["blocks"], [{"pos": [0, -2, 0], "to": S("piston", facing="up")}]), "not_periodic"))
    # 5. Extra parts outside the allowed box.
    h = M.hatch()
    out.append(("outside_box", "hatch", h["blocks"] + [M.b(3, -3, 0, "stone"), M.b(4, -3, 0, "stone")], "outside_box"))
    # 6. Over budget: the reference plus a pile of stone.
    rs = M.row_slide()
    pile = rs["blocks"] + [M.b(x, -2, z, "stone") for x in range(0, 6) for z in (-3, 3)]
    out.append(("over_budget", "row_slide", pile, "over_budget"))
    # 7. Torch support replaced by glass (non-conducting): the hatch never opens.
    nodrop = apply(h["blocks"], [{"pos": [1, -5, 0], "to": S("glass")}])
    out.append(("broken_support", "hatch", nodrop, None))
    return out


def run(k):
    rows = []
    for name, f in M.MACHINES.items():
        m = f()
        r = C.check(k, m["spec"], m["blocks"])
        rows.append({"case": f"reference:{name}", "pass": r["pass"], "expected": "pass", "ok": r["pass"]})
    for name, mach, build, want in hacks():
        m = M.MACHINES[mach]()
        r = C.check(k, m["spec"], build)
        codes = [f["code"] for f in r["failures"]]
        ok = (not r["pass"]) and (want is None or want in codes)
        rows.append({"case": name, "pass": r["pass"], "expected": want or "fail", "codes": codes, "ok": ok})
    (HERE / "selftest_result.json").write_text(json.dumps(rows, indent=1))
    return rows


if __name__ == "__main__":
    with C.kernel_for() as k:
        rows = run(k)
    for r in rows:
        print(r)
    sys.exit(0 if all(r["ok"] for r in rows) else 1)
