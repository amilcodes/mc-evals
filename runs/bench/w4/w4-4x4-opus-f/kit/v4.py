exec(open('v3.py').read())
TOP_LINES = {
  -3: (None,[2,2,1,1,1,1]),  # K A (16)
  -2: (None,[2,2,2,2,2,2]),  # K B (24)
  -1: ('obs',[1,1,1,1,1,1]), # S spit
   0: (None,[1,1,1,2,2,2,2]), # S level 22
   1: ('obs',[4,4,4,2,1,1]), # S p1
   2: ('obs',[4,4,4,4,4,4]), # S p2
   3: ('obs',[4,4,2,1,1,1,1]), # R A
   4: ('obs',[4,4,4,3,1,1,1]), # R B
   5: (None,[2,2,2,2,2,2]),  # K B
   6: (None,[2,2,1,1,1,1]),  # K A
}
SIDE4 = {
  -3: ('obs',[1]*7),                 # spit 16
  -2: (None,[2,2,2,2,2,2,1,1]),      # level 28
  -1: ('obs',[4,4,4,1,1,1,2]),       # p1 36
   0: ('obs',[4]*7),                 # p2 58
   4: ('obs',[4,2,2,2,2,2]),         # R_A 34 (7 el)
   5: ('obs',[4,4,4,4,2,2]),         # R_B 42
   6: ('obs',[4,4,4,4,4,2]),         # R_C 46
}
def comb(d, Y, lines, zL=12, zEnd=None):
    for x,(kind,ds) in lines.items():
        z = zL-1
        if kind=='obs':
            d.set(x,Y,z,"observer",facing="south"); sup(d,x,Y-1,z); z-=1
        for dl in ds:
            d.set(x,Y,z,"repeater",facing="south",delay=dl); sup(d,x,Y-1,z); z-=1
def full4(side=SIDE4, top=TOP_LINES):
    b = full3()
    # wipe both old combs and crossings on z>=1 above y>=5 that belong to brains
    keep = set()
    for p in list(b.blocks):
        x,y,z = p
        if z >= 3 and y >= 5: b.remove(*p)
    for p in [(1,7,3),(1,8,2),(2,8,2),(3,8,2),(3,6,2),(3,7,2),(-1,7,3)]:
        b.remove(*p)
    for z in range(2,-4,-1):
        b.remove(0,8,z); b.remove(0,7,z)
    for p in [(0,7,-4),(0,6,-4),(0,6,-5),(0,5,-5),(0,5,-6)]: b.remove(*p)
    for p in [(4,8,2),(4,7,2),(4,8,1),(4,7,1),(4,8,0),(4,7,0),(4,7,-1),(4,6,-1),(4,6,-2),(4,5,-2)]:
        b.remove(*p)
    # old top K stairs at z=3..5 y<5
    for p in [(-3,4,3),(-3,3,3),(-2,4,3),(-2,3,3),(6,4,3),(6,3,3),(5,4,3),(5,3,3)]:
        b.remove(*p)
    # --- top comb Y=5
    Y=5
    for x in range(-3,7):
        b.set(x,Y,12,"redstone_wire"); sup(b,x,Y-1,12)
    comb(b,Y,top)
    for x in range(-1,3):
        b.set(x,Y,4,"redstone_wire"); sup(b,x,Y-1,4)
    b.set(1,5,3,"redstone_wire")
    for x in (3,4):
        b.set(x,Y,3,"redstone_wire"); sup(b,x,Y-1,3)
    b.set(4,6,2,"redstone_wire"); sup(b,4,5,2)
    b.set(3,6,2,"glass"); b.set(3,7,2,"redstone_wire")
    for (xa,xb) in [(-3,-2),(6,5)]:
        b.set(xa,Y,5,"redstone_wire"); sup(b,xa,Y-1,5)
        b.set(xb,Y,5,"redstone_wire"); sup(b,xb,Y-1,5)
        b.set(xa,4,4,"redstone_wire"); sup(b,xa,3,4)
        b.set(xa,4,3,"redstone_wire"); sup(b,xa,3,3)
        b.set(xb,4,3,"redstone_wire"); sup(b,xb,3,3)
    b.set(5,5,3,"stone")  # cut K'/R
    # --- lever
    b.remove(4,7,12); b.remove(4,7,13)
    b.set(4,6,12,"stone"); b.set(4,6,13,"lever",face="wall",facing="south")
    # --- side comb Y=7
    Y=7
    for x in range(-3,7):
        b.set(x,Y,12,"redstone_wire"); sup(b,x,Y-1,12)
    comb(b,Y,side)
    for x in range(-3,1):
        b.set(x,Y,3,"redstone_wire"); sup(b,x,Y-1,3)
    for x in range(4,7):
        b.set(x,Y,4,"redstone_wire"); sup(b,x,Y-1,4)
    # S crossing x=0
    for z in (2,1,0):
        b.set(0,7,z,"repeater",facing="south"); sup(b,0,6,z)
    for z in (-1,-2,-3,-4):
        b.set(0,7,z,"redstone_wire"); sup(b,0,6,z)
    b.set(0,6,-5,"redstone_wire"); sup(b,0,5,-5)
    b.set(0,5,-6,"redstone_wire")
    # R crossing x=5
    for z in (3,2,1,0):
        b.set(5,7,z,"repeater",facing="south"); sup(b,5,6,z)
    b.set(5,7,-1,"redstone_wire"); sup(b,5,6,-1)
    b.set(5,6,-2,"redstone_wire"); sup(b,5,5,-2)
    return b
SIDE5 = dict(SIDE4); SIDE5[-2] = (None,[2,2,2,2,2,1,1,1])
def full5():
    b = full4(side=SIDE5)
    b.set(0,7,1,"redstone_wire"); b.set(0,7,0,"redstone_wire"); b.set(0,6,0,"glass")
    for z in (3,2,1):
        b.set(5,7,z,"redstone_wire")
    return b
def full6():
    b = full5()
    b.set(5,7,2,"repeater",facing="south"); b.set(5,7,0,"redstone_wire")
    b.set(-2,5,-3,"repeater",facing="east")
    return b
SIDE7 = dict(SIDE5); SIDE7[4] = ('obs',[4,4,2,2,2,2])
def full7():
    b = full4(side=SIDE7)
    b.set(0,7,1,"redstone_wire"); b.set(0,7,0,"redstone_wire"); b.set(0,6,0,"glass")
    for z in (3,1,0): b.set(5,7,z,"redstone_wire")
    b.set(5,7,2,"repeater",facing="south")
    b.set(-2,5,-3,"repeater",facing="east")
    return b
def full8():
    b = full7()
    # remove z=- K path
    rm = [(-2,5,0),(-2,5,-1),(-2,4,-1),(-2,6,-2),(-2,5,-2),(-3,7,-11),(-3,6,-11),(-2,-2,-2),(-2,-3,-2)]
    for z in range(-3,-12,-1): rm += [(-2,7,z),(-2,6,z)]
    for k in range(1,10): rm += [(-3,7-k,-11+k),(-3,6-k,-11+k)]
    for p in rm: b.remove(*p)
    # restore R stair supports possibly removed
    for p in [(-3,4,-3),(-3,3,-2),(-3,2,-1)]:
        if p not in b.blocks: b.set(*p,"stone")
    # remove z=- bottom line
    for x in range(-1,5):
        for p in [(x,-2,-2),(x,-3,-2),(x,-2,-1),(x,-3,-1)]: b.remove(*p)
    # z=+ bottom line
    for x in range(-1,5):
        b.set(x,-2,2,"redstone_wire"); sup(b,x,-3,2)
        b.set(x,-2,1,"repeater",facing="south"); sup(b,x,-3,1)
    # K branch from (-2,4,3)
    for (x,y,z) in [(-2,3,4),(-2,2,5),(-2,1,6),(-2,0,7),(-2,-1,8),(-2,-2,9),(-1,-2,9),(-1,-2,7),(-1,-2,5),(-1,-2,3)]:
        b.set(x,y,z,"redstone_wire"); sup(b,x,y-1,z)
    for (z,dl) in [(8,1),(6,1),(4,2)]:
        b.set(-1,-2,z,"repeater",facing="south",delay=dl); sup(b,-1,-3,z)
    b.set(-1,-1,3,"stone")
    return b
def full9():
    b = full8()
    rm = []
    for (x,y,z) in [(-2,1,-3),(-2,2,-4),(-2,3,-5),(-2,4,-6),(-2,0,-3),(-2,1,-4),(-2,2,-5),(-2,3,-6)]:
        rm += [(x,y,z),(3-x,y,z)]
    for x in range(-2,6): rm += [(x,5,-7),(x,4,-7)]
    rm += [(0,7,-4),(0,6,-4),(0,6,-5),(0,5,-5),(0,5,-6)]
    for p in rm:
        if not is_wall(*p): b.remove(*p)
    # new S crossing tail
    b.set(0,6,-4,"redstone_wire"); sup(b,0,5,-4)
    # S row z=-5
    for x in range(-2,6):
        b.set(x,5,-5,"redstone_wire"); sup(b,x,4,-5)
    b.set(-1,5,-5,"repeater",facing="east"); b.set(3,5,-5,"repeater",facing="west")
    # spirals
    cells = [(-3,4,-5),(-3,3,-4),(-2,2,-4),(-2,1,-5),(-3,0,-5),(-3,0,-4),(-3,0,-3),(-2,0,-3)]
    for (x,y,z) in cells:
        for xx in (x, 3-x):
            b.set(xx,y,z,"redstone_wire"); sup(b,xx,y-1,z)
    return b
def full10():
    b = full9()
    # wipe z=- rows/stairs/spirals/crossing tails (y>=-1.. careful to keep B path)
    keep = {(-2,1,-1),(-2,0,-1),(-2,0,-2),(-2,-1,-2),(-2,-1,-1),(-2,-2,-1)}
    keep |= {(3-x,y,z) for (x,y,z) in keep}
    for p in list(b.blocks):
        x,y,z = p
        if z <= -1 and p not in keep and not (x==0 and y in (6,7) and z in (-1,-2)) and not (x==5 and y in (6,7) and z==-1):
            b.remove(*p)
    # check what's left at z<=-1
    # R crossing tail: (5,7,0)->(5,6,-1)->(5,5,-2)
    b.remove(5,7,-1)
    b.set(5,6,-1,"redstone_wire"); sup(b,5,5,-1)
    # R row z=-2
    for x in range(-3,7):
        b.set(x,5,-2,"redstone_wire"); sup(b,x,4,-2)
    for x0,s in ((-3,1),(6,-1)):
        b.set(x0,4,-1,"redstone_wire"); sup(b,x0,3,-1)
        b.remove(x0,4,0)
    # S crossing: (0,7,-1),(0,7,-2) dust exist? ensure
    for z in (-1,-2):
        b.set(0,7,z,"redstone_wire"); sup(b,0,6,z)
    b.set(0,6,-3,"redstone_wire"); sup(b,0,5,-3)
    # S row z=-4
    for x in range(-2,6):
        b.set(x,5,-4,"redstone_wire"); sup(b,x,4,-4)
    b.set(-1,5,-4,"repeater",facing="east"); b.set(3,5,-4,"repeater",facing="west")
    cells = [(-3,4,-4),(-3,3,-3),(-2,2,-3),(-2,1,-4),(-3,0,-4),(-3,0,-3),(-3,0,-2)]
    for (x,y,z) in cells:
        for xx in (x, 3-x):
            b.set(xx,y,z,"redstone_wire"); sup(b,xx,y-1,z)
    return b
TOP11 = {
  -3: (None,[2,2,2,1,1]),      # K_A 16
  -2: (None,[3,3,2,2,2]),      # K_B 24
  -1: (None,[2,2,1,1,1,1,2]),  # level 20 (+2 rep) -> 22
   0: ('obs',[1]*6),           # spit 14
   1: ('obs',[4,4,4,2,1,1]),   # p1 34
   2: ('obs',[4,4,4,4,4,3]),   # p2 48 (+2) -> 50
   3: ('obs',[4,4,2,2,1,1]),   # R_A 30
   4: ('obs',[4,4,4,3,2,1]),   # R_B 38
   5: (None,[3,3,2,2,2]),
   6: (None,[2,2,2,1,1]),
}
SIDE11 = {
  -3: ('obs',[1]*6),             # spit 14
  -2: (None,[2,2,2,2,1,1,1]),    # level 22
  -1: ('obs',[3,3,3,2,2,2]),     # p1 32 w6
   0: ('obs',[4]*6),             # p2 50
   4: ('obs',[4,4,4,2,1]),       # R_A 32
   5: ('obs',[4,4,4,4,3]),       # R_B 40
   6: ('obs',[4,4,4,4,1]),       # R_C 36
}
def full11(top=TOP11, side=SIDE11):
    b = full10()
    for p in list(b.blocks):
        x,y,z = p
        if z >= 4 and y >= 4: b.remove(*p)
    b.remove(4,6,12); b.remove(4,6,13); b.remove(1,5,3)
    zL = 11
    # top comb Y=5
    for x in range(-3,7):
        b.set(x,5,zL,"redstone_wire"); sup(b,x,4,zL)
    comb(b,5,top,zL=zL)
    b.set(0,5,3,"redstone_wire"); b.set(1,5,3,"redstone_wire")
    b.set(-1,5,3,"repeater",facing="south"); sup(b,-1,4,3)
    b.set(2,5,3,"repeater",facing="south")
    b.set(-1,5,2,"redstone_wire"); sup(b,-1,4,2)
    b.set(0,5,2,"redstone_wire")
    for (xa,xb) in [(-3,-2),(6,5)]:
        b.set(xa,5,5,"redstone_wire"); sup(b,xa,4,5)
        b.set(xb,5,5,"redstone_wire"); sup(b,xb,4,5)
        b.set(xa,4,4,"redstone_wire"); sup(b,xa,3,4)
    # lever
    b.set(4,6,zL,"stone"); b.set(4,6,zL+1,"lever",face="wall",facing="south")
    # side comb Y=7
    for x in range(-3,7):
        b.set(x,7,zL,"redstone_wire"); sup(b,x,6,zL)
    comb(b,7,side,zL=zL)
    for x in range(4,7):
        b.set(x,7,4,"redstone_wire"); sup(b,x,6,4)
    # K return: fewer reps
    b.set(-1,-2,6,"redstone_wire"); b.set(-1,-2,4,"repeater",facing="south",delay=1)
    return b
TOP12 = {
  -3: (None,[2,2,2,2]),        # K_A 16
  -2: (None,[3,3,3,3]),        # K_B 24
  -1: (None,[2,2,2,2,1,1,1]),  # level 22
   0: ('obs',[1]*6),           # spit 14
   1: ('obs',[4,4,4,2,1,1]),   # p1 34
   2: ('obs',[4]*6),           # p2 50
   3: ('obs',[4,4,2,2,2]),     # R_A 30
   4: ('obs',[4,4,4,4,2]),     # R_B 38
   5: (None,[3,3,3,3]),
   6: (None,[2,2,2,2]),
}
SIDE12 = {
  -3: ('obs',[1]*6),             # spit 14
  -2: (None,[2,2,2,2,1,1,1]),    # level 22
  -1: ('obs',[3,3,3,2,2,2]),     # p1 32 w6
   0: ('obs',[4,4,4,4,4,3]),     # p2 48 (+2 rep) = 50
   5: ('obs',[4,4,4,2,1]),       # R_A 32
   6: ('obs',[4,4,4,4,3]),       # R_B 40
}
def full12(top=TOP12, side=SIDE12):
    b = full11()
    for p in list(b.blocks):
        x,y,z = p
        if z >= 3 and y >= 4: b.remove(*p)
    zL = 10
    for x in range(-3,7):
        b.set(x,5,zL,"redstone_wire"); sup(b,x,4,zL)
    comb(b,5,top,zL=zL)
    # top S row at z=2
    for x in range(-1,3):
        b.set(x,5,2,"redstone_wire"); sup(b,x,4,2)
    for x in (3,4):
        b.set(x,5,3,"redstone_wire"); sup(b,x,4,3)
    b.set(5,5,3,"stone")
    for (xa,xb) in [(-3,-2),(6,5)]:
        b.set(xa,5,5,"redstone_wire"); sup(b,xa,4,5)
        b.set(xb,5,5,"redstone_wire"); sup(b,xb,4,5)
        b.set(xa,4,4,"redstone_wire"); sup(b,xa,3,4)
        b.set(xa,4,3,"redstone_wire"); sup(b,xa,3,3)
        b.set(xb,4,3,"redstone_wire"); sup(b,xb,3,3)
    b.set(4,6,zL,"stone"); b.set(4,6,zL+1,"lever",face="wall",facing="south")
    # side comb
    for x in range(-3,7):
        b.set(x,7,zL,"redstone_wire"); sup(b,x,6,zL)
    comb(b,7,side,zL=zL)
    for x in (-3,-2,-1):
        b.set(x,7,2,"redstone_wire"); sup(b,x,6,2)
    b.set(-1,7,1,"redstone_wire"); sup(b,-1,6,1)
    b.set(0,7,2,"repeater",facing="south"); sup(b,0,6,2)
    b.set(0,7,1,"redstone_wire"); sup(b,0,6,1)
    for x in (5,6):
        b.set(x,7,3,"redstone_wire"); sup(b,x,6,3)
    b.set(5,7,2,"repeater",facing="south"); sup(b,5,6,2)
    return b
SIDE13 = dict(SIDE12)
SIDE13[-2] = (None,[2,2,2,2,2,1,1])
SIDE13[-1] = ('obs',[3,3,3,3,2,2])
def comb2(d, Y, lines, zL):
    for x,(kind,ds) in lines.items():
        z = zL-1
        if kind=='obs':
            d.set(x,Y,z,"observer",facing="south"); sup(d,x,Y-1,z); z-=1
        for dl in ds:
            if dl==0: d.set(x,Y,z,"redstone_wire")
            else: d.set(x,Y,z,"repeater",facing="south",delay=dl)
            sup(d,x,Y-1,z); z-=1
TOP14 = {
  -3: (None,[2,1,1]), -2: (None,[4,2,2]),
  -1: (None,[2,1,1,1,1,1]),
   0: ('obs',[0,0,0,1,1]),
   1: ('obs',[4,4,1,1,2]),
   2: ('obs',[4,4,4,4,4]),
   3: ('obs',[4,2,2,2]),
   4: ('obs',[4,4,4,2]),
   5: (None,[4,2,2]), 6: (None,[2,1,1]),
}
SIDE14 = {
  -3: ('obs',[0,0,0,1,1]),
  -2: (None,[2,2,1,1,1,1]),
  -1: ('obs',[3,3,3,2,1]),
   0: ('obs',[4,4,4,4,3]),
   5: ('obs',[4,3,2,2]),
   6: ('obs',[4,4,4,3]),
}
def full14(top=TOP14, side=SIDE14, zL=9):
    b = full11()
    for p in list(b.blocks):
        x,y,z = p
        if z >= 3 and y >= 4: b.remove(*p)
    for x in range(-3,7):
        b.set(x,5,zL,"redstone_wire"); sup(b,x,4,zL)
    comb2(b,5,top,zL)
    for x in range(-1,3):
        b.set(x,5,2,"redstone_wire"); sup(b,x,4,2)
    for x in (3,4):
        b.set(x,5,3,"redstone_wire"); sup(b,x,4,3)
    b.set(5,5,3,"stone")
    for (xa,xb) in [(-3,-2),(6,5)]:
        b.set(xa,5,5,"redstone_wire"); sup(b,xa,4,5)
        b.set(xb,5,5,"redstone_wire"); sup(b,xb,4,5)
        b.set(xa,4,4,"redstone_wire"); sup(b,xa,3,4)
        b.set(xa,4,3,"redstone_wire"); sup(b,xa,3,3)
        b.set(xb,4,3,"redstone_wire"); sup(b,xb,3,3)
    b.set(4,6,zL,"stone"); b.set(4,6,zL+1,"lever",face="wall",facing="south")
    for x in range(-3,7):
        b.set(x,7,zL,"redstone_wire"); sup(b,x,6,zL)
    comb2(b,7,side,zL)
    for x in (-3,-2,-1):
        b.set(x,7,2,"redstone_wire"); sup(b,x,6,2)
    b.set(-1,7,1,"redstone_wire"); sup(b,-1,6,1)
    b.set(0,7,2,"repeater",facing="south"); sup(b,0,6,2)
    b.set(0,7,1,"redstone_wire"); sup(b,0,6,1)
    for x in (5,6):
        b.set(x,7,3,"redstone_wire"); sup(b,x,6,3)
    b.set(5,7,2,"repeater",facing="south"); sup(b,5,6,2)
    return b
TOP15 = {
  -3: (None,[1,1]), -2: (None,[3,3]),
  -1: (None,[1,1,1,1,1]),
   0: ('obs',[0,0,0,0]),
   1: ('obs',[3,3,2,1]),
   2: ('obs',[4,4,4,4]),
   3: ('obs',[4,2,1]),
   4: ('obs',[4,4,3]),
   5: (None,[3,3]), 6: (None,[1,1]),
}
SIDE15 = {
  -3: ('obs',[0,0,0,0]),
  -2: (None,[1,1,1,1,1]),
  -1: ('obs',[3,3,2,1]),
   0: ('obs',[4,4,4,4]),
   5: ('obs',[4,2,2]),
   6: ('obs',[4,4,4]),
}
def full15(top=TOP15, side=SIDE15):
    b = full14(top=top, side=side, zL=8)
    b.set(-1,-2,4,"redstone_wire")
    return b
