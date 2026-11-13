def v12(top=(2,1,1), da=3, p1d=4):
    d = Design("open")
    for y in (0,1,2):
        d.set(-2,y,0,"sticky_piston",facing="east"); d.set(-1,y,0,"stone")
        d.set(4,y,0,"sticky_piston",facing="west"); d.set(3,y,0,"stone")
    d.set(1,4,0,"sticky_piston",facing="down"); d.set(1,3,0,"stone")
    d.set(0,3,0,"stone"); d.set(2,3,0,"stone")
    # center mech, H west
    d.set(1,-3,0,"sticky_piston",facing="up"); d.set(1,-2,0,"sticky_piston",facing="up")
    d.set(1,-1,0,"stone"); d.set(0,-1,0,"stone"); d.set(2,-1,0,"stone")
    d.set(-1,-1,0,"sticky_piston",facing="east"); d.set(-1,-2,0,"target")
    d.set(-2,-3,0,"stone"); d.set(-2,-2,0,"redstone_wire")
    # gated unit under B home
    d.set(0,-2,0,"observer",facing="down"); d.set(0,-3,0,"note_block")
    # east z=0: first pulse path
    d.set(4,-1,0,"observer",facing="up"); d.set(4,-2,0,"stone")
    d.set(3,-3,0,"stone"); d.set(3,-2,0,"redstone_wire",north="side",south="side",east="side",west="side")
    d.set(2,-2,0,"stone")
    # top z=0 (east): top piston power
    d.set(4,3,0,"stone"); d.set(4,4,0,"redstone_wire"); d.set(3,3,0,"stone"); d.set(3,4,0,"redstone_wire")
    d.set(2,4,0,"repeater",facing="east",delay=1)
    # top z=1
    d.set(4,3,1,"stone"); d.set(4,4,1,"lever",face="floor",facing="north")
    d.set(3,3,1,"repeater",facing="east",delay=top[0]); d.set(2,4,1,"redstone_wire")
    d.set(1,4,1,"repeater",facing="east",delay=top[1]); d.set(0,4,1,"redstone_wire")
    d.set(-1,3,1,"repeater",facing="east",delay=top[2]); d.set(-2,3,1,"stone")
    # east column
    d.set(4,2,1,"redstone_wire"); d.set(4,1,1,"stone"); d.set(4,0,1,"note_block")
    d.set(4,-1,1,"observer",facing="up"); d.set(4,-2,1,"stone")
    # west column
    d.set(-2,2,1,"redstone_wire"); d.set(-2,1,1,"stone")
    d.set(-2,0,1,"sticky_piston",facing="down"); d.set(-2,-1,1,"redstone_block"); d.set(-2,-3,1,"stone")
    # bottom row z=1
    dust(d,0,1); dust(d,1,1); rep(d,2,1,"east",p1d); rep(d,3,1,"east",da)
    return d
d12 = v12(); d12.save("v12.json")
r = test(d12); print(r.text[:1300])
K12 = ["(1,-3,0)","(1,-2,0)","(1,-1,0) ","(-1,-1,0)","(0,-1,0)","(0,-2,0)","(2,-2,1)","(3,-2,1)","(3,-2,0)","(4,-1,0)","(4,-1,1)","(1,-2,1)","(-2,-2,0)","(1,0,0)","(1,1,0)"]
if not r.valid: show(d12, keys=K12, width=150)
else: print(robust(d12,(4,4,1)))
