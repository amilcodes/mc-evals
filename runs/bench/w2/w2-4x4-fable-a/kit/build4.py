def side4():
    d = Design("open")
    def o(x, y, z, f): d.set(x, y, z, "observer", facing=f)
    for y in (1, 2):
        d.set(-3, y, 0, "sticky_piston", facing="east")
        d.set(-2, y, 0, "sticky_piston", facing="east")
    d.set(-1, 4, 0, "sticky_piston", facing="down")
    d.set(-1, -1, 0, "sticky_piston", facing="up")
    d.set(-1, 5, 0, "stone"); d.set(-1, -2, 0, "stone")
    # injections
    d.set(-2, 2, -1, "stone"); o(-2, 3, -1, "up"); o(-2, 1, -1, "down")
    d.set(-3, 2, -1, "stone"); o(-3, 1, -1, "down")
    o(-3, 3, 0, "up")
    o(-2, 2, 1, "west")
    # L0 left of trunk
    d.set(-1, 4, -1, "redstone_wire"); d.set(-2, 4, -1, "redstone_wire")
    # main top
    o(-1, 5, -1, "east"); o(-2, 5, -1, "east"); o(-3, 5, -1, "east")
    o(-3, 5, 0, "north"); o(-2, 5, 0, "west")
    o(-4, 5, -1, "east"); o(-4, 5, 0, "north")
    for y in range(4, -3, -1): o(-4, y, 0, "up")
    o(-3, -2, 0, "west"); o(-2, -2, 0, "west")
    o(-2, -2, 1, "north"); o(-1, -2, 1, "west"); o(0, -2, 1, "west"); d.set(1, -2, 1, "stone")
    o(-2, -1, 1, "down"); o(-2, -1, 0, "south")
    d.set(-2, -2, -1, "glass"); d.set(-2, -1, -1, "redstone_wire"); o(-2, 0, -1, "down")
    # ascent lane
    o(-3, -1, 1, "east"); o(-4, -1, 1, "east")
    for y in range(0, 6): o(-4, y, 1, "down")
    o(-3, 5, 1, "west"); o(-2, 5, 1, "west"); o(-1, 5, 1, "west")
    d.set(0, 5, 1, "redstone_wire"); d.set(1, 5, 1, "stone"); d.set(-1, 4, 1, "redstone_wire")
    # gate
    d.set(-2, 3, 0, "glass"); d.set(-2, 4, 0, "repeater", facing="north")
    d.set(-2, 3, 1, "glass"); d.set(-2, 4, 1, "repeater", facing="east")
    d.set(-3, 4, 1, "redstone_wire")
    # B
    o(-3, 4, 0, "south"); o(-3, 3, 1, "up"); o(-3, 2, 1, "up")
    o(-3, 1, 1, "up"); o(-3, 0, 1, "up"); o(-3, 0, 0, "south"); o(-3, 0, -1, "south")
    o(-4, 0, -1, "east"); o(-4, -1, -1, "up"); o(-3, -1, -1, "west")
    return d

def door4():
    L = side4()
    d = Design("open")
    d.merge(L); d.merge(L.mirrored_x(3))
    for x in range(4):
        d.set(x, 5, 0, "sticky_piston", facing="down")
        d.set(x, -2, 0, "sticky_piston", facing="up")
        d.set(x, 5, -1, "redstone_wire")
    for y in range(4):
        d.set(-1, y, 0, "stone"); d.set(4, y, 0, "stone")
    for x in range(4):
        d.set(x, 4, 0, "stone"); d.set(x, -1, 0, "stone")
    d.set(1, 5, -2, "lever", face="floor", facing="north")
    return d
LEV = (1, 5, -2)
