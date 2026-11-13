exec(open('core.py').read().split("d = core()")[0])
def build(rla=4, r1=4, rd1=4, rd2=4):
    d = core()
    S="stone"; G="glass"; W="redstone_wire"
    # S2 feed
    d.set(-2,-1,0,S)                                   # Bk
    d.set(-1,-2,0,S); d.set(-1,-1,0,"repeater",facing="west",delay=1)   # Rf
    d.set(0,-3,0,"observer",facing="east")            # Obs_S' watches P1
    d.set(0,-2,0,W)                                    # updater
    d.set(-1,-4,0,S); d.set(-1,-3,0,W)
    d.set(-2,-4,0,S); d.set(-2,-3,0,W)
    # left riser
    d.set(-2,-4,1,S); d.set(-2,-3,1,W)
    d.set(-2,-3,2,G); d.set(-2,-2,2,W)
    d.set(-2,-2,1,G); d.set(-2,-1,1,W)
    # right riser
    d.set(4,-4,3,S); d.set(4,-3,3,W)
    d.set(4,-3,2,G); d.set(4,-2,2,W)
    d.set(4,-2,1,G); d.set(4,-1,1,W)
    d.set(4,-1,2,G); d.set(4,0,2,W)
    d.set(4,0,1,G); d.set(4,1,1,W)
    d.set(4,1,2,G); d.set(4,2,2,W)
    d.set(4,2,1,G); d.set(4,3,1,W)
    d.set(4,-1,0,S); d.set(4,3,0,"target")
    # top wiring
    d.set(3,3,1,W); d.set(2,4,1,W); d.set(1,4,1,"repeater",facing="east",delay=1); d.set(0,4,1,W); d.set(-1,3,1,W)
    d.set(2,4,0,"target")
    d.set(-2,2,1,S); d.set(-2,3,1,W); d.set(-2,3,0,"target")
    # board y=-4, supports y=-5
    def comp(x,z,block,**p):
        d.set(x,-5,z,S); d.set(x,-4,z,block,**p)
    d.set(1,-4,0,S)                                    # FS
    comp(2,0,"comparator",facing="east",mode="subtract")
    comp(3,0,"repeater",facing="east",delay=rd2)
    comp(4,0,W)
    comp(-1,1,"repeater",facing="east",delay=4)        # R_w
    comp(0,1,"lever",face="floor",facing="north")
    comp(1,1,"repeater",facing="west",delay=4)         # R_e
    comp(2,1,W); comp(3,1,W)
    comp(4,1,"repeater",facing="south",delay=rd1)
    comp(-2,2,W)
    comp(-1,2,"observer",facing="east")                # Obs_L
    comp(0,2,W)
    comp(2,2,"repeater",facing="south",delay=rla)
    comp(3,2,W); comp(4,2,W)
    comp(0,3,W)
    comp(1,3,"repeater",facing="west",delay=r1)
    comp(2,3,W)
    return d
d = build()
d.save("v1.json")
r = test(d); print(r)
