def base():
    d = Design("open")
    S = "stone"
    for y in range(3):
        d.set(-1, y, 0, S); d.set(3, y, 0, S)
        d.set(-2, y, 0, "sticky_piston", facing="east")
        d.set(4, y, 0, "sticky_piston", facing="west")
    for x in range(3):
        d.set(x, -1, 0, S); d.set(x, 3, 0, S)
    d.set(1, -2, 0, "sticky_piston", facing="up")
    d.set(1, 4, 0, "sticky_piston", facing="down")   # B
    d.set(1, 5, 0, "sticky_piston", facing="down")   # A
    d.set(3, 3, 0, "sticky_piston", facing="west")   # F
    # west: lever + L + bottom machine
    d.set(-2, 1, 1, S)
    d.set(-2, 0, 1, "lever", face="ceiling", facing="north")
    d.set(-2, 2, 1, "redstone_wire")
    d.set(-2, -2, 1, S); d.set(-2, -1, 1, "redstone_wire")
    d.set(-2, -2, 0, "sticky_piston", facing="east")
    d.set(-1, -2, 0, "redstone_block")
    return d

def build5():
    d = base()
    S = "stone"
    d.set(-2, 2, 2, S); d.set(-2, 3, 2, "redstone_wire")
    d.set(-1, 3, 2, S); d.set(-1, 4, 2, "redstone_wire")
    d.set(0, 4, 2, "observer", facing="west")        # O1
    d.set(-1, 3, 3, S); d.set(-1, 4, 3, "redstone_wire")
    d.set(0, 4, 3, "redstone_wire")
    d.set(1, 4, 3, "repeater", facing="west", delay=4)   # R_d
    d.set(2, 4, 3, "redstone_wire")
    d.set(3, 3, 3, S); d.set(3, 4, 3, "redstone_wire")
    d.set(3, 3, 2, S); d.set(3, 4, 2, "redstone_wire")
    d.set(3, 3, 1, S); d.set(3, 4, 1, "redstone_wire")
    # BL
    d.set(1, 4, 1, "redstone_wire"); d.set(1, 4, 2, "redstone_wire")
    d.set(2, 4, 2, "repeater", facing="east", delay=2)  # R_b
    # O3 watching A
    d.set(1, 5, 1, "observer", facing="north")
    d.set(1, 5, 2, S)
    # right staircase
    d.set(4, 2, 3, S); d.set(4, 3, 3, "redstone_wire")
    d.set(4, 1, 2, S); d.set(4, 2, 2, "redstone_wire")
    d.set(4, 1, 1, S); d.set(4, 2, 1, "redstone_wire")
    # hold + O2
    d.set(4, 4, 3, "glass"); d.set(4, 5, 3, "redstone_wire")
    d.set(4, 4, 2, S); d.set(4, 5, 2, "redstone_wire")
    d.set(4, 3, 1, S); d.set(4, 4, 1, "repeater", facing="south", delay=4)
    d.set(4, 3, 0, S); d.set(4, 4, 0, "redstone_wire")
    d.set(4, 5, 1, "observer", facing="south")       # O2
    d.set(4, 5, 0, S)
    d.set(3, 4, 0, S); d.set(3, 5, 0, "repeater", facing="east", delay=1)
    d.set(2, 4, 0, "glass"); d.set(2, 5, 0, "repeater", facing="east", delay=4)
    return d
d5 = build5()
d5.save("d5.json")
r = test(d5)
print(str(r)[:1200])
