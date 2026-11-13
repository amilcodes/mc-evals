def build_v1():
    d = Design("closed")
    S = lambda x,y,z: d.set(x,y,z,"stone")
    W = lambda x,y,z,**p: d.set(x,y,z,"redstone_wire",**p)
    # doorway
    d.fill(0,0,0,2,2,0,"stone")
    for y in range(3):
        d.set(-2,y,0,"sticky_piston",facing="east",extended=True)
        d.set(-1,y,0,"piston_head",facing="east",type="sticky")
        d.set(4,y,0,"sticky_piston",facing="west",extended=True)
        d.set(3,y,0,"piston_head",facing="west",type="sticky")
    S(0,-1,0); S(2,-1,0)
    d.set(1,-2,0,"sticky_piston",facing="up",extended=True)
    d.set(1,-1,0,"piston_head",facing="up",type="sticky")
    S(0,3,0)
    d.set(1,3,0,"sticky_piston",facing="down")
    d.set(1,4,0,"piston_head",facing="down",type="sticky")
    d.set(1,5,0,"sticky_piston",facing="down",extended=True)
    d.set(3,3,0,"sticky_piston",facing="west",extended=True)
    d.set(2,3,0,"piston_head",facing="west",type="sticky")
    # z=1
    d.set(1,4,1,"observer",facing="south"); S(1,5,1)
    d.set(3,3,1,"redstone_wall_torch",facing="north")
    d.set(-2,2,1,"redstone_wall_torch",facing="north"); S(-2,0,1); W(-2,1,1)
    d.set(4,2,1,"redstone_wall_torch",facing="north"); S(4,0,1)
    W(4,1,1,north="side",south="side",east="side",west="side")
    S(1,-3,1); W(1,-2,1)
    # z=2
    d.set(1,4,2,"note_block",powered=True); W(1,5,2,power=15)
    S(-2,2,2); W(-2,3,2); S(4,2,2); W(4,3,2); S(3,3,2); W(3,4,2)
    S(-2,-1,2); W(-2,0,2); S(1,-3,2); W(1,-2,2)
    # z=3
    W(1,4,3,power=15)
    S(-2,-2,3); W(-2,-1,3); S(1,-3,3); W(1,-2,3)
    # z=4
    d.set(1,4,4,"repeater",facing="south",delay=4,powered=True)
    S(-2,-3,4); W(-2,-2,4)
    for x in (-1,0,1):
        S(x,-3,4); W(x,-2,4)
    # D columns
    for z in range(3,12):
        S(-2,3,z); W(-2,4,z); S(4,3,z); W(4,4,z)
    # control
    W(1,4,5,power=15)
    d.set(0,4,5,"redstone_wall_torch",facing="north")
    d.set(2,4,5,"observer",facing="east"); S(3,3,5); W(3,4,5)
    S(0,4,6); W(0,5,6); d.set(1,4,6,"observer",facing="south")
    S(-1,3,6); W(-1,4,6); S(-1,5,6)
    W(0,4,7); W(1,4,7)
    d.set(2,4,7,"lever",face="floor",facing="north")
    for z in (8,9,10):
        d.set(1,4,z,"repeater",facing="north",delay=4)
    for x in range(-1,4):
        if x in (-1,3): S(x,3,11)
        W(x,4,11)
    return d
