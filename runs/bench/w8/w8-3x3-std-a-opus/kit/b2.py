def build2(rep_at=(-5,-11)):
    d = build()
    # remove z=-2 and module lever
    for p in list(d.blocks):
        if p[2] == -2: d.remove(*p)
    for p in [(-1,-2,-1),(-1,-2,0),(-1,-2,1),(-1,-3,-1),(-1,-3,0),(-1,-3,1),(0,-2,1),(0,-3,1),
              (-15,3,1),(-15,4,1),(1,-2,1),(2,-2,1),(2,-3,1),
              (-7,1,-1),(-7,0,-1),(-9,1,-1),(-9,0,-1)]:
        d.remove(*p)
    # lever at (1,-2,1) ceiling on wall
    d.set(1,-2,1,"lever",face="ceiling",facing="north")
    d.set(2,-3,1,"stone"); d.set(2,-2,1,W)
    # bottom L line (x from 0 to -14) at y=-2,z=1
    for x in range(0,-15,-1):
        if x in rep_at: R(d,x,-2,1,"west",1)
        else: Wd(d,x,-2,1)
    # hmm repeaters facing west output east: we need flow WEST -> facing east
    for x in rep_at: R(d,x,-2,1,"east",1)
    # ascent zigzag z=1 cols -15/-14
    for (x,y),g in [((-15,-1),(-15,-2)),((-14,0),(-14,-1)),((-15,1),(-15,0)),((-14,2),(-14,1)),((-15,3),(-15,2))]:
        d.set(g[0],g[1],1,"glass"); d.set(x,y,1,W)
    d.set(-14,3,1,"glass")   # support of (-14,4,1), non-cutting
    # P line one-way repeater and second observer pair
    d.set(-10,1,0,"repeater",facing="west",delay=1)
    d.set(-9,3,0,"observer",facing="up"); d.set(-9,2,0,"observer",facing="up")
    return d
def build3():
    d = build2()
    d.set(-9,3,0,"stone"); d.remove(-9,2,0)
    d.set(-14,3,-1,"observer",facing="up")
    for x in (-14,-13,-12,-11,-10): Wd(d,x,2,-1)
    Wd(d,-9,1,-1)
    return d
def build4():
    d = build3()
    R(d,-12,2,-1,"west",1)
    return d
def build5():
    d = build4()
    # remove second-pulse path
    d.set(-14,3,-1,"stone")
    for x in (-14,-13,-12,-11,-10): d.remove(x,2,-1); d.remove(x,1,-1)
    d.remove(-9,1,-1); d.remove(-9,0,-1)
    # G fed by dust (lag)
    d.remove(-4,1,0); d.set(-4,1,0,W); d.set(-4,2,0,"stone")
    return d
def build6(db=4, gdust=True):
    d = build4()
    d.set(-14,3,-1,"stone")
    for x in (-14,-13,-12,-11,-10): d.remove(x,2,-1); d.remove(x,1,-1)
    d.remove(-9,1,-1); d.remove(-9,0,-1)
    if gdust:
        d.remove(-4,1,0); d.set(-4,1,0,W); d.set(-4,2,0,"stone")
    d.set(-12,3,0,"repeater",facing="west",delay=1)
    d.set(-11,3,0,"repeater",facing="west",delay=db)
    d.set(-11,2,0,"observer",facing="up")
    return d
def b7(rq=3,q4=1,q5=2,gd=False):
    d = build6(4,gd)
    d.set(-7,0,1,"repeater",facing="west",delay=rq)
    d.set(-4,0,1,"repeater",facing="west",delay=q4)
    d.set(-5,0,1,"repeater",facing="west",delay=q5)
    return d
def build8():
    d = b7()
    # remove everything at x<=-14 except what we re-add
    for p in list(d.blocks):
        if p[0] <= -14: d.remove(*p)
    d.remove(-13,4,1)   # r1
    # bottom line to x=-13
    Wd(d,-13,-2,1)
    # ascent cols -13/-14
    for (x,y),g in [((-14,-1),(-14,-2)),((-13,0),(-13,-1)),((-14,1),(-14,0)),((-13,2),(-13,1)),((-14,3),(-14,2))]:
        d.set(g[0],g[1],1,"glass"); d.set(x,y,1,W)
    d.set(-13,3,1,"glass"); d.set(-13,4,1,W)
    # A chain input
    Wd(d,-14,4,0); Wd(d,-14,4,-1)
    return d
def build9(reps=(-6,-11)):
    d = build8()
    for p in [(1,-2,1),(2,-2,1),(2,-3,1),(3,-2,1),(3,-3,1),(4,-1,1),(4,-2,1),(5,0,1),(5,-1,1),(5,1,0),(5,0,0),
              (5,2,1),(5,1,1),(4,2,1),(4,1,1),(3,4,0),(3,3,0),(3,5,1),(3,4,1),(3,3,1),(-1,5,1),
              (-13,-2,1),(-13,-3,1),(-14,-1,1),(-14,-2,1)]:
        d.remove(*p)
    for x in range(-13,1):
        d.remove(x,-2,1); d.remove(x,-3,1)
    Wd(d,3,4,1); Wd(d,4,3,1); Wd(d,4,3,0)
    d.set(-1,-2,0,"stone"); d.set(0,-2,0,"lever",face="wall",facing="east")
    d.set(-1,-1,0,W)
    for x in range(-2,-14,-1):
        if x in reps: R(d,x,-1,0,"east",1,sup="stone")
        else: Wd(d,x,-1,0)
    return d
def build10(rq=3, qreps=(1,1,1), qdust=False):
    d = build9(); d.set(-3,0,0,"stone")
    d.set(-12,3,0,W); d.set(-11,3,0,W); d.set(-11,2,0,"stone")
    d.set(-10,1,0,W)
    for x in (-6,-5,-4): d.set(x,1,0,W)
    d.set(-5,2,0,"stone"); d.set(-6,2,0,"stone")
    d.set(-7,0,1,"repeater",facing="west",delay=rq)
    for x,dl in zip((-6,-5,-4),qreps):
        if qdust: d.set(x,0,1,W)
        else: d.set(x,0,1,"repeater",facing="west",delay=dl)
    return d
def cyc(d, n=4):
    lab = Lab(d, walls=True); lab.rest()
    st=[]
    for c in range(n):
        lab.flip(0,-2,0); ok=lab.rest(max_ticks=250); st.append(lab.doorway() if ok else "NR")
    return st
def build11():
    d = build9(); d.set(-3,0,0,"stone")
    for p in list(d.blocks):
        if p[0] <= -14: d.remove(*p)
    for p in [(-13,-1,0),(-13,-2,0),(-13,0,1),(-13,-1,1),(-13,1,1),(-13,2,1),(-13,3,1),(-12,1,0),(-12,0,0),
              (-10,2,1),(-10,1,1),(-10,4,0),(-7,2,-1),(-6,1,-1)]:
        d.remove(*p)
    # comparators shifted
    d.set(-8,4,-1,"comparator",facing="west",mode="subtract")
    d.set(-8,4,1,"comparator",facing="west",mode="subtract")
    Wd(d,-8,4,0)
    d.set(-9,3,0,"stone"); d.set(-9,4,0,"redstone_torch")
    # A chain
    d.set(-13,3,-1,"glass"); d.set(-13,4,-1,W)
    for x in (-12,-11,-10,-9): R(d,x,4,-1,"west",4)
    # B chain
    d.set(-13,3,1,"stone"); d.set(-13,4,1,W); Wd(d,-12,4,1)
    for x in (-11,-10): R(d,x,4,1,"west",4)
    d.set(-9,3,1,"observer",facing="up"); R(d,-9,4,1,"west",4,sup=None)
    # torch feed
    Wd(d,-13,3,0); d.set(-12,2,0,"stone"); d.set(-12,3,0,"repeater",facing="west",delay=1)
    Wd(d,-10,3,0)
    # Q2 descent
    d.set(-7,3,-1,"stone"); d.set(-7,4,-1,W); d.set(-6,2,-1,"stone"); d.set(-6,3,-1,W)
    # Rv
    R(d,-7,4,1,"west",2)
    # P2
    Wd(d,-9,2,1); R(d,-8,2,1,"west",4)
    # ascent z=-1
    d.set(-12,-2,-1,"stone"); d.set(-12,-1,-1,W)
    d.set(-13,-1,-1,"glass"); d.set(-13,0,-1,W)
    d.set(-12,0,-1,"glass"); d.set(-12,1,-1,W)
    d.set(-13,1,-1,"glass"); d.set(-13,2,-1,W)
    return d
def b15():
    d0 = Design.load("valid432.json")
    d = Design("open")
    for (x,y,z),(blk,pr) in d0.blocks.items():
        if x == -6: continue
        nx = x+1 if x <= -7 else x
        d.blocks[(nx,y,z)] = (blk,dict(pr))
    # fix Q2 descent
    d.remove(-5,1,-1); d.set(-5,2,-1,"stone"); d.set(-5,3,-1,W)
    return d
def b17():
    d0 = Design.load("valid408.json")
    d = Design("open")
    for (x,y,z),(blk,pr) in d0.blocks.items():
        if x == -5: continue
        nx = x+1 if x <= -6 else x
        d.blocks[(nx,y,z)] = (blk,dict(pr))
    d.remove(-4,1,-1); d.set(-4,2,-1,"stone"); d.set(-4,3,-1,W)
    return d
def b18():
    d0 = Design.load("valid384.json")
    d = Design("open")
    for (x,y,z),(blk,pr) in d0.blocks.items():
        if x == -4: continue
        nx = x+1 if x <= -5 else x
        d.blocks[(nx,y,z)] = (blk,dict(pr))
    d.remove(-3,1,-1); d.set(-3,2,-1,"stone"); d.set(-3,3,-1,W)
    return d
