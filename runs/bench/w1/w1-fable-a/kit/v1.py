def fl(d, x, z, block, **p):
    """component on floor: stone at y=-3, block at y=-2"""
    d.set(x,-3,z,"stone"); d.set(x,-2,z,block,**p)
def rep(d,x,z,facing,delay=1): fl(d,x,z,"repeater",facing=facing,delay=delay)
def dust(d,x,z): fl(d,x,z,"redstone_wire")

def v1():
    d = Design("open")
    # side pistons + stones
    for y in (0,1,2):
        d.set(-2,y,0,"sticky_piston",facing="east"); d.set(-1,y,0,"stone")
        d.set(4,y,0,"sticky_piston",facing="west"); d.set(3,y,0,"stone")
    d.set(1,4,0,"sticky_piston",facing="down"); d.set(1,3,0,"stone")
    d.set(0,3,0,"stone"); d.set(2,3,0,"stone")
    # center mech
    d.set(1,-3,0,"sticky_piston",facing="up"); d.set(1,-2,0,"sticky_piston",facing="up")
    d.set(1,-1,0,"stone"); d.set(0,-1,0,"stone"); d.set(2,-1,0,"stone")
    d.set(-1,-1,0,"sticky_piston",facing="east"); d.set(-1,-2,0,"stone")
    # P2 line at z=0
    d.set(3,-2,0,"stone"); d.set(3,-1,0,"redstone_wire")
    d.set(4,-2,0,"stone"); d.set(4,-1,0,"redstone_wire")
    d.set(3,-1,-1,"stone")
    # top network
    d.set(1,4,1,"lever",face="floor",facing="north")
    for x in (0,2): d.set(x,4,1,"redstone_wire")
    for sx,cx in ((-2,-1),(4,3)):
        d.set(cx,3,1,"redstone_wire")
        d.set(sx,1,1,"stone"); d.set(sx,2,1,"redstone_wire"); d.set(sx,3,0,"redstone_wire")
    # stairs west
    d.set(-2,0,2,"stone"); d.set(-2,1,2,"redstone_wire")
    d.set(-2,-1,3,"stone"); d.set(-2,0,3,"redstone_wire")
    d.set(-2,-2,4,"stone"); d.set(-2,-1,4,"redstone_wire")   # X
    dust(d,-2,5); dust(d,-2,6); dust(d,-2,7)
    # row 7: O_L and pulse row
    fl(d,-1,7,"observer",facing="west")
    for x in range(0,5): dust(d,x,7)
    for z in (6,5,4,3,2,1): dust(d,4,z)
    dust(d,3,3)
    # row 5 chain
    rep(d,-1,5,"west",4); rep(d,0,5,"west",4); rep(d,1,5,"west",4); dust(d,2,5)
    # row 4
    rep(d,-1,4,"east",1); dust(d,0,4); rep(d,1,4,"east",2); dust(d,2,4)
    # row 3
    rep(d,-2,3,"south",1); dust(d,-1,3); dust(d,0,3); fl(d,1,3,"observer",facing="west"); rep(d,2,3,"west",2)
    # row 2
    dust(d,-2,2); rep(d,-1,2,"south",1)
    # row 1
    rep(d,-2,1,"south",1); dust(d,-1,1)
    # row 0
    dust(d,-2,0)
    # row -1
    dust(d,-2,-1); fl(d,-1,-1,"observer",facing="west"); rep(d,0,-1,"west",4); dust(d,1,-1)
    fl(d,2,-1,"observer",facing="west"); dust(d,3,-1); dust(d,4,-1)
    return d
d1 = v1(); d1.save("v1.json")
r = test(d1); print(r)
