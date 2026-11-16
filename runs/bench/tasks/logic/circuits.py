"""Reference circuits for the timing / sequential-logic family (vanilla 26.3 physics).

Every circuit shares one harness: a wall lever at (-1, 1, 0) on a stone block at (0, 1, 0) (input A),
and one output note block Q whose `powered` state is the output. Builds carry their own support
blocks (floor at y = 0). Repeater/comparator `facing` points at the input side.
"""
from lib import block as B


def harness(q):
    return {"inputs": {"A": {"lever": [-1, 1, 0], "support": [0, 1, 0], "facing": "west"}},
            "outputs": {"Q": {"pos": list(q), "block": "note_block"}}}


def floor(cells):
    return [B((x, 0, z), "stone") for x, z in cells]


def toggles(gaps, tail):
    """Lever events at cumulative gap sums; returns (inputs, end)."""
    t, ev = 0, []
    for g in gaps:
        t += g
        ev.append({"t": t, "lever": "A"})
    return ev, t + tail


def dust(x, z):
    return B((x, 1, z), "redstone_wire")


def rep(x, z, facing, delay):
    return B((x, 1, z), "repeater", facing=facing, delay=delay)


def comp(x, z, facing, mode="compare"):
    return B((x, 1, z), "comparator", facing=facing, mode=mode)


def obs(x, z, facing):
    return B((x, 1, z), "observer", facing=facing)


CIRCUITS = {}


def circuit(name, title, q, blocks, gaps, tail, notes):
    CIRCUITS[name] = {"name": name, "title": title, "harness": harness(q), "build": blocks,
                      "schedule": toggles(gaps, tail), "notes": notes}


# 1. Repeater delay line, 16 game ticks both edges: dust, R3, dust, R3, dust, R2 -> Q.
circuit("delay16", "Repeater delay line (16 game ticks)", (7, 1, 0),
        [dust(1, 0), rep(2, 0, "west", 3), dust(3, 0), rep(4, 0, "west", 3), dust(5, 0), rep(6, 0, "west", 2)]
        + floor([(x, 0) for x in range(1, 7)]),
        [10, 37, 41, 29, 45, 33], 40,
        "Q follows the lever 16 game ticks later on both edges (repeaters 3+3+2 = 6+6+4 gt).")

# 2. Short delay line, 12 game ticks: R4 then R2.
circuit("delay12", "Repeater delay line (12 game ticks)", (4, 1, 0),
        [dust(1, 0), rep(2, 0, "west", 4), rep(3, 0, "west", 2)] + floor([(1, 0), (2, 0), (3, 0)]),
        [10, 31, 37, 23, 43, 29], 40,
        "Q follows the lever 12 game ticks later on both edges (repeaters 4+2 = 8+4 gt).")

# 3. Pulse extender: a direct dust path ORed with a slow repeater path, both weakly powering Q (dust),
#    so the conductive note block cannot feed back into the direct path.
circuit("extender", "Pulse extender (+12 game ticks on the falling edge)", (4, 1, 0),
        [dust(1, 0), dust(2, 0), dust(3, 0), dust(1, 1), dust(1, 2), rep(2, 2, "west", 4), rep(3, 2, "west", 2),
         dust(4, 2), dust(4, 1)]
        + floor([(1, 0), (2, 0), (3, 0), (1, 1), (1, 2), (2, 2), (3, 2), (4, 2), (4, 1)]),
        [10, 37, 41, 29, 45, 33], 40,
        "Q turns on with the lever and turns off 12 game ticks after it (slow path 8+4 gt).")

# 4. Rising-edge monostable: comparator rear = input via dust (14), side = input via a repeater (15).
circuit("rise_mono", "Rising-edge monostable (pulse limiter)", (4, 1, 0),
        [dust(1, 0), dust(2, 0), comp(3, 0, "west"), dust(1, 1), rep(2, 1, "west", 2), dust(3, 1)]
        + floor([(1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (3, 1)]),
        [10, 37, 41, 29, 45, 33], 40,
        "On each lever-on, Q gives one short pulse (comparator 2 gt, side repeater 4 gt); lever-off does nothing.")

# 5. Falling-edge monostable: comparator (subtract) rear = delayed input (R3), side = quick input (R1).
circuit("fall_mono", "Falling-edge monostable", (4, 1, 0),
        [dust(1, 0), rep(2, 0, "west", 3), B((3, 1, 0), "comparator", facing="west", mode="subtract"),
         dust(1, 1), rep(2, 1, "west", 1), dust(3, 1)]
        + floor([(1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (3, 1)]),
        [10, 37, 41, 29, 45, 33], 40,
        "On each lever-off, Q gives one short pulse; lever-on does nothing.")

# 6. Observer chain: three observers in series watching the input dust; a pulse on every edge.
circuit("obs_chain", "Observer chain (dual-edge detector, 3 stages)", (5, 1, 0),
        [dust(1, 0), obs(2, 0, "west"), obs(3, 0, "west"), obs(4, 0, "west")] + floor([(1, 0)]),
        [10, 37, 41, 29, 45, 33], 40,
        "Each lever flip (either way) makes one short Q pulse after three observer delays.")

# 7. Lever-enabled torch clock: T2 (on input block) holds the clock block B powered while the lever is off.
circuit("clock20", "Lever-enabled clock (period 20 game ticks)", (5, 1, 0),
        [B((1, 1, 0), "redstone_wall_torch", facing="east", lit="true"), dust(2, 0), B((3, 1, 0), "stone"),
         B((4, 1, 0), "redstone_wall_torch", facing="east", lit="false"),
         dust(4, 1), dust(4, 2), dust(3, 2), rep(3, 1, "south", 4)]
        + floor([(2, 0), (4, 1), (4, 2), (3, 2), (3, 1)]),
        [10, 63, 31, 47, 29, 81], 40,
        "While the lever is on, Q blinks 10 gt on / 10 gt off; while it is off, Q stays off.")

# 8. T flip-flop. An observer makes a 2 gt pulse on every edge of the (delayed) input; a repeater gate,
#    locked while the inverted input (torch on the input block) is on, passes only the rising-edge pulse.
#    The 2 gt pulse makes a sticky piston spit its redstone block out, the next one pulls it back; Q is
#    powered only when the block sits at the far position.
circuit("tff", "T flip-flop (sticky piston block-drop)", (8, 1, 1),
        [dust(1, 0), rep(2, 0, "west", 3), dust(3, 0), obs(4, 0, "west"), rep(5, 0, "west", 1),
         B((0, 1, 1), "redstone_wall_torch", facing="south"), *[dust(x, 2) for x in range(0, 6)], rep(5, 1, "south", 1),
         B((6, 1, 0), "sticky_piston", facing="east"), B((7, 1, 0), "redstone_block")]
        + floor([(1, 0), (2, 0), (3, 0), (5, 0), (5, 1)] + [(x, 2) for x in range(0, 6)]),
        [10, 30, 34, 26, 38, 30, 42, 28], 40,
        "Each lever-on toggles Q; lever-off does nothing.")
