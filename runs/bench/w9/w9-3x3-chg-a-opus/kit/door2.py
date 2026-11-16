exec(open("door.py").read())
R_=d.remove
for p in [(1,6,0),(1,5,1),(1,6,1),(1,5,2),(1,6,2),(1,6,3),(1,5,4),(1,6,4),(2,5,4),(2,6,4),(3,4,4),(3,5,4)]: R_(*p)
S(0,4,0); S(0,5,0,"repeater",facing="west",delay=1); S(-1,4,0); S(-1,5,0,"repeater",facing="west",delay=4)
S(-2,5,0,"observer",facing="west"); S(-3,4,0); S(-3,5,0,W); S(-4,3,0); S(-4,4,0,W)
# right side rework
for p in list(d.blocks):
    if p[0]>=6: R_(*p)
for p in [(5,-1,0),(5,0,0),(5,1,0),(5,2,0)]: R_(*p)
for (y,z) in [(3,7),(2,6),(1,5),(0,4)]: S(5,y-1,z); S(5,y,z,W)
S(4,-1,4); S(4,0,4,W); S(4,-1,3); S(4,0,3,"repeater",facing="south",delay=1)
for z in (2,1): S(4,-1,z); S(4,0,z,W)
S(5,0,2); S(5,1,2,W); S(5,1,3); S(5,2,3,W)
S(4,1,3,"glass"); S(4,1,2,"glass"); S(4,1,1)
for z in (1,2,3): S(4,2,z,W)
d.save("door2.json")
