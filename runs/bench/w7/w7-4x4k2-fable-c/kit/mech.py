from pdbuild import Design

def left_half():
    d = Design("open")
    S = "stone"
    # frame stones (door stones at rest, open)
    for y in range(4):
        d.set(-1, y, 0, S)
    # K, F pistons
    for y in (1, 2):
        d.set(-3, y, 0, "sticky_piston", facing="east")
        d.set(-2, y, 0, "sticky_piston", facing="east")
    # V pistons
    d.set(-1, -1, 0, "sticky_piston", facing="up")
    d.set(-1, 4, 0, "sticky_piston", facing="down")
    # F feed (z=+1): corner dust, rest-stone, zigzag to low dust
    d.set(-1, 4, 1, "redstone_wire")
    d.set(-2, 2, 1, S); d.set(-2, 3, 1, "redstone_wire")
    d.set(-2, 2, 2, S); d.set(-2, 3, 2, "redstone_wire")
    d.set(-3, 1, 2, S); d.set(-3, 2, 2, "redstone_wire")
    d.set(-3, 0, 1, S); d.set(-3, 1, 1, "redstone_wire")
    d.set(-2, 0, 1, S); d.set(-2, 1, 1, "redstone_wire")
    # K feed (z=-1) stone + dust, fed over x=-4 column at y=4
    d.set(-3, 2, -1, S); d.set(-3, 3, -1, "redstone_wire")
    d.set(-4, 2, -1, S); d.set(-4, 3, -1, "redstone_wire")
    d.set(-4, 3, 0, S); d.set(-4, 4, 0, "redstone_wire")
    # V top-left via z=-1
    d.set(-1, 4, -1, S); d.set(-1, 5, -1, "redstone_wire")
    d.set(0, 5, -1, S); d.set(0, 6, -1, "redstone_wire")
    # V bottom-left: stone under V, repeater into it
    d.set(-1, -2, 0, S)
    return d

def middle():
    d = Design("open")
    S = "stone"
    for x in range(4):
        d.set(x, -1, 0, S); d.set(x, 4, 0, S)
        d.set(x, -2, 0, "sticky_piston", facing="up")
        d.set(x, 5, 0, "sticky_piston", facing="down")
        d.set(x, 6, 0, "redstone_wire")       # V top row
        d.set(x, 5, 1, "redstone_wire")       # F bus
        d.set(x, 6, 1, S)                     # cut stones
    for x in range(-1, 5):                    # V bottom row
        d.set(x, -3, 1, S); d.set(x, -2, 1, "repeater", facing="south")
        d.set(x, -3, 2, S); d.set(x, -2, 2, "redstone_wire")
    return d

def mech():
    L = left_half()
    d = middle()
    d.merge(L)
    d.merge(L.mirrored_x(3))
    return d
