from pdbuild import Design

FL = {"east": "west", "west": "east"}

class B:
    """builder with optional x mirror (x -> 3-x)"""
    def __init__(self, d, mirror=False):
        self.d, self.m = d, mirror
    def set(self, x, y, z, block, **p):
        if self.m:
            x = 3 - x
            if "facing" in p:
                p["facing"] = FL.get(p["facing"], p["facing"])
        key = (x, y, z)
        if key in self.d.blocks and self.d.blocks[key][0] != block:
            print("CONFLICT", key, self.d.blocks[key][0], "vs", block)
        self.d.set(x, y, z, block, **p)

def dir_name(frm, to):
    dx, dy, dz = to[0]-frm[0], to[1]-frm[1], to[2]-frm[2]
    return {(1,0,0):"east",(-1,0,0):"west",(0,1,0):"up",(0,-1,0):"down",(0,0,1):"south",(0,0,-1):"north"}[(dx,dy,dz)]

def chain(b, cells, first_facing=None):
    """cells: list of positions; cell i watches cell i-1. cells[0] gets first_facing (or is skipped if None)."""
    for i, c in enumerate(cells):
        if i == 0:
            if first_facing is None:
                continue
            f = first_facing
        else:
            f = dir_name(c, cells[i-1])
        b.set(*c, "observer", facing=f)

def side(d, mirror):
    b = B(d, mirror)
    # ---------- z=0 pistons: R module rows 1,2, a-singles rows 0,3
    for y in (1, 2):
        b.set(-3, y, 0, "sticky_piston", facing="east")
        b.set(-2, y, 0, "sticky_piston", facing="east")
        b.set(-1, y, 0, "stone")
    for y in (0, 3):
        b.set(-2, y, 0, "sticky_piston", facing="east")
        b.set(-1, y, 0, "stone")
    # R front
    b.set(-3, 1, -1, "glass"); b.set(-3, 2, -1, "repeater", facing="north", delay=4)
    b.set(-2, 2, -1, "observer", facing="west")
    b.set(-3, 2, -2, "observer", facing="north")
    b.set(-3, 2, -3, "observer", facing="north")
    # R back
    b.set(-3, 2, 1, "observer", facing="north")
    b.set(-3, 1, 2, "glass"); b.set(-3, 2, 2, "redstone_wire")
    b.set(-2, 1, 2, "glass"); b.set(-2, 2, 2, "redstone_wire")
    b.set(-2, 1, 1, "glass"); b.set(-2, 2, 1, "repeater", facing="south")
    # a-single triggers
    b.set(-2, 4, -1, "observer", facing="north")   # S3 via QC
    b.set(-2, 0, -1, "observer", facing="north")   # S0 direct
    # ---------- top C module (x=0)
    b.set(0, 6, 0, "sticky_piston", facing="down")
    b.set(0, 5, 0, "sticky_piston", facing="down")
    b.set(0, 4, 0, "stone")
    b.set(-3, 4, 0, "glass"); b.set(-3, 5, 0, "repeater", facing="north", delay=4)
    b.set(-3, 5, -1, "observer", facing="north")
    b.set(-3, 5, -2, "observer", facing="north")
    b.set(-2, 5, 0, "observer", facing="west")
    b.set(-1, 4, 0, "glass"); b.set(-1, 5, 0, "repeater", facing="west")
    for (x, z) in ((-3, 1), (-3, 2), (-2, 2), (-1, 2)):
        b.set(x, 4, z, "glass"); b.set(x, 5, z, "redstone_wire")
    b.set(0, 5, 2, "glass"); b.set(0, 6, 2, "redstone_wire")
    b.set(0, 5, 1, "glass"); b.set(0, 6, 1, "repeater", facing="south")
    # top b-single
    b.set(1, 5, 0, "sticky_piston", facing="down"); b.set(1, 4, 0, "stone")
    b.set(1, 5, -1, "observer", facing="north")
    # ---------- bottom C module (x=0)
    b.set(0, -3, 0, "sticky_piston", facing="up")
    b.set(0, -2, 0, "sticky_piston", facing="up")
    b.set(0, -1, 0, "stone")
    b.set(-3, -2, 0, "glass"); b.set(-3, -1, 0, "repeater", facing="north", delay=4)
    b.set(-3, -1, -1, "observer", facing="north")
    b.set(-3, -1, -2, "observer", facing="north")
    b.set(-2, -1, 0, "observer", facing="west")
    b.set(-1, -2, 0, "glass"); b.set(-1, -1, 0, "repeater", facing="west")
    b.set(-3, -2, 1, "stone"); b.set(-3, -1, 1, "redstone_wire")
    for x in (-2, 0):
        b.set(x, -3, 1, "stone"); b.set(x, -2, 1, "redstone_wire")
    b.set(-1, -3, 1, "stone"); b.set(-1, -2, 1, "repeater", facing="west")
    # bottom b-single
    b.set(1, -2, 0, "sticky_piston", facing="up"); b.set(1, -1, 0, "stone")
    b.set(1, -2, -1, "observer", facing="north")

def modules(d):
    side(d, False); side(d, True)
    return d

# source x positions
XS, XC, XR = -1, 1, 6

def chains(d):
    b = B(d)
    # PS, plane z=-2
    z = -2
    chain(b, [(XS, 6, z), (XS, 5, z)] + [(x, 5, z) for x in range(XS-1, -3, -1)] +
             [(-2, y, z) for y in range(4, -3, -1)] + [(x, -2, z) for x in range(-1, 2)])
    chain(b, [(XS, 5, z)] + [(x, 5, z) for x in range(XS+1, 6)] + [(5, y, z) for y in range(4, -3, -1)] + [(x, -2, z) for x in range(4, 1, -1)])
    # PC, plane z=-3
    z = -3
    chain(b, [(XC, 6, z), (XC, 5, z)] + [(x, 5, z) for x in range(XC-1, -3, -1)] + [(-2, y, z) for y in range(4, -2, -1)] + [(-3, -1, z)])
    chain(b, [(-2, 5, z), (-3, 5, z)])
    chain(b, [(XC, 5, z)] + [(x, 5, z) for x in range(XC+1, 6)] + [(5, y, z) for y in range(4, -2, -1)] + [(6, -1, z)])
    chain(b, [(5, 5, z), (6, 5, z)])
    # PR, plane z=-4
    z = -4
    chain(b, [(XR, 6, z), (XR, 5, z)] + [(XR, y, z) for y in range(4, 1, -1)])
    chain(b, [(XR, 5, z)] + [(x, 5, z) for x in range(XR-1, -4, -1)] + [(-3, y, z) for y in range(4, 1, -1)])
    return d

def sources(d):
    b = B(d)
    b.set(XS, 6, -2, "observer", facing="up")
    b.set(XC, 6, -3, "observer", facing="up")
    b.set(XR, 6, -4, "observer", facing="up")

def build_test():
    d = Design("open")
    modules(d); chains(d); sources(d)
    return d


def central(d, dl=(4,4,4,4,4,4), d8=4, d9=4, d10=4):
    b = B(d)
    y = 7
    # row N (z=-4): A line, Ra, Wb, RW
    for x in range(-3, 4):
        b.set(x, y, -4, "redstone_wire"); b.set(x, y-1, -4, "glass")
    b.set(4, y-1, -4, "glass"); b.set(4, y, -4, "repeater", facing="west")
    b.set(5, y, -4, "stone")
    b.set(6, y, -4, "repeater", facing="west")           # on O_R
    # row M (z=-3): lever block, chain
    b.set(-3, y, -3, "stone"); b.set(-3, y+1, -3, "lever", face="floor", facing="north")
    for i, x in enumerate(range(-2, 4)):
        b.set(x, y, -3, "repeater", facing="west", delay=dl[i])
        if x != XC:
            b.set(x, y-1, -3, "glass")
    b.set(4, y-1, -3, "glass"); b.set(4, y, -3, "redstone_wire")
    b.set(5, y-1, -3, "glass"); b.set(5, y, -3, "repeater", facing="south", delay=d8)
    # row S (z=-2)
    b.set(-3, y, -2, "redstone_wall_torch", facing="south")
    b.set(-1, y, -2, "redstone_wire")                    # S dust on O_S
    b.set(0, y-1, -2, "stone"); b.set(0, y, -2, "comparator", facing="east", mode="subtract")
    b.set(1, y-1, -2, "glass"); b.set(1, y, -2, "redstone_wire")
    b.set(2, y-1, -2, "glass"); b.set(2, y, -2, "repeater", facing="east", delay=d10)
    b.set(3, y-1, -2, "glass"); b.set(3, y, -2, "repeater", facing="east", delay=d9)
    b.set(4, y-1, -2, "glass"); b.set(4, y, -2, "redstone_wire")
    b.set(5, y-1, -2, "glass"); b.set(5, y, -2, "redstone_wire")
    # row z=-1: NA line
    for x in (-3, -2):
        b.set(x, y-1, -1, "glass"); b.set(x, y, -1, "redstone_wire")
    b.set(-1, y-1, -1, "glass"); b.set(-1, y, -1, "repeater", facing="west")
    b.set(0, y-1, -1, "glass"); b.set(0, y, -1, "redstone_wire")

def build(**kw):
    d = Design("open")
    modules(d); chains(d); sources(d); central(d, **kw)
    return d


# ---------------- version 2: central lowered onto the chain top rows (y=6)
def chains2(d):
    b = B(d)
    z = -2   # PS
    chain(b, [(XS, 6, z), (XS, 5, z)] + [(-2, 5, z)] + [(-2, y, z) for y in range(4, -3, -1)] + [(x, -2, z) for x in range(-1, 2)])
    chain(b, [(XS, 5, z)] + [(x, 5, z) for x in range(XS+1, 6)] + [(5, y, z) for y in range(4, -3, -1)] + [(x, -2, z) for x in range(4, 1, -1)])
    z = -3   # PC
    chain(b, [(XC, 6, z), (XC, 5, z)] + [(x, 5, z) for x in range(XC-1, -3, -1)] + [(-2, y, z) for y in range(4, -2, -1)] + [(-3, -1, z)])
    chain(b, [(-2, 5, z), (-3, 5, z)])
    chain(b, [(XC, 5, z)] + [(x, 5, z) for x in range(XC+1, 6)] + [(5, y, z) for y in range(4, -2, -1)] + [(6, -1, z)])
    chain(b, [(5, 5, z), (6, 5, z)])
    z = -4   # PR
    chain(b, [(XR, 6, z), (XR, 5, z)] + [(XR, y, z) for y in range(4, 1, -1)])
    chain(b, [(XR, 5, z)] + [(x, 5, z) for x in range(XR-1, -4, -1)] + [(-3, y, z) for y in range(4, 1, -1)])
    for (x, z) in ((XS, -2), (XC, -3), (XR, -4)):
        b.set(x, 5, z, "observer", facing="up")

def central2(d, dl=(4,4,4,4,4,4), d8=4, d9=4, d10=4):
    b = B(d)
    y = 6
    for x in range(-3, 4):
        b.set(x, y, -4, "redstone_wire")
    b.set(4, y, -4, "repeater", facing="west")
    b.set(5, y, -4, "stone")
    b.set(6, y, -4, "repeater", facing="west")
    b.set(-3, y, -3, "stone"); b.set(-3, y+1, -3, "lever", face="floor", facing="north")
    for i, x in enumerate(range(-2, 4)):
        b.set(x, y, -3, "repeater", facing="west", delay=dl[i])
    b.set(4, y, -3, "redstone_wire")
    b.set(5, y, -3, "repeater", facing="south", delay=d8)
    b.set(-3, y, -2, "redstone_wall_torch", facing="south")
    b.set(-1, y, -2, "redstone_wire")
    b.set(0, y, -2, "comparator", facing="east", mode="subtract")
    b.set(1, y, -2, "redstone_wire")
    b.set(2, y, -2, "repeater", facing="east", delay=d10)
    b.set(3, y, -2, "repeater", facing="east", delay=d9)
    b.set(4, y, -2, "redstone_wire")
    b.set(5, y, -2, "redstone_wire")
    for x in (-3, -2):
        b.set(x, y, -1, "redstone_wire")
    b.set(-1, y, -1, "repeater", facing="west")
    b.set(0, y, -1, "redstone_wire")
    for x in (-2, -1, 0):
        b.set(x, y-1, -1, "glass")

def build2(**kw):
    d = Design("open")
    modules(d); chains2(d); central2(d, **kw)
    return d
