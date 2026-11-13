from build1 import make as make1
def make():
    d = make1()
    S = lambda *a, **k: d.set(*a, **k)
    st = lambda x,y,z: d.set(x,y,z,"stone")
    def dust(x,y,z,sup=True):
        d.set(x,y,z,"redstone_wire")
        if sup and d.get(x,y-1,z) is None: st(x,y-1,z)
    # --- corridor mechanics (top) ---
    S(1,5,0,"sticky_piston",facing="down")   # A
    S(1,4,0,"sticky_piston",facing="down")   # B
    S(3,3,0,"sticky_piston",facing="west")   # V
    st(1,3,0)   # S
    st(2,3,0)   # X
    # --- L source for board: continue tower at x=-3 ---
    # wall torch (-3,2,1) lit when L=0 (already). block above (-3,3,1) powered when L=0
    st(-3,3,1)
    d.set(-3,4,1,"redstone_torch",lit=False)    # lit when L=1; L=0 -> off
    st(-3,5,1)
    # --- board plane y=6 ---
    dust(-3,6,1)                      # D_L
    d.set(-3,6,2,"observer",facing="north"); st(-3,5,2)   # O_P
    dust(-3,6,3)                      # P0
    # V delay chain
    d.set(-3,6,4,"repeater",facing="north",delay=1); st(-3,5,4)
    d.set(-3,6,5,"repeater",facing="north",delay=1); st(-3,5,5)
    dust(-3,6,6)                      # V0
    # east branch from P0
    for x in (-2,-1,0): dust(x,6,3)
    # R_A at (-2,6,2) facing south, O_A at (-2,6,1) facing south
    d.set(-2,6,2,"repeater",facing="south",delay=4); st(-2,5,2)
    d.set(-2,6,1,"observer",facing="south"); st(-2,5,1)
    # A line along z=0
    for x in (-2,-1,0): dust(x,6,0)
    dust(1,6,0,sup=False)
    # B descent at x=0: (0,6,3) start (already), (0,5,4), (0,4,5), lane (1,4,5..1)
    dust(0,5,4); dust(0,4,5,sup=False)
    for z in range(5,0,-1): dust(1,4,z,sup=False)
    return d
if __name__=="__main__":
    d=make(); d.save("d2.json")
