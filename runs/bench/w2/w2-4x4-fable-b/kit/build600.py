from pdbuild import Design
def OB(d,x,y,z,f): d.set(x,y,z,"observer",facing=f)
def W(d,x,y,z): d.set(x,y,z,"redstone_wire")
def ST(d,x,y,z): d.set(x,y,z,"stone")
def REP(d,x,y,z,f,delay): d.set(x,y,z,"repeater",facing=f,delay=delay)

def left(closed=True):
    d = Design()
    bx = -1 if closed else -2
    for y in (1,2):
        d.set(-3,y,0,"sticky_piston",facing="east")
        d.set(bx,y,0,"sticky_piston",facing="east")
        if closed:
            ST(d,0,y,0); ST(d,1,y,0)
        else:
            ST(d,-1,y,0)
    if not closed:
        ST(d,-1,0,0); ST(d,-1,3,0)
    d.set(-1,-1,0,"sticky_piston",facing="up"); d.set(-1,-2,0,"obsidian")
    d.set(-1,4,0,"sticky_piston",facing="down"); d.set(-1,5,0,"obsidian")
    ST(d,-3,3,0); W(d,-3,4,0)
    OB(d,-3,-1,0,"south"); OB(d,-2,-1,0,"west")
    # z=1
    OB(d,-3,1,1,"up"); OB(d,-3,0,1,"up"); OB(d,-3,-1,1,"up")
    W(d,-3,2,1); ST(d,-2,1,1); W(d,-2,2,1); ST(d,-2,3,1); W(d,-2,4,1); ST(d,-2,5,1)
    ST(d,-3,4,1); W(d,-3,5,1)
    OB(d,-1,4,1,"south")
    # z=2
    ST(d,-3,1,2); W(d,-3,2,2); ST(d,-2,2,2); W(d,-2,3,2)
    d.set(-2,4,2,"glass"); W(d,-2,5,2)
    OB(d,-1,4,2,"south"); W(d,-1,5,2)
    ST(d,-3,4,2); W(d,-3,5,2)
    # z=3
    ST(d,-2,2,3); W(d,-2,3,3); OB(d,-1,4,3,"south")
    # z=4
    ST(d,-2,2,4); W(d,-2,3,4); W(d,-1,4,4)
    return d

def build(closed=False, d01=2, w1=(4,4), d34=2, w2=(4,4), d56=1, dl=1, dA=1):
    L = left(closed)
    d = Design("closed" if closed else "open")
    d.merge(L); d.merge(L.mirrored_x(3))
    for x in range(4):
        d.set(x,-2,0,"sticky_piston",facing="up"); d.set(x,5,0,"sticky_piston",facing="down")
        if closed:
            ST(d,x,0,0); ST(d,x,3,0)
        else:
            ST(d,x,-1,0); ST(d,x,4,0)
        W(d,x,6,0)
        W(d,x,5,2); W(d,x,5,4)
        OB(d,x,-2,2,"west"); OB(d,x,-2,1,"south")
    W(d,0,5,1)
    W(d,-3,5,3)
    for y in range(-2,5): OB(d,-3,y,3,"up")
    OB(d,-2,-2,3,"west"); OB(d,-1,-2,3,"west"); OB(d,-1,-2,2,"south")
    # control beta row y=7 z=3
    for x in range(-3,7): ST(d,x,6,3)
    W(d,-3,7,3); OB(d,-3,6,2,"up"); W(d,-3,7,2)
    ST(d,-3,6,4); d.set(-3,7,4,"lever",face="floor",facing="north")
    REP(d,-2,7,3,"west",d01)
    W(d,-1,7,3); W(d,-1,7,4); OB(d,-1,6,4,"up"); OB(d,-1,5,4,"up")
    REP(d,0,7,3,"west",w1[0]); REP(d,1,7,3,"west",w1[1])
    W(d,2,7,3); OB(d,2,6,2,"up"); OB(d,2,7,2,"up"); W(d,2,8,2)
    REP(d,3,7,3,"west",d34)
    W(d,4,7,3); W(d,4,7,4); OB(d,4,6,4,"up"); OB(d,4,5,4,"up")
    REP(d,5,7,3,"west",w2[0])
    W(d,6,7,3); ST(d,6,7,2); W(d,6,8,2); d.set(6,8,3,"glass"); W(d,6,9,3)
    for x in range(-2,6): ST(d,x,8,3)
    d.set(2,8,3,"glass"); ST(d,2,9,2)
    REP(d,5,9,3,"east",w2[1])
    W(d,4,9,3); W(d,4,9,2); OB(d,4,8,2,"up"); OB(d,4,7,2,"up"); OB(d,4,6,2,"up")
    REP(d,3,9,3,"east",d56)
    W(d,2,9,3)
    OB(d,1,9,3,"east")
    REP(d,0,9,3,"east",1)
    for x in (4,3,2,1,0): ST(d,x,8,1); W(d,x,9,1)
    ST(d,0,8,2); REP(d,0,9,2,"north",dl)
    W(d,-1,9,3); W(d,-2,9,3); W(d,-2,9,4)
    for y in range(4,9): OB(d,-2,y,4,"up")
    return d
