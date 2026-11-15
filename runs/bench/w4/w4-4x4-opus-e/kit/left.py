def left_mech():
    d = Design("open")
    for y,yy in ((0,1),):
        pass
    # bottom quadrant
    d.set(-1,0,0,"stone"); d.set(-1,1,0,"stone")
    d.set(0,-1,0,"stone"); d.set(1,-1,0,"stone")
    d.set(0,-2,0,"sticky_piston",facing="up"); d.set(1,-2,0,"sticky_piston",facing="up")
    d.set(-1,-1,0,"sticky_piston",facing="up")
    d.set(-2,1,0,"sticky_piston",facing="east"); d.set(-3,1,0,"sticky_piston",facing="east")
    # top quadrant
    d.set(-1,3,0,"stone"); d.set(-1,2,0,"stone")
    d.set(0,4,0,"stone"); d.set(1,4,0,"stone")
    d.set(0,5,0,"sticky_piston",facing="down"); d.set(1,5,0,"sticky_piston",facing="down")
    d.set(-1,4,0,"sticky_piston",facing="down")
    d.set(-2,2,0,"sticky_piston",facing="east"); d.set(-3,2,0,"sticky_piston",facing="east")
    # P drive
    d.set(-2,1,1,"stone"); d.set(-2,2,1,"redstone_wire",north="side",south="side",east="side",west="side")
    d.set(-2,3,1,"stone"); d.set(-2,4,1,"observer",facing="up")   # watches D_X (-2,5,1)
    # Q drive: observer under W_Q dust
    d.set(-3,2,1,"observer",facing="south")  # watches (-3,2,2), emits north into Q_t
    # C drivers
    d.set(-1,4,1,"observer",facing="south")  # watches (-1,4,2), emits north into C_t
    d.set(-1,-1,1,"observer",facing="south") # watches (-1,-1,2), emits north into C_b
    return d
