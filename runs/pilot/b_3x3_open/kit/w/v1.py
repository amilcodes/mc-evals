import sys; sys.path.insert(0,'.')
from pdbuild import Design
d=Design("closed")
S="stone"
def sp(x,y,z,f,ext=True):
    d.set(x,y,z,"sticky_piston",facing=f,extended=ext)
    if ext:
        dx,dy={"east":(1,0),"west":(-1,0),"up":(0,1),"down":(0,-1)}[f]
        d.set(x+dx,y+dy,z,"piston_head",facing=f,type="sticky")
def dust(x,y,z,p=None,sup=True):
    if p is None: d.set(x,y,z,"redstone_wire")
    else: d.set(x,y,z,"redstone_wire",power=p)
    if sup and d.get(x,y-1,z) is None and not wall(x,y-1,z): d.set(x,y-1,z,S)
def wall(x,y,z):
    if z==0: return False
    return (x in(-1,3) and 0<=y<=2) or (y in(-1,3) and 0<=x<=2)
def rep(x,y,z,f,delay=4):
    d.set(x,y,z,"repeater",facing=f,delay=delay)
    if d.get(x,y-1,z) is None: d.set(x,y-1,z,S)
# door stones
for x in range(3):
    for y in range(3): d.set(x,y,0,S)
# perimeter pistons
for y in range(3):
    sp(-2,y,0,"east"); sp(4,y,0,"west")
sp(1,4,0,"down")
# center
sp(1,-2,0,"up"); sp(1,-3,0,"up",False)
sp(-1,-1,0,"east")
# tower + arch
d.set(-2,-1,1,S); d.set(-3,-1,1,"lever",face="wall",facing="west")
d.set(-2,0,1,"redstone_torch"); d.set(-2,1,1,S)
for (x,y,p) in [(-2,2,15),(-1,3,14),(0,4,13),(1,4,12),(2,4,11),(3,3,10),(4,2,9)]:
    dust(x,y,1,p)
d.set(4,1,1,S)
d.set(-1,3,0,"target"); d.set(0,4,0,"target"); d.set(3,3,0,"target")
# c0 in-plane + s-observer
dust(-2,-2,1); dust(-2,-2,0); dust(-1,-2,0)
d.set(0,-2,0,"observer",facing="west")
# Q torch
d.set(-1,-2,1,S); d.set(-1,-1,1,"redstone_torch")
# c0 to chain
d.set(-2,-2,2,S); dust(-2,-1,2); d.set(-1,-1,2,S)
for (x,z) in [(-2,3),(-2,4),(-1,4),(0,4),(1,4),(1,3)]: dust(x,-2,z)
rep(-1,-2,3,"south"); dust(-1,-2,2)
# torch_P
d.set(1,-2,2,S); d.set(1,-2,1,"redstone_wall_torch",facing="north")
# c2
rep(2,-2,4,"west"); rep(3,-2,4,"west")
for (x,z) in [(4,4),(4,3),(4,2),(4,1),(4,0),(3,0)]: dust(x,-2,z)
rep(3,-2,2,"east"); dust(2,-2,2)
# A stuff
d.set(2,-3,0,"comparator",facing="east",mode="subtract"); d.set(2,-4,0,S)
rep(2,-3,1,"south")
d.set(2,-2,0,"observer",facing="down"); d.set(2,-1,0,S)
d.save("w/v1.json")
print(d.bbox())
