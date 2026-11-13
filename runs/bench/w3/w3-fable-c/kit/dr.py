def build():
    d = Design("open")
    S="stone"; W="redstone_wire"; G="glass"
    def sp(x,y,z,f): d.set(x,y,z,"sticky_piston",facing=f)
    def dust(x,y,z,b=S): d.set(x,y-1,z,b); d.set(x,y,z,W)
    # mechanism z=0
    sp(-3,1,0,"east"); sp(-2,1,0,"east"); d.set(-1,1,0,S); d.set(-1,2,0,S); sp(-1,3,0,"down")
    d.set(-1,0,0,S); d.set(-1,-1,0,"obsidian")
    d.set(-3,0,0,"observer",facing="up"); dust(-3,-1,0); dust(-2,0,0)
    dust(-4,-1,0); dust(-5,-1,0)
    # A lane (dk)
    d.set(-2,3,0,"observer",facing="east")
    d.set(-3,2,0,G); d.set(-3,3,0,"repeater",facing="east",delay=4)
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
    d.set(-2,-1,1,"redstone_wall_torch",facing="west",lit=False)
    d.set(-2,0,1,"observer",facing="down"); d.set(-2,1,1,S)
    # hold chain
    d.set(-3,-2,1,S); d.set(-3,-1,1,"repeater",facing="east",delay=4)
    d.set(-4,-2,1,S); d.set(-4,-1,1,"repeater",facing="east",delay=1)
    d.set(-5,-1,1,S)
    # link
    d.set(-5,0,1,W); dust(-4,1,1); dust(-3,1,1)
    dust(-6,0,1); dust(-6,1,0,G); dust(-6,2,1,G); dust(-5,3,1,G)
    d.set(-4,2,1,S); d.set(-4,3,1,"repeater",facing="west",delay=1)
    dust(-3,3,1,G)
    d.set(-2,3,1,"observer",facing="west"); d.set(-1,3,1,S)
    d.set(-2,4,1,W)
    # top bus
    d.set(-1,4,1,"repeater",facing="west",delay=1)
    d.set(0,4,1,S); d.set(1,4,1,W,north="side",south="side",east="side",west="side"); d.set(2,4,1,S)
    d.set(3,3,1,S); d.set(3,4,1,"repeater",facing="west",delay=1)
    dust(4,4,1); dust(4,3,0)
    return d
