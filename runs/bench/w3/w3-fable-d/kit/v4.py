exec(open('v3.py').read())
def build_v4():
    d = Design("closed")
    S = lambda x,y,z: d.set(x,y,z,"stone")
    W = lambda x,y,z,**p: d.set(x,y,z,"redstone_wire",**p)
    door_plane(d)
    # T assembly, left edge
    d.set(-1,4,0,"note_block",powered=True); W(-1,5,0,power=14); S(0,5,0)
    d.set(0,4,0,"observer",facing="west")
    S(-2,4,0); W(-2,5,0,power=15)
    S(-2,4,1); d.set(-2,5,1,"repeater",facing="south",delay=4,powered=True)
    # X row y=5 z=2
    S(-2,4,2); W(-2,5,2,power=13)
    d.set(-1,4,2,"observer",facing="down"); W(-1,5,2,power=14)
    S(0,4,2); W(0,5,2,power=14); S(1,4,2); W(1,5,2,power=15)
    d.set(2,5,2,"observer",facing="east")              # obs2 watches D (3,5,2)
    # K
    S(1,4,3); d.set(1,5,3,"redstone_torch")
    # N net
    W(-1,3,2)
    S(-1,3,1); W(-1,4,1); S(-1,5,1)
    S(-1,3,3); W(-1,4,3); W(0,4,3); S(-1,5,3); S(0,5,3)
    d.set(-1,3,4,"lever",face="wall",facing="south")
    # chain row 1
    for x in (0,1,2):
        d.set(x,4,1,"repeater",facing="west",delay=4)
    S(3,4,1); d.set(3,4,0,"redstone_wall_torch",facing="north")
    # D net
    W(3,5,1); S(3,4,2); W(3,5,2); S(3,4,3); W(3,5,3); S(4,3,3); W(4,4,3)
    W(2,4,3)
    # sides
    d.set(-2,2,1,"redstone_wall_torch",facing="north"); S(-2,0,1); W(-2,1,1); S(-2,2,2); W(-2,3,2)
    d.set(4,2,1,"redstone_wall_torch",facing="north"); S(4,0,1); W(4,1,1,**CROSS); S(4,2,2); W(4,3,2)
    # bottom
    S(-2,-1,2); W(-2,0,2); S(-2,-2,3); W(-2,-1,3)
    for x in (-1,0,1): S(x,-3,3); W(x,-2,3)
    S(1,-3,2); W(1,-2,2); S(1,-3,1); W(1,-2,1)
    return d
