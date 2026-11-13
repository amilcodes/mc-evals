def core():
    d = Design("open")
    S = "stone"
    # z=0 mechanism
    d.set(-3,1,0,"sticky_piston",facing="east")   # A
    d.set(-2,1,0,"sticky_piston",facing="east")   # B
    d.set(-1,1,0,S)  # C
    d.set(-1,2,0,S)  # L
    d.set(-1,3,0,"sticky_piston",facing="down")  # W
    d.set(-1,0,0,S)
    d.set(3,1,0,S); d.set(4,1,0,"sticky_piston",facing="west")
    # B feed: cross dust on stone
    d.set(-2,0,1,S)
    d.set(-2,1,1,"redstone_wire",north="side",south="side",east="side",west="side")
    # A feed: repeater
    d.set(-3,0,1,S)
    d.set(-3,1,1,"repeater",facing="south",delay=4)
    # O_A
    d.set(-3,0,0,"observer",facing="up")
    d.set(-3,-2,0,S); d.set(-3,-1,0,"redstone_wire")
    for z in (1,2,3):
        d.set(-3,-2,z,S); d.set(-3,-1,z,"redstone_wire")
    # R_B, J on O_L
    d.set(-2,-1,2,S); d.set(-2,0,2,"repeater",facing="south",delay=1)
    d.set(-2,-1,3,"observer",facing="east")
    d.set(-2,0,3,"redstone_wire")
    # Wn
    d.set(-3,0,2,S); d.set(-3,1,2,"redstone_wire")
    d.set(-2,1,2,S); d.set(-2,2,2,"redstone_wire"); d.set(-2,2,1,S)
    d.set(-1,3,2,"redstone_wire"); d.set(-1,3,1,"redstone_wire")
    return d
