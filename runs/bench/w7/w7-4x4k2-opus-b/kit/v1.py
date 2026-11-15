from pdbuild import Design
def S(d,x,y,z,b="stone",**p):
    if (x,y,z) in d.blocks and d.blocks[(x,y,z)][0]!=b and b=="stone": return
    d.set(x,y,z,b,**p)
def dust(d,x,y,z,sup="stone"):
    d.set(x,y,z,"redstone_wire")
    if (x,y-1,z) not in d.blocks: d.set(x,y-1,z,sup)
def rep(d,x,y,z,facing,delay=1,sup="stone"):
    d.set(x,y,z,"repeater",facing=facing,delay=delay)
    if (x,y-1,z) not in d.blocks: d.set(x,y-1,z,sup)
def obs(d,x,y,z,facing): d.set(x,y,z,"observer",facing=facing)

def left():
    d=Design("closed")
    sp="sticky_piston"
    d.set(-3,2,0,sp,facing="east"); d.set(-3,1,0,sp,facing="east")
    d.set(-2,2,0,sp,facing="east"); d.set(-2,1,0,sp,facing="east")
    d.set(-1,-1,0,sp,facing="up",extended="true"); d.set(-1,0,0,"piston_head",facing="up",type="sticky")
    d.set(-1,4,0,sp,facing="down",extended="true"); d.set(-1,3,0,"piston_head",facing="down",type="sticky")
    # chain y=-4 z=0 going west
    for x in (-1,-2,-3): dust(d,x,-4,0)
    rep(d,-4,-4,0,"east",4); rep(d,-5,-4,0,"east",1); dust(d,-6,-4,0)
    rep(d,-7,-4,0,"east",2); dust(d,-8,-4,0)
    rep(d,-9,-4,0,"east",1); dust(d,-10,-4,0)
    rep(d,-11,-4,0,"east",4); rep(d,-12,-4,0,"east",4); dust(d,-13,-4,0)
    # Ph feed: stub + line y=2 z=2
    dust(d,-2,2,1); dust(d,-2,2,2)
    obs(d,-3,-4,1,"north"); obs(d,-3,-4,2,"north")
    for y in range(-3,2): obs(d,-3,y,2,"down")
    d.set(-3,2,2,"redstone_wire")
    for x in range(-12,-3): dust(d,x,2,2)
    obs(d,-13,-4,1,"north"); obs(d,-13,-4,2,"north")
    for y in range(-3,2): obs(d,-13,y,2,"down")
    d.set(-13,2,2,"redstone_wire")
    # Q feed
    obs(d,-6,-3,0,"down")
    for y in range(-2,2): obs(d,-6,y,0,"down")
    d.set(-6,2,0,"redstone_wire"); dust(d,-5,2,0)
    rep(d,-4,2,0,"west",4)
    # Pa feed
    obs(d,-10,-3,0,"down"); obs(d,-10,-3,-1,"south")
    for y in range(-2,3): obs(d,-10,y,-1,"down")
    d.set(-10,3,-1,"redstone_wire")
    for x in range(-9,-3): dust(d,x,3,-1)
    dust(d,-3,2,-1); dust(d,-2,2,-1)
    # K OR line
    rep(d,-8,-4,-1,"south",1); dust(d,-8,-4,-2); dust(d,-8,-4,-3)
    rep(d,-13,-4,-1,"south",1); dust(d,-13,-4,-2)
    for x in range(-13,-8): dust(d,x,-4,-3)
    rep(d,-7,-4,-3,"west",1); dust(d,-6,-4,-3)
    dust(d,-5,-3,-3); dust(d,-4,-2,-3); dust(d,-3,-1,-3)
    # tower z=-3 x=-2
    d.set(-2,-1,-3,"stone"); d.set(-2,0,-3,"redstone_torch",lit="true")
    d.set(-2,1,-3,"stone"); d.set(-2,2,-3,"redstone_torch",lit="false")
    d.set(-2,3,-3,"stone"); d.set(-2,4,-3,"redstone_torch",lit="true")
    d.set(-2,5,-3,"stone")
    # K1
    d.set(-1,-1,-3,"redstone_wall_torch",facing="east",lit="true")
    dust(d,-1,-1,-2); dust(d,-1,-1,-1)
    # K2 (dust on walls -> no support needed since walls exist; but supports would be wall cells: skip)
    d.set(-1,4,-3,"redstone_wire"); d.set(-1,4,-2,"redstone_wire"); d.set(-1,4,-1,"redstone_wire")
    # top edge line
    dust(d,-2,6,-3); dust(d,-2,6,-2); dust(d,-2,6,-1); dust(d,-2,6,0)
    d.set(-1,5,0,"glass"); d.set(-1,6,0,"redstone_wire")
    return d

def full():
    L=left()
    d=Design("closed")
    d.merge(L); d.merge(L.mirrored_x(3))
    for x in range(4):
        for y in range(4): d.set(x,y,0,"stone")
        d.set(x,-2,0,"sticky_piston",facing="up")
        d.set(x,-3,0,"observer",facing="down")
        d.set(x,5,0,"sticky_piston",facing="down",extended="true"); d.set(x,4,0,"piston_head",facing="down",type="sticky")
        d.set(x,6,0,"redstone_wire")
    for x in range(0,4): dust(d,x,-4,0)
    d.set(2,-5,1,"stone"); d.set(2,-4,1,"lever",face="floor",facing="north")
    return d
