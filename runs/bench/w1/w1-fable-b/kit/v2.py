exec(open('core.py').read().split("d = core()")[0])
def top_and_right(d, riser_from_block=True):
    S="stone"; G="glass"; W="redstone_wire"
    d.set(4,-2,1,G); d.set(4,-1,1,W)
    d.set(4,-1,2,G); d.set(4,0,2,W)
    d.set(4,0,1,G); d.set(4,1,1,W)
    d.set(4,1,2,G); d.set(4,2,2,W)
    d.set(4,2,1,G); d.set(4,3,1,W)
    d.set(4,-1,0,S); d.set(4,3,0,"target")
    d.set(3,3,1,W); d.set(2,4,1,W); d.set(1,4,1,"repeater",facing="east",delay=1); d.set(0,4,1,W); d.set(-1,3,1,W)
    d.set(2,4,0,"target")
    d.set(-2,2,1,S); d.set(-2,3,1,W); d.set(-2,3,0,"target")
def build2(rla=4, r1=4, rd1=4, rd2=1):
    d = core()
    S="stone"; G="glass"; W="redstone_wire"; Y=-3
    d.set(-2,-1,0,S)                                   # Bk
    d.set(-1,-2,0,S); d.set(-1,-1,0,"repeater",facing="west",delay=1)   # Rf
    d.set(0,-3,0,"observer",facing="east")            # Obs_S' watches P1
    d.set(0,-2,0,W)                                    # updater
    def comp(x,z,block,**p):
        d.set(x,Y-1,z,S); d.set(x,Y,z,block,**p)
    comp(-1,0,W); comp(-2,0,W); comp(-2,1,W)           # bus dusts
    d.set(-2,Y,2,S); d.set(-2,-2,2,W)                  # SB + riser
    d.set(-2,-2,1,G); d.set(-2,-1,1,W)
    # right riser: block B4 at (4,Y,2), dust on top
    d.set(4,Y,2,S); d.set(4,-2,2,W)
    top_and_right(d)
    comp(2,0,"comparator",facing="east",mode="subtract")
    comp(3,0,"repeater",facing="east",delay=rd2)
    comp(4,0,W)
    comp(-1,1,"repeater",facing="east",delay=4)        # R_w
    comp(0,1,"lever",face="floor",facing="north")
    comp(1,1,"repeater",facing="west",delay=4)         # R_e
    comp(2,1,W); comp(3,1,W)
    comp(4,1,"repeater",facing="south",delay=rd1)
    comp(-1,2,"observer",facing="east")                # Obs_L
    comp(0,2,W)
    comp(2,2,"repeater",facing="south",delay=rla)
    comp(3,2,W)
    comp(0,3,W)
    comp(1,3,"repeater",facing="west",delay=r1)
    comp(2,3,W)
    return d
d2 = build2()
d2.save("v2.json")
r = test(d2); print(r)
