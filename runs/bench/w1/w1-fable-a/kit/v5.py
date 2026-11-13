def v5(p1d=4, cd=(4,4,4,1)):
    d = base()
    d.set(1,4,1,"lever",face="floor",facing="north")
    for x in (0,2): d.set(x,4,1,"redstone_wire")
    for sx,cx in ((-2,-1),(4,3)):
        d.set(cx,3,1,"redstone_wire"); d.set(cx,3,2,"redstone_wire")
        d.set(sx,1,2,"stone"); d.set(sx,2,2,"redstone_wire")
        d.set(sx,1,1,"stone"); d.set(sx,2,1,"redstone_wire"); d.set(sx,3,1,"stone")
    # east: O_L observer under dust
    d.set(4,1,2,"observer",facing="up"); d.set(4,0,2,"stone")
    d.set(4,-2,2,"stone"); d.set(4,-1,2,"redstone_wire")
    # west: transmission piston with redstone block
    d.set(-2,0,1,"sticky_piston",facing="down"); d.set(-2,-1,1,"redstone_block")
    d.set(-2,-3,1,"stone")
    # z=3
    dust(d,-2,3); rep(d,-1,3,"west",cd[1]); rep(d,0,3,"west",cd[2]); dust(d,1,3)
    # z=2
    rep(d,-2,2,"north",cd[0]); dust(d,-1,2); rep(d,0,2,"east",cd[3]); dust(d,1,2)
    # z=1
    rep(d,-1,1,"south",1); fl(d,0,1,"observer",facing="west"); rep(d,1,1,"west",1); dust(d,2,1); dust(d,3,1); dust(d,4,1)
    d.set(3,-1,1,"stone")
    # z=0
    dust(d,-2,0); d.set(2,-3,0,"glass"); d.set(2,-2,0,"redstone_wire")
    # z=-1
    dust(d,-2,-1); fl(d,-1,-1,"observer",facing="west"); rep(d,0,-1,"west",p1d); dust(d,1,-1)
    fl(d,2,-1,"observer",facing="west"); dust(d,3,-1); dust(d,4,-1)
    return d
d5 = v5(); d5.save("v5.json")
r = test(d5); print(r.text[:900])
if not r.valid: show(d5, keys=KEYS+["(-2,-2,0)","(-2,-2,1)","(4,-1,2)","(-1,-2,1)"])
