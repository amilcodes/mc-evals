W="redstone_wire"
def R(d,x,y,z,f="west",dl=1,sup="stone"):
    if sup: d.set(x,y-1,z,sup)
    d.set(x,y,z,"repeater",facing=f,delay=dl)
def Wd(d,x,y,z,sup="stone"):
    if sup: d.set(x,y-1,z,sup)
    d.set(x,y,z,W)
def build():
    d = mech(False)
    # ---- M path (right side), fed from block (1,-2,1) via repeater (2,-2,1)
    d.set(1,-2,1,"stone")
    R(d,2,-2,1,"west",1)
    for (x,y,z),(sx,sy,sz),sup in [((3,-2,1),(3,-3,1),"stone"),((4,-1,1),(4,-2,1),"stone"),
                               ((5,0,1),(5,-1,1),"stone"),((5,1,0),(5,0,0),"stone"),((5,2,1),(5,1,1),"glass"),
                               ((4,2,1),(4,1,1),"stone"),((3,4,0),(3,3,0),"stone"),((3,5,1),(3,4,1),"glass"),
                               ((2,5,1),(2,4,1),"stone"),((1,5,1),(1,4,1),"stone"),((0,5,1),(0,4,1),"stone")]:
        d.set(sx,sy,sz,sup); d.set(x,y,z,W)
    d.set(3,3,1,W)
    # ---- G track
    d.set(-7,1,0,"stone")  # K
    for x in (-6,-5,-4): R(d,x,1,0)
    # ---- Q1 (z=1): y=0 track, step up to (-2,1,1)
    d.set(-2,0,1,"glass"); d.set(-2,1,1,W)
    Wd(d,-3,0,1)
    for x in (-4,-5,-6): R(d,x,0,1)
    R(d,-7,0,1,"west",4)          # Rq
    d.set(-3,1,1,"glass")
    # ---- P2 (z=1,y=2): block (-2,2,1) powered by repeater (-3,2,1)
    d.set(-2,2,1,"stone"); R(d,-3,2,1,"west",1,sup=None)
    # ---- Q2 (z=-1)
    d.set(-2,1,-1,"stone"); d.set(-2,2,-1,W)
    d.set(-3,1,-1,"glass"); d.set(-3,2,-1,W)
    for x in (-4,-5,-6): Wd(d,x,2,-1)
    Wd(d,-7,3,-1); Wd(d,-8,4,-1)
    # ---- V (z=1,y=4)
    d.set(-1,3,1,"stone"); d.set(-1,4,1,W); d.set(-1,5,1,"stone")
    for x in range(-7,-1): Wd(d,x,4,1)
    R(d,-8,4,1,"west",2)          # Rv
    # ---- K inputs
    R(d,-8,1,0,"west",4)          # R1
    R(d,-7,1,-1,"north",2)        # R2b: input from north (-7,1,-2), output south into K
    Wd(d,-7,1,-2)
    R(d,-8,1,-2,"west",4)         # R2a
    # ---- pulse line P from observer O (-12,2,0) facing up
    for p in [(-12,1,0),(-11,1,0),(-10,1,0),(-9,1,0),(-9,1,-1),(-9,1,-2),(-11,1,1),(-10,0,1),(-9,0,1),(-8,0,1)]:
        Wd(d,*p)
    # ---- module y=4
    d.set(-9,4,1,"comparator",facing="west",mode="subtract"); d.set(-9,3,1,"stone")   # B
    d.set(-9,4,-1,"comparator",facing="west",mode="subtract"); d.set(-9,3,-1,"stone") # A
    Wd(d,-9,4,0)                                                                     # T-dust
    d.set(-10,3,0,"stone"); d.set(-10,4,0,"redstone_torch")
    # torch feed
    Wd(d,-13,3,0); d.set(-12,2,0,"observer",facing="up"); d.set(-12,3,0,W); Wd(d,-11,3,0)
    # B chain z=1
    Wd(d,-14,4,1)
    for x in (-13,-12,-11): R(d,x,4,1,"west",4)
    d.set(-10,3,1,"observer",facing="up"); R(d,-10,4,1,"west",4,sup=None)   # RB on O3
    # A chain z=-1
    Wd(d,-15,4,-1)
    for x in (-14,-13,-12,-11,-10): R(d,x,4,-1,"west",4)
    # z=0 L
    Wd(d,-14,4,0); Wd(d,-15,4,0)
    # lever
    d.set(-15,3,1,"stone"); d.set(-15,4,1,"lever",face="floor",facing="north")
    # ---- P2 from O3 (-10,3,1) emitting down into (-10,2,1)
    d.set(-10,1,1,'glass'); d.set(-10,2,1,W); d.set(-10,2,0,'stone')
    R(d,-9,2,1,"west",4)          # P2 stretch
    Wd(d,-8,2,1); Wd(d,-7,2,1); Wd(d,-6,2,1); Wd(d,-5,2,1); Wd(d,-4,2,1)
    # ---- M feed: descend from (-15,4,0)->z=-2 path to (0,-2,1)
    path = [(-15,4,-2),(-14,3,-2),(-13,2,-2),(-12,1,-2),(-11,0,-2),(-10,-1,-2),(-9,-2,-2)]
    for p in path: Wd(d,*p)
    for x in range(-8,0): 
        if x in (-5,): R(d,x,-2,-2,"west",1)
        else: Wd(d,x,-2,-2)
    Wd(d,-1,-2,-1); Wd(d,-1,-2,0); Wd(d,-1,-2,1); Wd(d,0,-2,1)
    d.set(-11,2,1,'stone')
    return d
