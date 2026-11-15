from pdbuild import Design
from door import obs, chain, put

def left_half():
    d = Design("open")
    P = lambda *a, **k: put(d, *a, **k)
    # row 3 (O lane), variant B
    P(-3,3,0,"sticky_piston",facing="east"); P(-2,3,0,"sticky_piston",facing="east"); P(-1,3,0,"stone")
    P(-3,2,1,"stone"); P(-3,3,1,"repeater",facing="south",delay=4)
    P(-2,3,1,"observer",facing="west")            # Od
    P(-2,4,1,"observer",facing="south")           # Oh: out north into air (-2,4,0)
    P(-3,3,2,"stone"); P(-3,4,2,"redstone_wire")
    P(-2,3,2,"glass"); P(-2,4,2,"repeater",facing="west",delay=4)
    P(-4,4,2,"redstone_wire")                     # on O column top (-4,3,2)
    # row 0 (O lane)
    P(-3,0,0,"sticky_piston",facing="east"); P(-2,0,0,"sticky_piston",facing="east"); P(-1,0,0,"stone")
    P(-3,-1,1,"stone"); P(-3,0,1,"repeater",facing="south",delay=4)
    P(-2,0,1,"observer",facing="west")
    P(-2,-1,0,"observer",facing="down")
    P(-2,-3,0,"stone"); P(-2,-2,0,"repeater",facing="south",delay=4)
    P(-3,-1,2,"stone"); P(-3,0,2,"redstone_wire")
    P(-2,-2,2,"stone"); P(-2,-1,2,"redstone_wire")
    P(-2,-2,1,"redstone_wire")
    # rows 1,2 (F singles)
    P(-2,2,0,"sticky_piston",facing="east"); P(-1,2,0,"stone")
    P(-2,1,0,"sticky_piston",facing="east"); P(-1,1,0,"stone")
    # bottom: col 0 C single, col 1 I lane
    P(0,-2,0,"sticky_piston",facing="up"); P(0,-1,0,"stone")
    P(1,-3,0,"sticky_piston",facing="up"); P(1,-2,0,"sticky_piston",facing="up"); P(1,-1,0,"stone")
    P(1,-4,1,"stone"); P(1,-3,1,"repeater",facing="south",delay=4)
    P(1,-2,1,"observer",facing="down")
    P(1,-3,2,"redstone_wire")
    obs(d,(1,-4,2),(1,-5,2))
    # top: col 0 C single
    P(0,5,0,"sticky_piston",facing="down"); P(0,4,0,"stone")
    # O chain: E_O watches row B repeater (0,-5,1)
    chain(d, [(0,-4,1),(0,-4,2),(-1,-4,2),(-2,-4,2),(-2,-4,1),(-2,-3,1)], (0,-5,1))
    chain(d, [(-3,-4,2),(-3,-3,2),(-4,-3,2)] + [(-4,y,2) for y in range(-2,4)], (-2,-4,2))
    chain(d, [(-3,2,2),(-2,2,2),(-2,2,1)], (-4,2,2))
    # C chain column
    chain(d, [(-4,y,0) for y in range(-3,6)] + [(-3,5,0),(-2,5,0),(-1,5,0)], (-4,-4,0))
    obs(d,(0,-3,0),(0,-4,0))
    return d

def top_pair(d):
    P = lambda *a, **k: put(d, *a, **k)
    for x in (1,2):
        P(x,6,0,"sticky_piston",facing="down"); P(x,5,0,"sticky_piston",facing="down"); P(x,4,0,"stone")
        P(x,5,1,"observer",facing="south")
        P(x,6,1,"stone")
    for x in (0,1,2,3):
        P(x,5,2,"redstone_wire")
    for gx,cx in ((0,-1),(3,4)):
        P(cx,4,2,"glass"); P(cx,5,2,"redstone_wire")
        P(cx,4,1,"stone"); P(cx,5,1,"redstone_wire")
        P(gx,5,1,"glass"); P(gx,6,1,"redstone_wire")
        P(gx,6,2,"stone")

def central(d, dA, dB):
    P = lambda *a, **k: put(d, *a, **k)
    P(-4,-6,0,"stone"); P(-4,-5,0,"lever",face="floor",facing="north")
    xsA = [-3] + list(range(-1,7))
    for i,x in enumerate(xsA):
        P(x,-6,0,"stone"); P(x,-5,0,"repeater",facing="west",delay=dA[i])
    P(-2,-5,0,"stone"); P(-2,-4,0,"redstone_torch")
    for z in (0,1):
        P(7,-6,z,"stone"); P(7,-5,z,"redstone_wire")
    for i,x in enumerate(range(6,-3,-1)):
        P(x,-6,1,"stone"); P(x,-5,1,"repeater",facing="east",delay=dB[i])
    P(-3,-5,1,"stone"); P(-3,-4,1,"redstone_torch")
    P(-3,-4,0,"note_block",powered="true")
    # U
    P(-4,-6,1,"stone"); P(-4,-5,1,"redstone_wire")
    P(-4,-6,2,"stone"); P(-4,-5,2,"redstone_wire")
    P(-3,-6,2,"stone"); P(-3,-5,2,"repeater",facing="west",delay=1)
    for x in range(-2,7):
        P(x,-6,2,"stone"); P(x,-5,2,"redstone_wire")
    # C chain: E_C watches the note block
    obs(d,(-4,-4,0),(-3,-4,0))
    d.remove(-2,-3,0)
    chain(d, [(-3,-3,0),(-2,-3,0),(-1,-3,0),(-1,-4,0)] + [(x,-4,0) for x in range(0,8)], (-4,-3,0))
    # I chain (left only) and R_top
    chain(d, [(-4,-4,2),(-4,-4,1)] + [(-4,y,1) for y in range(-3,6)] + [(-3,5,1)], (-4,-5,2))
    P(-2,5,1,"repeater",facing="west",delay=4)

def build(dA=None, dB=None):
    dA = dA or [1,2,2,2,1,1,1,1,1]              # rep(-3), x=-1..6
    dB = dB or [1,1,1,1, 1,1,1, 4,4]            # x=6..3 | 2,1,0 | -1,-2
    L = left_half()
    d = Design("open")
    d.merge(L.mirrored_x(3)); d.merge(L)
    top_pair(d)
    central(d, dA, dB)
    return d

if __name__ == "__main__":
    d = build(); d.save("door3.json"); print(len(d.blocks), d.bbox())
