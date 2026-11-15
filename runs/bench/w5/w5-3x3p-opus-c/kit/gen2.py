from pdbuild import Design
def build():
    d = Design("open")
    S=lambda x,y,z,b="stone",**p: d.set(x,y,z,b,**p)
    sp=lambda x,y,z,f: d.set(x,y,z,"sticky_piston",facing=f)
    W=lambda x,y,z: d.set(x,y,z,"redstone_wire")
    # mechanics z=0
    for x in range(3): sp(x,4,0,"down"); S(x,3,0)
    sp(4,0,0,"west"); sp(4,1,0,"west"); S(3,0,0); S(3,1,0); S(3,2,0)
    sp(-2,1,0,"east"); S(-1,1,0); S(-1,2,0)
    sp(0,-2,0,"up"); S(0,-1,0)
    sp(-3,0,0,"east"); sp(-2,0,0,"east"); S(-1,0,0)
    sp(1,-3,0,"up"); sp(1,-2,0,"up"); S(1,-1,0)
    S(2,-1,0)
    # lever
    S(0,-3,1); d.set(0,-2,1,"lever",face="floor",facing="north")
    # pulse4
    S(-1,-3,1,"glass"); W(-1,-2,1); d.set(-1,-1,1,"observer",facing="down")
    # X bus bottom
    for x in range(1,5): S(x,-3,1,"glass"); W(x,-2,1)
    d.set(3,-2,1,"repeater",facing="west",delay=1)
    # right zigzag
    for (x,y) in [(5,-1),(4,0),(5,1),(4,2),(5,3),(4,4),(3,5)]:
        S(x,y-1,1,"glass"); W(x,y,1)
    W(4,2,0)  # on PR1
    for x in range(3): S(x,4,1); W(x,5,1)
    S(-1,3,1); W(-1,4,1); S(-2,2,1); W(-2,3,1); S(-2,2,0); W(-2,3,0)
    # R0
    S(0,-4,0); d.set(0,-3,0,"repeater",facing="south",delay=2)
    S(0,-4,-1); W(0,-3,-1)
    # X+6 to S#1
    S(1,-4,-1); W(1,-3,-1); S(2,-4,-1); W(2,-3,-1); S(3,-3,-1); W(3,-2,-1); S(4,-2,-1); W(4,-1,-1)
    S(4,-2,0,"glass"); d.set(4,-1,0,"repeater",facing="north",delay=1); d.set(3,-1,0,"observer",facing="east")
    S(4,-4,-1); W(4,-3,-1)
    # XQ
    S(4,-4,0); W(4,-3,0); S(3,-4,0); d.set(3,-3,0,"repeater",facing="east",delay=3)
    S(2,-4,0); d.set(2,-3,0,"repeater",facing="east",delay=1)
    d.set(2,-2,0,"observer",facing="down")
    # XM
    S(-1,-4,-1); d.set(-1,-3,-1,"repeater",facing="east",delay=4)
    S(-2,-4,-1); d.set(-2,-3,-1,"repeater",facing="east",delay=4)
    S(-3,-4,-1); W(-3,-3,-1)
    for (x,y) in [(-4,-2),(-3,-1),(-4,0),(-3,1)]:
        S(x,y-1,-1,"glass"); W(x,y,-1)
    S(-3,1,0); W(-3,2,0); S(-3,3,0)
    S(-3,-3,0); W(-3,-2,0); S(-2,-3,0); W(-2,-2,0)
    d.set(-2,-1,0,"observer",facing="down")
    return d
d=build()
d.save("door2.json")
