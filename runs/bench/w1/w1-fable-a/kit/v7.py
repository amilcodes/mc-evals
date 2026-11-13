def base7():
    d = Design("open")
    for y in (0,1,2):
        d.set(-2,y,0,"sticky_piston",facing="east"); d.set(-1,y,0,"stone")
        d.set(4,y,0,"sticky_piston",facing="west"); d.set(3,y,0,"stone")
    d.set(1,4,0,"sticky_piston",facing="down"); d.set(1,3,0,"stone")
    d.set(0,3,0,"stone"); d.set(2,3,0,"stone")
    d.set(1,-3,0,"sticky_piston",facing="up"); d.set(1,-2,0,"sticky_piston",facing="up")
    d.set(1,-1,0,"stone"); d.set(0,-1,0,"stone"); d.set(2,-1,0,"stone")
    d.set(-1,-1,0,"sticky_piston",facing="east"); d.set(-1,-2,0,"stone")
    # F unit under frame stone
    d.set(2,-3,0,"note_block"); d.set(2,-2,0,"observer",facing="down")
    return d
def v7(p1d=4, cd=(4,4,4,1), hd=1):
    d = base7()
    d.set(1,4,1,"lever",face="floor",facing="north")
    for x in (0,2): d.set(x,4,1,"redstone_wire")
    for sx,cx in ((-2,-1),(4,3)):
        d.set(cx,3,1,"redstone_wire"); d.set(cx,3,2,"redstone_wire")
        d.set(sx,1,2,"stone"); d.set(sx,2,2,"redstone_wire")
        d.set(sx,1,1,"stone"); d.set(sx,2,1,"redstone_wire"); d.set(sx,3,1,"stone")
    d.set(-2,0,1,"sticky_piston",facing="down"); d.set(-2,-1,1,"redstone_block"); d.set(-2,-3,1,"stone")
    d.set(4,0,2,"sticky_piston",facing="down"); d.set(4,-1,2,"redstone_block"); d.set(4,-3,2,"stone")
    # z=2 chain westward
    rep(d,3,2,"east",cd[0]); rep(d,2,2,"east",cd[1]); rep(d,1,2,"east",cd[2]); rep(d,0,2,"east",cd[3]); dust(d,-1,2)
    # z=1
    rep(d,-1,1,"south",hd); fl(d,0,1,"observer",facing="west")
    d.set(1,-3,1,"glass"); d.set(1,-2,1,"redstone_wire"); dust(d,2,1)
    fl(d,3,1,"observer",facing="east"); dust(d,4,1)
    # z=0
    dust(d,-2,0)
    # z=-1
    dust(d,-2,-1); fl(d,-1,-1,"observer",facing="west"); rep(d,0,-1,"west",p1d); dust(d,1,-1); dust(d,2,-1)
    return d
d7 = v7(); d7.save("v7.json")
r = test(d7); print(r.text[:900])
if not r.valid: show(d7, keys=KEYS+["(2,-2,0)","(2,-2,1)"])
else: print(robust(d7,(1,4,1)))
