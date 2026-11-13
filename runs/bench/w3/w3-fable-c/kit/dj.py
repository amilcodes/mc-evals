def build():
    d = Design("open")
    S="stone"; W="redstone_wire"
    def sp(x,y,z,f): d.set(x,y,z,"sticky_piston",facing=f)
    # mechanism z=0
    sp(-3,1,0,"east"); sp(-2,1,0,"east"); d.set(-1,1,0,S); d.set(-1,2,0,S); sp(-1,3,0,"down")
    d.set(-1,0,0,S); d.set(-1,-1,0,"obsidian")
    d.set(-3,0,0,"observer",facing="up"); d.set(-3,-2,0,S); d.set(-3,-1,0,W)
    d.set(-2,-1,0,S); d.set(-2,0,0,W)
    # A lane (west)
    d.set(-4,0,0,S); d.set(-4,1,0,"repeater",facing="west",delay=1)
    d.set(-5,1,0,S); d.set(-5,2,0,W)
    d.set(-4,2,0,S); d.set(-4,3,0,W)
    d.set(-3,2,0,"glass"); d.set(-3,3,0,"repeater",facing="east",delay=4)
    d.set(-2,3,0,"observer",facing="east")
    # simple pistons
    for y in (0,1): d.set(3,y,0,S); sp(4,y,0,"west")
    d.set(3,2,0,S)
    for x in (0,1,2): d.set(x,3,0,S); sp(x,4,0,"down")
    for x in (0,1): d.set(x,-1,0,S); sp(x,-2,0,"up")
    d.set(2,-1,0,S)
    # tower
    d.set(0,-2,1,S); d.set(1,-2,1,"lever",face="wall",facing="east")
    d.set(-1,-2,1,"redstone_wall_torch",facing="west"); d.set(-1,-1,1,S)
    d.set(-2,-2,1,"observer",facing="east"); d.set(-3,-2,1,S); d.set(-3,-1,1,W)
    d.set(-1,-2,2,S); d.set(-1,-1,2,"repeater",facing="north",delay=4)
    d.set(-1,-1,3,S); d.set(-2,-1,3,"redstone_wall_torch",facing="west")
    # J
    for (x,y,z,b) in [(-2,-1,2,S),(-3,-1,2,S),(-3,0,3,S),(-3,1,2,"glass"),(-2,2,2,S),(-2,2,1,S),(-2,2,3,S)]:
        d.set(x,y-1,z,b); d.set(x,y,z,W)
    d.set(-1,3,3,W); d.set(0,4,3,W)
    # W' lane
    d.set(-1,3,1,"repeater",facing="south",delay=1); d.set(-1,3,2,"observer",facing="south")
    # top row
    d.set(1,4,3,"repeater",facing="west",delay=1); d.set(2,4,3,W)
    d.set(3,3,3,S); d.set(3,4,3,W); d.set(4,2,3,S); d.set(4,3,3,W)
    d.set(4,1,2,S); d.set(4,2,2,W); d.set(4,0,1,S); d.set(4,1,1,W)
    d.set(0,4,2,"repeater",facing="south",delay=1); d.set(0,4,1,S)
    d.set(1,4,1,W,north="side",south="side",east="side",west="side"); d.set(2,4,1,S)
    return d
