"""Rulebook constants, geometry and the block allow-list (rulebook v0).

Coordinates are local to the doorway: doorway cells are (x, y, 0) for 0 <= x < w and
0 <= y < h, and the hallway runs through them along z in both directions.

A door size `n` is either an int (a square n x n door, the original tasks) or a pair [w, h]:
w cells wide along x, h cells tall along y. Square sizes are always stored as an int, so logs,
references and briefs for the original tasks are unchanged.
"""

GAME_VERSION = "26.3"
# Recorded in every run log. 0.3: observers no longer fire merely for being placed.
# Logs without a version were made under 0.2 and are scored with its placement rule.
RULES_VERSION = "0.3"
ORIGIN = (0, 100, 0)            # world position of local (0, 0, 0); the pinned headline position
DOOR_BLOCK = "minecraft:stone"
WALL_BLOCK = "minecraft:stone"

TIME_CAP = 200                  # game ticks allowed per open or close, including settling down
QUIET = 20                      # ticks with no block change that count as quiescent
HOLD = 40                       # ticks the door must then stay put
SETTLE_CAP = 40                 # ticks allowed for the build to come to rest after placement
CYCLES = {"dev": 3, "final": 8}
# Extra idle ticks before each flip in final mode, so flips do not all land on the same phase.
FINAL_DELAYS = [0, 1, 2, 3, 5, 7, 11, 13, 4, 6, 9, 10, 17, 19, 23, 29]
HALF_EXTENT = 24                # the test volume is 48 x 48 x 48 around the doorway
MAX_BLOCKS = 20000
SIZES = (1, 2, 3, 4, 5, 6, 7)   # 1 is for grader tests only; it is not a benchmark task
MAX_SIDE = 7                    # rectangular doors: each side 1..MAX_SIDE
TRACKS = ("open", "seamless")

# ---------------------------------------------------------------- geometry


def dims(n):
    """(w, h) for a size given as an int, a [w, h] pair or a "WxH" string."""
    if isinstance(n, str):
        parts = n.lower().replace("×", "x").split("x")
        n = int(parts[0]) if len(parts) == 1 else [int(p) for p in parts]
    if isinstance(n, bool):
        raise ValueError(f"bad door size {n!r}")
    if isinstance(n, int):
        return n, n
    w, h = n
    return int(w), int(h)


def norm(n):
    """Canonical form: an int for a square door, a (w, h) tuple otherwise."""
    w, h = dims(n)
    return w if w == h else (w, h)


def valid_size(n):
    try:
        w, h = dims(n)
    except (TypeError, ValueError):
        return False
    if w == h:
        return w in SIZES
    return 1 <= w <= MAX_SIDE and 1 <= h <= MAX_SIDE


def label(n):
    w, h = dims(n)
    return f"{w}x{h}"


def region(n):
    w, h = dims(n)
    return (w // 2 - HALF_EXTENT, h // 2 - HALF_EXTENT, -HALF_EXTENT), (w // 2 + HALF_EXTENT - 1, h // 2 + HALF_EXTENT - 1, HALF_EXTENT - 1)


def in_region(n, p):
    lo, hi = region(n)
    return all(lo[i] <= p[i] <= hi[i] for i in range(3))


def doorway(n):
    w, h = dims(n)
    return [(x, y, 0) for y in range(h) for x in range(w)]


def in_doorway(n, p):
    w, h = dims(n)
    return p[2] == 0 and 0 <= p[0] < w and 0 <= p[1] < h


def in_hallway(n, p):
    w, h = dims(n)
    return p[2] != 0 and 0 <= p[0] < w and 0 <= p[1] < h


def ring(n, z=0):
    """Cells that share a face with the doorway/hallway column at depth z (corners excluded)."""
    w, h = dims(n)
    cells = [(-1, y, z) for y in range(h)] + [(w, y, z) for y in range(h)]
    cells += [(x, -1, z) for x in range(w)] + [(x, h, z) for x in range(w)]
    return cells


def in_shell(n, p):
    """Hallway walls: harness-owned cells around the hallway at every z != 0."""
    w, h = dims(n)
    x, y, z = p
    if z == 0:
        return False
    return ((x in (-1, w)) and 0 <= y < h) or ((y in (-1, h)) and 0 <= x < w)


def shell(n):
    lo, hi = region(n)
    return [c for z in range(lo[2], hi[2] + 1) if z != 0 for c in ring(n, z)]


# ---------------------------------------------------------------- allow-list

_H4 = ("north", "south", "east", "west")
_D6 = _H4 + ("up", "down")
_BOOL = ("true", "false")
_WIRE = ("up", "side", "none")
_P16 = tuple(str(i) for i in range(16))

_COLOURS = (
    "white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray",
    "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black",
)

# Full, opaque, movable cubes with no behaviour beyond conducting power.
PLAIN = {"minecraft:stone", "minecraft:smooth_stone", "minecraft:iron_block"} | {
    f"minecraft:{c}_concrete" for c in _COLOURS
}

COMPONENTS = {
    "minecraft:piston": {"facing": _D6, "extended": _BOOL},
    "minecraft:sticky_piston": {"facing": _D6, "extended": _BOOL},
    "minecraft:piston_head": {"facing": _D6, "type": ("normal", "sticky"), "short": ("false",)},
    "minecraft:redstone_wire": {"north": _WIRE, "south": _WIRE, "east": _WIRE, "west": _WIRE, "power": _P16},
    "minecraft:repeater": {"facing": _H4, "delay": ("1", "2", "3", "4"), "locked": _BOOL, "powered": _BOOL},
    "minecraft:comparator": {"facing": _H4, "mode": ("compare", "subtract"), "powered": _BOOL},
    "minecraft:redstone_torch": {"lit": _BOOL},
    "minecraft:redstone_wall_torch": {"facing": _H4, "lit": _BOOL},
    "minecraft:redstone_block": {},
    "minecraft:observer": {"facing": _D6, "powered": _BOOL},
    "minecraft:slime_block": {},
    "minecraft:honey_block": {},
    "minecraft:target": {"power": _P16},
    "minecraft:note_block": {"note": tuple(str(i) for i in range(25)), "powered": _BOOL},
    "minecraft:lever": {"face": ("floor", "wall", "ceiling"), "facing": _H4, "powered": ("false",)},
    "minecraft:obsidian": {},
    "minecraft:glass": {},
    "minecraft:white_glazed_terracotta": {"facing": _H4},
}

ALLOWED = {**{b: {} for b in PLAIN}, **COMPONENTS}

_STEP = {"north": (0, 0, -1), "south": (0, 0, 1), "west": (-1, 0, 0), "east": (1, 0, 0), "up": (0, 1, 0), "down": (0, -1, 0)}


def step(pos, facing, k=1):
    d = _STEP[facing]
    return (pos[0] + k * d[0], pos[1] + k * d[1], pos[2] + k * d[2])


def state_string(block_id, props):
    if not props:
        return block_id
    return block_id + "[" + ",".join(f"{k}={v}" for k, v in sorted(props.items())) + "]"


def parse_state(s):
    """'minecraft:piston[extended=false,facing=east]' -> ('minecraft:piston', {...})."""
    if "[" not in s:
        return s, {}
    block_id, rest = s.split("[", 1)
    return block_id, dict(kv.split("=", 1) for kv in rest.rstrip("]").split(",") if kv)
