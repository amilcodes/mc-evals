def build4():
    d = Design("open")
    S = "stone"; G = "glass"; W = "redstone_wire"
    CROSS = dict(north="side", south="side", east="side", west="side")
    # --- door layer z=0
    d.set(-3,1,0,"sticky_piston",facing="east")   # A
    d.set(-2,1,0,"sticky_piston",facing="east")   # B
    d.set(-1,1,0,S)
    d.set(-1,3,0,"sticky_piston",facing="down")   # H
    d.set(-1,2,0,S)
    for x in range(3):
        d.set(x,4,0,"sticky_piston",facing="down"); d.set(x,3,0,S)
        d.set(x,-2,0,"sticky_piston",facing="up"); d.set(x,-1,0,S)
    d.set(4,1,0,"sticky_piston",facing="west"); d.set(3,1,0,S)
    d.set(-1,0,0,S); d.set(3,0,0,S); d.set(3,2,0,S)
    # P zigzag (z=0 part), PW
    d.set(-4,-2,0,G); d.set(-4,-1,0,W)
    d.set(-4,1,0,S); d.set(-4,2,0,W)
    # net1 on top
    d.set(-1,4,0,S); d.set(-1,5,0,W)
    for x in range(3): d.set(x,5,0,W)
    d.set(-2,4,0,G); d.set(-2,5,0,W)
    # right climb z=0 part
    d.set(4,-1,0,G); d.set(4,0,0,W)
    # --- z=1
    d.set(-2,0,1,S); d.set(-2,1,1,W,**CROSS); d.set(-2,2,1,S)   # K, C_B, K2
    d.set(-2,3,1,S)                                # Q'
    d.set(-2,4,1,"observer",facing="up")          # O_b
    d.set(-2,5,1,W)
    d.set(-2,-1,1,"observer",facing="down")       # p1
    d.set(-2,-3,1,S); d.set(-2,-2,1,W)
    d.set(-2,-3,2,"lever",face="wall",facing="south")
    d.set(-3,-3,1,S); d.set(-3,-2,1,"repeater",facing="east",delay=1)   # R_pre
    d.set(-4,-3,1,S); d.set(-4,-2,1,W)
    d.set(-4,-1,1,G); d.set(-4,0,1,W)
    d.set(-3,-1,1,S); d.set(-3,0,1,"repeater",facing="west",delay=3)    # R_K
    d.set(-3,2,1,"observer",facing="west")        # O_auto
    d.set(-3,3,1,"repeater",facing="east",delay=3)  # R_A
    d.set(-4,2,1,"note_block"); d.set(-4,3,1,W)
    # Bot row
    d.set(-1,-3,1,S); d.set(-1,-2,1,"repeater",facing="west",delay=1)
    d.set(0,-2,1,S); d.set(1,-3,1,S); d.set(1,-2,1,W,**CROSS); d.set(2,-2,1,S)
    d.set(3,-3,1,S); d.set(3,-2,1,"repeater",facing="west",delay=1)
    d.set(4,-2,1,S); d.set(4,-1,1,W)
    d.set(4,0,1,G); d.set(4,1,1,W)
    d.set(5,1,1,G); d.set(5,2,1,W)
    d.set(4,2,1,G); d.set(4,3,1,W)
    # top: Ra via wall, net1 taps, Rb, net2
    d.set(3,3,1,"repeater",facing="east",delay=1)
    d.set(2,4,1,W); d.set(1,4,1,W)
    d.set(0,4,1,"repeater",facing="east",delay=2)
    d.set(-1,3,1,S); d.set(-1,4,1,W)
    d.set(-1,5,1,S)
    return d
d4 = build4(); d4.save("d4.json")
print(d4.bbox())
print(trace(d4, flips=2, limit=0))
