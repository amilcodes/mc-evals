def build8(d4=4):
    d = Design("closed")
    S=lambda x,y,b="stone",**p: d.set(x,y,0,b,**p)
    W=lambda x,y,**p: d.set(x,y,0,"redstone_wire",**p)
    O=lambda x,y,f: d.set(x,y,0,"observer",facing=f)
    X4=dict(north="side",south="side",east="side",west="side")
    for x in (0,1,2):
        for y in (0,1,2): S(x,y)
    for y in (0,1,2):
        S(-2,y,"sticky_piston",facing="east"); S(4,y,"sticky_piston",facing="west")
    S(1,-2,"sticky_piston",facing="up"); S(0,-1); S(2,-1)
    # top module, feeder on the right
    S(1,5,"sticky_piston",facing="down"); S(1,4,"sticky_piston",facing="down")
    S(0,3); S(3,3,"sticky_piston",facing="west")
    # T net (left) with gated S5
    W(0,4); S(-1,3,"glass"); W(-1,4); O(0,5,"east")
    S(-2,5)                                   # S5 at rest (gate off)
    S(-3,5,"sticky_piston",facing="east")     # gate piston
    S(-2,6); S(-3,6,"lever",face="wall",facing="west")   # K + lever
    O(-3,4,"up"); O(-2,4,"west")              # watch gate piston; T#1 into n1
    # left stack
    O(-3,3,"up"); W(-3,2,**X4); O(-3,1,"up")
    O(-3,0,"up"); O(-3,-1,"up"); O(-3,-2,"up")
    O(-2,-2,"west"); O(-2,-1,"down"); O(-1,-2,"west"); O(0,-2,"west")
    O(2,-2,"west"); O(3,-2,"west"); O(4,-2,"west"); O(5,-2,"west")
    O(5,-1,"down"); O(5,0,"down"); S(5,1); W(5,2,**X4)
    O(5,3,"down"); O(5,4,"down"); O(5,5,"down"); O(5,6,"down")
    # feeder + final
    O(4,3,"east"); O(4,4,"down"); O(3,4,"east"); S(2,4)
    # P1 driver
    O(4,6,"east"); O(3,6,"east"); S(2,5,"glass"); S(2,6,"repeater",facing="east",delay=d4); S(1,6)
    return d
d=build8(); d.save("d8.json")
r=test(d); print(r)
