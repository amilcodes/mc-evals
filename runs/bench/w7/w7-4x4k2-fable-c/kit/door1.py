from pdbuild import Design
S = "stone"
OUT = {"n": "south", "s": "north", "e": "west", "w": "east"}   # output dir -> facing

def rep(d, x, y, z, out, delay):
    d.set(x, y, z, "repeater", facing=OUT[out], delay=delay)

def dust(d, x, y, z):
    d.set(x, y, z, "redstone_wire")

def half():
    """left-side pieces that mirror to the right"""
    d = Design("open")
    for y in range(4):
        d.set(-1, y, 0, S)
    for y in (1, 2):
        d.set(-3, y, 0, "sticky_piston", facing="east")
        d.set(-2, y, 0, "sticky_piston", facing="east")
    d.set(-1, -1, 0, "sticky_piston", facing="up")
    d.set(-1, 4, 0, "sticky_piston", facing="down")
    # F feed
    dust(d, -1, 4, 1)
    d.set(-2, 2, 1, S); dust(d, -2, 3, 1)
    d.set(-2, 2, 2, S); dust(d, -2, 3, 2)
    d.set(-3, 1, 2, S); dust(d, -3, 2, 2)
    d.set(-3, 0, 1, S); dust(d, -3, 1, 1)
    d.set(-2, 0, 1, S); dust(d, -2, 1, 1)
    # K contact and K bus (z=-1 over the top)
    d.set(-4, 2, 0, S); dust(d, -4, 3, 0)
    d.set(-4, 3, -1, S); dust(d, -4, 4, -1)
    d.set(-3, 4, -1, S); dust(d, -3, 5, -1)
    d.set(-2, 4, -1, S); dust(d, -2, 5, -1)
    d.set(-1, 4, -1, "glass"); dust(d, -1, 5, -1)
    d.set(-1, 6, -1, S)
    # V top end
    d.set(-1, 5, 0, S); dust(d, -1, 6, 0)
    # V bottom stone
    d.set(-1, -2, 0, S)
    return d

def mech():
    d = Design("open")
    for x in range(4):
        d.set(x, -1, 0, S); d.set(x, 4, 0, S)
        d.set(x, -2, 0, "sticky_piston", facing="up")
        d.set(x, 5, 0, "sticky_piston", facing="down")
        dust(d, x, 6, 0)
        dust(d, x, 5, 1); d.set(x, 6, 1, S)
        dust(d, x, 5, -1); d.set(x, 6, -1, S)
    for x in range(-1, 5):
        d.set(x, -3, 1, S); rep(d, x, -2, 1, "n", 1)
        d.set(x, -3, 2, S); dust(d, x, -2, 2)
    h = half()
    d.merge(h); d.merge(h.mirrored_x(3))
    return d

def seq(d, p=None):
    p = p or {}
    g = lambda k, v: p.get(k, v)
    floor = set()
    def R(x, z, out, delay, y=5):
        rep(d, x, y, z, out, delay); floor.add((x, y - 1, z))
    def D(x, z, y=5):
        dust(d, x, y, z); floor.add((x, y - 1, z))
    # --- K contact repeater on the left
    d.set(-4, 2, 1, S); rep(d, -4, 3, 1, "n", g("kc", 1))
    d.set(-4, 3, 2, S); dust(d, -4, 4, 2)
    d.set(-4, 3, 3, S); dust(d, -4, 4, 3)
    for z in (4, 5, 6, 7):
        D(-4, z)
    # --- pulse section
    R(-3, 7, "w", 4); R(-3, 5, "w", 4)          # formers
    D(-2, 7); D(-2, 8)                           # P
    R(-2, 6, "n", 2)                             # R2i
    D(-2, 5)                                     # Q
    R(-1, 5, "e", 2)                             # R2k
    D(0, 5); D(0, 6); D(1, 6)                    # Q2
    for z, dl in zip((4, 3, 2), g("f1", (1, 1, 1))):
        R(0, z, "n", dl)
    for z, dl in zip((5, 4, 3, 2), g("f2", (4, 4, 4, 1))):
        R(1, z, "n", dl)
    # --- observer, X, lever
    d.set(-1, 5, 8, "observer", facing="east")
    D(0, 8)
    d.set(0, 5, 9, "lever", face="floor", facing="north")
    R(1, 8, "w", g("x2", 4)); D(2, 8); R(3, 8, "w", g("x1", 4))
    # --- chain
    R(1, 9, "e", 4); R(2, 9, "e", 4); R(3, 9, "e", 4)
    for z in (9, 8, 7, 6, 5):
        D(4, z)
    D(3, 5)
    for z, dl in zip((4, 3, 2), g("fl", (2, 2, 2))):
        R(3, z, "n", dl)
    # V early / late
    R(4, 4, "n", g("ve", 2))
    D(5, 7)
    for z, dl in zip((6, 5, 4), g("vl", (4, 4, 2))):
        R(5, z, "n", dl)
    for x in (4, 5, 6, 7):
        D(x, 3)
    # riser at x=4
    d.set(4, 5, 2, S); dust(d, 4, 6, 2)
    d.set(4, 5, 1, "glass"); dust(d, 4, 6, 1)
    # spiral down
    sp = [(7, 4, 4), (6, 3, 4), (6, 2, 5), (7, 1, 5), (7, 0, 4), (6, -1, 4), (6, -2, 3)]
    for (x, y, z) in sp:
        d.set(x, y - 1, z, S); dust(d, x, y, z)
    d.set(6, -3, 2, S); dust(d, 6, -2, 2)
    d.set(5, -3, 2, S); rep(d, 5, -2, 2, "w", 1)
    # floors
    for (x, y, z) in floor:
        if not (0 <= x <= 3) and (x, y, z) not in d.blocks:
            d.set(x, y, z, S)
    return d

def door(p=None):
    d = mech()
    seq(d, p)
    return d
