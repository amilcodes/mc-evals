exec(open("door12.py").read())
for p in list(d.blocks):
    if p[0]==-4: d.remove(*p)
for p in [(-3,2,0),(-3,1,0),(-3,4,0),(-3,5,0),(-2,5,0),(-1,5,0),(-3,3,1)]: d.remove(*p)
# left top piston via (-2,2,1)
S(-2,1,3); S(-2,2,3,W); S(-2,1,2); S(-2,2,2,W)
# K torch
S(-3,3,2); S(-3,3,1,"redstone_wall_torch",facing="north"); S(-3,4,2,W)
for z in (2,3,4): S(-2,3,z); S(-2,4,z,W)
# R observer
S(-2,4,1); S(-2,5,1,W); S(-2,4,0); S(-2,5,0,W); S(-1,5,0,"observer",facing="west")
S(0,5,0,"repeater",facing="west",delay=R2)
d.save("door13.json")
