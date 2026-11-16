d = Design("open")
def dust(x,y,z,sup=True):
    d.set(x,y,z,"redstone_wire")
    if sup and (x,y-1,z) not in d.blocks: d.set(x,y-1,z,"stone")
def rep(x,y,z,f,delay=1,sup=True):
    d.set(x,y,z,"repeater",facing=f,delay=delay)
    if sup and (x,y-1,z) not in d.blocks: d.set(x,y-1,z,"stone")
# mechanics
for y in range(3):
    d.set(-2,y,0,"sticky_piston",facing="east"); d.set(-1,y,0,"stone")
    d.set(4,y,0,"sticky_piston",facing="west"); d.set(3,y,0,"stone")
d.set(1,4,0,"sticky_piston",facing="down"); d.set(1,3,0,"stone")
d.set(0,3,0,"stone"); d.set(2,3,0,"stone")
d.set(0,-1,0,"stone"); d.set(1,-1,0,"stone"); d.set(2,-1,0,"stone")
d.set(1,-2,0,"sticky_piston",facing="up"); d.set(1,-3,0,"sticky_piston",facing="up")
d.set(-1,-1,0,"sticky_piston",facing="east")
# P2 direct feed + D line
rep(1,-2,1,"south"); dust(1,-2,2); dust(0,-3,2); dust(0,-3,3); d.set(0,-2,3,"stone")
for z in range(3,8): dust(1,-3,z)
d.set(2,-3,7,"observer",facing="east"); d.set(2,-4,7,"stone")
d.set(0,-3,0,"observer",facing="east"); d.set(0,-4,0,"stone")
# S feed observer
d.set(2,-2,0,"observer",facing="down")
# P1 feed
rep(2,-3,0,"east"); dust(3,-3,0); dust(3,-3,1); dust(3,-3,2)
for z in (3,4,5): rep(3,-3,z,"south",4)
d.set(3,-3,6,"observer",facing="south"); d.set(3,-4,6,"stone")
# D observer from Q


# J observer -> D
d.set(-1,-2,0,"observer",facing="up"); d.set(-1,-3,0,"stone"); rep(-1,-3,1,"north"); dust(-1,-3,2)
# L row (y=-2, z=9), lever on support block
for x in range(-4,7): dust(x,-2,9)
d.set(2,-3,10,"lever",face="wall",facing="south")
dust(3,-3,8); dust(3,-3,7); dust(-3,-3,8)
# CJ chain folded
rep(-1,-3,6,"south",4); rep(-1,-3,7,"south",4); d.set(-1,-3,8,"stone")
for x in (0,1,2): rep(x,-3,8,"east",4)
d.set(-1,-3,5,"comparator",facing="south",mode="subtract"); d.set(-1,-4,5,"stone")
d.set(-3,-3,6,"stone"); d.set(-2,-3,6,"redstone_wall_torch",facing="east"); dust(-2,-3,5)
rep(-3,-3,7,"south",2)
dust(-1,-3,4); dust(-1,-2,3); dust(-1,-1,2); rep(-1,-1,1,"south",4)

# side/top bus
def side(m):
    pts=[(-2,1,2),(-2,1,1),(-3,1,2),(-4,2,1),(-4,3,0),(-3,4,0),(-2,4,0)]
    for (x,y,z) in pts:
        X = x if m==0 else 2-x
        dust(X,y,z)
    for z in range(2,7):
        X = -4 if m==0 else 6
        if z==4: rep(X,1,z,"south")
        else: dust(X,1,z)
    X = -4 if m==0 else 6
    dust(X,0,7); dust(X,-1,8)
side(0); side(1)
dust(-1,4,0); dust(0,4,0); dust(2,4,0); dust(3,4,0)
d.save("door8.json")
print(len(d.blocks))
