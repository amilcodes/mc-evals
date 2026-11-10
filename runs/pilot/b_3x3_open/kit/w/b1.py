import sys; sys.path.insert(0,'w')
from lib import *
b=B("closed"); b.door()
for y in range(3):
    b.sp(-2,y,0,"east",True); b.sp(4,y,0,"west",True)
b.sp(1,4,0,"down",True)
b.sp(1,-3,0,"up",True); b.sp(1,-1,0,"up"); b.sp(-1,-1,0,"east")
# tower + arch
b.set(-2,-1,1,S); b.set(-3,-1,1,"lever",face="wall",facing="west")
b.set(-2,0,1,"redstone_torch"); b.set(-2,1,1,S)
for (x,y,p) in [(-2,2,15),(-1,3,14),(0,4,13),(1,4,12),(2,4,11),(3,3,10),(4,2,9)]: b.dust(x,y,1,p)
b.set(4,1,1,S)
b.set(-1,3,0,"target"); b.set(0,4,0,"target"); b.set(3,3,0,"target")
# a: in-plane observer
b.dust(-2,-2,1); b.dust(-2,-2,0); b.dust(-1,-2,0); b.obs(0,-2,0,"west")
# b: Q observer
b.set(-1,-1,1,S); b.obs(-1,-2,1,"down"); b.rep(-1,-3,1,"west",2)
# chain
b.set(-2,-2,2,S); b.dust(-2,-1,2)
for (x,z) in [(-2,3),(-2,4),(-1,4),(0,4)]: b.dust(x,-2,z)
b.rep(1,-2,4,"west",4)
for (x,z) in [(2,4),(3,4),(4,4),(4,3),(4,2),(4,1),(4,0),(3,1),(2,3)]: b.dust(x,-2,z)
# c: N3 observer
b.set(1,-2,1,S); b.obs(2,-2,1,"east")
# rear
b.rep(3,-3,0,"east",3)
# side
b.rep(2,-3,2,"south",4); b.rep(2,-3,1,"south",4)
# A stuff
b.set(2,-3,0,"comparator",facing="east",mode="subtract"); b.set(2,-4,0,S)
b.obs(2,-2,0,"down"); b.set(2,-1,0,S)
print(b.save("w/b1.json"))
