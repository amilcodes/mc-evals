from pdbuild import Design
def make():
    d = Design("open")
    S = lambda *a, **k: d.set(*a, **k)
    st = lambda x,y,z: d.set(x,y,z,"stone")
    wire = lambda x,y,z: d.set(x,y,z,"redstone_wire")
    # ---------- ring stones & door pistons ----------
    # left L1 (y=1), L2 (y=2): tower at (-2,y,1)
    S(-2,1,0,"sticky_piston",facing="east"); st(-1,1,0)
    S(-2,2,0,"sticky_piston",facing="east"); st(-1,2,0)
    st(-1,0,0)
    # right R1,R2
    S(4,1,0,"sticky_piston",facing="west"); st(3,1,0)
    S(4,2,0,"sticky_piston",facing="west"); st(3,2,0)
    st(3,0,0)
    # bottom B0..B2
    for x in range(3):
        S(x,-2,0,"sticky_piston",facing="up"); st(x,-1,0)
    # top ring static (0,3)
    st(0,3,0)
    # ---------- L trunk (bottom) ----------
    # trunk along z=3 at y=-2, x=-2..4 ; supports y=-3
    for x in range(-2,5):
        wire(x,-2,3); st(x,-3,3)
    # branch dust + repeaters for bottom pistons
    for x in range(3):
        wire(x,-2,2); st(x,-3,2)
        d.set(x,-2,1,"repeater",facing="south",delay=1); st(x,-3,1)
    # tower bases fed by dust aimed north
    for tx in (-2,4):
        wire(tx,-2,2); st(tx,-3,2)
        st(tx,-2,1)   # base block
    # lever at west end of trunk
    d.set(-3,-2,3,"lever",face="floor",facing="north"); st(-3,-3,3)
    # towers: y=-2 block, -1 torch(lit), 0 block, 1 torch, 2 block, 3 torch, 4 block, 5 torch, 6 block
    def tower(tx, top):
        for y in range(-1, top+1):
            k = y+2   # 0 base
            if y%2==0:
                st(tx,y,1)
            else:
                lit = (y%4==3)  # y=-1 lit,1 unlit,3 lit,5 unlit ... for L=0
                lit = ((y+1)%4==0)
                d.set(tx,y,1,"redstone_torch",lit=lit)
    tower(-2,2); tower(4,2)
    # wall torch on west face of left tower block (-2,2,1), lit when L=0
    d.set(-3,2,1,'redstone_wall_torch',facing='west',lit=True)
    return d
if __name__=="__main__":
    d=make(); d.save("d1.json")
