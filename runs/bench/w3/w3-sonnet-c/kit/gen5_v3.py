exec(open('ctl2.py').read().split("def modR")[0])
exec(open('mods.py').read())
def dst(d,x,y,z,sup="stone"):
    d.set(x,y,z,"redstone_wire")
    if sup: d.set(x,y-1,z,sup)
def rp(d,x,y,z,facing,delay=1):
    d.set(x,y,z,"repeater",facing=facing,delay=delay)
    d.set(x,y-1,z,"stone")
def full():
    d=Design("open")
    for p in [(-1,0),(-1,1),(-1,2),(3,0),(3,1),(3,2),(0,3),(1,3),(2,3),(0,-1),(1,-1),(2,-1)]:
        d.set(p[0],p[1],0,"stone")
    d.set(-3,1,0,"sticky_piston",facing="east"); d.set(-2,1,0,"sticky_piston",facing="east")
    d.set(-1,-1,0,"sticky_piston",facing="up")
    # B feed
    dst(d,-1,3,0,sup=None); d.set(-2,1,1,"stone"); dst(d,-2,2,1,sup=None)
    for z in range(1,8): dst(d,-1,3,z,sup=None)
    # P feed
    dst(d,-4,1,0); dst(d,-5,1,0)
    # P observer + domino
    d.set(-3,1,1,"observer",facing="north")
    dst(d,-3,1,2); dst(d,-4,1,2); dst(d,-5,1,2); dst(d,-6,2,2); dst(d,-7,3,2); dst(d,-7,3,3)
    dst(d,-6,3,3)
    for x in (-5,-4,-3,-2): dst(d,x,3,3)
    # A feed
    dst(d,-2,-1,0); dst(d,-3,-1,0); dst(d,-4,-1,0); dst(d,-5,-1,0)
    # lever + chain
    d.set(-9,2,0,"stone"); d.set(-9,3,0,"lever",face="floor",facing="north")
    reps={-11:4,-12:4,-13:2,-15:2,-17:4,-18:1}
    for x in range(-10,-20,-1):
        if x in reps: rep(d,x,0,"east",reps[x])
        else: dust(d,x,0)
    mod(d,-10,-1,1,3)     # R(P)
    mod(d,-19,-1,3,1)     # F(P)
    # P collector
    for z in (-6,-7): dust(d,-10,z); dust(d,-19,z)
    # P level tap at x=-14
    dust(d,-14,-1); dust(d,-14,-2); rep(d,-14,-3,"south",3)
    for z in range(-4,-8,-1): dust(d,-14,z)
    for x in range(-19,-7):
        if x==-9: rep(d,x,-7,"west",4)
        else: dust(d,x,-7)
    dst(d,-7,3,-7); dst(d,-6,2,-7); dst(d,-5,1,-7)
    for z in range(-6,0):
        if z==-4: rp(d,-5,1,z,"north",1)
        else: dst(d,-5,1,z)
    # A' taps at x=-16 (t24) and -21 (t38): south spurs
    for x,dl in ((-16,1),(-19,3)):
        dust(d,x,1); dust(d,x,2); rep(d,x,3,"north",dl)
    for x in range(-19,-15): dust(d,x,4)
    for z in range(5,7):
        if z==5: rep(d,-16,z,"north",1)
        else: dust(d,-16,z)
    dst(d,-15,2,6); dst(d,-14,1,6); dst(d,-13,0,6); dst(d,-12,-1,6)
    for x in range(-11,-5):
        if x==-9: rp(d,x,-1,6,"west",1)
        else: dst(d,x,-1,6)
    for z in range(5,-1,-1):
        if z==4: rp(d,-6,-1,z,"south",1)
        else: dst(d,-6,-1,z)
    return d
def ring(d):
    for x in (0,1,2): d.set(x,4,0,"sticky_piston",facing="down")
    for y in (0,1): d.set(4,y,0,"sticky_piston",facing="west")
    for x in (0,1): d.set(x,-2,0,"sticky_piston",facing="up")
    # L start
    dst(d,-8,3,0,sup="stone"); dst(d,-7,4,0); dst(d,-6,5,0)
    for x in range(-5,6):
        if x in (-3,3): d.set(x,5,0,"repeater",facing="west",delay=1); d.set(x,4,0,"stone")
        elif x in (0,1,2): d.set(x,5,0,"redstone_wire")
        else: dst(d,x,5,0)
    # stairs down at x=5
    for k,(y,z) in enumerate([(4,1),(3,2),(2,3),(1,4),(0,5),(-1,6),(-2,7)]): dst(d,5,y,z)
    # right feed
    dst(d,4,1,4)
    for z in (3,2,1): dst(d,4,1,z)
    # bottom
    dst(d,4,-2,7); dst(d,3,-2,7)
    for z in range(6,1,-1):
        if z==5: d.set(3,-2,z,"repeater",facing="south",delay=1); d.set(3,-3,z,"stone")
        else: dst(d,3,-2,z)
    for x in (2,1,0): dst(d,x,-2,2)
    dst(d,0,-2,1)
    dst(d,3,-2,1); dst(d,3,-2,0); dst(d,2,-2,0)
    return d
def full2():
    d=full(); ring(d); return d
