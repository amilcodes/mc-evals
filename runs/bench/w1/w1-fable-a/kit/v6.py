def v6(p1d=4, cd=(4,4,4,1), hd=1):
    d = base()
    d.set(1,4,1,"lever",face="floor",facing="north")
    for x in (0,2): d.set(x,4,1,"redstone_wire")
    for sx,cx in ((-2,-1),(4,3)):
        d.set(cx,3,1,"redstone_wire"); d.set(cx,3,2,"redstone_wire")
        d.set(sx,1,2,"stone"); d.set(sx,2,2,"redstone_wire")
        d.set(sx,1,1,"stone"); d.set(sx,2,1,"redstone_wire"); d.set(sx,3,1,"stone")
    # west: L' block at z=1
    d.set(-2,0,1,"sticky_piston",facing="down"); d.set(-2,-1,1,"redstone_block"); d.set(-2,-3,1,"stone")
    # east: L' block at z=2 (chain start)
    d.set(4,0,2,"sticky_piston",facing="down"); d.set(4,-1,2,"redstone_block"); d.set(4,-3,2,"stone")
    # z=2 chain westward
    rep(d,3,2,"east",cd[0]); rep(d,2,2,"east",cd[1]); rep(d,1,2,"east",cd[2]); rep(d,0,2,"east",cd[3]); dust(d,-1,2)
    # z=1
    rep(d,-1,1,"south",hd); dust(d,0,1)
    d.set(1,-3,1,"note_block"); d.set(1,-2,1,"observer",facing="down")
    fl(d,4,1,"observer",facing="south")
    # z=0
    dust(d,-2,0); d.set(0,-3,0,"glass"); d.set(0,-2,0,"redstone_wire")
    # z=-1
    dust(d,-2,-1); fl(d,-1,-1,"observer",facing="west"); rep(d,0,-1,"west",p1d); dust(d,1,-1)
    fl(d,2,-1,"observer",facing="west"); dust(d,3,-1); dust(d,4,-1)
    return d
d6 = v6(); d6.save("v6.json")
r = test(d6); print(r.text[:900])
if not r.valid: show(d6, keys=KEYS+["(1,-2,1)","(4,-2,1)","(0,-2,1)"])
else: print(robust(d6,(1,4,1)))
