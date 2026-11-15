from pdbuild import Design
from door1 import mech, rep, dust, S

def seq2(d, p=None):
    p = p or {}
    g = lambda k, v: p.get(k, v)
    floor = set()
    def R(x, z, out, delay, y=5):
        rep(d, x, y, z, out, delay); floor.add((x, y - 1, z))
    def D(x, z, y=5):
        dust(d, x, y, z); floor.add((x, y - 1, z))
    # V row extension to x=5
    d.set(5, 5, 0, S); dust(d, 5, 6, 0); d.set(5, 6, -1, S)
    # K contact repeater + K-out column
    d.set(-4, 2, 1, S); rep(d, -4, 3, 1, "n", 1)
    d.set(-4, 3, 2, S); dust(d, -4, 4, 2)
    d.set(-4, 3, 3, S); dust(d, -4, 4, 3)
    for z in (4, 5, 6):
        D(-4, z)
    # pulse section
    R(-3, 6, "w", 4); R(-3, 4, "w", 4)
    D(-2, 6)                                  # P
    d.set(-1, 5, 6, "observer", facing="east"); 
    R(-2, 5, "n", 2)                          # R2i
    D(-2, 4); D(-1, 4)                        # Q
    R(0, 4, "e", 2)                           # R2k
    D(1, 4)                                   # Q2
    for z, dl in zip((3, 2), g("f1", (1, 2))):
        R(1, z, "n", dl)
    R(2, 4, "e", 4); D(3, 4)
    for z, dl in zip((3, 2), g("f2", (4, 4))):
        R(3, z, "n", dl)
    # X, lever, chain
    D(0, 6)
    d.set(0, 5, 5, "lever", face="floor", facing="north")
    R(1, 6, "w", g("x2", 4)); R(2, 6, "w", g("x1", 4))
    R(1, 5, "e", 4); R(2, 5, "e", 4); R(3, 5, "e", 4)
    d.set(4, 5, 5, S)                          # strong via
    dust(d, 4, 4, 5); dust(d, 4, 4, 6)         # J low (on corner walls)
    D(3, 6); D(5, 6); D(6, 6); D(7, 6)         # J
    # FL low column
    for z, dl in zip((4, 3, 2), g("fl", (2, 2, 2))):
        rep(d, 4, 4, z, "n", dl)
    # Vnet + riser at x=5
    D(5, 3); D(5, 4)
    d.set(5, 5, 2, S); dust(d, 5, 6, 2)
    d.set(5, 5, 1, S); dust(d, 5, 6, 1)
    R(5, 5, "n", g("ve", 1))
    R(7, 5, "n", g("vl1", 4)); D(7, 4); R(6, 4, "w", g("vl2", 4))
    # spiral
    sp = [(6, 4, 3), (7, 3, 3), (7, 2, 4), (6, 1, 4), (6, 0, 3), (7, -1, 3), (7, -2, 2)]
    for (x, y, z) in sp:
        d.set(x, y - 1, z, S); dust(d, x, y, z)
    d.set(6, -3, 2, S); dust(d, 6, -2, 2)
    d.set(5, -3, 2, S); rep(d, 5, -2, 2, "w", 1)
    for (x, y, z) in floor:
        if not (0 <= x <= 3) and (x, y, z) not in d.blocks:
            d.set(x, y, z, S)
    return d

def door(p=None):
    d = mech()
    seq2(d, p)
    return d
