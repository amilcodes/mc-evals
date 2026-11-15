import v1, v2, v3
from v1 import dust, rep, obs
from pdbuild import Design
def left():
    d=v3.left()
    for p in [(-2,5,-3),(-2,6,-3),(-2,6,-2),(-2,5,-2),(-2,6,-1),(-2,5,-1),(-2,6,0),(-2,5,0),(-1,5,0),(-1,6,0)]:
        d.remove(*p)
    return d
def full(left=left):
    L=left(); d=Design("closed")
    d.merge(L); d.merge(L.mirrored_x(3))
    for x in range(4):
        for y in range(4): d.set(x,y,0,"stone")
        d.set(x,-2,0,"sticky_piston",facing="up"); d.set(x,-3,0,"observer",facing="down")
        d.set(x,5,0,"sticky_piston",facing="down")   # pulse type now, retracted, gap at y=4
        d.set(x,5,-1,"observer",facing="north")
        d.set(x,5,-2,"redstone_wire")
    for x in range(0,4): dust(d,x,-4,0)
    d.set(2,-5,1,"stone"); d.set(2,-4,1,"lever",face="floor",facing="north")
    return d
def full2():
    d=full()
    pw={0:13,1:12,2:12,3:13}
    for x in range(4):
        d.set(x,5,-2,"redstone_wire",east="side",west="side",north="none",south="none",power=pw[x])
    return d
def full3(left=left):
    L=left(); d=Design("closed")
    d.merge(L); d.merge(L.mirrored_x(3))
    for x in range(4):
        for y in range(4): d.set(x,y,0,"stone")
        d.set(x,-2,0,"sticky_piston",facing="up"); d.set(x,-3,0,"observer",facing="down")
        d.set(x,5,0,"sticky_piston",facing="down",extended="true"); d.set(x,4,0,"piston_head",facing="down",type="sticky")
        d.set(x,5,-1,"repeater",facing="north",delay=1,powered="true")
        d.set(x,5,-2,"redstone_wire")
    for x in range(0,4): dust(d,x,-4,0)
    d.set(2,-5,1,"stone"); d.set(2,-4,1,"lever",face="floor",facing="north")
    return d
