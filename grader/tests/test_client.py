"""End-to-end tests of the agent's side: a real tool server, a real kit folder, and the
`./pd` commands run as separate processes, the way a command-line agent runs them."""
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class ClientTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.kit = cls.tmp / "kit"
        port = free_port()
        cls.server = subprocess.Popen(
            [sys.executable, "-m", "pdgrader", "serve", "--n", "1", "--track", "open", "--port", str(port),
             "--log", str(cls.tmp / "log.jsonl"), "--kit", str(cls.kit), "--tests", "4", "--lab-ticks", "5000"],
            cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        deadline = time.time() + 120
        while time.time() < deadline:
            try:
                socket.create_connection(("127.0.0.1", port), timeout=1).close()
                break
            except OSError:
                if cls.server.poll() is not None:
                    raise RuntimeError("tool server exited: " + cls.server.stdout.read())
                time.sleep(0.2)
        else:
            raise RuntimeError("tool server did not start")

    @classmethod
    def tearDownClass(cls):
        subprocess.run(["./pd", "py", "--reset"], cwd=cls.kit, capture_output=True)
        cls.server.terminate()
        cls.server.wait(timeout=30)
        cls.server.stdout.close()

    def pd(self, *args, stdin=None, code=0):
        r = subprocess.run(["./pd", *map(str, args)], cwd=self.kit, input=stdin, capture_output=True, text=True, timeout=120)
        self.assertEqual(r.returncode, code, r.stdout + r.stderr)
        return r.stdout + r.stderr

    def py(self, source, code=0):
        return self.pd("py", stdin=source, code=code)

    def test_kit_contents(self):
        names = {p.name for p in self.kit.iterdir()}
        self.assertLessEqual({"TASK.md", "pd", "pdbuild.py", "pdlab.py", "example_lab.py", "example_1x1.json"}, names)
        brief = (self.kit / "TASK.md").read_text()
        for phrase in ("## The lab", "./pd lab new part.json [--walls]", "### The Python session", "**5000 lab ticks**",
                       "{(x, y, z): state}"):
            self.assertIn(phrase, brief)
        self.assertNotIn("minutes", brief.split("## Budget")[1].split("##")[0])      # no time limit was set

    def test_lab_commands(self):
        self.assertIn("4 block(s) placed, hallway walls present, clock t=0", self.pd("lab", "new", "example_1x1.json", "--walls"))
        self.assertIn("lever at (-3,0,0) switched on", self.pd("lab", "flip", -3, 0, 0))        # negative coordinates parse
        out = self.pd("lab", "step", 3, "--grep", "(0,0,0)")
        self.assertIn("lab t=0 -> t=3:", out)
        self.assertIn("t=3 (0,0,0) moving_piston[facing=east,type=normal] -> stone", out)
        self.assertNotIn("(-2,0,0)", out)                                                         # --grep filtered the rest
        out = self.pd("lab", "look", "--at", 0, 0, 0, "--at", -1, 0, 1, "--at", 5, 5, 5)
        self.assertIn("doorway #", out)
        self.assertIn("(0,0,0) stone", out)
        self.assertIn("(-1,0,1) stone", out)                                                      # a hallway-wall cell
        self.assertIn("(5,5,5) air", out)
        self.assertIn("at rest; no block changed", self.pd("lab", "rest", "--limit", 0))
        self.assertIn("Lab at t=23.", self.pd("lab", "view", "--z", "0"))
        self.assertIn("no lever at 9, 9, 9", self.pd("lab", "flip", 9, 9, 9))
        self.assertIn("lab ticks used 23/5000", self.pd("status"))

    def test_python_session(self):
        self.pd("py", "--reset")
        self.assertEqual(self.pd("py", "-c", "x = 41"), "")                       # an assignment prints nothing
        self.assertEqual(self.pd("py", "-c", "x + 1"), "42\n")                    # kept between processes; last value echoed
        self.assertEqual(self.py("def twice(v):\n    return 2 * v\nprint('defined')\n"), "defined\n")
        (self.kit / "s.py").write_text("y = twice(x)\ny\n")
        self.assertEqual(self.pd("py", "s.py"), "82\n")
        self.assertEqual(self.pd("py", "-c", "None"), "")
        self.assertEqual(self.pd("py", "-c", "import os; os.path.basename(os.getcwd())"), "'kit'\n")   # runs in the kit folder

        err = self.pd("py", "-c", "1/0", code=1)
        self.assertIn("ZeroDivisionError", err)
        self.assertNotIn("py_serve", err)                                          # no frames from the tool itself
        self.assertIn("SyntaxError", self.pd("py", "-c", "def f(:", code=1))
        self.assertIn("SystemExit", self.pd("py", "-c", "import sys; sys.exit(3)", code=1))
        self.assertEqual(self.pd("py", "-c", "y"), "82\n")                        # the session outlived all three

        out = self.pd("py", "-c", "print('x' * 40000)")
        self.assertIn("output cut off here: 40001 characters in all, 30000 shown", out)
        self.assertEqual(out.count("x"), 30000)

        self.assertIn("no reply after 1 s", self.pd("py", "--timeout", 1, "-c", "import time; time.sleep(30)", code=1))
        self.assertIn("NameError", self.pd("py", "-c", "y", code=1))               # the timeout ended the session
        self.pd("py", "-c", "z = 1")
        self.assertIn("variables are gone", self.pd("py", "--reset"))
        self.assertIn("NameError", self.pd("py", "-c", "z", code=1))
        self.assertIn("There was no Python session", self.pd("py", "--reset") + self.pd("py", "--reset"))

    def test_python_calls_run_one_after_another(self):
        self.pd("py", "--reset")
        self.pd("py", "-c", "import time; order = []")
        slow = subprocess.Popen(["./pd", "py", "-c", "time.sleep(2); order.append('slow')"], cwd=self.kit,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        time.sleep(0.5)                                            # the slow call is now running
        t0 = time.time()
        self.assertEqual(self.pd("py", "-c", "order.append('quick'); order"), "['slow', 'quick']\n")
        self.assertGreater(time.time() - t0, 1.0)                  # it waited for the slow call
        slow.communicate(timeout=30)

    def test_a_stale_session_file_never_stops_another_process(self):
        self.pd("py", "--reset")
        bystander = subprocess.Popen(["sleep", "60"])
        try:
            port = free_port()                                       # nothing listens there
            (self.kit / ".pd_py").write_text(json.dumps({"port": port, "token": "x", "pid": bystander.pid}))
            self.assertEqual(self.pd("py", "-c", "6 * 7"), "42\n")   # a new session starts
            self.assertIsNone(bystander.poll())
            self.assertIn("variables are gone", self.pd("py", "--reset"))   # end the real session before faking its file again
            (self.kit / ".pd_py").write_text(json.dumps({"port": port, "token": "x", "pid": bystander.pid}))
            self.assertIn("There was no Python session", self.pd("py", "--reset"))
            self.assertIsNone(bystander.poll())                      # still running
        finally:
            bystander.kill()
            bystander.wait()

    def test_idle_python_session_ends_by_itself(self):
        self.pd("py", "--reset")
        env = {**os.environ, "PD_PY_IDLE_SECONDS": "1"}
        subprocess.run(["./pd", "py", "-c", "kept = 1"], cwd=self.kit, env=env, check=True, capture_output=True)
        self.assertTrue((self.kit / ".pd_py").exists())
        port = json.loads((self.kit / ".pd_py").read_text())["port"]
        time.sleep(2.5)
        self.assertFalse((self.kit / ".pd_py").exists())           # it cleaned up after itself
        with self.assertRaises(OSError):
            socket.create_connection(("127.0.0.1", port), timeout=2)   # and nothing listens there any more
        self.assertIn("NameError", self.pd("py", "-c", "kept", code=1))

    def test_python_tools(self):
        self.pd("py", "--reset")
        out = self.py('''
r = test("example_1x1.json")
print(r.valid, bool(r), r.volume, r.dims, r.failures, r.rejected, r.refused)
print(r.text.splitlines()[0])
bad = test({"initial_state": "open", "blocks": [{"pos": [0, 0, 1], "id": "stone"}]})
print(bad.valid, bool(bad), bad.rejected, bad.volume)
d = Design.load("example_1x1.json")
print(test(d).volume, "volume" in status(), "sticky_piston" in blocks(), "flip 1" in trace(d, flips=1), "z = 0" in view(d))
print(submit(d).split(".")[0])
moved = d.copy().translate(0, 5, 0)
print(d.get(-2, 0, 0)[0], moved.get(-2, 5, 0)[0], d.get(-2, 5, 0))
last = [test(d) for _ in range(5)][-1]
print(last.valid, last.refused, last.rejected, last.volume, last.text.splitlines()[0])
''')
        self.assertEqual(out.splitlines(), [
            "True True 8 [4, 2, 1] [] False False",
            "VALID. volume 8 (4 x 2 x 1), blocks 3, open 1 ticks, close 3 ticks, at rest by tick 3.",
            "False False True None",
            "8 True True True True",
            "Submitted the design with tested volume 8",
            "sticky_piston sticky_piston None",
            "False True False None No test calls left (budget 4). Use `pd status`; `pd submit` still works.",
        ])

    def test_python_lab(self):
        self.pd("py", "--reset")
        out = self.py('''
lab = Lab("example_1x1.json")
print(lab.t, lab.lost, lab.doorway(), lab.block(0, 0, 0), lab.block(-1, 0, 0))
print(lab.flip(-3, 0, 0))
print([c for c in lab.step(3) if c[1] == (0, 0, 0)])
print(lab.t, lab.doorway(), lab.rest(), lab.t, lab.entity, lab.ticks_left <= 5000 - 23)
print(lab.timeline(0, 0, 0), len(lab.history), sorted(lab.blocks())[0])
print(lab.view(z=0).splitlines()[0])
''')
        self.assertEqual(out.splitlines(), [
            "0 [] . air stone",
            "[]",
            "[(1, (0, 0, 0), 'air', 'moving_piston[facing=east,type=normal]'), (3, (0, 0, 0), 'moving_piston[facing=east,type=normal]', 'stone')]",
            "3 # True 23 None True",
            "[(1, 'moving_piston[facing=east,type=normal]'), (3, 'stone')] 5 (-3, -1, 0)",
            "Lab at t=23. x runs left to right (west to east), y bottom to top; one grid per z layer.",
        ])
        out = self.py('''
newer = Lab([{"pos": [2, 2, 2], "id": "stone"}])
for attempt in (lambda: lab.step(), lambda: newer.flip(2, 2, 2), lambda: Lab([{"pos": [0, 0, 0], "id": "tnt"}]),
                lambda: newer.step(5001)):
    try:
        attempt()
        print("no error")
    except PdError as e:
        print(str(e).splitlines()[0])
print(newer.t, newer.block(2, 2, 2))
# A lever on the side of a piston drops as an item when that piston extends.
drop = Lab([{"pos": [5, 6, 0], "id": "sticky_piston", "props": {"facing": "down"}}, {"pos": [5, 5, 0], "id": "stone"},
            {"pos": [6, 6, 0], "id": "lever", "props": {"face": "wall", "facing": "east"}}])
drop.flip(6, 6, 0)
drop.step(2)
print(drop.entity)
''')
        lines = out.splitlines()
        self.assertRegex(lines[0], r"^Lab \d+ no longer exists: a newer lab world")
        self.assertIn("no lever at 2, 2, 2", lines[1])
        self.assertIn("REJECTED", lines[2])
        self.assertIn("whole number from 1 to 2000", lines[3])
        self.assertEqual(lines[4], "0 stone")
        self.assertEqual(lines[5], "(1, 'minecraft:item')")

    def test_worked_example(self):
        self.pd("py", "--reset")
        out = self.pd("py", "example_lab.py")
        first, second = out.split("flip 2:")
        self.assertIn("+2  (6, 8, 0) observer[facing=west,powered=false] -> observer[facing=west,powered=true]", first)
        self.assertIn("+4  (6, 8, 0) observer[facing=west,powered=true] -> observer[facing=west,powered=false]", first)
        self.assertIn("stone now at x = [9]", first)             # the short pulse left the stone behind
        self.assertIn("stone now at x = [8]", second)            # the next pulse fetched it back
        self.assertIn("lab clock t=52", second)
        self.assertIn("Lab at t=52.", self.pd("py", "-c", "print(lab.view(z=0))"))   # still defined afterwards


if __name__ == "__main__":
    unittest.main()
