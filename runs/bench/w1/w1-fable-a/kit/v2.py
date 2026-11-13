def fl(d, x, z, block, **p):
    d.set(x,-3,z,"stone"); d.set(x,-2,z,block,**p)
def rep(d,x,z,facing,delay=1): fl(d,x,z,"repeater",facing=facing,delay=delay)
def dust(d,x,z): fl(d,x,z,"redstone_wire")

def base():
    d = Design("open")
    for y in (0,1,2):
        d.set(-2,y,0,"sticky_piston",facing="east"); d.set(-1,y,0,"stone")
        d.set(4,y,0,"sticky_piston",facing="west"); d.set(3,y,0,"stone")
    d.set(1,4,0,"sticky_piston",facing="down"); d.set(1,3,0,"stone")
    d.set(0,3,0,"stone"); d.set(2,3,0,"stone")
    d.set(1,-3,0,"sticky_piston",facing="up"); d.set(1,-2,0,"sticky_piston",facing="up")
    d.set(1,-1,0,"stone"); d.set(0,-1,0,"stone"); d.set(2,-1,0,"stone")
    d.set(-1,-1,0,"sticky_piston",facing="east"); d.set(-1,-2,0,"stone")
    d.set(3,-2,0,"stone"); d.set(3,-1,0,"redstone_wire")
    d.set(4,-2,0,"stone"); d.set(4,-1,0,"redstone_wire")
    d.set(3,-1,-1,"stone")
    return d

def v2(p2d=2, p1d=4, hd=1):
    d = base()
    d.set(1,4,1,"lever",face="floor",facing="north")
    for x in (0,2): d.set(x,4,1,"redstone_wire")
    for sx,cx in ((-2,-1),(4,3)):
        d.set(cx,3,1,"redstone_wire"); d.set(cx,3,2,"redstone_wire")
        d.set(sx,1,2,"stone"); d.set(sx,2,2,"redstone_wire")
        d.set(sx,1,1,"stone"); d.set(sx,2,1,"redstone_wire"); d.set(sx,3,1,"stone")
    # stairs west
    d.set(-2,0,3,"stone"); d.set(-2,1,3,"redstone_wire")
    d.set(-2,-1,4,"stone"); d.set(-2,0,4,"redstone_wire")
    d.set(-2,-2,5,"stone"); d.set(-2,-1,5,"redstone_wire")   # X
    dust(d,-2,6); dust(d,-2,7); dust(d,-2,8)
    fl(d,-1,8,"observer",facing="west")
    for x in range(0,5): dust(d,x,8)
    for z in (7,6,5,4,3,2,1): dust(d,4,z)
    dust(d,3,4)
    rep(d,-1,6,"west",4); rep(d,0,6,"west",4); rep(d,1,6,"west",4); dust(d,2,6)
    rep(d,-1,5,"east",1); dust(d,0,5); rep(d,1,5,"east",2); dust(d,2,5)
    rep(d,-2,4,"south",1); dust(d,-1,4); dust(d,0,4); fl(d,1,4,"observer",facing="west"); rep(d,2,4,"west",p2d)
    rep(d,-2,3,"south",1); dust(d,-1,3)
    dust(d,-2,2); rep(d,-1,2,"south",hd)
    rep(d,-2,1,"south",1); dust(d,-1,1)
    dust(d,-2,0)
    dust(d,-2,-1); fl(d,-1,-1,"observer",facing="west"); rep(d,0,-1,"west",p1d); dust(d,1,-1)
    fl(d,2,-1,"observer",facing="west"); dust(d,3,-1); dust(d,4,-1)
    return d
d2 = v2(); d2.save("v2.json")
r = test(d2); print(r.text[:1500])
print(trace(d2, flips=2, grep="(1,", limit=150))
