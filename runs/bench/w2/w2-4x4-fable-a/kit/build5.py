exec(open('build4.py').read())
def door5():
    L = side4()
    def o(d, x, y, z, f): d.set(x, y, z, "observer", facing=f)
    # ---- right side: mirror, then strip lanes and rebuild bottom
    R = L.mirrored_x(3)
    for p in list(R.blocks):
        if p[0] == 7: R.remove(*p)
    for p in [(6,-1,1),(6,5,1),(5,5,1),(4,5,1),(6,-1,-1),(5,-1,-1),(5,-2,-1),(5,-1,1),(5,-1,0),(2,5,1)]:
        R.remove(*p)
    o(R, 6,-2,0,"north"); o(R, 6,-2,-1,"west"); o(R, 5,-2,-1,"west")
    o(R, 6,-1,-1,"down"); o(R, 6,-1,0,"north")
    R.set(6,-2,1,"glass"); R.set(6,-1,1,"redstone_wire")
    o(R, 5,-1,1,"east"); o(R, 5,0,1,"down"); o(R, 5,0,0,"south"); o(R, 5,-1,0,"up"); o(R, 5,-1,-1,"south")
    # ---- left side modifications
    L.remove(-2,-2,-1); o(L, -2,-2,-1,"west"); o(L, -3,-2,-1,"south")
    L.remove(-3,-1,1); L.remove(-4,-1,1)
    o(L, -3,-1,0,"east"); o(L, -3,-1,1,"north"); o(L, -3,-2,1,"up"); o(L, -4,-2,1,"east"); o(L, -4,-1,1,"down")
    d = Design("open")
    d.merge(L); d.merge(R)
    for x in range(-1, 5): o(d, x, -2, -1, "west")
    for x in range(4):
        d.set(x, 5, 0, "sticky_piston", facing="down")
        d.set(x, -2, 0, "sticky_piston", facing="up")
        d.set(x, 5, -1, "redstone_wire")
    d.set(2, 5, -1, "stone"); d.set(2, 5, -2, "lever", face="wall", facing="north")
    d.set(2, 5, 1, "repeater", facing="west")
    for y in range(4):
        d.set(-1, y, 0, "stone"); d.set(4, y, 0, "stone")
    for x in range(4):
        d.set(x, 4, 0, "stone"); d.set(x, -1, 0, "stone")
    return d
LEV = (2, 5, -2)
