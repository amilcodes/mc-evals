"""Tests for the lab: every behaviour the task brief states about it."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "fixtures"))

from make_fixtures import FIXTURES  # noqa: E402
from pdgrader import kit, rules, server  # noqa: E402
from pdgrader.kernel import Kernel  # noqa: E402
from pdgrader.session import Session  # noqa: E402
from pdgrader.validate import validate  # noqa: E402

REF_3X3 = json.loads((ROOT / "reference_designs" / "ref_3x3_seamless_192.json").read_text())
LEVER = {"face": "floor", "facing": "north"}
# A lever on a stone beside a sticky piston that pushes one stone east. Far from the doorway.
PISTON = [
    {"pos": [5, 7, 0], "id": "stone"},
    {"pos": [5, 8, 0], "id": "lever", "props": LEVER},
    {"pos": [6, 7, 0], "id": "sticky_piston", "props": {"facing": "east"}},
    {"pos": [7, 7, 0], "id": "stone"},
]
OUT, IN = "sticky_piston[extended=true,facing=east]", "sticky_piston[extended=false,facing=east]"


def short(c):
    return [c[0], c[1], c[2], c[3], c[4].replace("minecraft:", ""), c[5].replace("minecraft:", "")]


class LabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k = Kernel()
        cls.tmp = Path(tempfile.mkdtemp())
        cls.s = Session(cls.k, 3, "seamless", cls.tmp / "lab.jsonl")

    @classmethod
    def tearDownClass(cls):
        cls.s.close()
        cls.k.close()

    def do(self, tool, **args):
        r = self.s.call_full("lab_" + tool, args)
        self.assertIsNotNone(r["data"], r["text"])
        return r["data"]

    def refused(self, tool, **args):
        r = self.s.call_full("lab_" + tool, args)
        self.assertIsNone(r["data"], r["text"])
        return r["text"]

    # ---- timing and the clock

    def test_piston_timing_matches_the_brief(self):
        self.assertEqual(self.do("new", blocks=PISTON)["t"], 0)
        flip = self.do("flip", pos=[5, 8, 0])
        self.assertEqual((flip["t"], flip["powered"], flip["changes"]), (0, True, []))   # no tick passed, lever line left out
        step = self.do("step", ticks=3)
        self.assertEqual(step["t"], 3)
        by_tick = {t: [c for c in step["changes"] if c[0] == t] for t in (1, 2, 3)}
        self.assertIn([1, 6, 7, 0, IN, OUT], by_tick[1])                  # starts moving at t+1
        self.assertEqual(by_tick[2], [])
        self.assertIn([3, 8, 7, 0, "moving_piston[facing=east,type=normal]", "stone"], by_tick[3])   # finished at t+3
        look = self.do("look", cells=[[8, 7, 0], [9, 7, 0]])
        self.assertEqual(look["blocks"], [[8, 7, 0, "stone"], [9, 7, 0, "air"]])

    def test_step_sizes_add_up(self):
        def run(sizes):
            self.do("new", blocks=PISTON)
            self.do("flip", pos=[5, 8, 0])
            changes = [c for n in sizes for c in self.do("step", ticks=n)["changes"]]
            self.do("flip", pos=[5, 8, 0])
            changes += [c for n in sizes for c in self.do("step", ticks=n)["changes"]]
            return changes, self.do("look")["blocks"], self.s.lab["t"]
        whole = run([8])
        self.assertEqual(run([5, 3]), whole)
        self.assertEqual(run([1] * 8), whole)
        self.assertEqual(whole[2], 16)

    def test_nothing_happens_between_calls_or_during_look_and_view(self):
        self.do("new", blocks=PISTON)
        self.do("flip", pos=[5, 8, 0])
        self.do("step", ticks=1)                                  # the piston is now mid-stroke
        mid = self.do("look")["blocks"]
        for _ in range(3):
            self.assertEqual(self.do("look")["blocks"], mid)
            self.assertIn("Lab at t=1.", self.s.call("lab_view", {}))
        self.assertEqual(self.s.lab["t"], 1)
        self.assertEqual([c[0] for c in self.do("step", ticks=2)["changes"]], [3, 3])   # it still finishes at t=3

    def test_rest_stops_twenty_ticks_after_the_last_change(self):
        self.do("new", blocks=PISTON)
        idle = self.do("rest")
        self.assertEqual((idle["at_rest"], idle["t"], idle["last_change"], idle["changes"]), (True, rules.QUIET, None, []))
        self.do("flip", pos=[5, 8, 0])
        r = self.s.call_full("lab_rest", {})
        self.assertEqual((r["data"]["at_rest"], r["data"]["last_change"], r["data"]["t"]), (True, 23, 43))   # 20 + 3, then 20 quiet ticks
        self.assertIn("lab t=20 -> t=43: at rest; last block change at t=23", r["text"])

    def test_rest_reports_a_clock_as_still_changing(self):
        self.do("new", blocks=FIXTURES["bad_clock"])
        r = self.s.call_full("lab_rest", {"max_ticks": 60})
        self.assertEqual((r["data"]["at_rest"], r["data"]["ticks"], r["data"]["t"]), (False, 60, 60))
        self.assertIn("STILL CHANGING after 60 ticks", r["text"])

    # ---- the lab against trace, and against tests

    def test_a_whole_design_does_in_the_lab_what_it_does_in_trace(self):
        """Same block changes on the same ticks, counted from each flip, for the 3x3 reference door."""
        _, blocks = validate(REF_3X3, 3)
        lever = next(list(p) for p, (bid, _) in blocks.items() if bid == "minecraft:lever")
        _, steps = self.s._sim(blocks, 2, 220)                      # what `trace` runs, in the test simulator
        self.do("new", blocks=REF_3X3, walls=True)
        got = [c for _ in range(steps["settle"]["ticks"]) for c in self.do("step")["changes"]]   # one tick per call
        self.assertEqual(got, [short(c) for c in steps["settle"]["changes"]])
        for i in range(2):
            lv, mv = steps[f"lever.{i}"], steps[f"move.{i}"]
            t0 = self.s.lab["t"]
            flip = self.do("flip", pos=lever)
            self.assertEqual([[c[0] - t0, *c[1:]] for c in flip["changes"]], [short(c) for c in lv["changes"] if c[1:4] != lever])
            got = [c for _ in range(mv["ticks"]) for c in self.do("step")["changes"]]
            self.assertGreater(len(got), 50)                        # a real mechanism, not a trivial comparison
            self.assertEqual(mv["changes_total"], len(mv["changes"]))   # the trace side was not cut short
            self.assertEqual([[c[0] - t0, *c[1:]] for c in got], [short(c) for c in mv["changes"]])
            door = self.do("look", cells=[])["doorway"]
            self.assertEqual(door.replace("/", ""), "".join(reversed([mv["door"][-1][y * 3:(y + 1) * 3] for y in range(3)])))
        self.assertEqual(door, ".../.../...")                       # closed, then open again

        # The recipe the brief gives: rest, flip, rest, flip, rest.
        self.do("new", blocks=REF_3X3, walls=True)
        r = self.do("rest", max_ticks=rules.SETTLE_CAP + rules.QUIET)
        self.assertEqual((r["ticks"], r["changes"]), (steps["settle"]["ticks"], [short(c) for c in steps["settle"]["changes"]]))
        for i in range(2):
            t0 = self.s.lab["t"]
            self.do("flip", pos=lever)
            r = self.do("rest", max_ticks=220)
            self.assertEqual((r["ticks"], r["at_rest"]), (steps[f"move.{i}"]["ticks"], True))
            self.assertEqual([[c[0] - t0, *c[1:]] for c in r["changes"]], [short(c) for c in steps[f"move.{i}"]["changes"]])

    def test_tests_and_the_lab_do_not_disturb_each_other(self):
        design = copy.deepcopy(REF_3X3)
        before = self.s.call_full("test", {"design": design})["data"]
        self.do("new", blocks=PISTON)
        self.do("flip", pos=[5, 8, 0])
        self.do("step", ticks=1)                                  # leave the lab mid-stroke
        mid = self.do("look")["blocks"]
        after = self.s.call_full("test", {"design": design})["data"]
        self.s.call("trace", {"design": design})
        self.s.call("view", {"design": design, "flips": 1})
        for key in ("valid", "volume", "dims", "open_ticks", "close_ticks", "failures"):
            self.assertEqual(before[key], after[key])
        self.assertEqual((before["valid"], before["volume"]), (True, 192))
        self.assertEqual(self.do("look")["blocks"], mid)          # the lab is exactly where it was left
        self.assertEqual([c[0] for c in self.do("step", ticks=2)["changes"]], [3, 3])

    # ---- placement

    def test_door_rules_do_not_apply_but_the_allow_list_does(self):
        two_levers = PISTON + [{"pos": [5, 12, 0], "id": "stone"}, {"pos": [5, 13, 0], "id": "lever", "props": LEVER}]
        self.assertEqual(self.do("new", blocks=two_levers)["placed"], 6)
        self.assertEqual(self.do("flip", pos=[5, 13, 0])["powered"], True)
        no_lever = [{"pos": [1, 1, 0], "id": "glass"}, {"pos": [1, 1, 5], "id": "stone"}, {"pos": [-1, 0, 3], "id": "stone"}]
        self.assertEqual(self.do("new", blocks=no_lever)["placed"], 3)        # doorway, hallway and wall cells are all usable
        self.assertEqual(self.do("look", cells=[])["doorway"], ".../.?./...")
        self.assertIn("in_shell at [-1, 0, 3]", self.refused("new", blocks=no_lever, walls=True))
        self.assertIn("block_not_allowed", self.refused("new", blocks=[{"pos": [1, 1, 1], "id": "tnt"}]))
        self.assertIn("out_of_region", self.refused("new", blocks=[{"pos": [0, 99, 0], "id": "stone"}]))
        self.assertIn("bad_format", self.refused("new", blocks="stone"))
        self.assertEqual(self.do("look", cells=[])["doorway"], ".../.?./...")  # a rejected lab leaves the old one in place

    def test_placement_removes_what_cannot_exist_and_observers_stay_quiet(self):
        floating = self.do("new", blocks=PISTON + [{"pos": [9, 9, 9], "id": "redstone_wire"}])
        self.assertEqual((floating["placed"], floating["lost"]), (5, [[9, 9, 9]]))
        self.assertEqual(self.do("look", cells=[[9, 9, 9]])["blocks"], [[9, 9, 9, "air"]])
        self.do("new", blocks=FIXTURES["good_idle_observers"])   # two observers facing each other
        r = self.do("rest")
        self.assertEqual((r["at_rest"], r["changes"], r["entity"]), (True, [], None))

    def test_walls_are_placed_only_on_request(self):
        self.do("new", blocks=PISTON)
        self.assertEqual(self.do("look", cells=[[-1, 0, 1]])["blocks"][0][3], "air")
        self.assertNotIn("%", self.s.call("lab_view", {}))
        self.do("new", blocks=PISTON, walls=True)
        self.assertEqual(self.do("look", cells=[[-1, 0, 1]])["blocks"][0][3], "stone")
        self.assertEqual(len(self.do("look")["blocks"]), 4)                  # wall cells are not listed among the blocks
        self.assertIn("%", self.s.call("lab_view", {"z": "1"}))

    def test_first_entity_is_reported_once(self):
        # A lever cannot stay on the side of a piston once that piston extends: it drops as an item.
        part = [{"pos": [5, 6, 0], "id": "sticky_piston", "props": {"facing": "down"}}, {"pos": [5, 5, 0], "id": "stone"},
                {"pos": [6, 6, 0], "id": "lever", "props": {"face": "wall", "facing": "east"}}]
        self.do("new", blocks=part)
        self.do("flip", pos=[6, 6, 0])
        r = self.s.call_full("lab_step", {"ticks": 2})
        self.assertEqual(r["data"]["entity"], {"t": 1, "type": "minecraft:item"})
        self.assertIn("ENTITY appeared at t=1: minecraft:item", r["text"])
        self.assertIsNone(self.do("step", ticks=2)["entity"])

    # ---- refusals and budget

    def test_refusals(self):
        fresh = Session(self.k, 3, "open", self.tmp / "fresh.jsonl")
        self.assertIn("no lab world yet", fresh.call("lab_step", {}))
        first = self.do("new", blocks=PISTON)["lab"]
        second = self.do("new", blocks=PISTON)["lab"]
        self.assertEqual(second, first + 1)
        self.assertIn(f"Lab {first} no longer exists", self.refused("step", lab=first))
        self.assertEqual(self.do("step", lab=second)["t"], 1)
        self.assertIn("no lever at 0, 0, 0", self.refused("flip", pos=[0, 0, 0]))
        self.assertIn("three whole numbers", self.refused("flip", pos=[0, 0]))
        for bad in (0, 2001, 1.5, "3", True):
            self.assertIn("whole number from 1 to 2000", self.refused("step", ticks=bad))
        self.assertIn("list of [x, y, z]", self.refused("look", cells=[[1, 2]]))
        self.assertEqual(self.s.lab["t"], 1)                      # none of the refusals moved the clock

    def test_budget_counts_ticks_only(self):
        s = Session(self.k, 3, "open", self.tmp / "budget.jsonl", budget={"lab": 30})
        try:
            for _ in range(5):                                    # free calls
                self.assertIsNotNone(s.call_full("lab_new", {"blocks": PISTON})["data"])
                s.call("lab_flip", {"pos": [5, 8, 0]})
                s.call("lab_look", {})
                s.call("lab_view", {})
            self.assertEqual(s.used["lab"], 0)
            self.assertEqual(s.call_full("lab_step", {"ticks": 12})["data"]["ticks_left"], 18)
            self.assertIn("Only 18 lab tick(s) left", s.call("lab_step", {"ticks": 19}))
            self.assertEqual((s.used["lab"], s.lab["t"]), (12, 12))                       # the refused step ran nothing
            s.call("lab_new", {"blocks": FIXTURES["bad_clock"]})
            r = s.call_full("lab_rest", {"max_ticks": 200})
            self.assertEqual((r["data"]["ticks"], r["data"]["at_rest"], r["data"]["ticks_left"]), (18, False, 0))
            self.assertIn("stopped by the lab tick budget", r["text"])
            self.assertIn("No lab ticks left", s.call("lab_rest", {}))
            self.assertIn("lab ticks used 30/30", s.call("status", {}))
            self.assertIsNotNone(s.call_full("lab_look", {})["data"])                      # still free
            score = server.score(s.log_path)
            self.assertEqual((score["lab_ticks"], score["lab_worlds"]), (30, 6))
        finally:
            s.close()

    def test_one_lab_world_runs_at_most_the_world_limit(self):
        self.do("new", blocks=FIXTURES["bad_clock"])               # never comes to rest
        self.assertEqual(self.do("step", ticks=2000)["t"], 2000)
        self.assertEqual(self.do("step", ticks=1990)["t"], 3990)
        self.assertIn("one lab world can run at most 4000 ticks. Step at most 10", self.refused("step", ticks=11))
        r = self.s.call_full("lab_rest", {"max_ticks": 200})
        self.assertEqual((r["data"]["ticks"], r["data"]["t"], r["data"]["at_rest"]), (10, 4000, False))
        self.assertIn("stopped at the 4000-tick limit for one lab world", r["text"])
        self.assertIn("Start a new lab", self.refused("rest"))
        self.assertEqual(self.do("new", blocks=PISTON)["t"], 0)

    def test_two_runs_sharing_one_simulator_do_not_disturb_each_other(self):
        other = Session(self.k, 2, "seamless", self.tmp / "other.jsonl")
        self.do("new", blocks=PISTON)
        self.do("flip", pos=[5, 8, 0])
        self.do("step", ticks=1)                                  # mid-stroke in this run's lab
        mid = self.do("look")["blocks"]
        other.call("lab_new", {"blocks": FIXTURES["bad_clock"]})  # the other run's lab never rests
        other.call("lab_step", {"ticks": 50})
        self.assertIn("VALID", other.call("test", {"design": copy.deepcopy(FIXTURES["good_2x2"])}))
        self.assertEqual(self.do("look")["blocks"], mid)
        self.assertEqual([c[0] for c in self.do("step", ticks=2)["changes"]], [3, 3])
        self.assertEqual(other.call_full("lab_step", {"ticks": 1})["data"]["t"], 51)


class TimeLimitTests(unittest.TestCase):
    def test_minutes_limit_counts_from_the_first_call(self):
        k = Kernel()
        try:
            s = Session(k, 1, "open", Path(tempfile.mkdtemp()) / "t.jsonl", minutes=10)
            clock = [1000.0]
            s.now = lambda: clock[0]
            clock[0] += 3600                                      # time before the first call does not count
            good = FIXTURES["good_1x1_open"]
            self.assertIn("time used: 0 of 10 minutes", s.call("status", {}))
            clock[0] += 599
            self.assertIn("VALID", s.call("test", {"design": copy.deepcopy(good)}))
            self.assertIn("time used: 9 of 10 minutes", s.call("status", {}))
            self.assertTrue(s.call("blocks", {}).endswith("\n[time left: 0 of 10 minutes]"))   # 599 s used: under a minute left
            clock[0] += 1
            for tool, args in (("test", {"design": good}), ("trace", {"design": good}), ("view", {"design": good}),
                               ("lab_new", {"blocks": good}), ("lab_step", {})):
                self.assertIn("Time is up: 10 minutes", s.call(tool, args))
            self.assertEqual(s.used, {"test": 1, "sim": 0, "lab": 0})
            self.assertIn("Allowed blocks", s.call("blocks", {}))
            self.assertIn("Submitted the design with tested volume 8", s.call("submit", {"design": copy.deepcopy(good)}))
            r = server.score(s.log_path)
            self.assertEqual((r["valid"], r["volume"], r["minutes_limit"]), (True, 8, 10))
            self.assertEqual((r["seconds_active"] is not None, r["seconds_to_first_valid"] is not None), (True, True))
            budget = {"test": 5, "sim": 9, "lab": 70}
            for interface in ("cli", "tools"):
                text = kit.brief(3, "open", budget, interface, minutes=10)
                self.assertIn("**70 lab ticks**", text)
                self.assertIn("**10 minutes**, counted from your\nfirst tool call", text)
                self.assertNotIn("minutes", kit.brief(3, "open", budget, interface).split("## Budget")[1].split("## Ground")[0])
        finally:
            k.close()


if __name__ == "__main__":
    unittest.main()
