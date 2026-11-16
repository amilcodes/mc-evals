"""Builds the port and hidden_rule tasks: one kernel per physics setting, booted one at a time.

Starts are either the vanilla reference (push-limit and slow-repeater ports, whose fixes are new
designs in machines.PORT_FIXES) or a one-edit variant of the reference that still passes in vanilla
but fails under the changed physics (found by scanning every vanilla-passing natural edit; see
work/variants_*.json). Difficulty is by the size of the reference fix (cells that differ).
"""
import json
import os

import build_tasks as BT
import check as C
import machines as M
from build_tasks import E, S

R = lambda f, d: S("repeater", facing=f, delay=d)  # noqa: E731

PLAN = [
    ({"push_limit": 11}, [("port_row_slide_pl11", "port", "row_slide", None, "split", "12 blocks > 11: split the carrier into slime + honey halves, second piston")]),
    ({"push_limit": 9}, [("hidden_row_slide", "hidden_rule", "row_slide", None, "split", "push_limit 9")]),
    ({"push_limit": 7}, [("port_hatch_pl7", "port", "hatch", None, "split", "8 blocks > 7: honey back row + its own piston on the same obsidian")]),
    ({"push_limit": 5}, [("hidden_hatch", "hidden_rule", "hatch", None, "split", "push_limit 5")]),
    ({"repeater_unit": 1}, [
        ("port_dpe_ru1", "port", "dpe", [E([2, -1, 2], R("south", 2))], "ref", "G column one step slower: fine at 2 ticks/step, out of order at 1"),
        ("port_swapper_ru1", "port", "swapper", [E([0, -2, 1], R("south", 3))], "ref", "bottom piston delay 3: at 1 tick/step it fires into the moving slot"),
        ("port_row_push_ru1", "port", "row_push", [E([0, -1, 2], R("south", 2))], "ref", "back piston too early once repeaters speed up; torch timing is fixed"),
        ("hidden_dpe_ru1", "hidden_rule", "dpe", [E([0, -1, 3], R("south", 1))], "ref", "repeater_unit 1"),
    ]),
    ({"repeater_unit": 3}, [("port_swapper_ru3", "port", "swapper", [E([4, -1, 2], R("south", 1))], "ref", "hold-off chain too short relative to the slower bottom piston")]),
    ({"repeater_unit": 4}, [("port_tpe_ru4", "port", "tpe", None, "fix", "all delays x2: over the 80-tick cap; re-derived schedule")]),
    ({"observer_delay": 1}, [
        ("port_tpe_od1", "port", "tpe", [E([1, -1, -7], R("north", 1))], "ref", "e-pulse chain shortened; with 1-tick observers it fires before P3 has folded"),
        ("hidden_tpe_od1", "hidden_rule", "tpe", [E([2, -1, 2], R("south", 3))], "ref", "observer_delay 1"),
    ]),
]


def diff(a, b):
    ca, cb = BT.cell_map(a), BT.cell_map(b)
    return sum(1 for p in set(ca) | set(cb)
               if (ca.get(p, {}).get("id"), ca.get(p, {}).get("props")) != (cb.get(p, {}).get("id"), cb.get(p, {}).get("props")))


def main():
    out = []
    for phys, items in PLAN:
        st = os.statvfs("/private/tmp")
        if st.f_bavail * st.f_frsize < 300e6:
            raise SystemExit("low disk")
        with C.kernel_for(phys) as k:
            for tid, kind, name, edits, fix, note in items:
                m = BT.load_ref(name)
                if edits:
                    cells = BT.cell_map(m["blocks"])
                    for e in edits:
                        c = cells[tuple(e["pos"])]
                        e["from"] = BT.key({"id": c["id"], "props": c.get("props") or {}})
                start = BT.apply(m["blocks"], edits) if edits else m["blocks"]
                ref = m["blocks"] if fix == "ref" else M.PORT_FIXES[name]()
                n = diff(start, ref)
                diffc = "easy" if n == 1 else "medium" if n <= 4 else "hard"
                r = BT.port(k, tid, name, phys, ref, kind=kind, difficulty=diffc, notes=note + f" (reference fix changes {n} cells)",
                            start=start, edits=edits)
                print(phys, r, flush=True)
                out.append(r)
    return out


if __name__ == "__main__":
    main()
    BT.write_index()
