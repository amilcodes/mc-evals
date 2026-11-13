def v9(dl=(1,1,1), dc=(4,4,4), p1d=4, cross=True):
    d = Design("open")
    for y in (0,1,2):
        d.set(-2,y,0,"sticky_piston",facing="east"); d.set(-1,y,0,"stone")
        d.set(4,y,0,"sticky_piston",facing="west"); d.set(3,y,0,"stone")
    d.set(1,4,0,"sticky_piston",facing="down"); d.set(1,3,0,"stone")
    d.set(0,3,0,"stone"); d.set(2,3,0,"stone")
    d.set(1,-3,0,"sticky_piston",facing="up"); d.set(1,-2,0,"sticky_piston",facing="up")
    d.set(1,-1,0,"stone"); d.set(0,-1,0,"stone"); d.set(2,-1,0,"stone")
    d.set(3,-1,0,"sticky_piston",facing="west"); d.set(3,-2,0,"stone")
    # z=0 bottom: P1 trigger chain
    d.set(-2,-1,0,"observer",facing="up"); d.set(-2,-2,0,"stone")
    rep(d,-1,0,"west",p1d); dust(d,0,0)
    # north: P1-edge unit
    d.set(1,-3,-1,"note_block"); d.set(1,-2,-1,"observer",facing="down"); dust(d,0,-1)
    # north west column (late)
    d.set(-2,3,-1,"stone"); d.set(-2,2,-1,"redstone_wire"); d.set(-2,1,-1,"stone")
    d.set(-1,3,-1,"repeater",facing="east",delay=dl[2]); d.set(0,4,-1,"redstone_wire")
    d.set(1,4,-1,"repeater",facing="east",delay=dl[1]); d.set(2,4,-1,"redstone_wire")
    # z=0 top
    d.set(2,4,0,"repeater",facing="south",delay=dl[0])
    d.set(-2,3,0,"stone"); d.set(-2,4,0,"redstone_wire"); d.set(-1,3,0,"stone"); d.set(-1,4,0,"redstone_wire")
    d.set(0,4,0,"repeater",facing="west",delay=1)
    # south top
    d.set(-2,3,1,"stone"); d.set(-2,4,1,"lever",face="floor",facing="north")
    d.set(-1,3,1,"repeater",facing="west",delay=dc[0]); d.set(0,4,1,"redstone_wire")
    d.set(1,4,1,"repeater",facing="west",delay=dc[1]); d.set(2,4,1,"redstone_wire")
    d.set(3,3,1,"repeater",facing="west",delay=dc[2]); d.set(4,3,1,"stone")
    for sx in (-2,4):
        d.set(sx,2,1,"redstone_wire"); d.set(sx,1,1,"stone")
        d.set(sx,0,1,"sticky_piston",facing="down"); d.set(sx,-1,1,"redstone_block"); d.set(sx,-3,1,"stone")
    # south bottom row
    dust(d,-1,1); fl(d,0,1,"observer",facing="west"); fl(d,1,1,"stone"); fl(d,2,1,"observer",facing="east")
    if cross: fl(d,3,1,"redstone_wire",north="side",south="side",east="side",west="side")
    else: dust(d,3,1)
    return d
d9 = v9(); d9.save("v9.json")
r = test(d9); print(r.text[:1200])
if not r.valid: show(d9, keys=["(1,-3,0)","(1,-2,0)","(1,-1,0) ","(3,-1,0)","(2,-1,0)","(1,-2,1)","(-2,-2,0)","(-2,0,0)","(3,-2,1)","(0,-2,0)","(1,-2,-1)","(-1,-2,1)"])
else: print(robust(d9,(-2,4,1)))
