def build():
    d = Design("open")
    S="stone"; W="redstone_wire"
    def sp(x,y,z,f): d.set(x,y,z,"sticky_piston",facing=f)
    def dust(x,y,z,b=S): d.set(x,y-1,z,b); d.set(x,y,z,W)
    # mechanism z=0
    sp(-3,1,0,"east"); sp(-2,1,0,"east"); d.set(-1,1,0,S); d.set(-1,2,0,S); sp(-1,3,0,"down")
    d.set(-1,0,0,S); d.set(-1,-1,0,"obsidian")
    d.set(-3,0,0,"observer",facing="up"); dust(-3,-1,0); dust(-2,0,0)
    # A lane
    d.set(-2,3,0,"observer",facing="east")
    d.set(-3,2,0,"glass"); d.set(-3,3,0,"repeater",facing="east",delay=4)
    d.set(-4,3,0,S); d.set(-4,2,0,W); d.set(-4,1,0,S)
    # simple pistons
    for y in (0,1): d.set(3,y,0,S); sp(4,y,0,"west")
    d.set(3,2,0,S)
    for x in (0,1,2): d.set(x,3,0,S); sp(x,4,0,"down")
    for x in (0,1): d.set(x,-1,0,S); sp(x,-2,0,"up")
    d.set(2,-1,0,S)
    # tower
    d.set(0,-2,1,S); d.set(1,-2,1,"lever",face="wall",facing="east")
    d.set(-1,-2,1,"redstone_wall_torch",facing="west"); d.set(-1,-1,1,S)
    d.set(-2,-2,1,"observer",facing="east"); dust(-3,-1,1)
    d.set(-1,-1,2,"redstone_wall_torch",facing="south")
    d.set(-2,-2,2,S); d.set(-2,-1,2,"repeater",facing="east",delay=4)
    # J
    dust(-3,0,2); dust(-2,1,2); dust(-2,2,1); dust(-3,3,1,"glass"); dust(-3,3,2)
    d.set(-2,2,2,"glass"); d.set(-2,3,2,"repeater",facing="west",delay=1)
    d.set(-1,3,2,W); d.set(-1,3,1,"observer",facing="south")
    # top row
    for x in (0,1,2): d.set(x,4,2,W)
    d.set(0,4,1,"repeater",facing="south",delay=1); d.set(2,4,1,"repeater",facing="south",delay=1); d.set(1,4,1,W)
    d.set(3,3,2,W); dust(4,2,2); dust(4,1,1)
    return d
