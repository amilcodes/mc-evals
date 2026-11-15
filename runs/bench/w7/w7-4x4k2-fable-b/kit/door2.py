from pdbuild import Design
from door import obs, chain, put, top_pair

def left_half():
    d = Design("open")
    P = lambda *a, **k: put(d, *a, **k)
    # row 3 (O lane)
    P(-3,3,0,"sticky_piston",facing="east"); P(-2,3,0,"sticky_piston",facing="east"); P(-1,3,0,"stone")
    P(-3,2,1,"stone"); P(-3,3,1,"repeater",facing="south",delay=4)
    P(-2,3,1,"observer",facing="west")
    P(-3,4,0,"observer",facing="west")
    P(-4,3,0,"glass"); P(-4,4,0,"repeater",facing="south",delay=4)
    P(-4,3,1,"stone"); P(-4,4,1,"redstone_wire")
    P(-4,3,2,"redstone_wire")
    P(-3,2,2,"stone"); P(-3,3,2,"redstone_wire")
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
    # top pair feed
    P(-2,4,2,"stone"); P(-2,5,2,"repeater",facing="west",delay=4)
    # O chain: E_O watches row B repeater (0,-5,1)
    chain(d, [(0,-4,1),(0,-4,2),(-1,-4,2),(-2,-4,2),(-2,-4,1),(-2,-3,1)], (0,-5,1))
    chain(d, [(-3,-3,1),(-4,-3,1)] + [(-4,y,1) for y in (-2,-1,0,1)] + [(-4,1,2),(-4,2,2)], (-2,-3,1))
    chain(d, [(-3,1,2),(-2,1,2),(-2,2,2),(-2,2,1)], (-4,1,2))
    # I chain
    chain(d, [(-3,-4,2),(-3,-3,2),(-4,-3,2),(-4,-2,2),(-5,-2,2)] + [(-5,y,2) for y in range(-1,6)] + [(-4,5,2),(-3,5,2)], (-3,-5,2))
    # C chain column
    chain(d, [(-5,y,0) for y in range(-3,6)] + [(-4,5,0),(-3,5,0),(-2,5,0),(-1,5,0)], (-5,-4,0))
    obs(d,(0,-3,0),(0,-4,0))
    return d

def central(d, dA, dB):
    P = lambda *a, **k: put(d, *a, **k)
    P(-5,-6,0,"stone"); P(-5,-5,0,"lever",face="floor",facing="north")
    # row A (z=0): rep(-4), block(-3), reps -2..7
    xsA = [-4] + list(range(-2,8))
    for i,x in enumerate(xsA):
        P(x,-6,0,"stone"); P(x,-5,0,"repeater",facing="west",delay=dA[i])
    P(-3,-5,0,"stone"); P(-3,-4,0,"redstone_torch")
    for z in (0,1):
        P(8,-6,z,"stone"); P(8,-5,z,"redstone_wire")
    # row B (z=1): reps 7..-3, then block (-4)
    for i,x in enumerate(range(7,-4,-1)):
        P(x,-6,1,"stone"); P(x,-5,1,"repeater",facing="east",delay=dB[i])
    P(-4,-5,1,"stone"); P(-4,-4,1,"redstone_torch")
    P(-4,-4,0,"note_block",powered="true")
    # U
    P(-5,-6,1,"stone"); P(-5,-5,1,"redstone_wire")
    P(-5,-6,2,"stone"); P(-5,-5,2,"redstone_wire")
    P(-4,-6,2,"stone"); P(-4,-5,2,"repeater",facing="west",delay=1)
    for x in range(-3,7):
        P(x,-6,2,"stone"); P(x,-5,2,"redstone_wire")
    # C chain: E_C watches the note block
    obs(d,(-5,-4,0),(-4,-4,0))
    d.remove(-2,-3,0)
    chain(d, [(-4,-3,0),(-3,-3,0),(-2,-3,0),(-1,-3,0),(-1,-4,0)] + [(x,-4,0) for x in range(0,9)], (-5,-3,0))

def build(dA=None, dB=None):
    dA = dA or [1,2,2,1,1,1,1,1,1,1,1]          # 11 reps
    dB = dB or [1,1,1,1,1, 1,1,1, 4,4,4]        # x=7..3 | 2,1,0 | -1,-2,-3
    L = left_half()
    d = Design("open")
    d.merge(L.mirrored_x(3)); d.merge(L)
    top_pair(d)
    central(d, dA, dB)
    return d

if __name__ == "__main__":
    d = build(); d.save("door2.json"); print(len(d.blocks), d.bbox())
