FL = {"east": "west", "west": "east"}
CROSS = dict(north="side", south="side", east="side", west="side")

def module(d, right):
    def X(x): return 3 - x if right else x
    def F(f): return FL.get(f, f) if right else f
    def s(x, y, z, b, **p):
        if "facing" in p: p["facing"] = F(p["facing"])
        d.set(X(x), y, z, b, **p)
    # z=0 mechanism
    for y in (1, 2):
        s(-3, y, 0, "sticky_piston", facing="east")
        s(-2, y, 0, "sticky_piston", facing="east")
    for y in (0, 1, 2, 3):
        s(-1, y, 0, "stone")
    s(-1, -1, 0, "sticky_piston", facing="up")
    s(-1, 4, 0, "sticky_piston", facing="down")
    s(-1, 5, 0, "stone"); s(-1, 6, 0, "redstone_wire")
    s(-4, 2, 0, "stone"); s(-4, 3, 0, "redstone_wire")
    s(-1, -2, 0, "redstone_wall_torch", facing="north", lit=False)
    # z=1
    s(-1, -2, 1, "stone")                                   # Bq
    s(-2, -3, 1, "stone"); s(-2, -2, 1, "repeater", facing="east", delay=1, powered=True)
    s(-2, -1, 1, "observer", facing="down")
    s(-2, 0, 1, "observer", facing="down")
    s(-2, 1, 1, "stone")                                    # Y
    s(-2, 2, 1, "redstone_wire", **CROSS)                   # D2
    s(-2, 3, 1, "stone")                                    # Z
    s(-2, 4, 1, "observer", facing="up")                    # Ou
    s(-2, 5, 1, "redstone_wire")                            # raw
    s(-1, 4, 1, "glass"); s(-1, 5, 1, "redstone_wire")
    s(-3, 3, 1, "observer", facing="west")                  # Ow
    s(-4, 3, 1, "note_block"); s(-4, 4, 1, "redstone_wire")
    s(-1, 6, 1, "stone"); s(-2, 6, 1, "stone")              # cutters

def far_diag(d, right):
    def X(x): return 3 - x if right else x
    for (x, y) in ((-1, 6), (-2, 6), (-3, 5), (-4, 4)):
        d.set(X(x), y - 1, 2, "stone"); d.set(X(x), y, 2, "redstone_wire")

def common(d):
    for x in range(4):
        d.set(x, 5, 0, "sticky_piston", facing="down"); d.set(x, 6, 0, "redstone_wire")
        d.set(x, 4, 0, "stone"); d.set(x, -1, 0, "stone")
        d.set(x, -2, 0, "sticky_piston", facing="up")
        d.set(x, -3, 0, "redstone_wall_torch", facing="north", lit=False)
        d.set(x, -3, 1, "stone"); d.set(x, -2, 1, "redstone_wire", power=15)
        d.set(x, 5, 1, "redstone_wire"); d.set(x, 6, 1, "stone")
        d.set(x, 5, 2, "stone"); d.set(x, 6, 2, "redstone_wire")
    # BL feed
    d.set(1, -2, 2, "stone")
    d.set(2, -3, 2, "stone"); d.set(2, -2, 2, "repeater", facing="east", delay=2, powered=True)
    d.set(3, -2, 2, "stone")
    d.set(4, -3, 2, "stone"); d.set(4, -2, 2, "redstone_wire", power=15)

def core():
    d = Design("open")
    module(d, False); module(d, True); far_diag(d, False); far_diag(d, True); common(d)
    return d
