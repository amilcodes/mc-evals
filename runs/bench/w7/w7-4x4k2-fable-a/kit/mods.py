from pdbuild import Design

def left_module(d):
    for y in (1, 2):
        d.set(-3, y, 0, "sticky_piston", facing="east")
        d.set(-2, y, 0, "sticky_piston", facing="east")
        d.set(-1, y, 0, "stone")
    for y in (0, 3):
        d.set(-2, y, 0, "sticky_piston", facing="east")
        d.set(-1, y, 0, "stone")
    # front: B rep, E observer -> wall
    d.set(-3, 1, -1, "glass"); d.set(-3, 2, -1, "repeater", facing="north")
    d.set(-2, 2, -1, "observer", facing="west")
    d.set(-3, 1, -2, "glass"); d.set(-3, 2, -2, "redstone_wire")
    # back: A' observer watching B2, dust, fetch rep
    d.set(-3, 2, 1, "observer", facing="north")
    d.set(-3, 1, 2, "glass"); d.set(-3, 2, 2, "redstone_wire")
    d.set(-2, 1, 2, "glass"); d.set(-2, 2, 2, "redstone_wire")
    d.set(-2, 1, 1, "glass"); d.set(-2, 2, 1, "repeater", facing="south")
    return d

def top_module(d, x=0, s=1):
    w = "west" if s == 1 else "east"
    d.set(x, 6, 0, "sticky_piston", facing="down")
    d.set(x, 5, 0, "sticky_piston", facing="down")
    d.set(x, 4, 0, "stone")
    d.set(x, 5, -1, "glass"); d.set(x, 6, -1, "repeater", facing="north")
    d.set(x, 5, -2, "glass"); d.set(x, 6, -2, "redstone_wire")
    # fetch from the side at z=0
    d.set(x - s, 4, 0, "glass"); d.set(x - s, 5, 0, "repeater", facing=w)
    d.set(x - 2*s, 5, 0, "observer", facing=w)
    d.set(x - 3*s, 4, 0, "glass"); d.set(x - 3*s, 5, 0, "redstone_wire")
    return d

def top_link(d, x=0, s=1):
    # connects tap (x-3s,5,0) to B-dust (x,6,-2)
    for (a, c) in ((x - 3*s, -1), (x - 3*s, -2), (x - 2*s, -2), (x - s, -2)):
        d.set(a, 4, c, "glass"); d.set(a, 5, c, "redstone_wire")
    return d

def bottom_module(d, x=0, s=1):
    w = "west" if s == 1 else "east"
    d.set(x, -3, 0, "sticky_piston", facing="up")
    d.set(x, -2, 0, "sticky_piston", facing="up")
    d.set(x, -1, 0, "stone")
    for i in (0, 1, 2):
        d.set(x - s*i, -3, -1, "stone"); d.set(x - s*i, -2, -1, "redstone_wire")
    d.set(x - 3*s, -2, -1, "stone"); d.set(x - 3*s, -1, -1, "redstone_wire")
    d.set(x - 3*s, -2, 0, "glass"); d.set(x - 3*s, -1, 0, "redstone_wire")
    d.set(x - 2*s, -1, 0, "observer", facing=w)
    d.set(x - s, -2, 0, "glass"); d.set(x - s, -1, 0, "repeater", facing=w)
    return d
