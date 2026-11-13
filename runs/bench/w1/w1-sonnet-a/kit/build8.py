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
    # remove x=-3 pieces from build1
    d.remove(-3,2,1); d.remove(-3,-2,3); d.remove(-3,-3,3)
    # lever moved: south of trunk west end
    d.set(-3,-3,3,"lever",face="wall",facing="west")
    # corridor mechanics
    S(1,5,0,"sticky_piston",facing="down"); S(1,4,0,"sticky_piston",facing="down")
    S(3,3,0,"sticky_piston",facing="west"); st(1,3,0); st(2,3,0)
    # upper tower at (-2,y,2): wall torch on south face of block (-2,2,1)
    d.set(-2,2,2,"redstone_wall_torch",facing="south",lit=True)
    st(-2,3,2)
    d.set(-2,4,2,"redstone_torch",lit=False)
    st(-2,5,2)
    dust(-2,6,2)   # D_L
    d.set(-2,6,1,"observer",facing="south")   # O_N -> back (-2,6,0)
    d.set(-1,6,2,"observer",facing="west")    # O_E -> back (0,6,2)
    # ---- A chain ----
    rep(0,6,2,"west",4)                        # R_A (input from O_E at west)
    d.set(1,6,2,"observer",facing="west")      # O_A watches R_A; back (2,6,2)
    dust(2,6,2); dust(2,6,1); dust(2,6,0)
    dust(1,6,0,sup=False)
    st(3,6,0)                                  # cut stone
    for z in range(3,0,-1): dust(1,4,z,sup=False)
    st(0,6,0); st(1,5,1)
    dust(0,5,0); dust(0,5,1); dust(0,4,2,sup=False)
    # ---- gated chain ----
    dust(-2,4,1)    # D_L2 (powered by torch (-2,4,2) when L=1)
    d.set(-2,4,0,"observer",facing="south")      # O_2 -> back (-2,4,-1)
    dust(-2,4,-1); dust(-1,4,-1)
    dust(-1,4,0)
    d.set(-1,4,1,"comparator",facing="north",mode="subtract"); st(-1,3,1)
    rep(-1,4,2,"north",1)
    rep(-1,4,3,"north",4)
    d.set(0,4,3,"observer",facing="west")
    # ---- V chain (-z side) ----
    rep(-2,6,0,"south",1)                      # r1
    dust(-2,6,-1); dust(-1,6,-1)
    st(-2,5,-1); st(-1,5,-1)                   # supports/cuts above gate path
    dust(0,5,-1)
    rep(1,5,-1,"west",1); rep(2,5,-1,"west",1)
    dust(3,5,-1)
    st(3,4,0)                                  # block above V
    dust(3,5,0,sup=False)                      # on top of block (3,4,0)
    return d
if __name__=="__main__":
    d=make(); d.save("d6.json")
