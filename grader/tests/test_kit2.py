"""Kit 2: the film (every tick of a run as data), structured test results, the facts added to
the brief (one test per bullet), and the gate that keeps kit 1 as it was.
Run from grader/: python3 -m unittest tests.test_kit2 -v
"""
import copy
import json
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "fixtures"))

from make_fixtures import FIXTURES  # noqa: E402
from pdgrader import kit  # noqa: E402
from pdgrader.kernel import Kernel  # noqa: E402
from pdgrader.session import Session  # noqa: E402

GOOD = FIXTURES["good_2x2"]


def B(x, y, z, i, **p):
    return {"pos": [x, y, z], "id": i, **({"props": p} if p else {})}


def L(x, y, z):
    return B(x, y, z, "lever", face="floor", facing="north")


class Kit2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k = Kernel()
        cls.tmp = Path(tempfile.mkdtemp())
        cls.s = Session(cls.k, 3, "seamless", cls.tmp / "facts.jsonl", kit=2)

    @classmethod
    def tearDownClass(cls):
        cls.k.close()

    def lab(self, blocks, lever=None, walls=False, flips=1):
        """Place, flip `flips` times resting after each. Returns (entity seen in any flip, look(cells) function)."""
        self.assertIsNotNone(self.s.call_full("lab_new", {"blocks": blocks, "walls": walls})["data"])
        entity = None
        for _ in range(flips if lever else 0):
            self.s.call("lab_flip", {"pos": lever})
            entity = entity or self.s.call_full("lab_rest", {"limit": 0})["data"]["entity"]
        if not lever:
            self.s.call_full("lab_rest", {"limit": 0})

        def look(*cell):
            return self.s.call_full("lab_look", {"cells": [list(cell)]})["data"]["blocks"][0][3]
        return entity, look

    # ---- the facts added to the brief, in the brief's order
    def test_dust_strength(self):
        for n, piston in ((15, "true"), (16, "false")):
            blocks = ([B(0, 0, 5, "stone"), L(0, 1, 5)] + [B(x, -1, 5, "stone") for x in range(1, n + 1)]
                      + [B(x, 0, 5, "redstone_wire") for x in range(1, n + 1)] + [B(n + 1, 0, 5, "piston", facing="up")])
            _, look = self.lab(blocks, [0, 1, 5])
            self.assertIn(f"power={16 - n}", look(n, 0, 5))
            self.assertIn(f"extended={piston}", look(n + 1, 0, 5))

    def test_dust_does_not_relay_through_a_block(self):
        row = lambda mid: [B(0, 0, 5, "stone"), L(0, 1, 5), B(1, -1, 5, "stone"), mid, B(2, 0, 5, "stone"), B(3, -1, 5, "stone"),
                           B(3, 0, 5, "redstone_wire")]
        _, look = self.lab(row(B(1, 0, 5, "redstone_wire")), [0, 1, 5])
        self.assertIn("power=15", look(1, 0, 5))
        self.assertIn("power=0", look(3, 0, 5))
        _, look = self.lab(row(B(1, 0, 5, "repeater", facing="west", delay="1")), [0, 1, 5])
        self.assertIn("power=15", look(3, 0, 5))

    def test_sticky_piston_pulls_one_block(self):
        blocks = [B(-1, 0, 5, "stone"), L(-1, 1, 5), B(0, 0, 5, "sticky_piston", facing="east"), B(1, 0, 5, "stone"), B(2, 0, 5, "iron_block")]
        _, look = self.lab(blocks, [-1, 1, 5], flips=2)
        self.assertEqual((look(1, 0, 5), look(2, 0, 5), look(3, 0, 5)), ("stone", "air", "iron_block"))

    def test_dust_on_a_sideways_piston_drops(self):
        for facing in ("north", "south", "east", "west", "down"):
            side = B(-1, 0, 5, "stone") if facing != "west" else B(0, 0, 4, "stone")
            lever = [-1, 1, 5] if facing != "west" else [0, 1, 4]
            floor = B(0, -1, 5, "stone") if facing != "down" else B(0, -1, 9, "stone")
            entity, look = self.lab([B(0, 0, 5, "piston", facing=facing), floor, side, L(*lever), B(0, 1, 5, "redstone_wire")], lever)
            if facing == "down":
                self.assertIsNone(entity)
                self.assertIn("redstone_wire", look(0, 1, 5))
            else:
                self.assertEqual(entity["type"], "minecraft:item", facing)
                self.assertEqual(look(0, 1, 5), "air")

    def test_lever_on_a_piston(self):
        entity, look = self.lab([B(0, 3, 5, "sticky_piston", facing="down"), B(0, 2, 5, "stone"), L(0, 4, 5)], [0, 4, 5], flips=2)
        self.assertIsNone(entity)                                   # on the back: stays through a close and an open
        self.assertIn("lever", look(0, 4, 5))
        self.assertEqual(look(0, 1, 5), "air")
        entity, look = self.lab([B(0, 3, 5, "sticky_piston", facing="down"), B(0, 2, 5, "stone"), L(0, 4, 5)], [0, 4, 5])
        self.assertEqual(look(0, 1, 5), "stone")                    # and it does power the piston
        entity, look = self.lab([B(0, 0, 5, "piston", facing="east"), B(0, -1, 5, "stone"), L(0, 1, 5)], [0, 1, 5])
        self.assertEqual(entity["type"], "minecraft:item")          # on a side face: drops
        self.assertEqual(look(0, 1, 5), "air")

    def test_lever_on_middle_piston_switches_three(self):
        blocks = [B(x, 3, 5, "sticky_piston", facing="down") for x in (0, 1, 2)] + [B(x, 2, 5, "stone") for x in (0, 1, 2)] + [L(1, 4, 5)]
        entity, look = self.lab(blocks, [1, 4, 5])
        self.assertEqual([look(x, 1, 5) for x in (0, 1, 2)], ["stone"] * 3)
        entity, look = self.lab(blocks, [1, 4, 5], flips=2)
        self.assertEqual([look(x, 1, 5) for x in (0, 1, 2)], ["air"] * 3)
        self.assertIsNone(entity)

    def test_note_block_and_observer(self):
        blocks = [B(0, 0, 5, "stone"), L(0, 1, 5), B(1, 0, 5, "note_block"), B(2, 0, 5, "observer", facing="west"),
                  B(3, 0, 5, "sticky_piston", facing="east"), B(4, 0, 5, "stone")]
        _, look = self.lab(blocks, [0, 1, 5])
        self.assertIn("powered=true", look(1, 0, 5))
        self.assertEqual((look(4, 0, 5), look(5, 0, 5)), ("air", "stone"))     # one short pulse: block pushed and left
        # the note block passes no power on: a piston beside it stays put
        _, look = self.lab([B(0, 0, 5, "stone"), L(0, 1, 5), B(1, 0, 5, "note_block"), B(2, 0, 5, "piston", facing="east")], [0, 1, 5])
        self.assertIn("extended=false", look(2, 0, 5))

    def test_observer_chain(self):
        def fired_at(n):
            blocks = ([B(0, -1, 5, "stone"), L(0, 0, 5)] + [B(x, 0, 5, "observer", facing="west") for x in range(1, n + 1)]
                      + [B(n + 1, 0, 5, "piston", facing="east")])
            self.s.call("lab_new", {"blocks": blocks})
            self.s.call("lab_flip", {"pos": [0, 0, 5]})
            for c in self.s.call_full("lab_rest", {"limit": 0})["data"]["changes"]:
                if c[1:4] == [n + 1, 0, 5] and "extended=true" in c[5]:
                    return c[0]
        self.assertEqual((fired_at(1), fired_at(2), fired_at(3)), (2, 4, 6))

    def test_moved_observer_fires(self):
        blocks = [B(-2, 0, 5, "stone"), L(-2, 1, 5), B(-1, 0, 5, "piston", facing="east"), B(0, 0, 5, "observer", facing="up"),
                  B(1, -1, 5, "sticky_piston", facing="down"), B(1, -2, 5, "stone")]
        _, look = self.lab(blocks, [-2, 1, 5])
        self.assertIn("observer", look(1, 0, 5))
        self.assertEqual((look(1, -2, 5), look(1, -3, 5)), ("air", "stone"))   # the piston under the landing cell got one pulse

    def test_dust_connects_to_redstone_block_and_target(self):
        _, look = self.lab([B(0, -1, 5, "stone"), B(0, 0, 5, "redstone_wire"), B(1, 0, 5, "redstone_block"),
                            B(5, -1, 5, "stone"), B(5, 0, 5, "redstone_wire"), B(6, 0, 5, "target"),
                            B(9, -1, 5, "stone"), B(9, 0, 5, "redstone_wire"), B(10, 0, 5, "stone")])
        self.assertIn("east=side", look(0, 0, 5))
        self.assertIn("east=side", look(5, 0, 5))
        self.assertIn("east=none", look(9, 0, 5))     # a plain block: no connection, the dust is a dot

    def test_slime_in_a_frame_cell_drags_the_wall(self):
        blocks = [B(-3, 1, 0, "stone"), L(-3, 2, 0), B(-2, 1, 0, "piston", facing="east"), B(-1, 1, 0, "slime_block")]
        _, look = self.lab(blocks, [-3, 2, 0], walls=True)
        self.assertEqual(self.s.call_full("lab_look", {"cells": [[0, 1, 1]]})["data"]["blocks"][0][3], "stone")   # wall block now in the hallway

    def test_region_text_matches_the_validator(self):
        text = kit.brief(4, "seamless", {"test": 5, "sim": 9}, "cli", kit=2)
        self.assertIn("The build region is exactly -22 <= x <= 25, -22 <= y <= 25 and -24 <= z <= 23.", text)
        s = Session(self.k, 4, "seamless", self.tmp / "region.jsonl", kit=2)
        ok = s.call_full("lab_new", {"blocks": [B(25, 25, 23, "stone"), B(-22, -22, -24, "stone")]})
        self.assertIsNotNone(ok["data"])
        for bad in ([26, 0, 5], [0, -23, 5], [5, 5, 24]):
            self.assertIsNone(s.call_full("lab_new", {"blocks": [B(*bad, "stone")]})["data"], bad)

    def test_lever_may_sit_off_plane_and_is_not_counted(self):
        s = Session(self.k, 1, "open", self.tmp / "lever.jsonl", kit=2)
        # A stone beside the piston with the lever hung on its south face, so the lever is at z = 1.
        design = {"initial_state": "open", "blocks": [
            B(-3, 0, 0, "stone"), B(-3, 0, 1, "lever", face="wall", facing="south"),
            B(-2, 0, 0, "sticky_piston", facing="east"), B(-1, 0, 0, "stone")]}
        r = s.call_full("test", {"design": design})
        self.assertTrue(r["data"]["valid"], r["text"])
        self.assertEqual((r["data"]["volume"], r["data"]["dims"]), (4, [4, 1, 1]))     # one layer deep: the lever's cell is ignored

    # ---- the film
    def test_film_matches_trace_and_reconstructs(self):
        s = Session(self.k, 2, "seamless", self.tmp / "film.jsonl", kit=2)
        r = s.call_full("film", {"design": copy.deepcopy(GOOD), "flips": 2})
        film = r["data"]
        self.assertEqual(film["task"], {"width": 2, "height": 2, "track": "seamless"})
        self.assertEqual(film["start"]["doorway"], "../..")
        self.assertEqual(len(film["start"]["blocks"]), len(GOOD["blocks"]))          # walls left out
        self.assertEqual([f["lever"] for f in film["flips"]], ["on", "off"])
        f1 = film["flips"][0]
        self.assertEqual([t["t"] for t in f1["ticks"]], list(range(f1["last_change_tick"] + 1)))   # every tick listed
        self.assertEqual(f1["ticks"][-1]["doorway"], "##/##")
        self.assertTrue(f1["complete"] and f1["at_rest"])
        self.assertEqual(sum(len(t["changes"]) for t in f1["ticks"]), f1["changes_total"])
        # the same changes on the same ticks as trace prints
        trace = s.call("trace", {"design": copy.deepcopy(GOOD), "flips": 2, "limit": 100000})
        lines = [ln.strip() for ln in trace.split("flip 1")[1].split("flip 2")[0].splitlines() if ln.strip().startswith("t=")]
        mine = [f"t={t['t']} ({c[0]},{c[1]},{c[2]}) {c[3]} -> {c[4]}" for t in f1["ticks"] for c in t["changes"]]
        self.assertEqual(sorted(lines), sorted(mine))
        self.assertIn("flip 1 (lever on): at rest after tick", r["text"])
        self.assertNotIn("    t=", r["text"])                                        # the summary only
        # applying the changes to the start gives the world the lab reaches by the same flips
        world = {(b[0], b[1], b[2]): b[3] for b in film["start"]["blocks"]}
        for t in f1["ticks"]:
            for x, y, z, _, after in t["changes"]:
                world.pop((x, y, z), None) if after == "air" else world.__setitem__((x, y, z), after)
        lever = next(b["pos"] for b in GOOD["blocks"] if b["id"] == "lever")
        s.call("lab_new", {"blocks": GOOD["blocks"], "walls": True})    # the door's dust rests on wall blocks
        s.call("lab_flip", {"pos": lever})
        s.call("lab_rest", {})
        lab = {(b[0], b[1], b[2]): b[3] for b in s.call_full("lab_look", {})["data"]["blocks"]}
        lab.pop(tuple(lever)); world.pop(tuple(lever), None)                         # the flip's own change to the lever is not listed
        self.assertEqual(world, lab)
        log = [json.loads(ln) for ln in (self.tmp / "film.jsonl").read_text().splitlines()]
        self.assertEqual(log[0]["kit"], 2)
        self.assertEqual(sum(1 for e in log if e["kind"] == "film"), 1)
        self.assertEqual(s.used["sim"], 2)                                           # one film, one trace

    def test_film_reports_what_went_wrong(self):
        s = Session(self.k, 1, "open", self.tmp / "filmbad.jsonl", kit=2)
        film = s.call_full("film", {"design": copy.deepcopy(FIXTURES["bad_item_drop"]), "flips": 1})["data"]
        self.assertEqual(film["entity"]["type"], "minecraft:item")
        film = s.call_full("film", {"design": copy.deepcopy(FIXTURES["bad_pushes_wall"]), "flips": 1})["data"]
        self.assertIsNotNone(film["protected_cell"])
        self.assertIn("REJECTED", s.call("film", {"design": copy.deepcopy(FIXTURES["bad_command_block"])}))

    def test_detailed_test_data(self):
        s = Session(self.k, 1, "open", self.tmp / "detail.jsonl", kit=2)
        ok = s.call_full("test", {"design": copy.deepcopy(FIXTURES["good_1x1_open"])})["data"]
        self.assertEqual(ok["bbox"], {"min": [-3, -1, 0], "max": [0, 0, 0]})
        self.assertEqual([t["to"] for t in ok["timings"]][:2], ["closed", "open"])
        self.assertEqual(ok["detail"], [])
        bad = s.call_full("test", {"design": copy.deepcopy(FIXTURES["bad_nonsticky"])})["data"]
        self.assertEqual(bad["detail"][0]["code"], "did_not_open")
        self.assertIn("doorway_at_end", bad["detail"][0])
        self.assertNotIn("changes", bad["detail"][0])

    # ---- kit 1 is untouched
    def test_kit1_gate(self):
        s = Session(self.k, 1, "open", self.tmp / "kit1.jsonl")
        self.assertEqual(s.call("film", {"design": copy.deepcopy(FIXTURES["good_1x1_open"])}), "unknown tool 'film'")
        data = s.call_full("test", {"design": copy.deepcopy(FIXTURES["good_1x1_open"])})["data"]
        self.assertNotIn("detail", data)
        self.assertNotIn("kit", json.loads((self.tmp / "kit1.jsonl").read_text().splitlines()[0]))
        budget = {"test": 5, "sim": 9}
        one = kit.brief(3, "seamless", budget, "cli")
        self.assertNotIn("film", one)
        self.assertNotIn("More facts", one)
        two = kit.brief(3, "seamless", budget, "cli", kit=2)
        for phrase in ("./pd film design.json", "### The film", "f.at(flip, t)", "r.detail", "More facts, added after earlier runs",
                       "An observer that a piston moves emits one pulse when it lands.", "importlib.reload"):
            self.assertIn(phrase, two)
        self.assertEqual(kit.brief(3, "seamless", budget, "tools", kit=2).count("More facts"), 1)   # tools interface: facts only
        self.assertNotIn("film", kit.brief(3, "seamless", budget, "tools", kit=2))
        changed = kit.brief(3, "seamless", budget, "cli", kit=2, physics={"observer_delay": 3})
        self.assertIn("each one adds 3 ticks", changed)
        out = kit.make_kit(self.tmp / "k1", 1, "open", "http://127.0.0.1:1", budget)
        self.assertNotIn("film", (out / "pd").read_text() + (out / "pdlab.py").read_text())


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Kit2ClientTests(unittest.TestCase):
    """The kit-2 folder as an agent uses it: `./pd film` and the Film class through `./pd py`."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.kit = cls.tmp / "kit"
        port = free_port()
        cls.server = subprocess.Popen(
            [sys.executable, "-m", "pdgrader", "serve", "--n", "2", "--track", "seamless", "--port", str(port), "--kit-version", "2",
             "--log", str(cls.tmp / "log.jsonl"), "--kit", str(cls.kit), "--minutes", "30"],
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
        (cls.kit / "door.json").write_text(json.dumps(GOOD))

    @classmethod
    def tearDownClass(cls):
        subprocess.run(["./pd", "py", "--reset"], cwd=cls.kit, capture_output=True)
        cls.server.terminate()
        cls.server.wait(timeout=30)
        cls.server.stdout.close()

    def pd(self, *args, stdin=None):
        r = subprocess.run(["./pd", *map(str, args)], cwd=self.kit, input=stdin, capture_output=True, text=True, timeout=120)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout + r.stderr

    def test_film_command(self):
        out = self.pd("film", "door.json", "--flips", 3)
        self.assertIn("wrote door.film.json", out)
        self.assertIn("flip 3 (lever on)", out)
        self.assertIn("[time left:", out)
        film = json.loads((self.kit / "door.film.json").read_text())
        self.assertEqual(len(film["flips"]), 3)
        self.pd("film", "door.json", "--out", "x.json")
        self.assertEqual(len(json.loads((self.kit / "x.json").read_text())["flips"]), 2)

    def test_film_in_python(self):
        out = self.pd("py", stdin="""
f = film("door.json", flips=2)
print("flips", f.flips, "ok", f.ok)
print("doorway", f.doorway(1))
print("end", f.doorway(1, 999), f.doorway(2, 999))
print("first", f.first(1, "sticky_piston[extended=true"))
print("cell", f.cell(0, 0, 0))
print("at0", f.at(0, 0) == f.start(), f.at(1, 999).get((0, 0, 0)), f.at(2, 999).get((0, 0, 0), "air"))
print("mid", f.at(1, 1).get((0, 0, 0)))
f.save("saved.json"); print("loaded", Film.load("saved.json").last_tick(1) == f.last_tick(1))
r = test("door.json"); print("test", r.valid, r.volume, r.bbox, len(r.timings), r.detail)
""")
        self.assertIn("flips 2 ok True", out)
        self.assertIn("doorway [(0, '../..'), (1, 'mm/mm'), (3, '##/##')]", out)
        self.assertIn("end ##/## ../..", out)
        self.assertIn("first (1, (-2, 0, 0), 'sticky_piston[extended=false,facing=east]', 'sticky_piston[extended=true,facing=east]')", out)
        self.assertIn("cell [(0, 0, 'air'), (1, 1, 'moving_piston[facing=east,type=normal]'), (1, 3, 'stone')", out)
        self.assertIn("at0 True stone air", out)
        self.assertIn("mid moving_piston[facing=east,type=normal]", out)
        self.assertIn("loaded True", out)
        self.assertIn("test True 110 {'min': [-5, -1, 0], 'max': [5, 3, 1]} 6 []", out)


if __name__ == "__main__":
    unittest.main()
