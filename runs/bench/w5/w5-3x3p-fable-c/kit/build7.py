exec(open("build6.py").read().split("d6 = build6()")[0])
def build7():
    d = build6()
    d.set(3,3,0,"stone")
    S = "stone"; G = "glass"; W = "redstone_wire"
    CROSS = dict(north="side", south="side", east="side", west="side")
    # remove everything at x=-4 and old left logic
    for p in list(d.blocks):
        if p[0] == -4: d.remove(*p)
    for p in [(-3,-3,1),(-3,-2,1),(-3,-1,1),(-3,0,1),(-3,2,1),(-3,3,1),(-2,3,1),
              (-2,-1,1),(-2,-2,1),(-2,-3,1),(-2,-3,2),(-1,-2,1),(-1,-3,1)]:
        d.remove(*p)
    # steady chain: LS''(0,-2,1) lever stone -> R_L -> L0 -> T_inv -> Y -> T_K -> K
    d.set(0,-2,2,"lever",face="wall",facing="south")
    d.set(-1,-3,1,S); d.set(-1,-2,1,"repeater",facing="east",delay=4)
    d.set(-2,-2,1,S)                                              # L0
    d.set(-3,-2,1,"redstone_wall_torch",facing="west",lit=True)  # T_inv
    d.set(-3,-1,1,S)                                              # Y
    d.set(-2,-1,1,"redstone_wall_torch",facing="east",lit=False) # T_K
    # P1: O1 watches Bot0, note, O2 -> stone under B
    d.set(-1,-2,0,"observer",facing="east")
    d.set(-2,-2,0,"note_block")
    d.set(-2,-1,0,"observer",facing="down")
    d.set(-2,0,0,S)
    # A-sig: O_b watches T0, R_A, strong stone, dust under it on stone above A
    d.set(-1,4,0,"observer",facing="east")
    d.set(-2,3,0,G); d.set(-2,4,0,"repeater",facing="east",delay=3)
    d.set(-3,4,0,S); d.set(-3,3,0,W); d.set(-3,2,0,S)
    # W note on O_top, A-sig cross
    d.set(-2,3,1,"observer",facing="up")
    d.set(-2,4,1,"note_block")
    d.set(-3,3,1,G); d.set(-3,4,1,W,**CROSS)
    return d
d7 = build7(); d7.save("d7.json")
print(d7.bbox())
print(trace(d7, flips=2, limit=0))
r = test(d7); print(r)
