import v1
from v1 import dust, rep, obs
from pdbuild import Design
def left():
    d=Design("closed")
    sp="sticky_piston"
    d.set(-3,2,0,sp,facing="east"); d.set(-3,1,0,sp,facing="east")
    d.set(-2,2,0,sp,facing="east"); d.set(-2,1,0,sp,facing="east")
    d.set(-1,-1,0,sp,facing="up",extended="true"); d.set(-1,0,0,"piston_head",facing="up",type="sticky")
    d.set(-1,4,0,sp,facing="down",extended="true"); d.set(-1,3,0,"piston_head",facing="down",type="sticky")
    # chain y=-4 z=0
    for x in (-1,-2,-3): dust(d,x,-4,0)
    rep(d,-4,-4,0,"east",4); rep(d,-5,-4,0,"east",4); dust(d,-6,-4,0)
    rep(d,-7,-4,0,"east",1); rep(d,-8,-4,0,"east",4); dust(d,-9,-4,0)
    # OR_a
    rep(d,-6,-4,-1,"south",1); dust(d,-6,-4,-2); dust(d,-6,-4,-3)
    # late
    rep(d,-9,-4,-1,"south",4); rep(d,-9,-4,-2,"south",4); dust(d,-9,-4,-3)
    rep(d,-8,-4,-3,"west",3); dust(d,-7,-4,-3)
    # K climb
    dust(d,-5,-3,-3); dust(d,-4,-2,-3); dust(d,-3,-1,-3)
    # Ph feed (Ph1 column x=-3 z=2 via hops)
    dust(d,-2,2,1); dust(d,-2,2,2)
    obs(d,-3,-4,1,"north"); obs(d,-3,-4,2,"north")
    for y in range(-3,2): obs(d,-3,y,2,"down")
    d.set(-3,2,2,"redstone_wire")
    # Ph-mid, Ph-late
    obs(d,-3,2,1,"north"); obs(d,-2,4,0,"east"); obs(d,-2,3,0,"up")
    # Q column x=-7
    obs(d,-7,-3,0,"down")
    for y in range(-2,2): obs(d,-7,y,0,"down")
    d.set(-7,2,0,"redstone_wire"); dust(d,-6,2,0); dust(d,-6,2,-1); dust(d,-6,2,-2); dust(d,-5,2,-2)
    rep(d,-4,2,-2,"west",4); dust(d,-3,2,-2); dust(d,-3,2,-1)
    obs(d,-2,2,-1,"west")
    # tower z=-3 x=-2
    d.set(-2,-1,-3,"stone"); d.set(-2,0,-3,"redstone_torch",lit="true")
    d.set(-2,1,-3,"stone"); d.set(-2,2,-3,"redstone_torch",lit="false")
    d.set(-2,3,-3,"stone"); d.set(-2,4,-3,"redstone_torch",lit="true")
    d.set(-2,5,-3,"stone")
    d.set(-1,-1,-3,"redstone_wall_torch",facing="east",lit="true")
    dust(d,-1,-1,-2); dust(d,-1,-1,-1)
    for z in (-3,-2,-1): d.set(-1,4,z,"redstone_wire")
    dust(d,-2,6,-3); dust(d,-2,6,-2); dust(d,-2,6,-1); dust(d,-2,6,0)
    d.set(-1,5,0,"glass"); d.set(-1,6,0,"redstone_wire")
    return d
def full(left=left):
    L=left(); d=Design("closed")
    d.merge(L); d.merge(L.mirrored_x(3))
    for x in range(4):
        for y in range(4): d.set(x,y,0,"stone")
        d.set(x,-2,0,"sticky_piston",facing="up"); d.set(x,-3,0,"observer",facing="down")
        d.set(x,5,0,"sticky_piston",facing="down",extended="true"); d.set(x,4,0,"piston_head",facing="down",type="sticky")
        d.set(x,6,0,"redstone_wire")
    for x in range(0,4): dust(d,x,-4,0)
    d.set(2,-5,1,"stone"); d.set(2,-4,1,"lever",face="floor",facing="north")
    return d
