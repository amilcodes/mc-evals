#!/usr/bin/env python3
"""Generates the reference ("oracle") 3x3 seamless piston door: oracle_3x3.json.

    python3 oracles/make_oracle.py            # writes oracles/oracle_3x3.json
    python3 -m pdgrader grade oracles/oracle_3x3.json --n 3 --track seamless --final --translations

Coordinates: doorway cells are (x, y, 0) for x, y in 0..2; +x east, +y up, +z south.
Lever on = door closed. See NOTES.md for how it works and the measured timing.

Parts (names used in the comments below):
  easy cells  eight sticky pistons that simply follow the lever: left/right columns, bottom middle
  S_a, S_b    the two stones of the middle column's top two cells; S_a rests at (1,3,0), S_b at (0,3,0)
  B, F        double piston extender above the middle column (B on top pushes F; F handles the stones)
  P           feeder piston that slides S_b sideways under F
  L           the lever line                       G   L delayed by 40 ticks (both edges)
  X           2-tick trigger pulses (observers)    T   the pulse train: B on, F pulse, B off, F pulse
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from pdgrader import rules  # only for in_shell(): never place a support inside the harness's tube

N = 3


class Build:
    def __init__(self):
        self.blocks = {}

    def set(self, x, y, z, block, **props):
        assert (x, y, z) not in self.blocks, f"two blocks at {(x, y, z)}"
        assert not rules.in_shell(N, (x, y, z)) and not rules.in_hallway(N, (x, y, z)), (x, y, z)
        self.blocks[(x, y, z)] = (block, {k: str(v).lower() for k, v in props.items()})

    def support(self, x, y, z, block="stone"):
        """A block under (x, y, z), unless the hallway wall is already there or one was placed."""
        p = (x, y - 1, z)
        if not rules.in_shell(N, p) and p not in self.blocks:
            self.set(*p, block)

    def wire(self, x, y, z, under="stone"):
        self.support(x, y, z, under)
        self.set(x, y, z, "redstone_wire")

    def rep(self, x, y, z, facing, delay, powered=False):
        """Repeater. `facing` is the side its input comes from; output leaves the opposite side."""
        self.support(x, y, z)
        self.set(x, y, z, "repeater", facing=facing, delay=delay, **({"powered": "true"} if powered else {}))

    def to_json(self, initial_state="open"):
        out = []
        for (x, y, z), (block, props) in sorted(self.blocks.items()):
            b = {"pos": [x, y, z], "id": block}
            if props:
                b["props"] = props
            out.append(b)
        return {"initial_state": initial_state, "blocks": out}


def easy_cells(d):
    """Eight cells that just follow the lever, the frame, the lever, and the L bus with its two risers."""
    for y in range(3):
        d.set(-2, y, 0, "sticky_piston", facing="east")
        d.set(-1, y, 0, "stone")                      # left frame column = left door stones
        d.set(4, y, 0, "sticky_piston", facing="west")
        d.set(3, y, 0, "stone")                       # right frame column = right door stones
    d.set(1, -2, 0, "sticky_piston", facing="up")
    for x in range(3):
        d.set(x, -1, 0, "stone")                      # bottom frame; the middle one is a door stone
    # The lever hangs on a block under the hallway floor. That block powers the bottom piston
    # (it is next to it) and the bus dust on both sides of it.
    d.set(1, -2, -1, "stone")
    d.set(1, -2, -2, "lever", face="wall", facing="north")
    for sgn in (-1, 1):
        X = lambda k: 1 + sgn * k                     # k cells outward from x = 1
        for k in range(1, 6):
            d.wire(X(k), -2, -1)                      # bus under the floor, z = -1
        # Riser: dust zigzagging up on glass (glass does not cut the diagonal links), 2 wide, no delay.
        d.wire(X(6), -1, -1, "glass")
        d.wire(X(5), 0, -1, "glass")
        d.wire(X(6), 1, -1, "glass")
        d.wire(X(5), 2, -1, "glass")
        d.wire(X(5), 2, 0)                            # step into the door plane
        # Dust on the block beside the middle piston, pointing into the top piston. The top piston
        # is powered by the dust, the middle one by the block under the dust, and the bottom one by
        # quasi-connectivity from that same block (it is updated when the middle piston moves).
        d.wire(X(4), 2, 0)


def centre_column(d):
    d.set(1, 5, 0, "sticky_piston", facing="down")    # B
    d.set(1, 4, 0, "sticky_piston", facing="down")    # F
    d.set(1, 3, 0, "stone")                           # S_a (frame cell while open)
    d.set(-1, 3, 0, "sticky_piston", facing="east")   # P
    d.set(0, 3, 0, "stone")                           # S_b (frame cell while open)
    d.set(2, 3, 0, "stone")                           # frame


def lower_deck(d):
    """Level logic at y = 4 (on blocks at y = 3; over x = 0..2 the hallway roof is the floor)."""
    # L from the top of the right riser up two steps onto the deck.
    d.wire(6, 2, 1)
    d.wire(6, 3, 2)
    d.wire(6, 4, 3)
    # G = L delayed 40 ticks: five 4-tick repeaters in a row.
    for z in range(4, 9):
        d.rep(6, 4, z, "north", 4)
    for x in (6, 5, 4, 3):
        d.wire(x, 4, 9)
    for z in range(4, 9):
        d.wire(3, 4, z)
    for x in (2, 1, 0, -1, -2, -3):
        d.wire(x, 4, 7)
    # F line. M_F is the merge point: F_hold comes in through rep_F, the T pulses come from O3 above.
    # Two 1-tick repeaters then lead to the dust at (1,4,1). That dust points north into F at
    # (1,4,0) and powers the roof stone (1,3,1) under it, which powers F when B has pushed it to (1,3,0).
    d.rep(2, 4, 4, "east", 1)                         # rep_F: G -> M_F (also keeps the pulses out of G)
    d.wire(1, 4, 4)                                   # M_F
    d.rep(1, 4, 3, "south", 1)
    d.rep(1, 4, 2, "south", 1)
    d.wire(1, 4, 1)
    # Placed already powered with nothing behind it: it switches off for good 8 ticks after
    # placement. Until then it locks the repeater beside it, which swallows O3's placement pulse.
    d.rep(2, 4, 3, "east", 4, powered=True)
    # P line: P_hold = G delayed 2 ticks OR G delayed 10 ticks, so it rises before F_hold and
    # falls after it. Both repeaters feed the same dust cell, so the level O2 sees never changes
    # while the two overlap.
    for z in range(1, 6):
        d.wire(-1, 4, z)                              # trunk; (-1,4,1) sits on the block beside P
    d.rep(-1, 4, 6, "south", 1)                       # short branch
    d.rep(-3, 4, 6, "south", 4)                       # long branch, first half
    d.wire(-3, 4, 5)
    d.rep(-2, 4, 5, "west", 1)                        # long branch, second half


def upper_deck(d):
    """The T generator at y = 6 (on blocks at y = 5), linked to the lower deck by vertical observers."""
    d.set(6, 5, 3, "observer", facing="down")         # O1: watches L, pulses X (above it)
    d.set(-1, 5, 2, "observer", facing="down")        # O2: watches P_hold, pulses X
    d.set(1, 5, 4, "observer", facing="up")           # O3: watches the B line, pulses M_F (below it)
    # B line: dust on the block beside B.
    d.set(1, 5, 1, "stone")
    d.wire(1, 6, 1)
    d.wire(1, 6, 2)
    d.wire(1, 6, 3)
    d.set(1, 6, 4, "redstone_wire")                   # on top of O3
    d.wire(1, 6, 5)                                   # J: both stretcher outputs feed this one cell
    # Pulse stretcher: X (2 ticks) -> 8 ticks at N0 -> [N0 + 2, N0 + 10) OR [N0 + 8, N0 + 16) = 14 ticks.
    d.rep(1, 6, 6, "south", 1)
    d.rep(2, 6, 5, "east", 4)
    for x, z in ((1, 7), (2, 7), (3, 7), (3, 6), (3, 5)):
        d.wire(x, 6, z)                               # N0
    d.rep(2, 6, 8, "south", 4)                        # X -> N0
    d.rep(3, 6, 8, "east", 4, powered=True)           # lock for the first 8 ticks: swallows O1/O2's placement pulse
    # X: from the top of O1 and of O2 to the stretcher input.
    for x in range(-1, 7):
        d.wire(x, 6, 9)
    for z in range(3, 9):
        d.wire(-1, 6, z)
    for z in range(4, 9):
        d.wire(6, 6, z)
    d.set(-1, 6, 2, "redstone_wire")                  # on top of O2
    d.set(6, 6, 3, "redstone_wire")                   # on top of O1


def oracle():
    d = Build()
    easy_cells(d)
    centre_column(d)
    lower_deck(d)
    upper_deck(d)
    return d.to_json("open")


def save(design, path):
    with open(path, "w") as f:
        f.write('{"initial_state": ' + json.dumps(design["initial_state"]) + ',\n "blocks": [\n  ')
        f.write(",\n  ".join(json.dumps(b) for b in design["blocks"]) + "\n ]}\n")
    return path


if __name__ == "__main__":
    print("wrote", save(oracle(), HERE / "oracle_3x3.json"))
    try:
        from make_oracle_small import small
        print("wrote", save(small(), HERE / "oracle_3x3_small.json"))
    except ImportError:
        pass
