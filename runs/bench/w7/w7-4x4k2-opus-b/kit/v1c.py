import v1, v1b
from pdbuild import Design
def left():
    d=v1b.left()
    for p in [(-4,2,0),(-4,1,0),(-5,2,0),(-5,1,0)]: d.remove(*p)
    # route column top dust (-6,2,0) -> (-6,2,-1) -> (-6,2,-2) -> (-5,2,-2) -> R_q (-4,2,-2) W -> (-3,2,-2) -> (-3,2,-1) -> Q2
    v1.dust(d,-6,2,-1); v1.dust(d,-6,2,-2); v1.dust(d,-5,2,-2)
    v1.rep(d,-4,2,-2,"west",4)
    v1.dust(d,-3,2,-2); v1.dust(d,-3,2,-1)
    d.set(-2,2,-1,"observer",facing="west")
    return d
def full():
    L=left(); d=Design("closed")
    d.merge(L); d.merge(L.mirrored_x(3))
    for x in range(4):
        for y in range(4): d.set(x,y,0,"stone")
        d.set(x,-2,0,"sticky_piston",facing="up"); d.set(x,-3,0,"observer",facing="down")
        d.set(x,5,0,"sticky_piston",facing="down",extended="true"); d.set(x,4,0,"piston_head",facing="down",type="sticky")
        d.set(x,6,0,"redstone_wire")
    for x in range(0,4): v1.dust(d,x,-4,0)
    d.set(2,-5,1,"stone"); d.set(2,-4,1,"lever",face="floor",facing="north")
    return d
