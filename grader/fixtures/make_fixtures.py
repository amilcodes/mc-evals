#!/usr/bin/env python3
"""Writes the grader's test fixtures as submission JSON files next to this script.

These are hand-built doors for testing the grader. They are not compact and are not
community designs. Coordinates: doorway cells are (x, y, 0) for 0 <= x < w, 0 <= y < h (w = h = n for square doors).
"""
import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def B(x, y, z, block, **props):
    b = {"pos": [x, y, z], "id": block}
    if props:
        b["props"] = props
    return b


def stone(*cells):
    return [B(x, y, z, "stone") for x, y, z in cells]


def dust(*cells):
    return [B(x, y, z, "redstone_wire") for x, y, z in cells]


# ---- 1x1: lever beside one sticky piston that pushes one stone block into the doorway.
ONE = [
    B(-3, -1, 0, "stone"),
    B(-3, 0, 0, "lever", face="floor", facing="north"),
    B(-2, 0, 0, "sticky_piston", facing="east"),
    B(-1, 0, 0, "stone"),
]
ONE_RING = stone((1, 0, 0), (0, -1, 0), (0, 1, 0))

# ---- 2x2: two sticky pistons each side. Lever off = open.
# Each side: dust pointing into the upper piston, sitting on a block beside the lower piston
# (dust powers the block under it). A dust line one layer back (z = 1) carries the signal
# over the hallway roof to the other side.
TWO = (
    [B(-2, y, 0, "sticky_piston", facing="east") for y in (0, 1)]
    + [B(3, y, 0, "sticky_piston", facing="west") for y in (0, 1)]
    + stone((-1, 0, 0), (-1, 1, 0), (2, 0, 0), (2, 1, 0))          # door blocks, retracted
    + stone((0, -1, 0), (1, -1, 0), (0, 2, 0), (1, 2, 0))          # frame above and below the doorway
    + stone((-3, 0, 0), (-4, 0, 0), (-5, 0, 0)) + dust((-3, 1, 0), (-4, 1, 0))
    + [B(-5, 1, 0, "lever", face="floor", facing="north")]
    + stone((-3, 2, 0), (4, 2, 0))                                  # stop the bus dust linking down to the piston dust
    + stone((4, 0, 0), (5, 0, 0)) + dust((4, 1, 0), (5, 1, 0))
    # bus at z = 1: up the left, across the roof (two of its supports are hallway wall), down the right
    + stone((-4, 0, 1), (-3, 1, 1), (-2, 2, 1), (-1, 2, 1), (2, 2, 1), (3, 2, 1), (4, 1, 1), (5, 0, 1))
    + dust((-4, 1, 1), (-3, 2, 1), (-2, 3, 1), (-1, 3, 1), (0, 3, 1), (1, 3, 1), (2, 3, 1), (3, 3, 1), (4, 2, 1), (5, 1, 1))
)

# ---- 2 wide x 1 tall: two sticky pistons above the doorway push their blocks down. Dust on the
# blocks above the pistons powers them; lever off = open.
TWO_BY_ONE = (
    [B(x, 2, 0, "sticky_piston", facing="down") for x in (0, 1)]
    + stone((0, 1, 0), (1, 1, 0))                                   # door blocks, retracted
    + stone((-1, 0, 0), (2, 0, 0), (0, -1, 0), (1, -1, 0))          # frame beside and below the doorway
    + stone((0, 3, 0), (1, 3, 0), (-1, 3, 0)) + dust((0, 4, 0), (1, 4, 0))
    + [B(-1, 4, 0, "lever", face="floor", facing="north")]
)

# ---- 1 wide x 2 tall: the left half of the 2x2.
ONE_BY_TWO = (
    [B(-2, y, 0, "sticky_piston", facing="east") for y in (0, 1)]
    + stone((-1, 0, 0), (-1, 1, 0))
    + stone((1, 0, 0), (1, 1, 0), (0, -1, 0), (0, 2, 0))
    + stone((-3, 0, 0), (-4, 0, 0), (-5, 0, 0)) + dust((-3, 1, 0), (-4, 1, 0))
    + [B(-5, 1, 0, "lever", face="floor", facing="north")] + stone((-3, 2, 0))
)


def sub(blocks, state="open"):
    return {"initial_state": state, "blocks": copy.deepcopy(blocks)}


def swap(blocks, pos, **changes):
    out = copy.deepcopy(blocks)
    for b in out:
        if b["pos"] == list(pos):
            b.update(changes)
    return out


FIXTURES = {
    # known-good
    "good_1x1_open": sub(ONE),
    "good_1x1_seamless": sub(ONE + ONE_RING),
    "good_2x2": sub(TWO),
    "good_2x1": sub(TWO_BY_ONE),
    "good_1x2": sub(ONE_BY_TWO),
    # known-bad: rejected before simulation
    "bad_command_block": sub(ONE + [B(-3, 1, 0, "command_block")]),
    "bad_two_levers": sub(ONE + [B(-4, 0, 0, "lever", face="floor", facing="north"), B(-4, -1, 0, "stone")]),
    "bad_hallway_block": sub(ONE + [B(0, 0, 1, "stone")]),
    "bad_wall_cell": sub(ONE + [B(-1, 0, 1, "stone")]),
    "bad_headless_piston": sub(swap(ONE, (-2, 0, 0), props={"facing": "east", "extended": "true"})),
    "bad_property": sub(swap(ONE, (-2, 0, 0), props={"facing": "sideways"})),
    "bad_moving_piston": sub(ONE + [B(-3, 1, 0, "moving_piston")]),
    # declared closed with an empty doorway
    "bad_declared_closed": sub(ONE, "closed"),
    # known-bad: fail in simulation
    # declared open, but a redstone block powers the piston, so it closes as soon as it is placed
    "bad_starts_powered": sub(ONE + [B(-2, 1, 0, "redstone_block")]),
    "bad_nonsticky": sub(swap(ONE, (-2, 0, 0), id="piston")),
    "bad_item_drop": sub(ONE + [B(-1, 1, 0, "redstone_wire")]),
    # a second piston one layer back shoves a hallway wall block into the hallway
    "bad_pushes_wall": sub(ONE + [B(-3, 0, 1, "sticky_piston", facing="east"), B(-2, 0, 1, "stone")]),
    # runs forever: a torch on a block that its own output, delayed by a repeater, switches off
    "bad_clock": sub(ONE + [
        B(-8, 0, 0, "stone"), B(-9, 0, 0, "redstone_wall_torch", facing="west"),
        B(-9, -1, 1, "stone"), B(-9, -1, 2, "stone"), B(-8, -1, 2, "stone"), B(-8, -1, 1, "stone"),
        B(-9, 0, 1, "redstone_wire"), B(-9, 0, 2, "redstone_wire"), B(-8, 0, 2, "redstone_wire"),
        B(-8, 0, 1, "repeater", facing="south", delay="4"),
    ]),
    # two observers watching each other: inert, because observers do not fire merely for being placed
    "good_idle_observers": sub(ONE + [B(-6, 0, 0, "observer", facing="east"), B(-5, 0, 0, "observer", facing="west")]),
    # Not a door. A lever flip makes an observer give a sticky piston a short pulse, so the piston
    # leaves its block behind on one flip and fetches it on the next. Used by the parity check to
    # exercise observer timing and short-pulse piston behaviour.
    "probe_short_pulse": sub([
        B(-5, -1, 0, "stone"), B(-5, 0, 0, "lever", face="floor", facing="north"),
        B(-4, 0, 0, "observer", facing="west"), B(-3, 0, 0, "sticky_piston", facing="east"), B(-2, 0, 0, "stone"),
    ]),
}

if __name__ == "__main__":
    for name, s in FIXTURES.items():
        (HERE / f"{name}.json").write_text(json.dumps(s, indent=1))
    print(f"wrote {len(FIXTURES)} fixtures")
