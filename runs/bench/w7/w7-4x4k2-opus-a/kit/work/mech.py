from pdbuild import Design
def mech_left(d):
    # lines rows 1,2
    for y in (1,2):
        d.set(-2,y,0,"sticky_piston",facing="east")
        d.set(-3,y,0,"sticky_piston",facing="east")
    # C pistons (pulse toggled, rest retracted). closed: s empty
    d.set(-1,-1,0,"sticky_piston",facing="up")
    d.set(-1,4,0,"sticky_piston",facing="down")
    # A low delivery: O_AL watches (-2,4,0) obs S watches (-2,4,1) obs W watches IA1=(-3,4,1)
    d.set(-2,3,0,"observer",facing="up")
    d.set(-2,4,0,"observer",facing="south")
    d.set(-2,4,1,"observer",facing="west")
    # A high: rep (-2,2,1) W on block (-2,1,1); rep (-3,2,1) W on block (-3,1,1); input IA2=(-4,2,1)
    d.set(-2,1,1,"stone"); d.set(-2,2,1,"repeater",facing="west",delay=1)
    d.set(-3,1,1,"stone"); d.set(-3,2,1,"repeater",facing="west",delay=1)
    # B: O_B (-3,3,0) up watches (-3,4,0) obs W watches IB=(-4,4,0)
    d.set(-3,3,0,"observer",facing="up")
    d.set(-3,4,0,"observer",facing="west")
    # top C/singles PX: obs (-2,5,0) facing W watches (-3,5,0), back into dust (-1,5,0)
    d.set(-2,5,0,"observer",facing="west")
    d.set(-1,5,0,"redstone_wire")
    # bottom: hub (-1,-2,0) <- obs (-2,-2,0) W watches (-3,-2,0); block (1,-2,1) <- obs (0,-2,1) W watches (-1,-2,1)
    d.set(-1,-2,0,"stone"); d.set(-2,-2,0,"observer",facing="west")
    d.set(1,-2,1,"stone"); d.set(0,-2,1,"observer",facing="west")
def mech(initial="closed"):
    d=Design(initial)
    L=Design(); mech_left(L)
    R=L.mirrored_x(3)
    d.merge(L); d.merge(R)
    # doorway
    if initial=="closed":
        d.fill(0,0,0,3,3,0,"stone")
    # top singles (retracted rest), PX dust on top
    for x in range(4):
        d.set(x,5,0,"sticky_piston",facing="down"); d.set(x,6,0,"redstone_wire")
        d.set(x,-2,0,"sticky_piston",facing="up")
    return d
