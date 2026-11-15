def build2(snake=True, rs2_delay=2):
    d = Design("closed")
    d.fill(0,0,0,2,2,0,"stone")
    for y in range(3):
        d.set(-2,y,0,"sticky_piston",facing="east",extended=True)
        d.set(-1,y,0,"piston_head",facing="east",type="sticky")
        d.set(4,y,0,"sticky_piston",facing="west",extended=True)
        d.set(3,y,0,"piston_head",facing="west",type="sticky")
    d.set(0,-1,0,"stone"); d.set(2,-1,0,"stone"); d.set(0,3,0,"stone")
    # bottom piston + observer snake (12 observers)
    d.set(1,-2,0,"sticky_piston",facing="up")
    chain = [((-2,-1,0),"up"), ((-2,-2,0),"up"), ((-2,-2,1),"north"), ((-1,-2,1),"west"),
             ((0,-2,1),"west"), ((1,-2,1),"west"), ((2,-2,1),"west"), ((3,-2,1),"west"),
             ((4,-2,1),"west"), ((4,-2,0),"south"), ((3,-2,0),"east"), ((2,-2,0),"east")]
    for pos, f in chain:
        d.set(*pos,"observer",facing=f)
    # top mechanics
    d.set(1,5,0,"sticky_piston",facing="down")
    d.set(1,4,0,"sticky_piston",facing="down")
    d.set(3,3,0,"sticky_piston",facing="west")
    # west: A pulse stretcher + relay
    d.set(0,4,0,"observer",facing="west")
    d.set(-1,4,0,"observer",facing="up")
    d.set(-1,5,0,"repeater",facing="west",delay=4)
    d.set(0,5,0,"stone")
    d.set(-2,4,0,"glass"); d.set(-2,5,0,"redstone_wire")
    d.set(-2,4,1,"stone"); d.set(-2,5,1,"redstone_wire")
    d.set(-1,4,1,"observer",facing="east")
    # east: S chain
    d.set(3,4,0,"observer",facing="up")
    d.set(3,5,0,"repeater",facing="south",delay=rs2_delay)
    # z=1 arch
    d.set(0,5,1,"stone"); d.set(0,6,1,"lever",face="floor",facing="north")
    d.set(-1,3,1,"redstone_wire"); d.set(0,4,1,"redstone_wire")
    d.set(1,4,1,"repeater",facing="west",delay=1)
    d.set(2,4,1,"redstone_wire"); d.set(3,3,1,"redstone_wire")
    d.set(3,4,1,"glass"); d.set(3,5,1,"redstone_wire")
    d.set(4,3,1,"glass"); d.set(4,4,1,"redstone_wire")
    d.set(-2,2,1,"redstone_wall_torch",facing="west")
    d.set(-2,0,1,"stone"); d.set(-2,1,1,"redstone_wire")
    d.set(4,2,1,"redstone_wall_torch",facing="east")
    d.set(4,0,1,"stone"); d.set(4,1,1,"redstone_wire")
    # P1 path
    d.set(4,3,0,"glass"); d.set(4,4,0,"repeater",facing="south",delay=1)
    d.set(4,3,-1,"glass"); d.set(4,4,-1,"redstone_wire")
    d.set(3,4,-1,"observer",facing="east")
    d.set(2,4,-1,"stone")
    d.set(1,4,-1,"redstone_wire",north="side",south="side",east="side",west="side")
    return d
d2 = build2()
d2.save("d2.json")
print(trace(d2, flips=2, limit=0))
print(trace(d2, flips=1, grep="(1,", limit=120))
