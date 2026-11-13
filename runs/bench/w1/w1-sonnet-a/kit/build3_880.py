from build1 import make as make1
def make():
    d = make1()
    S = lambda *a, **k: d.set(*a, **k)
    st = lambda x,y,z: d.set(x,y,z,"stone")
    def dust(x,y,z,sup=True):
        d.set(x,y,z,"redstone_wire")
        if sup and d.get(x,y-1,z) is None: st(x,y-1,z)
    def rep(x,y,z,facing,delay=1,sup=True):
        d.set(x,y,z,"repeater",facing=facing,delay=delay)
        if sup and d.get(x,y-1,z) is None: st(x,y-1,z)
    # corridor mechanics
    S(1,5,0,"sticky_piston",facing="down"); S(1,4,0,"sticky_piston",facing="down")
    S(3,3,0,"sticky_piston",facing="west"); st(1,3,0); st(2,3,0)
    # tower extension
    st(-3,3,1); d.set(-3,4,1,"redstone_torch",lit=False); st(-3,5,1)
    dust(-3,6,1)   # D_L
    # observers around D_L
    d.set(-3,6,2,"observer",facing="north")   # O_S -> back (-3,6,3)
    d.set(-2,6,1,"observer",facing="west")    # O_E -> back (-1,6,1)
    d.set(-3,6,0,"observer",facing="south")   # O_N -> back (-3,6,-1)
    # ---- A chain ----
    rep(-1,6,1,"west",4)                       # R_A
    d.set(0,6,1,"observer",facing="west")      # O_A -> back (1,6,1)
    dust(1,6,1); dust(1,6,0,sup=False)
    # ---- B-direct row (+z) ----
    for x in range(-3,4): dust(x,6,3)
    dust(3,5,4); dust(3,4,5)
    rep(2,4,5,"east",1,sup=False)              # R_D (support wall (2,3,5))
    for z in range(5,0,-1): dust(1,4,z,sup=False)
    # ---- gated chain (comparator gate), y=4 near the tower ----
    dust(-2,4,1)    # D_L2 (powered by torch (-3,4,1) when L=1)
    d.set(-2,4,0,"observer",facing="south")      # O_2 -> back (-2,4,-1)
    dust(-2,4,-1); dust(-1,4,-1); dust(-1,4,0)
    d.set(-1,4,1,"comparator",facing="north",mode="subtract"); st(-1,3,1)
    rep(-1,4,2,"north",4); rep(-1,4,3,"north",1)
    d.set(-1,4,4,"observer",facing="north")      # O_B -> back (-1,4,5)
    dust(-1,4,5); dust(0,4,5,sup=False)
    # ---- V chain (-z side) ----
    rep(-3,6,-1,"south",1)                     # r1 (input from O_N at south)
    dust(-3,6,-2)
    for x in (-2,-1): dust(x,6,-2)
    rep(0,6,-2,"west",1)                       # refresh (flows east)
    for x in (1,2,3,4): dust(x,6,-2)
    dust(4,5,-3); dust(4,4,-4); dust(4,3,-5)
    dust(3,3,-5,sup=False)
    dust(3,3,-4,sup=False)
    rep(3,3,-3,"north",1,sup=False)            # refresh (flows +z)
    for z in (-2,-1): dust(3,3,z,sup=False)
    return d
if __name__=="__main__":
    d=make(); d.save("d3.json")
