def left_side():
    d = Design("open")
    for y in (1, 2):
        d.set(-3, y, 0, "sticky_piston", facing="east")
        d.set(-2, y, 0, "sticky_piston", facing="east")
    d.set(-1, 4, 0, "sticky_piston", facing="down")
    d.set(-1, -1, 0, "sticky_piston", facing="up")
    # home observer from R edges
    d.set(-2, 3, 0, "observer", facing="up")
    d.set(-2, 4, 0, "repeater", facing="south")
    d.set(-2, 5, 0, "stone")
    # +z : R local net
    d.set(-3, 1, 1, "stone"); d.set(-3, 2, 1, "redstone_wire")
    d.set(-2, 2, 1, "observer", facing="west")
    d.set(-2, 3, 1, "glass"); d.set(-2, 4, 1, "redstone_wire")
    d.set(-3, 1, 2, "stone"); d.set(-3, 2, 2, "redstone_wire")
    d.set(-2, 2, 2, "stone"); d.set(-2, 3, 2, "redstone_wire")
    d.set(-1, 4, 2, "redstone_wire")
    # -z : F1 + U-edge
    d.set(-2, 2, -1, "stone"); d.set(-2, 3, -1, "redstone_wire")
    d.set(-2, 4, -1, "observer", facing="up")
    d.set(-2, 5, -1, "repeater", facing="south", delay=3)
    d.set(-1, 4, -1, "redstone_wire")
    # U top
    d.set(-1, 5, 0, "stone"); d.set(-1, 6, 0, "redstone_wire"); d.set(-2, 6, 0, "redstone_wire")
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
    if state == "open":
        for y in range(4):
            d.set(-1, y, 0, "stone"); d.set(4, y, 0, "stone")
        for x in range(4):
            d.set(x, 4, 0, "stone"); d.set(x, -1, 0, "stone")
    return d
