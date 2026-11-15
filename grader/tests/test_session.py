"""Tests for the agent-facing session (budget, log, submit) and final scoring from the log."""
import copy
import json
import os
import sys
import tempfile
import types
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "fixtures"))

from make_fixtures import FIXTURES  # noqa: E402
from pdgrader import kit, server  # noqa: E402
from pdgrader.kernel import Kernel  # noqa: E402
from pdgrader.session import Session  # noqa: E402

GOOD, SMALLER = FIXTURES["good_1x1_seamless"], FIXTURES["good_1x1_open"]


class SessionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k = Kernel()
        cls.tmp = Path(tempfile.mkdtemp())

    @classmethod
    def tearDownClass(cls):
        cls.k.close()

    def session(self, name, track="open", **budget):
        return Session(self.k, 1, track, self.tmp / f"{name}.jsonl", budget={"test": 3, "sim": 2, **budget})

    def test_budget_and_free_rejections(self):
        s = self.session("budget")
        self.assertIn("REJECTED", s.call("test", {"design": FIXTURES["bad_command_block"]}))
        self.assertEqual(s.used["test"], 0)                      # rejected designs are free
        for _ in range(3):
            self.assertIn("VALID", s.call("test", {"design": copy.deepcopy(GOOD)}))
        self.assertIn("No test calls left", s.call("test", {"design": copy.deepcopy(GOOD)}))
        self.assertIn("flip 1", s.call("trace", {"design": GOOD, "flips": 1}))
        self.assertIn("z = 0", s.call("view", {"design": GOOD}))
        self.assertIn("No sim calls left", s.call("view", {"design": GOOD}))
        self.assertIn("unknown tool", s.call("explode", {}))
        self.assertIn("bad arguments", s.call("test", {"nope": 1}))
        self.assertIn("must be a JSON object", s.call("test", {"design": "text"}))

    def test_best_tracking_and_failure_text(self):
        s = self.session("best")
        s.call("test", {"design": copy.deepcopy(GOOD)})
        self.assertEqual(s.best["volume"], 15)
        out = s.call("test", {"design": copy.deepcopy(FIXTURES["bad_nonsticky"])})
        self.assertIn("FAIL did_not_open", out)
        self.assertIn("doorway over time", out)
        self.assertEqual(s.best["volume"], 15)                   # an invalid design never becomes the best
        self.assertIn("best valid design so far", s.call("test", {"design": copy.deepcopy(SMALLER)}))
        self.assertEqual(s.best["volume"], 8)

    def test_score_uses_last_submit(self):
        s = self.session("submit")
        s.call("test", {"design": copy.deepcopy(SMALLER)})       # volume 8
        s.call("test", {"design": copy.deepcopy(GOOD)})          # volume 15
        self.assertIn("smaller valid design", s.call("submit", {"design": copy.deepcopy(GOOD)}))
        r = server.score(s.log_path, reference=30)
        self.assertEqual((r["valid"], r["volume"], r["candidate_source"], r["score"]), (True, 15, "last submit", 2.0))
        self.assertEqual((r["best_dev_volume"], r["test_calls"], r["translations"]["passed"]), (8, 2, 11))

    def test_score_without_submit_uses_best(self):
        s = self.session("nosubmit")
        s.call("test", {"design": copy.deepcopy(GOOD)})
        s.call("test", {"design": copy.deepcopy(SMALLER)})
        r = server.score(s.log_path)
        self.assertEqual((r["valid"], r["volume"], r["candidate_source"]), (True, 8, "best tested (no submit)"))

    def test_untested_submit_that_fails_scores_zero(self):
        s = self.session("badsubmit")
        s.call("test", {"design": copy.deepcopy(GOOD)})
        self.assertIn("has not passed", s.call("submit", {"design": copy.deepcopy(FIXTURES["bad_nonsticky"])}))
        r = server.score(s.log_path, reference=30)
        self.assertEqual((r["valid"], r["score"], r["final_failures"][0]["code"]), (False, 0.0, "did_not_open"))

    def test_nothing_valid(self):
        s = self.session("empty")
        s.call("test", {"design": copy.deepcopy(FIXTURES["bad_nonsticky"])})
        r = server.score(s.log_path, reference=30)
        self.assertEqual((r["valid"], r["score"], r["candidate_source"]), (False, 0.0, None))

    def test_seamless_session(self):
        s = self.session("seamless", track="seamless")
        self.assertIn("FAIL not_seamless", s.call("test", {"design": copy.deepcopy(SMALLER)}))
        self.assertIn("VALID", s.call("test", {"design": copy.deepcopy(GOOD)}))

    def test_trace_shows_changes_made_at_the_flip(self):
        s = Session(self.k, 2, "open", self.tmp / "trace2.jsonl")
        trace = s.call("trace", {"design": copy.deepcopy(FIXTURES["good_2x2"]), "flips": 1, "limit": 300})
        self.assertRegex(trace, r"t=0 \(.*redstone_wire\[.*power=0.*-> redstone_wire\[.*power=1")  # dust powers up at once
        self.assertNotIn("lever[", trace)

    def test_resume_after_restart(self):
        log = self.tmp / "resume.jsonl"
        clock = [5000.0]
        fake = types.SimpleNamespace(time=lambda: clock[0], monotonic=lambda: clock[0])   # the session's clocks only
        patcher = mock.patch("pdgrader.session.time", fake)
        patcher.start()
        self.addCleanup(patcher.stop)
        s = Session(self.k, 1, "open", log, budget={"test": 5, "sim": 4, "lab": 100}, minutes=30)
        s.call("test", {"design": copy.deepcopy(GOOD)})                       # 15
        s.call("test", {"design": copy.deepcopy(SMALLER)})                    # 8
        s.call("test", {"design": FIXTURES["bad_command_block"]})             # rejected: free
        s.call("trace", {"design": GOOD, "flips": 1})
        part = [{"pos": [3, 3, 3], "id": "stone"}]
        s.call("lab_new", {"blocks": part})
        s.call("lab_step", {"ticks": 7})
        clock[0] += 600                                                       # 10 minutes of the 30 used
        s.call("submit", {"design": copy.deepcopy(GOOD)})
        s.close()
        os.utime(log, (clock[0], clock[0]))
        clock[0] += 3600                                                      # an hour with no server

        r = Session(self.k, 1, "open", log, budget={"test": 999}, minutes=999, resume=True)   # the log's limits win
        self.assertEqual(r.budget["test"], 5)
        self.assertEqual(r.minutes, 30)
        self.assertEqual(r.used, {"test": 2, "sim": 1, "lab": 7})
        self.assertEqual((r.best["volume"], r.submitted["volume"], r.lab_count), (8, 15, 1))
        self.assertIn("lab world is gone: the tool server was restarted", r.call("lab_step", {}))
        status = r.call("status", {})
        self.assertIn("test calls used 2/5", status)
        self.assertIn("lab ticks used 7/100", status)
        self.assertIn("submitted: volume 15", status)
        self.assertEqual((r.now() - r.first_call) / 60, 10)                  # the hour with no server is not counted
        self.assertIn("time used: 10 of 30 minutes", status)
        resumed = json.loads(log.read_text().splitlines()[-1])
        self.assertEqual((resumed["kind"], resumed["t"], resumed["seconds_since_last_entry"]), ("resume", 600, 3600))
        self.assertEqual(r.call_full("lab_new", {"blocks": part})["data"]["lab"], 2)   # lab numbers carry on
        r.call("test", {"design": copy.deepcopy(GOOD)})
        r.close()

        score = server.score(log, reference=30)
        self.assertEqual((score["server_restarts"], score["test_calls"], score["candidate_source"], score["volume"]),
                         (1, 3, "last submit", 15))
        times = [json.loads(line)["t"] for line in log.read_text().splitlines()]
        self.assertEqual(times, sorted(times))                                # log time never runs backwards
        with self.assertRaises(ValueError):
            Session(self.k, 2, "open", log, resume=True)                      # wrong task

    def test_rectangular_session(self):
        log = self.tmp / "rect.jsonl"
        s = Session(self.k, [2, 1], "seamless", log, budget={"test": 3, "sim": 2})
        self.assertEqual(s.n, (2, 1))
        self.assertIn("Task: 2x1 door", s.call("status", {}))
        self.assertIn("VALID", s.call("test", {"design": copy.deepcopy(FIXTURES["good_2x1"])}))
        self.assertIn("z = 0", s.call("view", {"design": FIXTURES["good_2x1"]}))
        self.assertIn("flip 1", s.call("trace", {"design": FIXTURES["good_2x1"], "flips": 1}))
        # The lab uses the same doorway: with the hallway walls placed, the 2x1 door closes and reopens there too.
        s.call("lab_new", {"blocks": FIXTURES["good_2x1"]["blocks"], "walls": True})
        s.call("lab_flip", {"pos": [-1, 4, 0]})
        self.assertIn("(1,0,0) moving_piston[facing=down,type=normal] -> stone", s.call("lab_rest", {}))
        self.assertIn("doorway ##", s.call("lab_look", {}))
        r = Session(self.k, (2, 1), "seamless", log, resume=True)          # the log stores [2, 1]
        self.assertEqual(r.best["volume"], 24)
        with self.assertRaises(ValueError):
            Session(self.k, (1, 2), "seamless", log, resume=True)             # the other orientation is a different task
        text = kit.brief((2, 1), "seamless", {"test": 5, "sim": 9}, "cli")
        self.assertIn("smallest working 2x1 piston door", text)
        self.assertIn("2 cells wide (along x) and 1 cells tall", text)
        self.assertNotIn("{", text.split("```json")[0])

    def test_briefs_render(self):
        budget = {"test": 5, "sim": 9}
        for n in (2, 3, 7):
            for track in ("open", "seamless"):
                for interface in ("cli", "tools"):
                    text = kit.brief(n, track, budget, interface, FIXTURES["good_2x2"], 110)
                    self.assertNotIn("{", text.split("```json")[0])   # no unfilled placeholders before the example
                    self.assertIn(f"{n}x{n}", text)
                    self.assertIn("**5 test calls**", text)
        out = kit.make_kit(self.tmp / "kit", 2, "seamless", "http://127.0.0.1:1", budget, ROOT / "fixtures" / "good_2x2.json", 110)
        self.assertEqual(json.loads((out / "start.json").read_text()), FIXTURES["good_2x2"])


if __name__ == "__main__":
    unittest.main()
