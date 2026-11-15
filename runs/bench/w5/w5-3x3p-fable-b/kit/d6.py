def build6(dr=(1,1,1), d4=4):
    d = Design("open")
    S=lambda x,y,z,b="stone",**p: d.set(x,y,z,b,**p)
    W=lambda x,y,z,**p: d.set(x,y,z,"redstone_wire",**p)
    G=lambda x,y,z: d.set(x,y,z,"glass")
    O=lambda x,y,z,f: d.set(x,y,z,"observer",facing=f)
    for y in (0,1,2):
        S(-2,y,0,"sticky_piston",facing="east"); S(-1,y,0)
        S(4,y,0,"sticky_piston",facing="west"); S(3,y,0)
    S(1,-2,0,"sticky_piston",facing="up"); S(1,-1,0); S(0,-1,0); S(2,-1,0)
    # top module
    S(1,5,0,"sticky_piston",facing="down"); S(1,4,0,"sticky_piston",facing="down")
    S(1,3,0); S(0,3,0); S(2,3,0)
    S(-1,3,0,"sticky_piston",facing="east")
    # T net
    W(2,4,0); G(3,3,0); W(3,4,0); S(3,5,0); O(2,5,0,"west")
    S(2,4,1); O(3,4,1,"east")
    # lever + S chain (right to left) on level 5, z=1
    S(4,5,1); S(4,4,1,"lever",face="ceiling",facing="north")
    S(3,5,1,"repeater",facing="east",delay=dr[0])
    S(2,5,1,"repeater",facing="east",delay=dr[1])
    S(1,4,1); S(1,5,1,"repeater",facing="east",delay=dr[2])
    O(0,4,1,"west"); W(0,5,1)
    O(-1,4,1,"up"); W(-1,5,1)
    S(-1,3,1)
    # C stage
    S(0,4,0); S(0,5,0,"comparator",facing="west",mode="subtract")
    G(-1,4,0); S(-1,5,0,"repeater",facing="west",delay=d4)
    O(-2,4,0,"down"); W(-2,5,0)
    O(-2,3,0,"east")
    # right stack: level for y=2,1
    S(4,2,1); W(4,3,1)
    # pulse chain down right column
    O(4,1,1,"north"); O(4,0,1,"up"); O(4,-1,1,"up"); O(4,-2,1,"up")
    O(4,-2,0,"south"); O(4,-1,0,"down")
    O(3,-2,1,"east"); O(2,-2,1,"east"); S(1,-2,1)
    # left: chain from bottom piston
    O(0,-2,0,"east"); O(-1,-2,0,"east"); O(-2,-2,0,"east")
    O(-2,-2,1,"north"); O(-2,-1,1,"down"); O(-2,0,1,"down")
    S(-2,1,1); W(-2,2,1,north="side",south="side",east="side",west="side")
    return d
d=build6(); d.save("d6.json")
r=test(d); print(r)
