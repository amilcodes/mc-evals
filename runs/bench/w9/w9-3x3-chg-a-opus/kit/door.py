d=Design("open")
S=lambda x,y,z,b="stone",**p: d.set(x,y,z,b,**p)
W="redstone_wire"
for p in [(0,-1),(2,-1),(2,3),(0,3),(1,3),(1,-1)]: S(p[0],p[1],0)
for y in range(3): S(-1,y,0); S(3,y,0); S(-2,y,0,"sticky_piston",facing="east"); S(4,y,0,"sticky_piston",facing="west")
S(1,4,0,"sticky_piston",facing="down"); S(1,5,0,"sticky_piston",facing="down")
S(-1,3,0,"sticky_piston",facing="east"); S(1,-2,0,"sticky_piston",facing="up")
# S3/S4 pulse
S(2,5,0,"observer",facing="west"); S(3,4,0); S(3,5,0,W); S(2,4,0,W)
# R chain
S(1,6,0); S(1,5,1); S(1,6,1,"repeater",facing="south",delay=1); S(1,5,2); S(1,6,2,"repeater",facing="south",delay=4)
S(1,6,3,"observer",facing="south"); S(1,5,4); S(1,6,4,W)
# AND_S
S(1,4,1,"repeater",facing="south",delay=1); S(1,4,2,"comparator",facing="south",mode="subtract")
for z,dl in zip(range(3,8),[1,3,4,4,4]): S(1,4,z,"repeater",facing="south",delay=dl)
S(2,4,2,"repeater",facing="east",delay=1); S(4,4,2); S(3,4,2,"redstone_wall_torch",facing="west")
S(4,5,2,W)
for z in range(3,8): S(4,3,z); S(4,4,z,W)
S(3,4,4); S(3,5,4,W); S(2,5,4); S(2,6,4,W)
# AND_K
S(-1,3,1,"comparator",facing="south",mode="subtract")
for z in (2,3,4): S(-1,3,z,"repeater",facing="south",delay=4)
for z in (5,6,7): S(-1,3,z,W)
S(-2,2,1); S(-2,3,1,"repeater",facing="west",delay=3); S(-4,3,1); S(-3,3,1,"redstone_wall_torch",facing="east")
for z in range(1,8): S(-4,3,z); S(-4,4,z,W)
# trunk
for x in range(-5,8):
    if x not in (0,1,2): S(x,3,8)
    S(x,4,8,W)
S(1,4,9,"lever",face="floor",facing="north")
# left feed
for i,(y,z) in enumerate([(3,7),(2,6),(1,5),(0,4)]): S(-5,y-1,z); S(-5,y,z,W); S(7,y-1,z); S(7,y,z,W)
for X in (-5,7):
    S(X,-1,3); S(X,0,3,"repeater",facing="south",delay=1)
    for z in (2,1): S(X,-1,z); S(X,0,z,W)
S(-4,-1,1); S(-4,0,1,W); S(6,-1,1); S(6,0,1,W)
for X,Xr,Xs,f in [(-4,-3,-5,"west"),(6,5,7,"east")]:
    S(X,-1,0); S(X,0,0,W); S(X,1,0,"glass"); S(X,2,0,W); S(Xs,0,0); S(Xs,1,0,W)
    S(Xr,-1,0); S(Xr,0,0,"repeater",facing=f,delay=1); S(Xr,1,0); S(Xr,2,0,"repeater",facing=f,delay=1)
# B feed
S(-3,-2,1); S(-3,-1,1,W); S(-2,-3,1); S(-2,-2,1,W); S(-1,-3,1); S(-1,-2,1,W); S(-1,-3,0); S(-1,-2,0,W)
S(0,-3,0); S(0,-2,0,"repeater",facing="west",delay=1)
d.save("door.json")
