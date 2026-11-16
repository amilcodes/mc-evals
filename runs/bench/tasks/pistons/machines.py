"""Reference piston machines (vanilla 26.3 physics) and their specs.

Each machine() returns {"name", "title", "blocks", "spec"}. Coordinates: x east, y up, z south.
Component facings follow the game's block states:
  piston/sticky_piston facing = direction the head pushes;
  repeater facing = side the INPUT comes from (output is the opposite side);
  observer facing = side its face WATCHES (output is the opposite side).
"""

SCHEDULE = [0, 3, 7, 1, 11, 2]      # idle ticks before each of the 6 toggles (odd gaps shift the phase)


def b(x, y, z, bid, **props):
    out = {"pos": [x, y, z], "id": "minecraft:" + bid}
    if props:
        out["props"] = {k: str(v).lower() if isinstance(v, bool) else str(v) for k, v in props.items()}
    return out


def floor(cells, y=None, bid="stone"):
    return [b(x, (y if y is not None else yy - 1), z, bid) for (x, yy, z) in cells]


def rep(x, y, z, facing, delay=1):
    return b(x, y, z, "repeater", facing=facing, delay=delay)


def _bbox(blocks, pad=1, extra=()):
    ps = [bl["pos"] for bl in blocks] + [list(e) for e in extra]
    lo = [min(p[i] for p in ps) - pad for i in range(3)]
    hi = [max(p[i] for p in ps) + pad for i in range(3)]
    return {"min": lo, "max": hi}


def _spec(blocks, lever, states, extra=(), keep_clear=(), conserve=None, fixed=(), time_cap=60, slack=3, pad=1, **kw):
    spec = {
        "lever": list(lever),
        "box": _bbox(blocks, pad, extra),
        "block_budget": len(blocks) + slack,
        "states": states,
        "schedule": SCHEDULE,
        "time_cap": time_cap,
        "keep_clear": [list(c) for c in keep_clear],
        "fixed": [list(f) for f in fixed],
    }
    if conserve:
        spec["conserve"] = conserve
    spec.update(kw)
    return spec


# ---------------------------------------------------------------- 1. double piston extender

def dpe():
    """Sticky back piston B pushes sticky front piston F + payload; F then fires from a powered
    block it lands on (G). Retraction: G drops (F pulls payload back 1), B retracts (pulls F),
    then a delayed observer pulse under F's home cell makes F grab the payload back."""
    bl = [
        b(0, 0, 0, "sticky_piston", facing="east"),   # B
        b(1, 0, 0, "sticky_piston", facing="east"),   # F
        b(2, 0, 0, "lime_concrete"),                  # payload
        b(0, -1, 0, "stone"), b(1, -1, 0, "stone"), b(2, -1, 0, "stone"),   # power blocks under B, F-home, G
        b(-1, -1, 4, "lever", face="floor", facing="north"),
    ]
    bl += [b(x, -1, 4, "redstone_wire") for x in range(0, 3)]
    # x=0 column: B, 3 repeaters of delay 2 (12 ticks)
    bl += [rep(0, -1, z, "south", 2) for z in (3, 2, 1)]
    # x=1 column: repeater 4 -> observer -> repeater 4 (pulse into F's home block, ~18 ticks later)
    bl += [rep(1, -1, 3, "south", 4), b(1, -1, 2, "observer", facing="south"), rep(1, -1, 1, "south", 4)]
    # x=2 column: G, 3 repeaters of delay 1 (6 ticks)
    bl += [rep(2, -1, z, "south", 1) for z in (3, 2, 1)]
    bl += floor([(-1, -1, 4)] + [(x, -1, 4) for x in range(3)] + [(x, -1, z) for x in (0, 2) for z in (1, 2, 3)]
                + [(1, -1, 3), (1, -1, 1)])
    states = {
        "off": [{"at": [2, 0, 0], "is": "lime_concrete"}, {"at": [[3, 4], 0, 0], "is": "air"}],
        "on": [{"at": [4, 0, 0], "is": "lime_concrete"}, {"at": [2, 0, 0], "is": ["sticky_piston", "piston"]}],
    }
    track_side = [[x, y, z] for x in (3, 4, 5) for (y, z) in ((1, 0), (-1, 0), (0, 1), (0, -1))] + [[5, 0, 0]]
    return {"name": "dpe", "title": "double piston extender",
            "goal": "Pushes the lime concrete block 2 cells east, from (2,0,0) to (4,0,0), when the lever is switched on, "
                    "and brings it fully back to (2,0,0) when the lever is switched off.",
            "blocks": bl,
            "spec": _spec(bl, (-1, -1, 4), states, extra=[[5, 1, 0]], keep_clear=track_side,
                          conserve={"minecraft:lime_concrete": 1})}



# ---------------------------------------------------------------- 2. block swapper

def swapper():
    """Slot (0,0,0) shows red concrete with the lever off and blue concrete with it on.
    Red is held by an extended sticky side piston (powered by a torch); blue waits below, on a
    sticky piston facing up. On: the torch goes out first (side piston pulls red aside), then the
    bottom piston pushes blue up into the slot. Off: the bottom piston pulls blue back down, and only then
    does the torch relight (its block is held on by a delayed second input) to push red back."""
    bl = [
        b(0, 0, 0, "red_concrete"),
        b(0, -1, 0, "blue_concrete"),
        b(0, -2, 0, "sticky_piston", facing="up"),
        b(2, 0, 0, "sticky_piston", facing="west", extended=True),
        b(1, 0, 0, "piston_head", facing="west", type="sticky"),
        b(2, -1, 1, "stone"),                                   # T: the torch's block
        b(2, 0, 1, "redstone_torch"),                           # powers the side piston
        b(-1, -1, 3, "lever", face="floor", facing="north"),
    ]
    bl += [b(x, -1, 3, "redstone_wire") for x in range(0, 5)]
    bl += [rep(2, -1, 2, "south", 1)]                            # T on fast
    bl += [rep(4, -1, 2, "south", 4), b(4, -1, 1, "redstone_wire"), rep(3, -1, 1, "east", 2)]  # T off late
    # bottom piston: bus steps down to y=-2, then a delay-4 repeater into the piston
    bl += [b(0, -2, 2, "redstone_wire"), rep(0, -2, 1, "south", 4)]
    bl += floor([(-1, -1, 3)] + [(x, -1, 3) for x in range(5)] + [(4, -1, 2), (4, -1, 1), (3, -1, 1), (2, -1, 2),
                                                                  (0, -2, 2), (0, -2, 1)])
    states = {"off": [{"at": [0, 0, 0], "is": "red_concrete"}], "on": [{"at": [0, 0, 0], "is": "blue_concrete"}]}
    return {"name": "swapper", "title": "block swapper",
            "goal": "The slot (0,0,0) holds the red concrete block while the lever is off and the blue concrete block while it is on; "
                    "the two blocks swap every time the lever is flipped.",
            "blocks": bl,
            "spec": _spec(bl, (-1, -1, 3), states, conserve={"minecraft:red_concrete": 1, "minecraft:blue_concrete": 1})}


# ---------------------------------------------------------------- 3. 2x2 flush floor hatch

def hatch():
    """A 2x2 hatch in a smooth-stone floor at y=0, flush when closed. The four hatch blocks sit on a
    2x2 slime pad; one sticky piston below (powered through an obsidian block by a torch) holds the
    pad up. Lever on: the torch goes out and the piston pulls pad + hatch down one cell (8 blocks)."""
    ring = [(x, 0, z) for x in range(-1, 3) for z in range(-1, 3) if not (0 <= x <= 1 and 0 <= z <= 1)]
    bl = [b(x, y, z, "smooth_stone") for (x, y, z) in ring]
    bl += [b(x, 0, z, "stone") for x in (0, 1) for z in (0, 1)]
    bl += [b(x, -1, z, "slime_block") for x in (0, 1) for z in (0, 1)]
    bl += [b(0, -3, 0, "sticky_piston", facing="up", extended=True), b(0, -2, 0, "piston_head", facing="up", type="sticky")]
    bl += [b(1, -3, 0, "obsidian"), b(1, -4, 0, "redstone_torch"), b(1, -5, 0, "stone"),
           b(2, -5, 0, "lever", face="wall", facing="east")]
    states = {"off": [{"at": [[0, 1], 0, [0, 1]], "is": "stone"}], "on": [{"at": [[0, 1], 0, [0, 1]], "is": "air"}]}
    return {"name": "hatch", "title": "2x2 flush floor hatch",
            "goal": "A 2x2 hatch (0..1, 0, 0..1) in the smooth-stone floor: closed (four stone blocks, flush with the floor) while the "
                    "lever is off, open (all four cells empty) while it is on. The smooth-stone floor ring must never move.",
            "blocks": bl,
            "spec": _spec(bl, (2, -5, 0), states, fixed=[[*c, "minecraft:smooth_stone"] for c in ring],
                          keep_clear=[[[0, 1], [1, 2], [0, 1]]])}


# ---------------------------------------------------------------- 4. sideways row slide (push limit)

def row_slide(n=6):
    """A row of n orange concrete blocks at y=1 rides on a row of n slime blocks; one sticky piston,
    powered by the lever beside it, slides the whole 2 x n structure (2n blocks, 12 at n=6) one cell south."""
    bl = [b(x, 1, 0, "orange_concrete") for x in range(n)] + [b(x, 0, 0, "slime_block") for x in range(n)]
    bl += [b(2, 0, -1, "sticky_piston", facing="south"), b(2, -1, -2, "stone"), b(2, 0, -2, "lever", face="floor", facing="north")]
    states = {"off": [{"at": [[0, n - 1], 1, 0], "is": "orange_concrete"}, {"at": [[0, n - 1], 1, 1], "is": "air"}],
              "on": [{"at": [[0, n - 1], 1, 1], "is": "orange_concrete"}, {"at": [[0, n - 1], 1, 0], "is": "air"}]}
    return {"name": "row_slide", "title": f"{n}-block row slide",
            "goal": f"A row of {n} orange concrete blocks at (0..{n - 1}, 1, 0) slides one cell south to (0..{n - 1}, 1, 1) when the "
                    "lever is switched on and back when it is switched off.",
            "blocks": bl,
            "spec": _spec(bl, (2, 0, -2), states, extra=[[0, 1, 2], [n - 1, 1, 2]], conserve={"minecraft:orange_concrete": n})}


# ---------------------------------------------------------------- 5. inline row shuttle

def row_push(n=10):
    """A row of n concrete blocks shuttled one cell along x by two normal pistons that face each
    other: the front piston (torch-powered, extended while off) must get out of the way before the
    back piston pushes, and the back piston must retract before the front one pushes the row back."""
    e = n + 2                       # front piston x
    bl = [b(x, 0, 0, "cyan_concrete") for x in range(1, n + 1)]
    bl += [b(0, 0, 0, "piston", facing="east"), b(0, -1, 0, "stone"),
           b(e, 0, 0, "piston", facing="west", extended=True), b(e - 1, 0, 0, "piston_head", facing="west", type="normal"),
           b(e, -1, 1, "stone"), b(e, 0, 1, "redstone_torch")]
    lever = (-1, -1, 3)
    bl += [b(*lever, "lever", face="floor", facing="north")]
    bl += [b(x, -1, 3, "redstone_wire") for x in range(0, e + 3)]
    bl += [rep(0, -1, 2, "south", 3), rep(0, -1, 1, "south", 1)]                  # back piston: 8 ticks both ways
    bl += [rep(e, -1, 2, "south", 1)]                                               # torch block on fast
    bl += [rep(e + 2, -1, 2, "south", 4), b(e + 2, -1, 1, "redstone_wire"), rep(e + 1, -1, 1, "east", 2)]  # off late
    bl += floor([lever] + [(x, -1, 3) for x in range(0, e + 3)] + [(0, -1, 2), (0, -1, 1), (e, -1, 2), (e + 2, -1, 2),
                                                                   (e + 2, -1, 1), (e + 1, -1, 1)])
    states = {"off": [{"at": [[1, n], 0, 0], "is": "cyan_concrete"}, {"at": [n + 1, 0, 0], "is": ["air", "piston_head"]}],
              "on": [{"at": [[2, n + 1], 0, 0], "is": "cyan_concrete"}, {"at": [1, 0, 0], "is": ["air", "piston_head"]}]}
    side = [[[1, n + 1], 1, 0], [[1, n + 1], 0, -1]]
    return {"name": "row_push", "title": f"{n}-block row shuttle",
            "goal": f"A row of {n} cyan concrete blocks at (1..{n}, 0, 0) moves one cell east to (2..{n + 1}, 0, 0) when the lever is "
                    "switched on and one cell back west when it is switched off.",
            "blocks": bl,
            "spec": _spec(bl, lever, states, keep_clear=side, conserve={"minecraft:cyan_concrete": n})}


# ---------------------------------------------------------------- 6. slime elevator with non-sticky neighbours

def elevator():
    """A slime-block platform (3 slime in a row) carrying three white concrete blocks is lifted one
    cell by a sticky piston beneath its middle. Glazed terracotta posts beside the platform do not
    stick to slime, so they stay put while the platform moves along them."""
    bl = [b(x, 0, 0, "slime_block") for x in range(3)] + [b(x, 1, 0, "white_concrete") for x in range(3)]
    bl += [b(1, -1, 0, "sticky_piston", facing="up")]
    bl += [b(-1, y, 0, "white_glazed_terracotta", facing="north") for y in (0, 1, 2)]
    bl += [b(3, y, 0, "white_glazed_terracotta", facing="north") for y in (0, 1, 2)]
    bl += [b(x, y, 1, "white_glazed_terracotta", facing="north") for x in (0, 2) for y in (0, 1, 2)]
    bl += [b(1, -2, 0, "stone"), b(1, -2, 1, "lever", face="wall", facing="south")]
    states = {"off": [{"at": [[0, 2], 1, 0], "is": "white_concrete"}, {"at": [[0, 2], 2, 0], "is": "air"}],
              "on": [{"at": [[0, 2], 2, 0], "is": "white_concrete"}, {"at": [[0, 2], 1, 0], "is": "slime_block"}]}
    posts = [p["pos"] + [p["id"]] for p in bl if p["id"].endswith("glazed_terracotta")]
    return {"name": "elevator", "title": "slime platform lift",
            "goal": "The three white concrete blocks at (0..2, 1, 0) rise one cell to (0..2, 2, 0) when the lever is switched on and "
                    "come back down when it is switched off. The glazed terracotta posts around the platform must never move.",
            "blocks": bl,
            "spec": _spec(bl, (1, -2, 1), states, fixed=posts, conserve={"minecraft:white_concrete": 3})}


# ---------------------------------------------------------------- 7. triple piston extender

def tpe(south=None, north=None):
    """Three sticky pistons in a row (P3 at x=0, P2 at 1, P1 at 2) push the magenta block from x=3 to x=6.
    Each track cell 0..4 has a power block U under it (y=-1). South repeater columns hold levels:
    U0 fast (P3 pushes first), U2 (P2 fires once it has been carried onto x=2), U4 (P1 fires on x=4).
    North columns: U0 slow hold (P3 stays out until the front is folded), and three observer pulses
    that make the folded pistons grab and pull back: U3 (P1 pulls X 5->4), U1 (P2 pulls P1 3->2),
    U2 (P1 pulls X 4->3)."""
    bl = [b(0, 0, 0, "sticky_piston", facing="east"), b(1, 0, 0, "sticky_piston", facing="east"),
          b(2, 0, 0, "sticky_piston", facing="east"), b(3, 0, 0, "magenta_concrete")]
    bl += [b(x, -1, 0, "stone") for x in range(5)]
    lever = (-3, -1, 0)
    bl += [b(*lever, "lever", face="floor", facing="north")]
    dust = [(-2, -1, z) for z in range(-8, 7)] + [(x, -1, 6) for x in range(-1, 5)] + [(x, -1, -8) for x in range(-1, 4)]
    south = south or {0: ["w", "w", "w", "w", 1], 2: [2, 2, 2, 1, 1], 4: [1, 1, 1, 1, 1]}   # z=5..1; "w" = dust
    comps = []
    for x, col in south.items():
        for z, d in zip(range(5, 0, -1), col):
            if d == "w":
                dust.append((x, -1, z))
            else:
                comps.append(rep(x, -1, z, "south", d))
    bl += [b(*d, "redstone_wire") for d in dust]
    north = north or {0: [4, 4, 2, 1, 1, 1, 1], 1: [4, 4, 4, "o", 1, 1, 2], 2: [4, 4, 4, 4, 4, "o", 2],
                      3: [1, "o", 1, 1, 2, 2, 2]}  # z=-7..-1
    for x, col in north.items():
        for z, d in zip(range(-7, 0), col):
            comps.append(b(x, -1, z, "observer", facing="north") if d == "o" else rep(x, -1, z, "north", d))
    bl += comps
    bl += floor([lever] + dust + [tuple(c["pos"]) for c in comps])
    states = {"off": [{"at": [3, 0, 0], "is": "magenta_concrete"}, {"at": [[4, 6], 0, 0], "is": "air"}],
              "on": [{"at": [6, 0, 0], "is": "magenta_concrete"}, {"at": [[3, 5], 0, 0], "is": ["sticky_piston", "piston_head", "piston"]}]}
    track_side = [[[4, 7], 1, 0], [[5, 7], -1, 0], [[4, 7], 0, 1], [[4, 7], 0, -1], [7, 0, 0]]
    return {"name": "tpe", "title": "triple piston extender",
            "goal": "Pushes the magenta concrete block 3 cells east, from (3,0,0) to (6,0,0), when the lever is switched on, and "
                    "brings it fully back to (3,0,0) when the lever is switched off.",
            "blocks": bl,
            "spec": _spec(bl, lever, states, extra=[[7, 1, 0]], keep_clear=track_side, time_cap=80,
                          conserve={"minecraft:magenta_concrete": 1})}


MACHINES = {"dpe": dpe, "tpe": tpe, "swapper": swapper, "hatch": hatch, "row_slide": row_slide, "row_push": row_push, "elevator": elevator}


# ---------------------------------------------------------------- port fixes (changed physics)

def _swap(blocks, changes, add=()):
    cells = {tuple(bl["pos"]): bl for bl in blocks}
    for pos, new in changes.items():
        cells.pop(tuple(pos), None)
        if new is not None:
            cells[tuple(pos)] = new
    for bl in add:
        cells[tuple(bl["pos"])] = bl
    return [cells[p] for p in sorted(cells)]


def row_slide_split():
    """Push limit < 12: carriers x=3..5 become honey (honey and slime do not stick), so there are two
    6-block groups; a second sticky piston at x=4 pushes the honey group, fed from the lever by dust
    and a repeater on the north side."""
    m = row_slide()
    ch = {(x, 0, 0): b(x, 0, 0, "honey_block") for x in (3, 4, 5)}
    add = [b(4, 0, -1, "sticky_piston", facing="south"), rep(4, 0, -2, "north", 1),
           b(3, 0, -2, "redstone_wire"), b(3, 0, -3, "redstone_wire"), b(4, 0, -3, "redstone_wire")]
    add += floor([(4, 0, -2), (3, 0, -2), (3, 0, -3), (4, 0, -3)])
    return _swap(m["blocks"], ch, add)


def hatch_split():
    """Push limit < 8: the back row of the pad becomes honey and gets its own sticky piston at
    (1,-3,1), which the same obsidian block powers. Two 4-block groups."""
    m = hatch()
    ch = {(x, -1, 1): b(x, -1, 1, "honey_block") for x in (0, 1)}
    add = [b(1, -3, 1, "sticky_piston", facing="up", extended=True), b(1, -2, 1, "piston_head", facing="up", type="sticky")]
    return _swap(m["blocks"], ch, add)


PORT_FIXES = {"row_slide": row_slide_split, "hatch": hatch_split}


def tpe_halved():
    """Slow repeaters (repeater_unit 4): every repeater delay d becomes ceil(d/2), roughly
    restoring vanilla tick timings so the extender comes to rest inside its 80-tick cap."""
    out = []
    for bl in tpe()["blocks"]:
        bl = dict(bl)
        if bl["id"].endswith(":repeater"):
            bl["props"] = {**bl["props"], "delay": str((int(bl["props"]["delay"]) + 1) // 2)}
        out.append(bl)
    return out


def dpe_unstretched():
    """DPE variant whose grab pulse comes straight from an observer (no stretching repeater):
    two delay-4 repeaters, then the observer outputs into F's home block. Fine with vanilla's
    2-tick observer pulse."""
    m = dpe()
    ch = {(1, -1, 3): rep(1, -1, 3, "south", 4), (1, -1, 2): rep(1, -1, 2, "south", 4),
          (1, -1, 1): b(1, -1, 1, "observer", facing="south")}
    return _swap(m["blocks"], ch, floor([(1, -1, 2)]))


def tpe_ru4():
    """Port of the TPE to repeater_unit 4 (every delay step is 4 ticks). Re-derived schedule:
    U0 fast 4, U4 8 (dust in its column), U2 12 (dust), pulses c 26, e 42, f 50, slow hold 36.
    Rests in about 56 ticks, inside the 80-tick cap."""
    south = {0: ["w", "w", "w", "w", 1], 2: [1, "w", "w", 1, 1], 4: [1, "w", "w", "w", 1]}
    north = {0: [2, 2, 1, 1, 1, 1, 1], 1: [3, 2, 2, "o", 1, 1, 1], 2: [3, 2, 2, 2, 2, "o", 1], 3: [1, "o", 1, 1, 1, 1, 1]}
    return tpe(south, north)["blocks"]


PORT_FIXES.update({"tpe": tpe_ru4})
