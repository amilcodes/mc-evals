d=Design("open")
S=lambda x,y,z,b="stone",**p: d.set(x,y,z,b,**p)
W="redstone_wire"
for p in [(0,-1),(2,-1),(2,3),(0,3),(1,3),(1,-1)]: S(p[0],p[1],0)
for y in range(3): S(-1,y,0); S(3,y,0); S(-2,y,0,"sticky_piston",facing="east"); S(4,y,0,"sticky_piston",facing="west")
S(1,4,0,"sticky_piston",facing="down"); S(1,5,0,"sticky_piston",facing="down")
S(-1,3,0,"sticky_piston",facing="east"); S(1,-2,0,"sticky_piston",facing="up")
S(2,5,0,"observer",facing="west"); S(3,4,0); S(3,5,0,W); S(2,4,0,W)
# R chain
S(0,4,0); S(0,5,0,"repeater",facing="west",delay=1); S(-1,4,0); S(-1,5,0,"repeater",facing="west",delay=4)
S(-2,5,0,"observer",facing="west"); S(-3,4,0); S(-3,5,0,W); S(-4,3,0); S(-4,4,0,W)
# AND_S
S(1,4,1,"comparator",facing="south",mode="subtract")
for z,dl in zip(range(2,6),[2,4,4,4]): S(1,4,z,"repeater",facing="south",delay=dl)
S(2,4,1,"repeater",facing="east",delay=1); S(4,4,1); S(3,4,1,"redstone_wall_torch",facing="west"); S(4,5,1,W)
for z in range(2,6): S(4,3,z); S(4,4,z,W)
# AND_K
S(-1,3,1,"comparator",facing="south",mode="subtract")
for z in (2,3,4): S(-1,3,z,"repeater",facing="south",delay=4)
S(-1,3,5,W)
S(-2,2,1); S(-2,3,1,"repeater",facing="west",delay=2); S(-4,3,1); S(-3,3,1,"redstone_wall_torch",facing="east")
for z in range(1,6): S(-4,3,z); S(-4,4,z,W)
# trunk z=6
for x in range(-5,6):
    if x not in (0,1,2): S(x,3,6)
    S(x,4,6,W)
S(-2,2,6,"lever",face="ceiling",facing="north")
# left feed
for (y,z) in [(3,5),(2,4),(1,3),(0,2),(0,1)]: S(-5,y-1,z); S(-5,y,z,W)
S(-4,-1,1); S(-4,0,1,W)
S(-4,-1,0); S(-4,0,0,W); S(-4,1,0,"glass"); S(-4,2,0,W); S(-5,0,0); S(-5,1,0,W)
S(-3,-1,0); S(-3,0,0,"repeater",facing="west",delay=1); S(-3,1,0); S(-3,2,0,"repeater",facing="west",delay=1)
# right feed
for (y,z) in [(3,5),(2,4),(1,3),(0,2)]: S(5,y-1,z); S(5,y,z,W)
for z in (1,2,3,4): S(4,1,z); S(4,2,z,W)
for z in (1,2): S(4,-1,z); S(4,0,z,W)
# B feed
S(-3,-2,1); S(-3,-1,1,W); S(-2,-3,1); S(-2,-2,1,W); S(-1,-3,1); S(-1,-2,1,W); S(-1,-3,0); S(-1,-2,0,W)
S(0,-3,0); S(0,-2,0,"repeater",facing="west",delay=1)
d.save("door4.json")
