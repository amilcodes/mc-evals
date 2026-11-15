from pdbuild import Design
import sys
def build(rq=4):
    d = Design("open")
    S=lambda x,y,z,b="stone",**p: d.set(x,y,z,b,**p)
    sp=lambda x,y,z,f: d.set(x,y,z,"sticky_piston",facing=f)
    W=lambda x,y,z: d.set(x,y,z,"redstone_wire")
    sp(1,4,0,"down"); sp(2,4,0,"down")
    for x in range(3): S(x,3,0)
    sp(4,0,0,"west"); sp(4,1,0,"west"); S(3,0,0); S(3,1,0); S(3,2,0)
    sp(-2,1,0,"east"); S(-1,1,0); sp(-2,2,0,"east"); S(-1,2,0)
    sp(0,-2,0,"up"); S(0,-1,0)
    sp(-3,0,0,"east"); sp(-2,0,0,"east"); S(-1,0,0)
    sp(1,-3,0,"up"); sp(1,-2,0,"up"); S(1,-1,0)
    S(2,-1,0)
    S(0,-3,1); d.set(0,-2,1,"lever",face="floor",facing="north")
    S(-1,-3,1,"glass"); W(-1,-2,1); d.set(-1,-1,1,"observer",facing="down")
    S(1,-3,1); W(1,-2,1)  # Q early power
    for (x,y) in [(-2,-1),(-3,0),(-2,1),(-3,2),(-2,3)]:
        S(x,y-1,1,"glass"); W(x,y,1)
    S(-2,3,0); W(-2,4,0); S(-1,4,0); W(-1,5,0); S(-1,4,1); W(-1,5,1)
    S(0,4,1); d.set(0,5,1,"repeater",facing="west",delay=1)
    S(1,4,1); W(1,5,1); S(2,4,1); W(2,5,1)
    S(3,4,1); W(3,5,1); S(4,3,1); W(4,4,1); S(4,2,0); W(4,3,0)
    # chain
    S(0,-4,0); d.set(0,-3,0,"repeater",facing="south",delay=2)
    S(0,-3,-1); W(0,-2,-1)
    S(1,-4,-1); W(1,-3,-1); d.set(1,-2,-1,"observer",facing="down")
    S(2,-4,-1); d.set(2,-3,-1,"repeater",facing="west",delay=rq)
    S(3,-4,-1); W(3,-3,-1); S(3,-3,0); W(3,-2,0); S(2,-4,0); W(2,-3,0)
    d.set(2,-2,0,"observer",facing="east")
    # XM
    S(-1,-3,-1); d.set(-1,-2,-1,"repeater",facing="east",delay=4)
    S(-2,-3,-1); d.set(-2,-2,-1,"repeater",facing="east",delay=4)
    S(-3,-2,-1); d.set(-3,-1,-1,"redstone_wire",north="side",south="side",east="side",west="side")
    S(-3,-1,0)
    d.set(-2,-1,-1,"observer",facing="down"); S(-2,0,-1)
    return d
if __name__=="__main__":
    build().save(sys.argv[1] if len(sys.argv)>1 else "door5.json")
