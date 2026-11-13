exec(open('v2.py').read().split("def build2")[0])
def build4(rw=4, r1=1, rx=4, rd=4):
    d = core()
    S="stone"; G="glass"; W="redstone_wire"; Y=-3
    d.set(-2,-1,0,S)                                   # Bk
    d.set(-1,-2,0,S); d.set(-1,-1,0,"repeater",facing="west",delay=1)   # Rf
    d.set(0,-3,0,G); d.set(0,-2,0,W)                   # updater on glass
    def comp(x,z,block,**p):
        d.set(x,Y-1,z,S); d.set(x,Y,z,block,**p)
    # west
    comp(-2,1,W)                                       # bus dust
    d.set(-2,Y,2,S); d.set(-2,-2,2,W)                  # SB + riser
    d.set(-2,-2,1,G); d.set(-2,-1,1,W)
    comp(-1,1,"repeater",facing="east",delay=rw)       # R_w reads lever
    comp(0,1,"lever",face="floor",facing="north")
    comp(-1,2,"repeater",facing="west",delay=r1)       # R1' reads SB -> X0
    comp(0,2,W)                                        # X0
    comp(1,2,"repeater",facing="west",delay=rx)        # Rx crossing
    # middle
    d.set(1,Y,1,"note_block")
    d.set(1,-2,1,"observer",facing="down")
    # east
    comp(2,1,"comparator",facing="east",mode="subtract")
    comp(2,2,W); comp(3,2,W)
    comp(3,1,"repeater",facing="east",delay=rd)
    comp(4,1,W)
    d.set(4,Y,2,S); d.set(4,-2,2,W)
    top_and_right(d)
    return d
d4 = build4(); d4.save("v4.json")
r = test(d4); print(r)
