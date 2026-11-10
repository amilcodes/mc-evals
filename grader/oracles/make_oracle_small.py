#!/usr/bin/env python3
"""Compacted variant of the oracle (same mechanism, see make_oracle.py and NOTES.md): oracle_3x3_small.json.

Differences from the big one:
  * everything is at z >= 0 and x in -2..4: the side columns are fed from the south (dust at
    (-2,2,1) / (4,2,1) pointing north into the top piston), the bus runs under the floor at z = 2;
  * O3 sits directly between the B dust (above it) and the F dust (below it), so the T pulses reach
    F with no repeater, and B is powered by quasi-connectivity from the dust pointing into the cell above it;
  * B's pulse is then only 8 ticks (one repeater), T takes 24 ticks, and G is L delayed by 24;
  * the placement pulse of O3 is covered by placing rep_F powered (F does one harmless full stroke).
"""
from make_oracle import Build, save, HERE


def easy_cells(d):
    for y in range(3):
        d.set(-2, y, 0, "sticky_piston", facing="east")
        d.set(-1, y, 0, "stone")
        d.set(4, y, 0, "sticky_piston", facing="west")
        d.set(3, y, 0, "stone")
    d.set(1, -2, 0, "sticky_piston", facing="up")
    for x in range(3):
        d.set(x, -1, 0, "stone")
    # Lever block south of the bottom piston; the lever hangs under it.
    d.set(1, -2, 1, "stone")
    d.set(1, -3, 1, "lever", face="ceiling", facing="north")
    for x in range(-2, 5):
        d.wire(x, -2, 2)                               # bus under the floor at z = 2
    for x in (-2, 4):
        # riser: glass zigzag between z = 2 and z = 3
        d.wire(x, -1, 3)
        d.wire(x, 0, 2, "glass")
        d.wire(x, 1, 3, "glass")
        d.wire(x, 2, 2, "glass")
        # dust on the block south of the middle piston, pointing north into the top piston
        d.wire(x, 2, 1)
    # the right riser goes on up to the lower deck: L arrives at (4,4,2)
    d.wire(4, 3, 3, "glass")
    d.wire(4, 4, 2, "glass")


def centre_column(d):
    d.set(1, 5, 0, "sticky_piston", facing="down")    # B
    d.set(1, 4, 0, "sticky_piston", facing="down")    # F
    d.set(1, 3, 0, "stone")                           # S_a
    d.set(-1, 3, 0, "sticky_piston", facing="east")   # P
    d.set(0, 3, 0, "stone")                           # S_b
    d.set(2, 3, 0, "stone")                           # frame


def lower_deck(d, dF=3):
    d.wire(3, 4, 2)                                   # L
    d.rep(3, 4, 3, "north", 4)                        # c1
    d.rep(3, 4, 4, "north", 4)                        # c2
    d.wire(3, 4, 5)
    d.rep(2, 4, 5, "east", 4)                         # c3 -> G
    for z in (3, 4, 5):
        d.wire(1, 4, z)                               # G = L + 24
    d.rep(1, 4, 2, "south", dF, powered=True)         # rep_F (placed on: holds F out over O3's placement pulse)
    d.wire(1, 4, 1)                                   # F dust
    for z in (1, 2, 3):
        d.wire(-1, 4, z)                              # P dust; (-1,4,3) is where both feeds arrive
    d.rep(0, 4, 3, "east", 1)                         # short feed: G + 2
    d.rep(0, 4, 5, "east", 4)                         # long feed: G + 8 ...
    d.wire(-1, 4, 5)
    d.rep(-1, 4, 4, "south", 1)                       # ... + 2


def upper_deck(d):
    d.set(3, 5, 2, "observer", facing="down")         # O1 watches L
    d.set(-1, 5, 3, "observer", facing="down")        # O2 watches P_hold
    d.set(1, 5, 1, "observer", facing="up")           # O3 watches the B dust, pulses the F dust under it
    d.set(1, 6, 1, "redstone_wire")                   # B dust on O3: points north into the cell above B
    d.rep(1, 6, 2, "south", 4)                        # X -> B, stretched to 8 ticks
    d.rep(0, 6, 2, "west", 4, powered=True)           # lock for the first 8 ticks
    d.set(-1, 6, 3, "redstone_wire")                  # X, on O2
    for x in (0, 1, 2, 3):
        d.wire(x, 6, 3)
    d.set(3, 6, 2, "redstone_wire")                   # X, on O1


def small(dF=3):
    d = Build()
    easy_cells(d)
    centre_column(d)
    lower_deck(d, dF)
    upper_deck(d)
    return d.to_json("open")


if __name__ == "__main__":
    print("wrote", save(small(), HERE / "oracle_3x3_small.json"))
