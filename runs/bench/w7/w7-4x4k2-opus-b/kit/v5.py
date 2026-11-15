from v1 import dust, rep, obs
from pdbuild import Design
Y=-3  # chain plane
def left():
    d=Design("closed")
    sp="sticky_piston"
    d.set(-3,2,0,sp,facing="east"); d.set(-3,1,0,sp,facing="east")
    d.set(-2,2,0,sp,facing="east"); d.set(-2,1,0,sp,facing="east")
    d.set(-1,-1,0,sp,facing="up",extended="true"); d.set(-1,0,0,"piston_head",facing="up",type="sticky")
    d.set(-1,4,0,sp,facing="down",extended="true"); d.set(-1,3,0,"piston_head",facing="down",type="sticky")
    # chain row z=0
    dust(d,-1,Y,0); dust(d,-2,Y,0)
    rep(d,-3,Y,0,"east",1); rep(d,-4,Y,0,"east",4); rep(d,-5,Y,0,"east",3); dust(d,-6,Y,0)
    rep(d,-7,Y,0,"east",2)
    # OR_a
    rep(d,-6,Y,-1,"south",2); dust(d,-6,Y,-2); dust(d,-6,Y,-3)
    # climb: start (-6,Y,-3); (-5,-2,-3) on stone (-5,-3,-3); (-4,-1,-3) on (-4,-2,-3); (-3,-1,-3) on (-3,-2,-3)
    d.set(-5,Y,-3,"stone"); dust(d,-5,-2,-3); dust(d,-4,-1,-3); dust(d,-3,-1,-3)
    # late chain
    rep(d,-1,Y,-1,"south",4); rep(d,-1,Y,-2,"south",4); dust(d,-1,Y,-3)
    rep(d,-2,Y,-3,"east",4); dust(d,-3,Y,-3)
    rep(d,-3,Y,-2,"north",4); dust(d,-3,Y,-1)
    rep(d,-4,Y,-1,"east",4); dust(d,-5,Y,-1)
    rep(d,-5,Y,-2,"south",4)
    # Ph feed
    dust(d,-2,2,1); dust(d,-2,2,2)
    obs(d,-3,Y,1,"north"); obs(d,-3,Y,2,"north")
    for y in range(Y+1,2): obs(d,-3,y,2,"down")
    d.set(-3,2,2,"redstone_wire")
    obs(d,-3,2,1,"north"); obs(d,-2,4,0,"east"); obs(d,-2,3,0,"up")
    # Q column x=-7
    for y in range(Y+1,2): obs(d,-7,y,0,"down")
    d.set(-7,2,0,"redstone_wire"); dust(d,-6,2,0); dust(d,-6,2,-1); dust(d,-6,2,-2); dust(d,-5,2,-2)
    rep(d,-4,2,-2,"west",4); dust(d,-3,2,-2); dust(d,-3,2,-1)
    obs(d,-2,2,-1,"west")
    # tower
    d.set(-2,-1,-3,"stone"); d.set(-2,0,-3,"redstone_torch",lit="true")
    d.set(-2,1,-3,"stone"); d.set(-2,2,-3,"redstone_torch",lit="false")
    d.set(-2,3,-3,"stone"); d.set(-2,4,-3,"redstone_torch",lit="true")
    d.set(-1,-1,-3,"redstone_wall_torch",facing="east",lit="true")
    dust(d,-1,-1,-2); dust(d,-1,-1,-1)
    for z in (-3,-2,-1): d.set(-1,4,z,"redstone_wire")
    # bottom L0 link
    dust(d,-1,Y,1); dust(d,-1,-2,2)
    return d
def full(left=left):
    L=left(); d=Design("closed")
    d.merge(L); d.merge(L.mirrored_x(3))
    for x in range(4):
        for y in range(4): d.set(x,y,0,"stone")
        d.set(x,-2,0,"sticky_piston",facing="up"); d.set(x,-2,1,"observer",facing="south"); dust(d,x,-2,2)
        d.set(x,5,0,"sticky_piston",facing="down",extended="true"); d.set(x,4,0,"piston_head",facing="down",type="sticky")
        d.set(x,5,-1,"repeater",facing="north",delay=1,powered="true")
        d.set(x,5,-2,"redstone_wire")
        dust(d,x,Y,0)
    d.set(1,Y-1,1,"stone"); d.set(1,Y,1,"lever",face="floor",facing="north")
    return d
