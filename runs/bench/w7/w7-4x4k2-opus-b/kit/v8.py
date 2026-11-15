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
    # L0 row
    dust(d,-1,Y,0); rep(d,-2,Y,0,"east",2); dust(d,-3,Y,0); dust(d,-4,Y,0)
    # OR_a
    rep(d,-4,Y,-1,"south",3); rep(d,-4,Y,-2,"south",1); dust(d,-4,Y,-3)
    d.set(-3,Y,-3,"stone"); dust(d,-3,-2,-3)
    # Q tap + column + R_q
    for y in range(-2,2): obs(d,-4,y,-2,"down")
    d.set(-4,2,-2,"redstone_wire"); dust(d,-3,2,-2)
    rep(d,-3,2,-1,"north",4)
    obs(d,-2,2,-1,"west")
    # late chain
    rep(d,1,Y,-1,"south",4); rep(d,1,Y,-2,"south",4); dust(d,1,Y,-3)
    rep(d,0,Y,-3,"east",4); rep(d,-1,Y,-3,"east",4); rep(d,-2,Y,-3,"east",4)
    # tower (B0 at y=-2)
    d.set(-2,-2,-3,"stone"); d.set(-2,-1,-3,"redstone_torch",lit="true")
    d.set(-2,0,-3,"stone"); d.set(-2,1,-3,"redstone_torch",lit="false")
    d.set(-2,2,-3,"stone"); d.set(-2,3,-3,"redstone_torch",lit="true")
    d.set(-2,4,-3,"stone")
    d.set(-1,-2,-3,"redstone_wall_torch",facing="east",lit="true")
    dust(d,-1,-2,-2); dust(d,-1,-1,-1)
    for z in (-3,-2,-1): d.set(-1,4,z,"redstone_wire")
    # Ph feed
    dust(d,-2,2,1); dust(d,-2,2,2)
    for y in range(-1,2): obs(d,-3,y,2,"down")
    d.set(-3,2,2,"redstone_wire")
    obs(d,-3,2,1,"north"); obs(d,-2,4,0,"east"); obs(d,-2,3,0,"up")
    # bottom line ext + link
    dust(d,-1,Y,1); dust(d,-1,-2,2); dust(d,-2,-2,2); dust(d,-3,-2,2)
    return d
