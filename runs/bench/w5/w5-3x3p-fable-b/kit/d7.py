def build7(d4=4):
    d = Design("closed")
    S=lambda x,y,b="stone",**p: d.set(x,y,0,b,**p)
    W=lambda x,y,**p: d.set(x,y,0,"redstone_wire",**p)
    O=lambda x,y,f: d.set(x,y,0,"observer",facing=f)
    # door stones (closed)
    for x in (0,1,2):
        for y in (0,1,2): S(x,y)
    for y in (0,1,2):
        S(-2,y,"sticky_piston",facing="east"); S(4,y,"sticky_piston",facing="west")
    S(1,-2,"sticky_piston",facing="up"); S(0,-1); S(2,-1)
    # top module (mirrored): feeder on the right
    S(1,5,"sticky_piston",facing="down"); S(1,4,"sticky_piston",facing="down")
    S(0,3); S(3,3,"sticky_piston",facing="west")
    # T net on the left
    W(0,4); S(-1,3,"glass"); W(-1,4); S(-1,5); O(0,5,"east")
    # G strong block + its two observers
    S(2,4); O(2,5,"up"); O(3,4,"east")
    # gate: X stone at (2,6), piston (3,6), lever (4,6) on K (5,6)
    S(2,6); S(3,6,"sticky_piston",facing="west")
    S(5,6); S(4,6,"lever",face="wall",facing="west")
    # right column chain
    W(5,5); O(5,4,"up"); O(5,3,"up"); S(5,2)
    O(4,3,"east"); O(4,4,"down")
    O(5,1,"west"); O(5,0,"up"); O(5,-1,"up"); O(5,-2,"up")
    O(4,-2,"east"); O(4,-1,"down"); O(3,-2,"east"); O(2,-2,"east")
    # left bottom chain
    O(0,-2,"east"); O(-1,-2,"east"); O(-2,-2,"east"); O(-3,-2,"east")
    O(-3,-1,"down"); O(-3,0,"down"); S(-3,1)
    W(-3,2,north="side",south="side",east="side",west="side")
    # left column up to Rep4
    O(-2,3,"down"); O(-2,4,"down"); O(-2,5,"down"); O(-2,6,"down")
    O(-1,6,"west"); S(0,6,"repeater",facing="west",delay=d4)
    return d
d=build7(); d.save("d7.json")
r=test(d); print(r)
