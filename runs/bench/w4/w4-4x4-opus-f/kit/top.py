exec(open('base.py').read())
def sup(d,x,y,z,b="stone"):
    if (x,y,z) not in d.blocks and not is_wall(x,y,z): d.set(x,y,z,b)
def top_brain(d, zL=12, lever=True):
    Y=6
    # remove old top K feeds
    for p in [(-1,4,1),(-1,4,2),(4,4,1),(4,4,2),(-2,4,1),(-2,4,2),(5,4,1),(5,4,2)]:
        d.remove(*p)
    for x in range(-3,7):
        d.set(x,Y,zL,"redstone_wire"); sup(d,x,Y-1,zL)
    if lever:
        d.set(1,Y,zL+1,"lever",face="floor",facing="north"); sup(d,1,Y-1,zL+1)
    lines = {
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
    for x,(kind,ds) in lines.items():
        z = zL-1
        if kind=='obs':
            d.set(x,Y,z,"observer",facing="south"); sup(d,x,Y-1,z); z-=1
        for dl in ds:
            d.set(x,Y,z,"repeater",facing="south",delay=dl); sup(d,x,Y-1,z); z-=1
    # S net row z=4
    for x in range(-1,3):
        d.set(x,Y,4,"redstone_wire"); sup(d,x,Y-1,4)
    d.set(1,Y,3,"redstone_wire"); sup(d,1,Y-1,3)
    d.set(1,7,3,"stone")  # cut
    # R net
    for x in (3,4):
        d.set(x,Y,3,"redstone_wire"); sup(d,x,Y-1,3)
    d.set(3,6,2,"glass"); d.set(3,7,2,"redstone_wire")
    # K left/right
    for (xa,xb,sx) in [(-3,-2,1),(6,5,-1)]:
        d.set(xa,Y,5,"redstone_wire"); sup(d,xa,Y-1,5)
        d.set(xb,Y,5,"redstone_wire"); sup(d,xb,Y-1,5)
        d.set(xa,5,4,"redstone_wire"); sup(d,xa,4,4)
        d.set(xa,4,3,"redstone_wire"); sup(d,xa,3,3)
        d.set(xb,4,3,"redstone_wire"); sup(d,xb,3,3)
        d.set(xb,4,2,"repeater",facing="south"); sup(d,xb,3,2)
        d.set(xb,4,1,"repeater",facing="south"); sup(d,xb,3,1)
        d.set(xb,4,0,"stone")
    return d
