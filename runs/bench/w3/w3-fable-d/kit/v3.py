def door_plane(d):
    S = lambda x,y,z: d.set(x,y,z,"stone")
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

CROSS = dict(north="side",south="side",east="side",west="side")

def sides(d):
    S = lambda x,y,z: d.set(x,y,z,"stone")
    W = lambda x,y,z,**p: d.set(x,y,z,"redstone_wire",**p)
    d.set(3,3,1,"redstone_wall_torch",facing="north"); S(3,3,2); W(3,4,2)
    d.set(-2,2,1,"redstone_wall_torch",facing="north"); S(-2,0,1); W(-2,1,1); S(-2,2,2); W(-2,3,2)
    d.set(4,2,1,"redstone_wall_torch",facing="north"); S(4,0,1); W(4,1,1,**CROSS); S(4,2,2); W(4,3,2)

def t1_left(d):
    S = lambda x,y,z: d.set(x,y,z,"stone")
    W = lambda x,y,z,**p: d.set(x,y,z,"redstone_wire",**p)
    d.set(-1,4,0,"note_block",powered=True)
    W(-1,5,0,power=15,**CROSS)
    S(0,5,0)
    d.set(0,4,0,"observer",facing="west")
    S(-1,3,1); d.set(-1,4,1,"repeater",facing="south",delay=4,powered=True)

def control_v3(d):
    S = lambda x,y,z: d.set(x,y,z,"stone")
    W = lambda x,y,z,**p: d.set(x,y,z,"redstone_wire",**p)
    S(-1,3,2)
    for x in (-1,0,1): W(x,4,2,power=15)                  # X row
    d.set(-1,4,3,"observer",facing="south")               # obs1 watches N (-1,4,4)
    d.set(2,4,2,"observer",facing="east")                 # obs2 watches D (3,4,2)
    d.set(1,5,2,"redstone_wall_torch",facing="north")     # K on Kb (1,5,3)
    S(1,5,3)
    S(0,4,3); W(0,5,3); W(-1,5,3)                         # N aimed east into Kb
    S(2,4,3); W(2,5,3); S(3,4,3); W(3,5,3)                # D aimed west into Kb
    S(-1,5,2); S(0,5,2)                                   # cut stones
    # N net
    S(-1,3,4); W(-1,4,4); S(-2,3,4); W(-2,4,4); S(-2,3,3); W(-2,4,3)
    d.set(-3,3,4,"lever",face="wall",facing="west")
    # chain
    for x in (0,1,2):
        d.set(x,4,4,"repeater",facing="west",delay=4)
    S(3,3,4); W(3,4,4)

def build_v3():
    d = Design("closed")
    door_plane(d); sides(d); t1_left(d); control_v3(d)
    exec(open('v2.py').read(), globals())
    bottom_v1(d)
    return d
