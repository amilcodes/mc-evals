"""Component facts the task brief states, each checked in the lab.

One test per statement in the brief's "Component facts" section that was added after the
second pilot round. If a game update or a kernel change breaks one, the brief is wrong.
"""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pdgrader import rules  # noqa: E402
from pdgrader.kernel import Kernel  # noqa: E402
from pdgrader.session import Session  # noqa: E402

FLOOR = {"face": "floor", "facing": "north"}
CROSS = {"north": "side", "south": "side", "east": "side", "west": "side"}


def B(x, y, z, block, **props):
    return {"pos": [x, y, z], "id": block, **({"props": {k: str(v) for k, v in props.items()}} if props else {})}


def prop(state, key):
    return dict(kv.split("=") for kv in state[:-1].split("[", 1)[1].split(",")).get(key) if "[" in state else None


class FactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k = Kernel()
        cls.s = Session(cls.k, 3, "open", Path(tempfile.mkdtemp()) / "facts.jsonl")

    @classmethod
    def tearDownClass(cls):
        cls.s.close()
        cls.k.close()

    def lab(self, blocks, rest=True):
        r = self.s.call_full("lab_new", {"blocks": blocks})
        self.assertIsNotNone(r["data"], r["text"])
        if rest:
            self.s.call("lab_rest", {})
        return r["data"]["lost"]

    def at(self, x, y, z):
        return self.s.call_full("lab_look", {"cells": [[x, y, z]]})["data"]["blocks"][0][3]

    def flip(self, pos, ticks=6, watch=None):
        """Flip, step, and return [(ticks after the flip, pos, new state)] for the cells watched."""
        t0 = self.s.lab["t"]
        f = self.s.call_full("lab_flip", {"pos": list(pos)})["data"]
        changes = f["changes"] + self.s.call_full("lab_step", {"ticks": ticks})["data"]["changes"]
        return [(c[0] - t0, tuple(c[1:4]), c[5]) for c in changes if watch is None or tuple(c[1:4]) in watch]

    def extends(self, events, pos):
        return [t for t, p, st in events if p == pos and prop(st, "extended") == "true"]

    # ---- what holds dust

    def test_dust_supports(self):
        for block, props in [("glass", {}), ("slime_block", {}), ("redstone_block", {}), ("observer", {"facing": "up"}),
                             ("sticky_piston", {"facing": "north"}), ("piston", {"facing": "up"}), ("sticky_piston", {"facing": "down"})]:
            with self.subTest(block=block, **props):
                self.assertEqual(self.lab([B(9, 5, 9, block, **props), B(9, 6, 9, "redstone_wire")]), [])

    # ---- connections

    def test_dust_feeds_a_comparator_side(self):
        blocks = [B(10, 4, 10, "stone"), B(10, 5, 10, "comparator", facing="north", mode="subtract"), B(10, 5, 9, "redstone_block"),
                  B(11, 4, 10, "stone"), B(11, 5, 10, "redstone_wire"), B(11, 4, 11, "stone"), B(11, 5, 11, "lever", **FLOOR)]
        self.lab(blocks)
        self.assertEqual(prop(self.at(11, 5, 10), "west"), "side")          # the dust points into the comparator's side
        self.assertEqual(prop(self.at(10, 5, 10), "powered"), "true")
        self.flip((11, 5, 11))
        self.assertEqual(prop(self.at(11, 5, 10), "power"), "15")
        self.assertEqual(prop(self.at(10, 5, 10), "powered"), "false")      # 15 from behind minus 15 at the side

    def test_which_blocks_cut_a_dust_step(self):
        keep = {"minecraft:glass", "minecraft:honey_block", "minecraft:observer", "minecraft:piston",
                "minecraft:sticky_piston", "minecraft:redstone_block"}
        skip = {"minecraft:piston_head", "minecraft:redstone_wire", "minecraft:lever", "minecraft:redstone_torch",
                "minecraft:redstone_wall_torch", "minecraft:repeater", "minecraft:comparator"}
        for bid in sorted(set(rules.ALLOWED) - skip):
            props = {"facing": "north"} if "facing" in rules.ALLOWED[bid] else {}
            with self.subTest(block=bid):
                # Lower dust at (5,5,5); dust on top of the stone east of it at (6,6,5); the block under test above the lower dust.
                self.lab([B(5, 4, 5, "stone"), B(5, 5, 5, "redstone_wire"), B(6, 5, 5, "stone"), B(6, 6, 5, "redstone_wire"),
                          B(5, 6, 5, bid, **props)], rest=False)
                self.assertEqual(prop(self.at(5, 5, 5), "east") == "up", bid in keep)

    def test_glass_step_carries_power_up_not_down(self):
        for support, powered in (("glass", "0"), ("stone", "14")):
            with self.subTest(upper_dust_on=support):
                self.lab([B(5, 4, 5, support), B(5, 5, 5, "redstone_wire"), B(6, 3, 5, "stone"), B(6, 4, 5, "redstone_wire"),
                          B(4, 4, 5, "stone"), B(4, 5, 5, "lever", **FLOOR)])
                self.assertEqual(prop(self.at(6, 4, 5), "west"), "up")      # connected in both cases
                self.flip((4, 5, 5), ticks=2)
                self.assertEqual(prop(self.at(5, 5, 5), "power"), "15")
                self.assertEqual(prop(self.at(6, 4, 5), "power"), powered)
        self.lab([B(5, 4, 5, "stone"), B(5, 5, 5, "redstone_wire"), B(6, 5, 5, "glass"), B(6, 6, 5, "redstone_wire"),
                  B(4, 4, 5, "stone"), B(4, 5, 5, "lever", **FLOOR)])
        self.flip((4, 5, 5), ticks=2)
        self.assertEqual(prop(self.at(6, 6, 5), "power"), "14")             # up onto dust on glass works

    def test_a_listed_cross_lasts_only_while_nothing_connects(self):
        base = [B(5, 4, 5, "stone"), B(5, 5, 5, "redstone_wire", **CROSS)]
        self.lab(base, rest=False)
        self.assertEqual(self.at(5, 5, 5), "redstone_wire[east=side,north=side,power=0,south=side,west=side]")
        for name, extra, east in [("beside", [B(6, 4, 5, "stone"), B(6, 5, 5, "redstone_wire")], "side"),
                                  ("one up", [B(6, 5, 5, "stone"), B(6, 6, 5, "redstone_wire")], "up"),
                                  ("one down", [B(6, 3, 5, "stone"), B(6, 4, 5, "redstone_wire")], "side")]:
            with self.subTest(neighbour=name):
                self.lab(base + extra, rest=False)
                self.assertEqual(self.at(5, 5, 5), f"redstone_wire[east={east},north=none,power=0,south=none,west=side]")

    # ---- conduction

    def test_glass_and_observers_do_not_pass_power_on(self):
        for block, props, moves in [("observer", {"facing": "east"}, False), ("observer", {"facing": "up"}, False),
                                    ("glass", {}, False), ("stone", {}, True)]:
            with self.subTest(block=block, **props):
                # Dust runs east-west across the top of the block; a piston on the block's north side.
                self.lab([B(5, 5, 5, block, **props), B(5, 6, 5, "redstone_wire"),
                          B(4, 5, 5, "glass"), B(4, 6, 5, "redstone_wire"), B(6, 5, 5, "glass"), B(6, 6, 5, "redstone_wire"),
                          B(7, 5, 5, "stone"), B(7, 6, 5, "lever", **FLOOR), B(5, 5, 4, "sticky_piston", facing="north"), B(5, 5, 3, "stone")])
                events = self.flip((7, 6, 5))
                self.assertEqual(prop(self.at(5, 6, 5), "power"), "14")
                self.assertEqual(bool(self.extends(events, (5, 5, 4))), moves)

    # ---- quasi-connectivity

    PISTON = [B(5, 5, 5, "sticky_piston", facing="north"), B(5, 5, 4, "stone")]
    # A second piston that moves a stone into (4,5,5), next to the test piston, without powering it.
    NUDGE = [B(1, 4, 5, "stone"), B(1, 5, 5, "lever", **FLOOR), B(2, 5, 5, "sticky_piston", facing="east"), B(3, 5, 5, "stone")]

    def test_quasi_connectivity_waits_for_an_update_except_from_nearby_dust(self):
        cases = {
            "lever on a stone beside the cell above": ([B(6, 6, 5, "stone"), B(6, 7, 5, "lever", **FLOOR)], (6, 7, 5), False),
            "lever on a stone two above": ([B(5, 7, 5, "stone"), B(5, 8, 5, "lever", **FLOOR)], (5, 8, 5), False),
            "dust on glass beside the cell above, aimed into it": (
                [B(6, 5, 5, "glass"), B(6, 6, 5, "redstone_wire"), B(7, 5, 5, "glass"), B(7, 6, 5, "redstone_wire"),
                 B(8, 5, 5, "stone"), B(8, 6, 5, "lever", **FLOOR)], (8, 6, 5), True),
            "dust on glass in the cell above": (
                [B(5, 6, 5, "glass"), B(5, 7, 5, "redstone_wire"), B(5, 6, 6, "glass"), B(5, 7, 6, "redstone_wire"),
                 B(5, 6, 7, "glass"), B(5, 7, 7, "redstone_wire"), B(5, 6, 8, "stone"), B(5, 7, 8, "lever", **FLOOR)], (5, 7, 8), True),
        }
        for name, (extra, lever, at_once) in cases.items():
            with self.subTest(source=name):
                self.lab(self.PISTON + self.NUDGE + extra)
                first = self.extends(self.flip(lever), (5, 5, 5))
                later = self.extends(self.flip((1, 5, 5)), (5, 5, 5))      # now a block next to the piston changes
                self.assertEqual(first, [1] if at_once else [])
                self.assertEqual(later, [] if at_once else [4])               # the stone lands at t=3; the piston starts at t=4

    def test_redstone_block_two_above_switches_a_piston(self):
        self.lab(self.PISTON + [B(5, 7, 5, "redstone_block")])                # placement updates every block
        self.assertEqual(prop(self.at(5, 5, 5), "extended"), "true")

    # ---- repeaters, observers, pushed pistons

    def test_repeater_inputs(self):
        self.lab([B(5, 4, 5, "stone"), B(5, 5, 5, "observer", facing="north"), B(5, 4, 6, "stone"), B(5, 5, 6, "repeater", facing="north"),
                  B(5, 5, 2, "sticky_piston", facing="south"), B(5, 5, 3, "stone"), B(4, 4, 2, "stone"), B(4, 5, 2, "lever", **FLOOR)])
        events = self.flip((4, 5, 2), ticks=10, watch={(5, 5, 5), (5, 5, 6)})
        self.assertEqual([(t, p, prop(st, "powered")) for t, p, st in events],
                         [(3, (5, 5, 5), "true"), (5, (5, 5, 5), "false"), (5, (5, 5, 6), "true"), (7, (5, 5, 6), "false")])
        self.lab([B(5, 4, 5, "stone"), B(5, 5, 5, "stone"), B(5, 6, 5, "lever", **FLOOR), B(5, 4, 6, "stone"), B(5, 5, 6, "repeater", facing="north")])
        self.assertEqual([(t, prop(st, "powered")) for t, _, st in self.flip((5, 6, 5), ticks=4, watch={(5, 5, 6)})], [(2, "true")])

    def test_observer_on_a_piston_fires_once_per_stroke(self):
        self.lab([B(5, 5, 5, "sticky_piston", facing="east"), B(6, 5, 5, "stone"), B(4, 4, 5, "stone"), B(4, 5, 5, "lever", **FLOOR),
                  B(5, 5, 6, "observer", facing="north")])
        for stroke in ("extend", "retract"):
            with self.subTest(stroke=stroke):
                events = self.flip((4, 5, 5), ticks=12, watch={(5, 5, 6)})
                self.assertEqual([(t, prop(st, "powered")) for t, _, st in events], [(3, "true"), (5, "false")])
                self.s.call("lab_rest", {})

    def test_piston_pushed_into_a_powered_position(self):
        self.lab([B(5, 8, 5, "sticky_piston", facing="down"), B(5, 7, 5, "sticky_piston", facing="down"), B(5, 6, 5, "stone"),
                  B(6, 8, 5, "stone"), B(7, 8, 5, "lever", face="wall", facing="east"), B(6, 6, 5, "redstone_block")])
        events = self.flip((7, 8, 5), ticks=10)
        self.assertIn((3, (5, 6, 5), "sticky_piston[extended=false,facing=down]"), events)   # lands at t=3
        self.assertEqual(self.extends(events, (5, 6, 5)), [4])                                       # starts at t+1
        self.assertIn((6, (5, 4, 5), "stone"), events)                                       # finished at t+3


if __name__ == "__main__":
    unittest.main()
