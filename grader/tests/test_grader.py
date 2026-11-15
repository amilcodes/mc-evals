"""End-to-end tests for the grader. Run: python3 -m unittest discover -s tests -v (from grader/)."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "fixtures"))

from make_fixtures import FIXTURES  # noqa: E402
from pdgrader.grade import grade, translation_pass_rate  # noqa: E402
from pdgrader.kernel import Kernel  # noqa: E402


class GraderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k = Kernel()

    @classmethod
    def tearDownClass(cls):
        cls.k.close()

    def g(self, name, n=1, **kw):
        return grade(self.k, copy.deepcopy(FIXTURES[name]), n, **kw)

    def codes(self, r):
        return [f["code"] for f in r["failures"]]

    # ---- known-good
    def test_1x1_open(self):
        r = self.g("good_1x1_open")
        self.assertTrue(r["valid"], r["failures"])
        self.assertEqual((r["volume"], r["dims"], r["block_count"]), (8, [4, 2, 1], 3))
        self.assertEqual((r["close_ticks"], r["open_ticks"], r["reset_ticks"]), (3, 1, 3))

    def test_1x1_seamless(self):
        r = self.g("good_1x1_seamless", track="seamless")
        self.assertTrue(r["valid"], r["failures"])
        self.assertEqual((r["volume"], r["dims"]), (15, [5, 3, 1]))

    def test_2x2_seamless(self):
        r = self.g("good_2x2", n=2, track="seamless")
        self.assertTrue(r["valid"], r["failures"])
        self.assertEqual((r["volume"], r["dims"], r["block_count"]), (110, [11, 5, 2], 41))
        self.assertEqual(r["warnings"], [])

    def test_rectangular_doors(self):
        # A size is an int (square) or [w, h]: w along x, h along y.
        r = self.g("good_2x1", n=(2, 1), track="seamless", mode="final")
        self.assertTrue(r["valid"], r["failures"])
        self.assertEqual((r["volume"], r["dims"]), (24, [4, 6, 1]))
        r = self.g("good_1x2", n=[1, 2], track="seamless", mode="final")
        self.assertTrue(r["valid"], r["failures"])
        self.assertEqual((r["volume"], r["dims"]), (28, [7, 4, 1]))
        # Width and height are not interchangeable: the 2x1 door's blocks sit in a 1x2 doorway.
        self.assertEqual(self.codes(self.g("good_2x1", n=(1, 2))), ["doorway_block"])
        self.assertEqual(self.codes(self.g("good_2x1", n=(8, 1))), ["bad_size"])
        t = translation_pass_rate(self.k, FIXTURES["good_2x1"], (2, 1), track="seamless")
        self.assertEqual((t["passed"], t["of"]), (11, 11))

    def test_final_mode(self):
        r = self.g("good_2x2", n=2, track="seamless", mode="final")
        self.assertTrue(r["valid"], r["failures"])
        self.assertEqual(len(r["timings"]), 16)
        self.assertEqual(r["volume"], 110)

    def test_score(self):
        self.assertEqual(self.g("good_2x2", n=2, reference=55)["score"], 0.5)
        self.assertEqual(self.g("bad_nonsticky", reference=55)["score"], 0.0)

    def test_repeatable(self):
        a = self.g("good_2x2", n=2)
        self.g("bad_clock")           # a messy job in between must not leak into the next one
        self.g("bad_item_drop")
        b = self.g("good_2x2", n=2)
        for r in (a, b):
            r.pop("sim_seconds")
        self.assertEqual(a, b)

    def test_translations(self):
        t = translation_pass_rate(self.k, FIXTURES["good_2x2"], 2, track="seamless")
        self.assertEqual((t["passed"], t["of"]), (11, 11))

    # ---- rejected before simulation
    def test_static_rejections(self):
        expect = {
            "bad_command_block": "block_not_allowed", "bad_moving_piston": "block_not_allowed",
            "bad_two_levers": "lever_count", "bad_hallway_block": "in_hallway", "bad_wall_cell": "in_shell",
            "bad_headless_piston": "piston_head_mismatch", "bad_property": "bad_property_value",
            "bad_declared_closed": "doorway_block",
        }
        for name, code in expect.items():
            r = self.g(name)
            self.assertFalse(r["valid"], name)
            self.assertEqual(r["stage"], "validation", name)
            self.assertIn(code, self.codes(r), name)

    def test_wrong_size_and_format(self):
        self.assertEqual(self.codes(grade(self.k, {"blocks": "x"}, 1)), ["bad_format"])
        self.assertEqual(self.codes(grade(self.k, FIXTURES["good_1x1_open"], 9)), ["bad_size"])
        # A 1x1 door graded as a 2x2 fills one of the four doorway cells.
        r = self.g("good_1x1_open", n=2)
        self.assertEqual(self.codes(r), ["did_not_close"])
        self.assertEqual(r["failures"][0]["doorway_at_end"], "../#.")

    # ---- fail in simulation
    def test_starts_powered(self):
        r = self.g("bad_starts_powered")
        self.assertEqual((r["stage"], self.codes(r)), ("settle", ["wrong_initial_state"]))

    def test_clock_never_settles(self):
        r = self.g("bad_clock")
        self.assertEqual((r["stage"], self.codes(r)), ("settle", ["not_settled"]))

    def test_reference_table_matches_the_grader(self):
        from pdgrader import references
        for (n, track), ref in references.REFERENCES.items():
            if ref["verified"]:
                r = grade(self.k, json.loads((references.DESIGNS / ref["file"]).read_text()), n, track)
                self.assertEqual((r["valid"], r["volume"]), (True, ref["volume"]), (n, track, r["failures"]))
        for (n, track), (name, volume) in references.STARTING.items():
            r = grade(self.k, json.loads((references.DESIGNS / name).read_text()), n, track)
            self.assertEqual((r["valid"], r["volume"]), (True, volume), (n, track, r["failures"]))

    def test_observers_do_not_fire_on_placement(self):
        self.assertTrue(self.g("good_idle_observers")["valid"])
        # the 0.2 placement rule, kept for scoring older run logs, starts the pair as a clock
        r = self.g("good_idle_observers", legacy_placement=True)
        self.assertEqual(self.codes(r), ["not_settled"])

    def test_nonsticky_closes_but_cannot_open(self):
        r = self.g("bad_nonsticky")
        self.assertEqual(self.codes(r), ["did_not_open"])
        self.assertEqual(r["failures"][0]["cycle"], 1)
        self.assertEqual(len(r["timings"]), 1)  # the close half of cycle 1 succeeded

    def test_partial_progress(self):
        r = self.g("good_2x2", n=2)
        self.assertEqual((r["flips_passed"], r["flips_total"], r["partial"]), (6, 6, 1.0))
        r = self.g("bad_nonsticky")  # closes once, then cannot reopen its single cell
        self.assertEqual((r["flips_passed"], r["partial"]), (1, round(1 / 6, 4)))
        r = self.g("good_1x1_open", n=2)  # fills one of four cells on the first flip
        self.assertEqual(self.codes(r), ["did_not_close"])
        self.assertEqual((r["flips_passed"], r["failures"][0]["cells_reached"], r["partial"]), (0, 1, round(0.25 / 6, 4)))
        self.assertEqual(self.g("bad_two_levers")["partial"], 0.0)

    def test_item_drop_is_an_entity(self):
        r = self.g("bad_item_drop")
        self.assertIn("entity", self.codes(r))
        self.assertEqual(r["failures"][-1]["type"], "minecraft:item")

    def test_pushing_a_wall_block(self):
        self.assertIn("wall_changed", self.codes(self.g("bad_pushes_wall")))

    def test_time_cap(self):
        r = self.g("good_1x1_open", time_cap=2)  # closing takes 3 ticks
        self.assertEqual(self.codes(r), ["too_slow"])
        self.assertTrue(self.g("good_1x1_open", time_cap=3)["valid"])

    def test_not_seamless(self):
        r = self.g("good_1x1_open", track="seamless")
        self.assertEqual((r["stage"], self.codes(r)), ("seamless", ["not_seamless"]))
        self.assertEqual(sorted(c[0] for c in r["failures"][0]["cells"]), [[0, -1, 0], [0, 1, 0], [1, 0, 0]])


if __name__ == "__main__":
    unittest.main()
