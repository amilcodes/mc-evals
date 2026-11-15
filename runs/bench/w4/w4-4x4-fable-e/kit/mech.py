def W(d,x,y,z,sup="stone"):
    """dust with support"""
    if sup: d.set(x,y-1,z,sup)
    d.set(x,y,z,"redstone_wire")
def lefthalf(d):
    SP="sticky_piston"
    # row units
    for y in (1,2):
        d.set(-3,y,0,SP,facing="east"); d.set(-2,y,0,SP,facing="east"); d.set(-1,y,0,"stone")
    for y in (0,3):
        d.set(-2,y,0,SP,facing="east"); d.set(-1,y,0,"stone")
    d.set(-2,2,1,"stone"); d.set(-2,3,1,"redstone_wire")
    d.set(-3,2,1,"glass"); d.set(-3,3,1,"redstone_wire")
    W(d,-4,2,1)
    W(d,-3,1,1,"glass"); W(d,-2,1,1,"glass")
    # A_r
    W(d,-3,2,-1); W(d,-3,2,-2)
    # singles vertical
    d.set(1,-2,0,SP,facing="up"); d.set(1,-1,0,"stone")
    d.set(1,5,0,SP,facing="down"); d.set(1,4,0,"stone")
    # S feeds
    d.set(-2,-1,-1,"glass"); d.set(-2,0,-1,"repeater",facing="north"); W(d,-2,0,-2)
    W(d,-2,4,-1,"glass"); W(d,-2,4,-2)
    W(d,1,-2,-1); W(d,1,-2,-2)
    W(d,1,5,-1,None); W(d,1,5,-2,None)
    # bottom col unit
    d.set(0,-3,0,SP,facing="up"); d.set(0,-2,0,SP,facing="up"); d.set(0,-1,0,"stone")
    W(d,-1,-1,0,"glass"); W(d,-2,-1,0); W(d,-2,-1,1)
    d.set(0,-4,-1,"stone"); d.set(0,-3,-1,"repeater",facing="north")
    # top col unit
    d.set(0,6,0,SP,facing="down"); d.set(0,5,0,SP,facing="down"); d.set(0,4,0,"stone")
    W(d,-1,5,0,"glass"); d.set(-2,4,0,"glass"); d.set(-2,5,0,"repeater",facing="west")
    W(d,-3,5,0,"glass"); W(d,-3,5,1)
    W(d,0,7,-1,"glass"); W(d,0,7,-2)
    return d
