"""Changed-physics variants: the agent's constant patches, their measured effects, and how
the session, brief and scorer carry the setting. Run from grader/:
python3 -m unittest tests.test_physics -v
"""
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
from pdgrader import kit, server  # noqa: E402
from pdgrader.grade import grade  # noqa: E402
from pdgrader.kernel import Kernel, KernelError, physics_key  # noqa: E402
from pdgrader.session import Session  # noqa: E402

CHANGED = {"repeater_unit": 3, "push_limit": 8, "observer_delay": 3, "observer_pulse": 4}


def B(x, y, z, i, **p):
    return {"pos": [x, y, z], "id": i, **({"props": p} if p else {})}


REPEATER = [B(0, -1, 5, "stone"), B(0, 0, 5, "lever", face="floor", facing="north"), B(1, -1, 5, "stone"),
            B(1, 0, 5, "repeater", facing="west", delay="1"), B(2, 0, 5, "piston", facing="east")]
OBSERVER = [B(-5, -1, 5, "stone"), B(-5, 0, 5, "lever", face="floor", facing="north"), B(-4, 0, 5, "observer", facing="west"),
            B(-3, 0, 5, "sticky_piston", facing="east"), B(-2, 0, 5, "stone")]
PUSH9 = [B(-1, -1, 5, "stone"), B(-1, 0, 5, "lever", face="floor", facing="north"), B(0, 0, 5, "piston", facing="east")] + [
    B(x, 0, 5, "iron_block") for x in range(1, 10)]


def first_change(text, cell, needle):
    """Tick of the first lab change at `cell` whose text contains `needle`."""
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("t=") and f" {cell} " in line + " " and needle in line:
            return int(line.split()[0][2:])
    return None


class PhysicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.vanilla = Kernel()
        cls.changed = Kernel(physics=CHANGED)

    @classmethod
    def tearDownClass(cls):
        cls.vanilla.close()
        cls.changed.close()

    def lab(self, kernel, blocks, lever, name):
        s = Session(kernel, 1, "open", self.tmp / f"{name}.jsonl", physics=kernel.physics)
        s.call("lab_new", {"blocks": blocks})
        s.call("lab_flip", {"pos": lever})
        return s.call("lab_rest", {})

    def test_patches_reported(self):
        applied = [line for line in self.changed.log if line.startswith("PDK_PHYSICS ")]
        self.assertEqual(sorted(line.split()[1] for line in applied), sorted(CHANGED))
        self.assertFalse([line for line in self.vanilla.log if line.startswith("PDK_PHYSICS")])

    def test_repeater_unit(self):
        self.assertEqual(first_change(self.lab(self.vanilla, REPEATER, [0, 0, 5], "rv"), "(2,0,5)", "extended=true"), 2)
        self.assertEqual(first_change(self.lab(self.changed, REPEATER, [0, 0, 5], "rc"), "(2,0,5)", "extended=true"), 3)

    def test_observer_delay_and_pulse(self):
        v = self.lab(self.vanilla, OBSERVER, [-5, 0, 5], "ov")
        c = self.lab(self.changed, OBSERVER, [-5, 0, 5], "oc")
        self.assertEqual((first_change(v, "(-4,0,5)", "-> observer[facing=west,powered=true]"), first_change(v, "(-4,0,5)", "-> observer[facing=west,powered=false]")), (2, 4))
        self.assertEqual((first_change(c, "(-4,0,5)", "-> observer[facing=west,powered=true]"), first_change(c, "(-4,0,5)", "-> observer[facing=west,powered=false]")), (3, 7))
        # Vanilla: the 2-tick pulse leaves the block behind (it lands at (-1,0,5) and stays).
        # Changed: the 4-tick pulse lets the push finish, then the piston pulls the block back.
        self.assertIn("(-1,0,5) moving_piston[facing=east,type=normal] -> stone", v)
        self.assertIn("(-1,0,5) moving_piston[facing=east,type=normal] -> stone", c)
        self.assertIsNotNone(first_change(c, "(-1,0,5)", "stone -> "))
        self.assertIsNone(first_change(v, "(-1,0,5)", "stone -> "))

    def test_solvable_variant_keeps_block_dropping(self):
        # The benchmark's changed-physics task: repeater step 3, observer delay 3, pulse still 2.
        phys = {"repeater_unit": 3, "observer_delay": 3}
        with Kernel(physics=phys) as k:
            s = Session(k, 1, "open", self.tmp / "solvable.jsonl", physics=phys)
            s.call("lab_new", {"blocks": OBSERVER})
            s.call("lab_flip", {"pos": [-5, 0, 5]})
            out = s.call("lab_rest", {})
        self.assertEqual(first_change(out, "(-4,0,5)", "-> observer[facing=west,powered=true]"), 3)
        self.assertEqual(first_change(out, "(-4,0,5)", "-> observer[facing=west,powered=false]"), 5)
        self.assertIn("t=5 (-1,0,5) moving_piston[facing=east,type=normal] -> stone", out)   # left behind
        self.assertIsNone(first_change(out, "(-1,0,5)", "stone -> "))
        text = kit.brief(3, "seamless", {"test": 5, "sim": 9}, "cli", physics=phys)
        self.assertIn("An observer turns on 3 ticks after the change it sees and off 2 ticks later.", text)
        self.assertIn("leaves it behind", text)

    def test_push_limit(self):
        self.assertIn("(1,0,5) iron_block -> moving_piston", self.lab(self.vanilla, PUSH9, [-1, 0, 5], "pv"))
        self.assertNotIn("moving_piston", self.lab(self.changed, PUSH9, [-1, 0, 5], "pc"))

    def test_settings_checked(self):
        with self.assertRaises(KernelError):
            physics_key({"gravity": 2})
        self.assertEqual(physics_key({"repeater_unit": 2, "push_limit": 8}), {"push_limit": 8})  # vanilla values drop out
        with self.assertRaises(ValueError):   # a run's physics must match its simulator's
            Session(self.vanilla, 1, "open", self.tmp / "mismatch.jsonl", physics={"push_limit": 8})

    def test_session_log_resume_and_score(self):
        log = self.tmp / "phys-run.jsonl"
        s = Session(self.changed, 2, "seamless", log, budget={"test": 3}, physics=CHANGED)
        self.assertIn("VALID", s.call("test", {"design": copy.deepcopy(FIXTURES["good_2x2"])}))
        start = json.loads(log.read_text().splitlines()[0])
        self.assertEqual(start["physics"], physics_key(CHANGED))
        with self.assertRaises(ValueError):   # the same log is not a vanilla run
            Session(self.vanilla, 2, "seamless", log, resume=True)
        Session(self.changed, 2, "seamless", log, resume=True, physics=CHANGED)
        out = server.score(log, translations=False)
        self.assertEqual(out["physics"], physics_key(CHANGED))
        self.assertTrue(out["valid"])
        self.assertIsNone(out["reference"])   # vanilla references never apply to changed physics

    def test_vanilla_reference_fails_under_changed_physics(self):
        ref = json.loads((ROOT / "reference_designs" / "ref_3x3_seamless_192.json").read_text())
        self.assertTrue(grade(self.vanilla, copy.deepcopy(ref), 3, "seamless")["valid"])
        self.assertFalse(grade(self.changed, copy.deepcopy(ref), 3, "seamless")["valid"])

    def test_brief(self):
        budget = {"test": 5, "sim": 9}
        vanilla = kit.brief(3, "seamless", budget, "cli")
        self.assertEqual(vanilla, kit.brief(3, "seamless", budget, "cli", physics={"repeater_unit": 2}))
        self.assertNotIn("physics are changed", vanilla)
        text = kit.brief(3, "seamless", budget, "cli", physics=CHANGED)
        self.assertIn("**This world's physics are changed.**", text)
        self.assertIn("Pistons push at most 8 blocks.", text)
        self.assertIn("A repeater adds 3 ticks per delay step", text)
        self.assertIn("An observer turns on 3 ticks after the change it sees and off 4 ticks later.", text)
        self.assertIn("pulls its block back", text)
        with self.assertRaises(ValueError):    # a pulse length whose behaviour was never measured
            kit.brief(3, "seamless", budget, "cli", physics={"observer_pulse": 3})


if __name__ == "__main__":
    unittest.main()
