import v1
from pdbuild import Design
def left():
    d=v1.left()
    # remove Pa column + line
    for p in list(d.blocks):
        x,y,z=p
        if z==-1 and (x==-10 or (y in (2,3) and -10<=x<=-2) or (y==1 and x in (-3,-2))): d.remove(*p)
        if (x,y,z) in [(-10,-3,0),(-10,-3,-1),(-10,-4,-1)]: d.remove(*p)
    for x in range(-9,-3): d.remove(x,2,-1)
    d.remove(-10,2,-1)
    # derived Pa
    d.set(-3,2,-1,"observer",facing="south")
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
