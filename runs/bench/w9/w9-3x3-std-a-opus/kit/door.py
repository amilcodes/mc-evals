def build():
    d = Design("open")
    S=lambda x,y,z,b="stone",**p: d.set(x,y,z,b,**p)
    # fixed frame
    S(-1,2,0); S(3,2,0); S(2,-1,0)
    # open state blocks: D1 (1,-1), D0 (0,-1); simple movers' blocks in frame
    S(1,-1,0); S(0,-1,0)
    S(-1,0,0); S(-1,1,0); S(3,0,0); S(3,1,0); S(0,3,0); S(1,3,0); S(2,3,0)
    # simple mover pistons (sticky, retracted, spit/fetch)
    S(-2,0,0,"sticky_piston",facing="east"); S(-2,1,0,"sticky_piston",facing="east")
    S(4,0,0,"sticky_piston",facing="west"); S(4,1,0,"sticky_piston",facing="west")
    for x in range(3): S(x,4,0,"sticky_piston",facing="down")
    # core
    S(1,-2,0,"sticky_piston",facing="up"); S(1,-3,0,"sticky_piston",facing="up")
    S(-1,-1,0,"sticky_piston",facing="east")
    # top ring
    S(-3,0,0,"observer",facing="down"); S(-3,1,0,"observer",facing="down")
    S(-3,2,0,"redstone_wire"); S(-2,2,0,"redstone_wire")
    S(-2,3,0,"glass"); S(-1,3,0,"redstone_wire"); S(-1,4,0,"glass"); S(-2,4,0,"redstone_wire")
    S(-1,5,0,"redstone_wire"); 
    for x in range(3): S(x,5,0,"redstone_wire")
    S(3,3,0); S(3,4,0,"redstone_wire"); S(4,2,0,"observer",facing="up"); S(4,3,0,"redstone_wire")
    # C chain start
    S(-3,-1,0,"redstone_wire"); S(-3,-2,0)
    S(-3,-1,1,"redstone_wire"); S(-3,-2,1,"observer",facing="down"); S(-3,-3,1,"observer",facing="down"); S(-3,-4,1,"observer",facing="down")
    S(-2,-1,1,"repeater",facing="west"); S(-2,-2,1); S(-1,-1,1)
    # P_low
    S(1,-2,1); S(2,-2,1,"repeater",facing="east"); S(2,-3,1)
    S(3,-2,1,"redstone_wire"); S(3,-3,1,"observer",facing="down"); S(3,-4,1,"observer",facing="down")
    S(3,-1,1); S(3,-2,0)  # cutters
    # Q
    S(1,-3,1); S(0,-3,1,"observer",facing="west"); S(-1,-3,1,"repeater",facing="west",delay=4); S(-1,-4,1)
    S(-2,-3,1,"redstone_wire"); S(-2,-4,1,"observer",facing="down")
    # LL level line z=1 y=-5
    for x in range(-3,4): S(x,-5,1,"redstone_wire"); S(x,-6,1)
    d.set(0,-6,2,"lever",face="wall",facing="south")
    # gate
    S(-2,-5,0,"redstone_wire"); S(-2,-6,0)
    S(-1,-5,0,"observer",facing="west")
    S(0,-5,0,"comparator",facing="west",mode="subtract"); S(0,-6,0)
    S(1,-5,0,"repeater",facing="west"); S(1,-6,0)
    S(2,-5,0,"repeater",facing="west"); S(2,-6,0)
    S(3,-5,0,"repeater",facing="west"); S(3,-6,0)
    S(4,-5,0,"redstone_wire"); S(4,-6,0)
    # T4
    S(3,-4,0,"observer",facing="down"); S(3,-3,0,"redstone_wire")
    S(2,-3,0,"repeater",facing="east"); S(2,-4,0); S(2,-2,0,"observer",facing="down")
    # T6
    S(4,-5,1,"repeater",facing="north"); S(4,-6,1)
    S(4,-4,1,"observer",facing="down"); S(4,-3,1,"observer",facing="down"); S(4,-2,1,"redstone_wire")
    return d
d = build(); d.save("door1.json")
def build2():
    d = build()
    for p in [(-2,2,0),(-2,3,0),(-1,3,0),(-1,4,0),(-2,4,0),(-1,5,0),(0,5,0),(1,5,0),(2,5,0),(3,3,0),(3,4,0),(4,2,0),(4,3,0),
              (4,-5,1),(4,-6,1),(4,-4,1),(4,-3,1),(4,-2,1),(4,-5,0),(4,-6,0),(3,-4,1)]:
        d.remove(*p)
    S=lambda x,y,z,b="stone",**p: d.set(x,y,z,b,**p)
    S(3,-5,1); S(3,-4,1,"redstone_wire")
    S(2,-3,0,"repeater",facing="east",delay=4)
    S(-2,2,0); S(-2,3,0,"redstone_wire"); S(-1,3,0); S(-1,4,0,"redstone_wire"); S(-1,5,0,"glass")
    S(-2,4,0,"glass"); S(-2,5,0,"redstone_wire"); S(-1,6,0,"redstone_wire")
    for x in range(3): S(x,5,0); S(x,6,0,"redstone_wire")
    S(3,4,0); S(3,5,0,"redstone_wire"); S(4,3,0,"observer",facing="up"); S(4,4,0,"redstone_wire"); S(4,2,0)
    return d
def build3():
    d = build2(); d.set(3,-3,0,"stone")
    for p in list(d.blocks):
        if p[0]==-3: d.remove(*p)
    for p in [(-2,-1,1),(-2,-2,1),(-1,-1,1)]: d.remove(*p)
    S=lambda x,y,z,b="stone",**p: d.set(x,y,z,b,**p)
    S(-1,-2,0,"observer",facing="down"); S(-1,-3,0,"observer",facing="down"); S(-1,-4,0,"observer",facing="down")
    for y in (-2,-1,0,1): S(-2,y,1,"observer",facing="down")
    S(-2,2,1,"redstone_wire")
    return d
def build4():
    d = build3()
    for p in [(0,4,0),(2,4,0),(0,5,0),(1,5,0),(2,5,0),(0,6,0),(1,6,0),(2,6,0),(-1,6,0),(-2,5,0),(-2,4,0),(-1,5,0),
              (-1,4,0),(-1,3,0),(-2,3,0),(-2,2,0),(3,4,0),(3,5,0),(4,3,0),(4,4,0),(4,2,0),(-2,2,1)]:
        d.remove(*p)
    S=lambda x,y,z,b="stone",**p: d.set(x,y,z,b,**p)
    S(-2,2,0,"sticky_piston",facing="east"); S(4,2,0,"sticky_piston",facing="west")
    for y in (2,3,4): S(-2,y,1,"observer",facing="down")
    for x in range(-2,5):
        if x>-2: S(x,4,1)
        S(x,5,1,"redstone_wire")
    S(-2,3,0); S(-2,4,0,"redstone_wire"); S(4,3,0); S(4,4,0,"redstone_wire")
    S(-2,-2,0,"observer",facing="east"); S(-2,-1,0,"observer",facing="down")
    S(4,-4,1,"redstone_wire"); S(4,-5,1)
    for y in (-3,-2,-1): S(4,y,1,"observer",facing="down")
    S(4,0,1)
    return d
def build5():
    d = build4(); d.set(-1,3,0,"stone"); d.set(-1,4,0,"redstone_wire")
    for x in range(-2,5): d.remove(x,5,1); d.remove(x,4,1)
    S=lambda x,y,z,b="stone",**p: d.set(x,y,z,b,**p)
    for x in range(-2,5): S(x,4,1,"redstone_wire")
    S(-1,3,1); S(3,3,1); S(4,3,1)
    S(0,4,0,"observer",facing="west")
    return d
def build6(var=0):
    d = build5()
    rm=[(x,-5,1) for x in range(-2,3)]+[(x,-6,1) for x in range(-3,5)]+[(0,-6,2),(-2,-5,0),(-2,-6,0),(-1,-5,0),(0,-5,0),(0,-6,0)]
    rm+=[(x,-5,0) for x in (1,2,3)]+[(x,-6,0) for x in (1,2,3)]+[(3,-4,0),(3,-3,0),(2,-3,0),(2,-4,0),(-1,-4,1),(-2,-4,1)]
    for p in rm: d.remove(*p)
    S=lambda x,y,z,b="stone",**p: d.set(x,y,z,b,**p)
    d.set(1,-4,1,"lever",face="floor",facing="north"); S(1,-5,1)
    S(0,-4,1,"redstone_wire"); S(0,-5,1); S(2,-4,1,"redstone_wire"); S(2,-5,1)
    S(-1,-4,1,"observer",facing="east"); S(-2,-4,1)
    S(-2,-4,0,"redstone_wire"); S(-2,-5,0)
    S(-1,-4,0,"observer",facing="west")
    S(0,-4,0,"comparator",facing="west",mode="subtract"); S(0,-5,0)
    S(1,-4,0,"repeater",facing="west",delay=4); S(1,-5,0)
    S(2,-4,0,"redstone_wire"); S(2,-5,0)
    S(2,-3,0,"observer",facing="down")
    return d
