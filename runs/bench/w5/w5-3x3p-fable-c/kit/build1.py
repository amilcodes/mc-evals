def build():
    d = Design("open")
    S = "stone"; G = "glass"; W = "redstone_wire"
    CROSS = dict(north="side", south="side", east="side", west="side")
    # --- door layer z=0
    d.set(-3,1,0,"sticky_piston",facing="east")   # A
    d.set(-2,1,0,"sticky_piston",facing="east")   # B
    d.set(-1,1,0,S)                                # S
    d.set(-1,3,0,"sticky_piston",facing="down")   # H
    d.set(-1,2,0,S)                                # X
    for x in range(3):
        d.set(x,4,0,"sticky_piston",facing="down"); d.set(x,3,0,S)
        d.set(x,-2,0,"sticky_piston",facing="up"); d.set(x,-1,0,S)
    d.set(4,1,0,"sticky_piston",facing="west"); d.set(3,1,0,S)
    d.set(-1,0,0,S); d.set(3,0,0,S); d.set(3,2,0,S)
    # --- B control (south)
    d.set(-2,0,1,S)                # K
    d.set(-2,1,1,W,**CROSS)        # C_B
    d.set(-2,2,1,S)                # K2
    d.set(-2,-1,1,"observer",facing="down")   # p1
    # lever + raw bus
    d.set(-3,-2,1,S); d.set(-3,-1,1,"lever",face="floor",facing="north")
    d.set(-2,-3,1,S); d.set(-2,-2,1,W)
    # R_pre -> P
    d.set(-2,-3,0,S); d.set(-2,-2,0,"repeater",facing="south",delay=1)
    d.set(-2,-3,-1,S); d.set(-2,-2,-1,W)
    d.set(-3,-2,-1,S); d.set(-3,-1,-1,W)
    d.set(-2,-1,-1,G); d.set(-2,0,-1,W)
    d.set(-3,0,-1,G); d.set(-3,1,-1,W)
    # R_K
    d.set(-2,-1,0,G); d.set(-2,0,0,"repeater",facing="north",delay=3)
    # O_b, Q, R_A
    d.set(-3,2,-1,"observer",facing="down")
    d.set(-3,3,-1,S)
    d.set(-3,2,0,G); d.set(-3,3,0,"repeater",facing="north",delay=4)
    # A-sig
    d.set(-3,2,1,"observer",facing="west")   # O_auto -> K2
    d.set(-3,3,1,W)
    d.set(-4,1,1,S); d.set(-4,2,1,W)
    d.set(-4,1,0,S); d.set(-4,2,0,W)         # PW
    # Bot row
    d.set(-1,-3,1,S); d.set(-1,-2,1,"repeater",facing="west",delay=1)
    d.set(0,-2,1,S); d.set(1,-3,1,S); d.set(1,-2,1,W,**CROSS); d.set(2,-2,1,S)
    d.set(3,-3,1,S); d.set(3,-2,1,"repeater",facing="west",delay=1)
    d.set(4,-2,1,S); d.set(4,-1,1,W)
    d.set(4,-1,0,G); d.set(4,0,0,W)
    d.set(4,0,1,G); d.set(4,1,1,W)
    d.set(4,2,0,W)
    d.set(4,2,1,G); d.set(4,3,1,W)
    d.set(4,3,0,G); d.set(4,4,0,W)
    d.set(3,3,0,S); d.set(3,4,0,W)
    for x in range(3): d.set(x,5,0,W)
    # H logic
    d.set(1,4,1,W); d.set(1,4,-1,W)
    d.set(0,4,-1,"repeater",facing="east",delay=1); d.set(-1,3,-1,S); d.set(-1,4,-1,W)
    d.set(0,4,1,"repeater",facing="east",delay=3); d.set(-1,3,1,S); d.set(-1,4,1,W)
    return d
d1 = build()
d1.save("d1.json")
print(d1.bbox())
print(trace(d1, flips=2, limit=0))
