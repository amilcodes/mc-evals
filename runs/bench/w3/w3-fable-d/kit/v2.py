def front(d):
    S = lambda x,y,z: d.set(x,y,z,"stone")
    W = lambda x,y,z,**p: d.set(x,y,z,"redstone_wire",**p)
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
    # z=2
    d.set(1,4,2,"note_block",powered=True)
    W(1,5,2,power=15,north="side",south="side",east="side",west="side")
    S(-2,2,2); W(-2,3,2); S(4,2,2); W(4,3,2); S(3,3,2); W(3,4,2)
    d.set(1,4,3,"repeater",facing="south",delay=4,powered=True)

def bottom_v1(d):
    S = lambda x,y,z: d.set(x,y,z,"stone")
    W = lambda x,y,z,**p: d.set(x,y,z,"redstone_wire",**p)
    S(1,-3,1); W(1,-2,1)
    S(-2,-1,2); W(-2,0,2); S(1,-3,2); W(1,-2,2)
    S(-2,-2,3); W(-2,-1,3); S(1,-3,3); W(1,-2,3)
    S(-2,-3,4); W(-2,-2,4)
    for x in (-1,0,1):
        S(x,-3,4); W(x,-2,4)

def control_v2(d):
    S = lambda x,y,z: d.set(x,y,z,"stone")
    W = lambda x,y,z,**p: d.set(x,y,z,"redstone_wire",**p)
    W(1,4,4,power=15)                                   # X
    d.set(0,4,4,"observer",facing="west")               # obs1 watches N (-1,4,4)
    d.set(2,4,4,"observer",facing="east")               # obs2 watches D (3,4,4)
    d.set(1,4,5,"redstone_wall_torch",facing="north")   # K
    S(1,4,6)                                            # Kb
    # N net
    S(-2,3,3); W(-2,4,3); S(-2,3,4); W(-2,4,4)
    for z in (4,5,6,7):
        S(-1,3,z); W(-1,4,z)
    W(0,4,6)
    S(-2,3,5); d.set(-2,4,5,"lever",face="floor",facing="north")
    # chain
    for x in (0,1,2):
        d.set(x,4,7,"repeater",facing="west",delay=4)
    for z in range(3,8):
        S(3,3,z); W(3,4,z)
    W(2,4,6)

def build_v2():
    d = Design("closed")
    front(d); bottom_v1(d); control_v2(d)
    return d
