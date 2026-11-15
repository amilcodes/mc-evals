exec(open('top.py').read())
def both(d, x,y,z,b,**pr):
    d.set(x,y,z,b,**pr); d.set(3-x,y,z,b,**mirror_props(pr))
def side_brain(d, zL=-19, lines=None):
    # remove old z=+ R1 feeds and bottom stuff
    for x0 in (-3,6):
        for p in [(x0,3,1),(x0,3,2),(x0,2,1),(x0,2,2)]: d.remove(*p)
    for p in [(-1,-3,1),(-1,-2,1),(-1,-3,2),(-1,-2,2),(-1,-1,2),(4,-3,1),(4,-2,1),(4,-3,2),(4,-2,2),(4,-1,2)]:
        d.remove(*p)
    for x in range(0,4):
        for p in [(x,-3,1),(x,-2,1),(x,-3,2),(x,-2,2)]: d.remove(*p)
    # bottom K line on z=-
    for x in range(-1,5):
        d.set(x,-2,-2,"redstone_wire"); sup(d,x,-3,-2)
        d.set(x,-2,-1,"repeater",facing="north"); sup(d,x,-3,-1)
    # A path (z=+) both sides
    both(d,-2,-1,2,"repeater",facing="north")
    for (x,y,z) in [(-2,-1,3),(-2,0,4),(-3,0,4),(-3,1,3)]:
        both(d,x,y,z,"redstone_wire")
        if (x,y-1,z) not in d.blocks: both(d,x,y-1,z,"stone")
    # R stair ends
    for (x,y,z) in [(-3,3,-1),(-3,4,-2)]:
        both(d,x,y,z,"redstone_wire"); both(d,x,y-1,z,"stone")
    # S stairs
    for (x,y,z) in [(-2,1,-3),(-2,2,-4),(-2,3,-5),(-2,4,-6)]:
        both(d,x,y,z,"redstone_wire"); both(d,x,y-1,z,"stone")
    Y=5
    # S row z=-7, R row z=-3
    for x in range(-2,6):
        d.set(x,Y,-7,"redstone_wire"); sup(d,x,Y-1,-7)
    for x in range(-3,7):
        d.set(x,Y,-3,"redstone_wire"); sup(d,x,Y-1,-3)
    # K net + stair (left only)
    for x in (-2,-1):
        d.set(x,Y,-11,"redstone_wire"); sup(d,x,Y-1,-11)
    for k,(y,z) in enumerate([(4,-10),(3,-9),(2,-8),(1,-7),(0,-6),(-1,-5),(-2,-4)]):
        d.set(-2,y,z,"redstone_wire"); sup(d,-2,y-1,z)
    d.set(-1,-2,-4,"redstone_wire"); sup(d,-1,-3,-4)
    d.set(-1,-2,-3,"repeater",facing="north"); sup(d,-1,-3,-3)
    # L row
    for x in range(-3,7):
        d.set(x,Y,zL,"redstone_wire"); sup(d,x,Y-1,zL)
    if lines is None: lines = {
      -3: ('obs',[4,2]+[1]*12),          # R_A 15 el
      -2: (None,[2,2,2,2,1,1,1]),        # K_A
      -1: (None,[3,2,2,2,2,2,2]),        # K_B
       0: ('obs',[1]*10),                # S spit
       1: (None,[2,2,2,2]+[1]*7),        # S level
       2: ('obs',[2]*10), # S p1
       3: ('obs',[4,4,4,4,4,2,2,2,1,1]), # S p2
       6: ('obs',[4,3,2,2,2]+[1]*9),     # R_B
    }
    for x,(kind,ds) in lines.items():
        z = zL+1
        if kind=='obs':
            d.set(x,Y,z,"observer",facing="north"); sup(d,x,Y-1,z); z+=1
        for dl in ds:
            d.set(x,Y,z,"repeater",facing="north",delay=dl); sup(d,x,Y-1,z); z+=1
    return d
def lever_line(d, zL=-19, zTop=13):
    d.remove(1,6,13); d.remove(1,5,13)
    d.set(4,8,13,"lever",face="floor",facing="north"); d.set(4,7,13,"stone")
    d.set(4,6,13,"redstone_wire"); sup(d,4,5,13)
    for z in range(12,-10,-1):
        d.set(4,8,z,"repeater",facing="south"); sup(d,4,7,z)
    d.set(4,8,-10,"redstone_wire"); sup(d,4,7,-10)
    d.set(4,7,-11,"redstone_wire"); sup(d,4,6,-11)
    d.set(4,6,-12,"redstone_wire"); sup(d,4,5,-12)
    for z in range(-13,zL,-1):
        if z==-16: d.set(4,5,z,"repeater",facing="south")
        else: d.set(4,5,z,"redstone_wire")
        sup(d,4,4,z)
    return d
def full():
    b = base(); top_brain(b); side_brain(b); lever_line(b); return b
