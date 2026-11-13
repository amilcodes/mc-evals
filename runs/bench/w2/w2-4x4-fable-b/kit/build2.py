from pdbuild import Design
def OB(d,x,y,z,f): d.set(x,y,z,"observer",facing=f)
def W(d,x,y,z): d.set(x,y,z,"redstone_wire")
def ST(d,x,y,z): d.set(x,y,z,"stone")
def GL(d,x,y,z): d.set(x,y,z,"glass")
def REP(d,x,y,z,f,delay): d.set(x,y,z,"repeater",facing=f,delay=delay)

def left():
    d = Design()
    for y in (1,2):
        d.set(-3,y,0,"sticky_piston",facing="east")
        d.set(-2,y,0,"sticky_piston",facing="east")
        ST(d,-1,y,0)
    ST(d,-1,0,0); ST(d,-1,3,0)
    d.set(-1,-1,0,"sticky_piston",facing="up"); d.set(-1,-2,0,"obsidian")
    d.set(-1,4,0,"sticky_piston",facing="down"); d.set(-1,5,0,"obsidian")
    ST(d,-3,3,0); OB(d,-3,4,0,"up"); W(d,-3,5,0)
    OB(d,-3,-1,0,"south"); OB(d,-2,-1,0,"west")
    # z=1
    OB(d,-3,1,1,"up"); OB(d,-3,0,1,"up"); OB(d,-3,-1,1,"up")
    W(d,-3,2,1); ST(d,-2,1,1); W(d,-2,2,1); ST(d,-2,3,1); W(d,-2,4,1)
    ST(d,-3,5,1); W(d,-3,6,1)
    OB(d,-1,4,1,"south"); OB(d,-1,5,1,"east"); ST(d,-2,5,1)
    # z=2
    ST(d,-3,1,2); W(d,-3,2,2); ST(d,-2,2,2); W(d,-2,3,2)
    OB(d,-2,4,2,"down"); OB(d,-1,4,2,"west")
    ST(d,-3,4,2); W(d,-3,5,2); GL(d,-3,6,2)
    # z=3
    ST(d,-1,4,3); W(d,-1,5,3); ST(d,-2,4,3); W(d,-2,5,3); ST(d,-3,4,3); W(d,-3,5,3)
    return d

def build(d01=3, w1=(4,4), da=2, w2=(4,4,2), db=3):
    L = left()
    d = Design("open")
    d.merge(L); d.merge(L.mirrored_x(3))
    for x in range(4):
        d.set(x,-2,0,"sticky_piston",facing="up"); d.set(x,5,0,"sticky_piston",facing="down")
        ST(d,x,-1,0); ST(d,x,4,0)
        OB(d,x,6,0,"up"); OB(d,x,7,0,"east"); W(d,x,5,1); W(d,x,5,3)
        OB(d,x,-2,2,"west"); OB(d,x,-2,1,"south")
    for y in range(-2,5): OB(d,-3,y,3,"up")
    OB(d,-2,-2,3,"west"); OB(d,-1,-2,3,"west"); OB(d,-1,-2,2,"south")
    ST(d,5,5,0); W(d,5,6,0); OB(d,5,7,0,"down"); OB(d,4,7,0,"east")
    for x in range(-3,7): ST(d,x,6,3)
    for x in (-3,2,6): OB(d,x,6,3,"up")
    W(d,-3,7,3); d.set(-3,7,2,"lever",face="floor",facing="north")
    REP(d,-2,7,3,"west",d01)
    W(d,-1,7,3); ST(d,-1,6,2); W(d,-1,7,2); GL(d,-1,6,1); W(d,-1,7,1); OB(d,0,6,1,"up"); W(d,0,7,1)
    REP(d,0,7,3,"west",w1[0]); REP(d,1,7,3,"west",w1[1])
    W(d,2,7,3)
    for i,x in enumerate((3,4,5)): REP(d,x,7,3,"west",w2[i])
    W(d,6,7,3)
    GL(d,2,6,2); REP(d,2,7,2,"south",da); OB(d,2,6,1,"up"); W(d,2,7,1)
    GL(d,3,6,1); W(d,3,7,1); GL(d,3,6,2); W(d,3,7,2); GL(d,4,6,2); W(d,4,7,2)
    GL(d,5,6,2); REP(d,5,7,2,"east",db); W(d,6,7,2); ST(d,6,7,1)
    return d
