def build_v1():
    d = Design("open")
    S = lambda x,y,z: d.set(x,y,z,"stone")
    G = lambda x,y,z: d.set(x,y,z,"glass")
    W = lambda x,y,z: d.set(x,y,z,"redstone_wire")
    def dust_on(x,y,z,sup="stone"):
        d.set(x,y-1,z,sup); W(x,y,z)
    # --- mechanism
    d.set(-3,1,0,"sticky_piston",facing="east")
    d.set(-2,1,0,"sticky_piston",facing="east")
    S(-1,1,0); S(-1,2,0); S(-1,0,0)
    d.set(-1,3,0,"sticky_piston",facing="down")
    # frame statics
    S(3,0,0); S(3,2,0)
    # simple pistons
    for x in range(3):
        S(x,3,0); d.set(x,4,0,"sticky_piston",facing="down")
        S(x,-1,0); d.set(x,-2,0,"sticky_piston",facing="up")
    S(3,1,0); d.set(4,1,0,"sticky_piston",facing="west")
    # crosses
    S(-2,0,1); d.set(-2,1,1,"redstone_wire",north="side",south="side",east="side",west="side")
    S(-2,0,-1); d.set(-2,1,-1,"redstone_wire",north="side",south="side",east="side",west="side")
    # O_a
    d.set(-2,-1,1,"observer",facing="down")
    dust_on(-2,-2,1)
    S(-2,-3,2); d.set(-2,-2,2,"lever",face="floor",facing="north")
    # south bottom bus
    for x in range(-1,5): dust_on(x,-2,2)
    for x in range(3):
        S(x,-3,1); d.set(x,-2,1,"repeater",facing="south",delay=1)
    # crossing at x=3
    for z in (1,0,-1,-2): dust_on(3,-2,z)
    # right tower
    dust_on(4,-1,1)            # A on stone (4,-2,1)
    dust_on(4,0,2,"glass")     # C
    dust_on(4,1,1,"glass")     # D
    dust_on(4,2,2,"glass")     # E
    W(3,3,2)                   # F on wall
    for x in range(3):
        W(x,4,2); d.set(x,4,1,"repeater",facing="south",delay=1)
    # top-left L path
    S(-1,3,2); d.set(-1,4,2,"repeater",facing="east",delay=1)
    dust_on(-2,4,2); dust_on(-3,4,2); dust_on(-3,4,1); dust_on(-3,4,0,"glass"); dust_on(-3,4,-1)
    # H
    d.set(-2,2,-1,"observer",facing="up")
    d.set(-2,3,-1,"repeater",facing="west",delay=3)
    S(-1,3,-1)
    # north platform
    for x in (2,1,0): dust_on(x,-2,-2)
    S(-1,-3,-2); d.set(-1,-2,-2,"repeater",facing="east",delay=4)
    S(-2,-3,-2); d.set(-2,-2,-2,"repeater",facing="east",delay=3)
    dust_on(-3,-2,-2); S(-3,-1,-2)
    S(2,-3,-1); d.set(2,-2,-1,"repeater",facing="east",delay=4)
    S(1,-3,-1); d.set(1,-2,-1,"repeater",facing="east",delay=4)
    S(0,-3,-1); d.set(0,-2,-1,"repeater",facing="east",delay=3)
    dust_on(-1,-2,-1)
    S(-2,-3,-1); d.set(-2,-2,-1,"repeater",facing="east",delay=1)
    S(-3,-3,-1); d.set(-3,-2,-1,"comparator",facing="east",mode="subtract")
    # tower for tau
    dust_on(-4,-2,-1)
    dust_on(-4,-1,-2)
    dust_on(-4,0,-1,"glass")
    dust_on(-4,1,-2,"glass")
    dust_on(-4,2,-1,"glass")
    dust_on(-4,2,0)
    # O_c
    d.set(-3,1,-2,"observer",facing="west")
    S(-2,1,-2)
    return d
v1 = build_v1()
v1.save("v1.json")
print(len(v1.blocks), v1.bbox())
r = test(v1)
print(r)
