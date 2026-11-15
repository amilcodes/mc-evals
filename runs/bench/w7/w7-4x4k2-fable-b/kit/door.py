from pdbuild import Design

DIRS = {(1,0,0):"east",(-1,0,0):"west",(0,1,0):"up",(0,-1,0):"down",(0,0,1):"south",(0,0,-1):"north"}

def obs(d, pos, watch):
    """observer at pos watching the adjacent cell `watch`"""
    delta = tuple(w-p for p,w in zip(pos,watch))
    assert delta in DIRS, (pos, watch)
    assert d.get(*pos) is None, ("occupied", pos, d.get(*pos))
    d.set(*pos, "observer", facing=DIRS[delta])

def chain(d, cells, watch):
    """observers along cells; first watches `watch`, each next watches the previous"""
    prev = watch
    for c in cells:
        obs(d, c, prev); prev = c

def put(d, x,y,z, block, **props):
    assert d.get(x,y,z) is None, ("occupied", (x,y,z), d.get(x,y,z), block)
    d.set(x,y,z,block,**props)

def left_half():
    d = Design("open")
    P = lambda *a, **k: put(d, *a, **k)
    # ---- row 3 (O lane): delivers (1,3) via (0,3)
    P(-3,3,0,"sticky_piston",facing="east"); P(-2,3,0,"sticky_piston",facing="east"); P(-1,3,0,"stone")
    P(-3,2,1,"stone"); P(-3,3,1,"repeater",facing="south",delay=4)
    P(-2,3,1,"observer",facing="west")
    P(-3,4,0,"observer",facing="west")
    P(-4,3,0,"glass"); P(-4,4,0,"repeater",facing="south",delay=4)
    P(-4,3,1,"stone"); P(-4,4,1,"redstone_wire")
    P(-4,3,2,"redstone_wire")                     # on tap observer (-4,2,2)
    P(-3,2,2,"stone"); P(-3,3,2,"redstone_wire")
    # ---- row 0 (O lane): delivers (1,0) via (0,0)
    P(-3,0,0,"sticky_piston",facing="east"); P(-2,0,0,"sticky_piston",facing="east"); P(-1,0,0,"stone")
    P(-3,-1,1,"stone"); P(-3,0,1,"repeater",facing="south",delay=4)
    P(-2,0,1,"observer",facing="west")
    P(-2,-1,0,"observer",facing="down")
    P(-2,-3,0,"stone"); P(-2,-2,0,"repeater",facing="south",delay=4)
    P(-3,-1,2,"stone"); P(-3,0,2,"redstone_wire")
    P(-2,-2,2,"stone"); P(-2,-1,2,"redstone_wire")
    P(-2,-2,1,"redstone_wire")                    # on tap observer (-2,-3,1)
    # ---- rows 1,2 (F singles)
    P(-2,2,0,"sticky_piston",facing="east"); P(-1,2,0,"stone")
    P(-2,1,0,"sticky_piston",facing="east"); P(-1,1,0,"stone")
    # ---- bottom: col 0 C single, col 1 I lane
    P(0,-2,0,"sticky_piston",facing="up"); P(0,-1,0,"stone")
    P(1,-3,0,"sticky_piston",facing="up"); P(1,-2,0,"sticky_piston",facing="up"); P(1,-1,0,"stone")
    P(1,-4,1,"stone"); P(1,-3,1,"repeater",facing="south",delay=4)
    P(1,-2,1,"observer",facing="down")
    P(1,-3,2,"redstone_wire")                     # on tap observer (1,-4,2)
    obs(d,(1,-4,2),(1,-5,2))                      # watches U dust
    # ---- top: col 0 C single
    P(0,5,0,"sticky_piston",facing="down"); P(0,4,0,"stone")
    # ---- top pair feed (R_top)
    P(-2,4,2,"stone"); P(-2,5,2,"repeater",facing="west",delay=4)
    # ---- O chain (left part), source E_O at (1,-4,3)
    chain(d, [(x,-4,3) for x in (0,-1,-2,-3,-4)], (1,-4,3))
    chain(d, [(-2,-4,2),(-2,-4,1),(-2,-3,1)], (-2,-4,3))            # row 0 tap
    chain(d, [(-4,y,3) for y in (-3,-2,-1,0,1)] + [(-4,1,2),(-4,2,2)], (-4,-4,3))   # row 3 tap
    chain(d, [(-3,1,2),(-2,1,2),(-2,2,2),(-2,2,1)], (-4,1,2))       # F tap
    # ---- I chain to the top pair; E_I watches U dust (-3,-5,2)
    chain(d, [(-3,-4,2),(-3,-3,2),(-4,-3,2),(-4,-2,2),(-5,-2,2)] + [(-5,y,2) for y in range(-1,6)] + [(-4,5,2),(-3,5,2)], (-3,-5,2))
    # ---- C chain top part: column from (-5,-3,0)
    chain(d, [(-5,y,0) for y in range(-2,6)] + [(-4,5,0),(-3,5,0),(-2,5,0),(-1,5,0)], (-5,-3,0))
    # bottom C tap
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
        P(cx,4,2,"stone"); P(cx,5,2,"redstone_wire")
        P(cx,4,1,"stone"); P(cx,5,1,"redstone_wire")
        P(gx,5,1,"glass"); P(gx,6,1,"redstone_wire")
        P(gx,6,2,"stone")

def central(d, dA, dB):
    """dA: delays for row A reps x=-4..7 ; dB: delays for row B reps x=7..-4"""
    P = lambda *a, **k: put(d, *a, **k)
    P(-5,-5,3,"stone"); d.set(-5,-5,4,"lever",face="wall",facing="south")
    P(-5,-4,3,"redstone_torch")
    for i,x in enumerate(range(-4,8)):
        P(x,-6,3,"stone"); P(x,-5,3,"repeater",facing="west",delay=dA[i])
    for z in (1,2,3):
        P(8,-6,z,"stone"); P(8,-5,z,"redstone_wire")
    for i,x in enumerate(range(7,-5,-1)):
        P(x,-6,1,"stone"); P(x,-5,1,"repeater",facing="east",delay=dB[i])
    P(-5,-5,1,"stone"); P(-5,-4,1,"redstone_torch")
    P(-5,-6,2,"stone"); P(-5,-5,2,"redstone_wire")
    P(-5,-4,2,"note_block",powered="true")
    P(-4,-6,2,"stone"); P(-4,-5,2,"repeater",facing="west",delay=1)
    for x in range(-3,7):
        P(x,-6,2,"stone"); P(x,-5,2,"redstone_wire")
    # E_O and the extra right link
    obs(d,(1,-4,3),(1,-5,3)); obs(d,(2,-4,3),(1,-4,3))
    # E_C and C chain seeds
    chain(d, [(-5,-3,2),(-5,-3,1),(-5,-3,0),(-5,-4,0)] + [(x,-4,0) for x in range(-4,9)] + [(8,-3,0)], (-5,-4,2))

def build(dA=None, dB=None):
    dA = dA or [3]*6 + [1]*6
    dB = dB or [2]*4 + [1]*8
    L = left_half()
    d = Design("open")
    d.merge(L.mirrored_x(3)); d.merge(L)
    # right C column bottom link is (8,-3,0) from central; mirrored column starts at (8,-2,0) watching (8,-3,0)
    top_pair(d)
    central(d, dA, dB)
    return d

if __name__ == "__main__":
    d = build(); d.save("door.json"); print(len(d.blocks), d.bbox())
