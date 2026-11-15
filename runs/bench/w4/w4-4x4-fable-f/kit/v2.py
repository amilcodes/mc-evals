exec(open("core.py").read())
W = "redstone_wire"
def v2(bl_delay=3):
    d = core()
    d.set(2, -2, 2, "repeater", facing="east", delay=bl_delay, powered=True)
    # top-right z=0: QL injection at y=6
    d.set(5, 5, 0, "glass"); d.set(5, 6, 0, W)
    d.set(6, 5, 0, "glass"); d.set(6, 6, 0, "repeater", facing="east", delay=4)
    d.set(7, 5, 0, "glass"); d.set(7, 6, 0, "repeater", facing="east", delay=1)
    d.set(8, 5, 0, "stone"); d.set(8, 6, 0, W)
    d.set(9, 6, 0, "stone"); d.set(9, 5, 0, "lever", face="ceiling", facing="north")
    d.set(9, 3, 0, "stone"); d.set(9, 4, 0, W)
    d.set(10, 5, 0, "glass"); d.set(10, 6, 0, W)
    # raw-top via z=1
    d.set(6, 4, 1, "glass"); d.set(6, 5, 1, "repeater", facing="east", delay=1)
    d.set(7, 5, 1, "stone"); d.set(7, 6, 1, W)
    d.set(8, 5, 1, "stone"); d.set(8, 6, 1, W)
    # S1 chain
    d.set(8, 3, 1, "glass"); d.set(8, 4, 1, "repeater", facing="east", delay=4)
    d.set(9, 3, 1, "glass"); d.set(9, 4, 1, "comparator", facing="east", mode="subtract")
    d.set(10, 3, 1, "glass"); d.set(10, 4, 1, W, **CROSS)
    d.set(10, 5, 1, "observer", facing="up")
    d.set(10, 6, 1, "repeater", facing="north", delay=4)
    # spiral down
    d.set(10, 2, 0, "stone"); d.set(10, 3, 0, W)
    d.set(10, 1, 1, "stone"); d.set(10, 2, 1, W)
    d.set(9, 0, 1, "stone"); d.set(9, 1, 1, W)
    d.set(9, -1, 0, "stone"); d.set(9, 0, 0, W)
    d.set(10, -2, 0, "stone"); d.set(10, -1, 0, W)
    d.set(10, -3, 1, "stone"); d.set(10, -2, 1, W)
    d.set(10, -2, 2, "stone"); d.set(9, -2, 2, "redstone_wall_torch", facing="west", lit=True)
    for x in range(5, 9):
        d.set(x, -3, 2, "stone"); d.set(x, -2, 2, W, power=15)
    return d
