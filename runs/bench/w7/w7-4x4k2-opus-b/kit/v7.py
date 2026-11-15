from v1 import dust, rep, obs
from pdbuild import Design
import v5
Y=-3
def left():
    d=Design("closed")
    sp="sticky_piston"
    d.set(-3,2,0,sp,facing="east"); d.set(-3,1,0,sp,facing="east")
    d.set(-2,2,0,sp,facing="east"); d.set(-2,1,0,sp,facing="east")
    d.set(-1,-1,0,sp,facing="up",extended="true"); d.set(-1,0,0,"piston_head",facing="up",type="sticky")
    d.set(-1,4,0,sp,facing="down",extended="true"); d.set(-1,3,0,"piston_head",facing="down",type="sticky")
    # row z=0 all dust L0
    for x in range(-5,0): dust(d,x,Y,0)
    # OR_a + Q tap
    rep(d,-5,Y,-1,"south",4); rep(d,-5,Y,-2,"south",4); dust(d,-5,Y,-3)
    # climb
    d.set(-4,Y,-3,"stone"); dust(d,-4,-2,-3); dust(d,-3,-1,-3)
    # late chain (center)
    rep(d,-1,Y,-1,"south",4); dust(d,-1,Y,-2)
    rep(d,0,Y,-2,"west",4); dust(d,1,Y,-2); dust(d,1,Y,-3)
    rep(d,0,Y,-3,"east",4); rep(d,-1,Y,-3,"east",4); rep(d,-2,Y,-3,"east",4); rep(d,-3,Y,-3,"east",2)
    # Ph feed
    dust(d,-2,2,1); dust(d,-2,2,2)
    obs(d,-3,Y,1,"north"); obs(d,-3,Y,2,"north")
    for y in range(Y+1,2): obs(d,-3,y,2,"down")
    d.set(-3,2,2,"redstone_wire")
    obs(d,-3,2,1,"north"); obs(d,-2,4,0,"east"); obs(d,-2,3,0,"up")
    # Q column x=-5 z=-2
    for y in range(Y+1,2): obs(d,-5,y,-2,"down")
    d.set(-5,2,-2,"redstone_wire")
    rep(d,-4,2,-2,"west",4); dust(d,-3,2,-2); dust(d,-3,2,-1)
    obs(d,-2,2,-1,"west")
    # tower
    d.set(-2,-1,-3,"stone"); d.set(-2,0,-3,"redstone_torch",lit="true")
    d.set(-2,1,-3,"stone"); d.set(-2,2,-3,"redstone_torch",lit="false")
    d.set(-2,3,-3,"stone"); d.set(-2,4,-3,"redstone_torch",lit="true")
    d.set(-1,-1,-3,"redstone_wall_torch",facing="east",lit="true")
    dust(d,-1,-1,-2); dust(d,-1,-1,-1)
    for z in (-3,-2,-1): d.set(-1,4,z,"redstone_wire")
    dust(d,-1,Y,1); dust(d,-1,-2,2)
    return d
