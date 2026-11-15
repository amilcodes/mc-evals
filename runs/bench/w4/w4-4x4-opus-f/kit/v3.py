exec(open('v2.py').read())
SIDE_LINES3 = {
  -1: ('obs',[1]*7),                 # spit 16
   0: (None,[2,2,2,2,2,2,1,1]),      # level 28
   1: ('obs',[4,4,4,1,1,1,2]),       # p1 36 (w8)
   2: ('obs',[4]*7),                 # p2 58
   4: ('obs',[4,2,2,2,2,2,2]),       # R_A 34
   5: ('obs',[4,4,4,2,2,2,2]),       # R_B 42
   6: ('obs',[4,4,4,4,2,2,2]),       # R_C 46
}
def full3(side_lines=SIDE_LINES3, krep_z=-8):
    b = base(); top_brain(b, lever=False); side_brain(b, zL=-16, lines=LINES2)
    # strip z=- comb: everything at z<=-8, plus K stair / R line remnants
    for p in list(b.blocks):
        if p[2] <= -8: b.remove(*p)
    for p in [(-2,1,-7),(-2,0,-6),(-2,-1,-5),(-2,-2,-4),(-2,0,-7),(-2,-1,-6),(-2,-2,-5),(-2,-3,-4),
              (-1,-2,-4),(-1,-3,-4),(-1,-2,-3),(-1,-3,-3)]:
        b.remove(*p)
    for x0 in (-3,6):
        for z in range(-7,-3):
            b.remove(x0,5,z); b.remove(x0,4,z)
    # S row reps on z=-
    b.set(-1,5,-7,"repeater",facing="east"); b.set(3,5,-7,"repeater",facing="west")
    # lever + shared L
    b.set(4,7,12,"stone"); b.set(4,7,13,"lever",face="wall",facing="south")
    Y=8
    for x in range(-1,7):
        if x==3: continue
        b.set(x,Y,12,"redstone_wire"); sup(b,x,Y-1,12)
    b.set(3,Y,12,"redstone_wire"); sup(b,3,Y-1,12)
    for x,(kind,ds) in side_lines.items():
        z = 11
        if kind=='obs':
            b.set(x,Y,z,"observer",facing="south"); sup(b,x,Y-1,z); z-=1
        for dl in ds:
            b.set(x,Y,z,"repeater",facing="south",delay=dl); sup(b,x,Y-1,z); z-=1
    for x in range(-1,3):
        b.set(x,Y,3,"redstone_wire"); sup(b,x,Y-1,3)
    for x in range(4,7):
        b.set(x,Y,3,"redstone_wire"); sup(b,x,Y-1,3)
    for p in [(1,8,2),(2,8,2),(3,8,2)]: b.set(*p,"stone")
    # S crossing x=0
    for z in range(2,-4,-1):
        b.set(0,8,z,"redstone_wire")
        if z==0: b.set(0,7,0,"glass")
        else: sup(b,0,7,z)
    for (y,z) in [(7,-4),(6,-5),(5,-6)]:
        b.set(0,y,z,"redstone_wire"); sup(b,0,y-1,z)
    # R crossing x=4
    b.set(4,8,2,"redstone_wire"); sup(b,4,7,2)
    b.set(4,8,1,"repeater",facing="south"); sup(b,4,7,1)
    b.set(4,8,0,"redstone_wire"); sup(b,4,7,0)
    for (y,z) in [(7,-1),(6,-2)]:
        b.set(4,y,z,"redstone_wire"); sup(b,4,y-1,z)
    # K path from top K block
    b.set(-2,5,0,"redstone_wire")
    b.set(-2,5,-1,"redstone_wire"); sup(b,-2,4,-1)
    b.set(-2,6,-2,"redstone_wire"); sup(b,-2,5,-2)
    for z in range(-3,-12,-1):
        if z==krep_z: b.set(-2,7,z,"repeater",facing="south")
        else: b.set(-2,7,z,"redstone_wire")
        sup(b,-2,6,z)
    b.set(-3,7,-11,"redstone_wire"); sup(b,-3,6,-11)
    for k in range(1,10):
        y=7-k; z=-11+k
        b.set(-3,y,z,"redstone_wire"); sup(b,-3,y-1,z)
    b.set(-2,-2,-2,"repeater",facing="west"); sup(b,-2,-3,-2)
    return b
