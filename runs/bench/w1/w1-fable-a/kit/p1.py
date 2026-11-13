def planar(dtop=4, p1d=4):
    d = Design("open")
    S = lambda x,y,b="stone",**k: d.set(x,y,0,b,**k)
    for y in (0,1,2):
        S(-2,y,"sticky_piston",facing="east"); S(-1,y)
    for y in (0,1):
        S(4,y,"sticky_piston",facing="west"); S(3,y)
    S(3,2); S(4,2)
    S(1,4,"sticky_piston",facing="down"); S(1,3)
    S(2,4,"sticky_piston",facing="down"); S(2,3)
    S(0,3)
    # center, H east
    S(1,-3,"sticky_piston",facing="up"); S(1,-2,"sticky_piston",facing="up")
    S(1,-1); S(0,-1); S(2,-1)
    S(3,-1,"sticky_piston",facing="west"); S(3,-2,"target")
    S(2,-2,"observer",facing="down"); S(2,-4); S(2,-3,"repeater",facing="east",delay=p1d)
    S(3,-3,"observer",facing="east"); S(4,-3,"note_block"); S(4,-2,"redstone_wire")
    # east column (late)
    S(5,3); S(5,2,"redstone_wire"); S(5,1); S(5,0,"sticky_piston",facing="down"); S(5,-1,"redstone_block")
    S(4,3,"repeater",facing="west",delay=dtop); S(3,3); S(3,4,"redstone_wire")
    # crossing
    S(2,5,"redstone_wire"); S(1,5,"redstone_wire")
    # west top (early)
    S(0,4,"redstone_wire"); S(-1,3); S(-1,4,"redstone_wire"); S(-2,3); S(-2,4,"redstone_wire")
    S(-3,3); S(-3,4,"lever",face="floor",facing="north"); S(-3,2,"redstone_wire"); S(-3,1)
    # west bottom: first pulse
    S(-2,-1,"observer",facing="up"); S(-2,-2); S(-1,-3)
    S(-1,-2,"redstone_wire",north="side",south="side",east="side",west="side"); S(0,-2)
    return d
dp = planar(); dp.save("p1.json")
r = test(dp); print(r.text[:1500])
KP = ["(1,-3,0)","(1,-2,0)","(1,-1,0) ","(3,-1,0)","(2,-2,0)","(2,-3,0)","(3,-3,0)","(4,-2,0)","(0,-2,0)","(-2,-1,0)","(5,3,0)","(1,5,0)","(2,4,0)","(4,1,0)","(4,0,0)"]
if not r.valid: show(dp, keys=KP, width=150)
else: print(robust(dp,(-3,4,0)))
