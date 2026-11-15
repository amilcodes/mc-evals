def build2(dB=1, d3=4, d1=3):
    d = Design("open")
    S=lambda x,y,z,b="stone",**p: d.set(x,y,z,b,**p)
    W=lambda x,y,z: d.set(x,y,z,"redstone_wire")
    G=lambda x,y,z: d.set(x,y,z,"glass")
    for y in (0,1,2):
        S(-2,y,0,"sticky_piston",facing="east"); S(-1,y,0)
        S(4,y,0,"sticky_piston",facing="west"); S(3,y,0)
    S(1,-2,0,"sticky_piston",facing="up"); S(1,-1,0); S(0,-1,0); S(2,-1,0)
    # top module
    S(1,5,0,"sticky_piston",facing="down"); S(1,4,0,"sticky_piston",facing="down")
    S(1,3,0); S(0,3,0); S(2,3,0)
    S(-1,3,0,"sticky_piston",facing="east")
    W(2,4,0); S(3,4,0); W(3,5,0)
    # lever bottom right, hanging from frame stone
    S(2,-2,0,"lever",face="ceiling",facing="north")
    for z in (0,1,2): S(3,-2,z); W(3,-1,z)
    S(4,-2,2); W(4,-1,2)
    for y,z in ((0,1),(1,2),(2,1),(3,2),(4,1)):
        G(4,y-1,z); W(4,y,z)
    S(4,5,1)
    # crossing at level 4, z=2
    S(3,3,2); W(3,4,2); W(2,4,2)
    S(1,4,2,"repeater",facing="east",delay=d1)
    W(0,4,2); S(-1,3,2); W(-1,4,2); S(-2,3,2); W(-2,4,2)
    S(0,5,2); S(3,5,2)             # cut blocks
    # left top
    G(-2,2,1); W(-2,3,1); S(-2,3,0)
    G(-2,4,1); W(-2,5,1); G(-2,4,0); W(-2,5,0)
    G(-1,4,0); S(-1,5,0,"repeater",facing="west",delay=d3)
    G(-1,4,1); S(-1,5,1,"repeater",facing="west",delay=dB)
    G(0,4,1); W(0,5,1)
    S(0,4,0); S(0,5,0,"comparator",facing="west",mode="subtract")
    S(2,4,1); S(3,4,1,"observer",facing="east"); S(1,5,1,"observer",facing="west")
    S(2,5,1); W(3,5,1); S(2,5,0,"observer",facing="west")
    # pulse chain to left-bottom piston
    S(0,-2,0,"observer",facing="east"); S(-1,-2,0,"observer",facing="east"); S(-2,-2,0,"observer",facing="east")
    S(-2,-1,0,"observer",facing="down")
    return d
d=build2(); d.save("d2.json")
r=test(d); print(r)
