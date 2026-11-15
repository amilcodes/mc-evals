from pdbuild import Design
def left_half(ct_mode="a"):
    d = Design("open"); S=d.set
    # mechanism z=0
    S(-1,0,0,"stone"); S(-1,1,0,"stone"); S(0,-1,0,"stone"); S(1,-1,0,"stone")
    S(0,-2,0,"sticky_piston",facing="up"); S(1,-2,0,"sticky_piston",facing="up")
    S(-1,-1,0,"sticky_piston",facing="up")
    S(-2,1,0,"sticky_piston",facing="east"); S(-3,1,0,"sticky_piston",facing="east")
    S(-1,3,0,"stone"); S(-1,2,0,"stone"); S(0,4,0,"stone"); S(1,4,0,"stone")
    S(0,5,0,"sticky_piston",facing="down"); S(1,5,0,"sticky_piston",facing="down")
    S(-1,4,0,"sticky_piston",facing="down")
    S(-2,2,0,"sticky_piston",facing="east"); S(-3,2,0,"sticky_piston",facing="east")
    # lane z=2 on walls, E_t taps
    S(0,5,2,"repeater",facing="east",delay=1); S(1,5,2,"redstone_wire")
    S(0,5,1,"observer",facing="south"); S(1,5,1,"observer",facing="south")
    # P drive
    S(-2,1,1,"stone"); S(-2,2,1,"redstone_wire",north="side",south="side",east="side",west="side")
    S(-2,3,1,"stone"); S(-2,4,1,"observer",facing="up"); S(-2,5,1,"redstone_wire")
    S(-1,5,2,"repeater",facing="east",delay=1)   # L diode -> (-2,5,2) -> D_X
    S(-2,5,2,"stone")
    S(-1,4,2,"observer",facing="west")
    S(-1,4,1,"observer",facing="south")          # C_t driver
    # chain down x=-2,z=2
    for y in range(4,-2,-1):
        S(-2,y,2,"observer",facing=("west" if y==4 else "up"))
    S(-1,-1,2,"observer",facing="west")
    S(-3,4,2,"observer",facing="up"); S(-3,5,2,"repeater",facing="east",delay=1)
    S(-1,-1,1,"observer",facing="south")         # C_b driver
    S(-2,-1,1,"observer",facing="east"); S(-3,-2,1,"stone"); S(-3,-1,1,"redstone_wire")
    S(-3,-2,2,"stone"); S(-3,-1,2,"repeater",facing="north",delay=4); S(-3,0,2,"observer",facing="down")
    S(-3,1,2,"stone"); S(-3,2,2,"redstone_wire")
    S(-3,1,1,"stone"); S(-3,2,1,"repeater",facing="south",delay=1)   # Q window
    S(-3,3,1,"observer",facing="down"); S(-3,4,1,"stone"); S(-3,5,1,"redstone_wire")   # X path
    # E_b chain
    S(-1,-2,2,"observer",facing="up"); S(0,-2,2,"observer",facing="west"); S(1,-2,2,"observer",facing="west")
    S(0,-2,1,"observer",facing="south"); S(1,-2,1,"observer",facing="south")
    return d
def full(**kw):
    L = left_half(**kw)
    R = L.mirrored_x(3)
    d = Design("open"); d.merge(L); d.merge(R)
    d.set(1,5,3,"lever",face="floor",facing="north")
    return d
if __name__=="__main__":
    full().save("door5.json")
