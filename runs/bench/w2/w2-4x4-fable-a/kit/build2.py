def left_side():
    d = Design("open")
    for y in (1, 2):
        d.set(-3, y, 0, "sticky_piston", facing="east")
        d.set(-2, y, 0, "sticky_piston", facing="east")
    d.set(-1, 4, 0, "sticky_piston", facing="down")
    d.set(-1, -1, 0, "sticky_piston", facing="up")
    d.set(-2, 3, 0, "observer", facing="up")
    d.set(-2, 4, 0, "repeater", facing="south")
    d.set(-3, 1, 1, "stone"); d.set(-3, 2, 1, "redstone_wire")
    d.set(-2, 2, 1, "observer", facing="west")
    d.set(-2, 3, 1, "glass"); d.set(-2, 4, 1, "redstone_wire")
    d.set(-3, 1, 2, "stone"); d.set(-3, 2, 2, "redstone_wire")
    d.set(-2, 2, 2, "stone"); d.set(-2, 3, 2, "redstone_wire")
    d.set(-1, 4, 2, "redstone_wire")
    d.set(-2, 2, -1, "stone"); d.set(-2, 3, -1, "redstone_wire")
    d.set(-1, 4, -1, "redstone_wire")
    d.set(-1, 5, 0, "stone"); d.set(-1, 6, 0, "redstone_wire")
    d.set(-1, -2, 0, "stone")
    return d

def obs(d, x, y, z, f): d.set(x, y, z, "observer", facing=f)

def control(d):
    d.set(-3, 4, -1, "stone")
    d.set(-3, 4, -2, "lever", face="wall", facing="north")
    obs(d, -4, 3, -1, "up"); d.set(-4, 4, -1, "redstone_wire")
    for y in (2, 1, 0, -1): obs(d, -4, y, -1, "up")
    obs(d, -4, 5, -1, "down"); obs(d, -3, 3, -1, "west")
    obs(d, -2, 4, -1, "up"); obs(d, -2, 5, -1, "south")
    obs(d, -4, 6, -1, "down"); obs(d, -4, 6, 0, "north"); obs(d, -4, 6, 1, "north")
    obs(d, -3, 6, 1, "west"); obs(d, -3, 6, 0, "south"); obs(d, -2, 6, 0, "west")
    obs(d, -3, 5, 1, "up"); obs(d, -3, 5, 2, "north"); obs(d, -2, 5, 2, "west")
    obs(d, -2, 5, 1, "south"); obs(d, -2, 5, 0, "south")
    obs(d, -4, 0, 0, "north"); obs(d, -4, 0, 1, "north"); obs(d, -4, 0, 2, "north")
    obs(d, -4, 1, 2, "down"); obs(d, -4, 1, 1, "south"); obs(d, -4, 2, 1, "down"); obs(d, -4, 3, 1, "down")
    d.set(-4, 4, 1, "redstone_wire")
    d.set(-3, 3, 1, "glass"); d.set(-3, 4, 1, "repeater", facing="west", delay=4)
    d.set(-3, 3, 0, "glass"); d.set(-3, 4, 0, "repeater", facing="north", delay=1)
    d.set(-1, 4, 1, "glass"); d.set(-1, 5, 1, "redstone_wire"); d.set(0, 5, 1, "redstone_wire")
    d.set(0, 6, 1, "stone"); d.set(-1, 6, 1, "stone")
    # bottom
    for z in (-1, 0, 1):
        d.set(-4, -3, z, "stone"); d.set(-4, -2, z, "redstone_wire")
    for x in range(-4, 5):
        d.set(x, -3, 2, "stone"); d.set(x, -2, 2, "redstone_wire")
    for x in range(-1, 5):
        d.set(x, -3, 1, "stone"); d.set(x, -2, 1, "repeater", facing="south")
    return d

def door(state="open"):
    L = left_side()
    d = Design(state)
    d.merge(L); d.merge(L.mirrored_x(3))
    for x in range(4):
        d.set(x, 5, 0, "sticky_piston", facing="down")
        d.set(x, -2, 0, "sticky_piston", facing="up")
        d.set(x, 6, 0, "redstone_wire")
        d.set(x, 5, 2, "redstone_wire")
        d.set(x, 5, -1, "redstone_wire"); d.set(x, 6, -1, "stone")
    for y in range(4):
        d.set(-1, y, 0, "stone"); d.set(4, y, 0, "stone")
    for x in range(4):
        d.set(x, 4, 0, "stone"); d.set(x, -1, 0, "stone")
    control(d)
    return d
LEV = (-3, 4, -2)
