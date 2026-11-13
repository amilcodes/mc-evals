"""The test tools and the lab, from Python.

    from pdbuild import Design
    from pdlab import Lab, test, trace, view, submit, status

    lab = Lab(part)            # empty the lab world, place the part, clock at 0
    lab.flip(0, 6, 0)          # flip the lever at that position; no tick passes
    lab.step(3)                # advance exactly 3 game ticks
    lab.block(3, 5, 0)         # -> "stone"

    r = test(design)           # r.valid, r.volume, r.failures; print(r) shows the usual report

Everything here talks to the same tool server as `./pd`, so the same budgets apply.
A refused call (rejected blocks, no budget left, no lever at that position) raises PdError.
"""
import json
import os
import urllib.request
from pathlib import Path

from pdbuild import Design

__all__ = ["Design", "Lab", "PdError", "TestResult", "test", "trace", "view", "submit", "status", "blocks"]

_HERE = Path(__file__).resolve().parent


class PdError(Exception):
    """The tool server refused the call. The message is the server's own text."""


def _server():
    url = os.environ.get("PD_SERVER")
    if not url and (_HERE / ".pd_server").exists():
        url = (_HERE / ".pd_server").read_text().strip()
    if not url:
        raise PdError("no tool server configured (set PD_SERVER or create .pd_server)")
    return url


def call(tool, **args):
    """One tool call. Returns (text, data); data is None when the server has only text to give."""
    req = urllib.request.Request(_server(), data=json.dumps({"tool": tool, "args": args}).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            reply = json.loads(r.read())
    except OSError as e:
        raise PdError(f"cannot reach the tool server at {_server()}: {e}") from None
    return reply["text"], reply.get("data")


def _design(d):
    """A design as the server wants it: from a Design, a dict, or the path of a JSON file."""
    if isinstance(d, Design):
        return d.to_json()
    if isinstance(d, dict):
        return d
    if isinstance(d, (str, Path)):
        return json.loads(Path(d).read_text())
    raise TypeError("expected a Design, a design dict, or the path of a design file")


def _part(p):
    """A list of blocks for the lab: from a Design, a design dict, a list of blocks, or a file path."""
    if isinstance(p, list):
        return p
    return _design(p)["blocks"]


class TestResult:
    """What `test` reported.

    valid      True if the design passed.
    rejected   True if it was rejected before simulation (free; no test call used).
    refused    True if no test calls were left.
    volume     Bounding-box volume, or None if nothing was simulated.
    dims       [width, height, depth], or None.
    failures   Failure codes, e.g. ["did_not_open"]. Empty when valid, rejected or refused.
    open_ticks, close_ticks   Slowest open and close, when valid.
    text       The full report, as `./pd test` prints it.

    The object is truthy exactly when the design is valid.
    """

    def __init__(self, text, data):
        data = data or {}
        self.text = text
        self.valid = bool(data.get("valid"))
        self.rejected = bool(data.get("rejected"))
        self.refused = bool(data.get("refused"))
        self.volume = data.get("volume")
        self.dims = data.get("dims")
        self.failures = list(data.get("failures") or [])
        self.open_ticks = data.get("open_ticks")
        self.close_ticks = data.get("close_ticks")

    def __bool__(self):
        return self.valid

    def __repr__(self):
        return self.text


def test(design):
    """The full test (uses one test call unless the design is rejected first). Returns a TestResult."""
    return TestResult(*call("test", design=_design(design)))


def trace(design, flips=2, ticks=None, grep=None, limit=80):
    """Every block change after placement and each flip, as text (uses one trace/view call)."""
    return call("trace", design=_design(design), flips=flips, ticks=ticks, grep=grep, limit=limit)[0]


def view(design, flips=0, z=None):
    """ASCII picture of the build, as text (uses one trace/view call)."""
    return call("view", design=_design(design), flips=flips, z=z)[0]


def submit(design):
    """Nominate a design for final scoring; the last submit counts. Returns the server's text."""
    return call("submit", design=_design(design))[0]


def status():
    return call("status")[0]


def blocks():
    return call("blocks")[0]


class Lab:
    """A free-form world for trying out parts. See TASK.md, "The lab", for the exact rules.

    There is one lab world. Creating a Lab empties it, so an older Lab object stops working
    (its calls raise PdError).

    A block change is a tuple (t, (x, y, z), before, after), with block states written as in
    trace output, e.g. "sticky_piston[extended=true,facing=east]"; an empty cell is "air".
    """

    def __init__(self, part, walls=False):
        text, data = call("lab_new", blocks=_part(part), walls=bool(walls))
        if data is None:
            raise PdError(text)
        self.id = data["lab"]
        self.t = 0                    # the lab clock: game ticks since this lab was started
        self.walls = bool(walls)
        self.lost = [tuple(p) for p in data["lost"]]   # blocks that could not exist where they were put
        self.history = []             # every change reported so far, in order
        self.entity = None            # (t, type) of the first entity that appeared, if any
        self.ticks_left = None        # lab tick budget left, known after the first step or rest

    def _do(self, tool, **args):
        text, data = call(tool, lab=self.id, **args)
        if data is None:
            raise PdError(text)
        return data

    def _ran(self, data):
        self.t = data["t"]
        self.ticks_left = data["ticks_left"]
        if data["entity"] and self.entity is None:
            self.entity = (data["entity"]["t"], data["entity"]["type"])
        if data["changes_total"] > len(data["changes"]):
            raise PdError(f"{data['changes_total']} blocks changed in one call but only {len(data['changes'])} "
                          "could be reported; history is incomplete. Advance fewer ticks per call.")
        return self._changes(data)

    def _changes(self, data):
        out = [(c[0], (c[1], c[2], c[3]), c[4], c[5]) for c in data["changes"]]
        self.history += out
        return out

    def flip(self, x, y, z):
        """Flip the lever at (x, y, z). No tick passes. Returns the changes made at that instant."""
        return self._changes(self._do("lab_flip", pos=[x, y, z]))

    def step(self, ticks=1):
        """Advance exactly `ticks` game ticks (1 to 2000). Returns the changes, in order."""
        return self._ran(self._do("lab_step", ticks=ticks, limit=0))

    def rest(self, max_ticks=200):
        """Advance until no block has changed for 20 ticks in a row, or for max_ticks.

        Returns True if it came to rest. The clock then stands 20 ticks after the last change.
        """
        data = self._do("lab_rest", max_ticks=max_ticks, limit=0)
        self._ran(data)
        return data["at_rest"]

    def blocks(self):
        """{(x, y, z): state} for every non-air cell (hallway walls left out). No tick passes."""
        return {(b[0], b[1], b[2]): b[3] for b in self._do("lab_look")["blocks"]}

    def block(self, x, y, z):
        """The state of one cell, "air" if empty. No tick passes."""
        return self._do("lab_look", cells=[[x, y, z]])["blocks"][0][3]

    def doorway(self):
        """The doorway as rows, top row first, e.g. "###/#.#/###": # stone, . air, m moving, ? other."""
        return self._do("lab_look", cells=[])["doorway"]

    def view(self, z=None):
        """ASCII picture of the lab as it is now, as text. No tick passes."""
        text, _ = call("lab_view", lab=self.id, z=z)
        if not text.startswith("Lab at t="):
            raise PdError(text)
        return text

    def timeline(self, x, y, z):
        """[(t, state), ...]: each state the cell took, from the changes reported so far."""
        return [(t, after) for t, pos, _, after in self.history if pos == (x, y, z)]

    def __repr__(self):
        return f"<Lab {self.id} at t={self.t}>"
