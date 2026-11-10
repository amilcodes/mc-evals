import sys; sys.path.insert(0,'w')
from lib import *
def build(init="V", lane_on=True, out="w/d126.json"):
    b=B("closed"); b.door()
    for y in range(3):
        b.sp(-2,y,0,"east",True); b.sp(4,y,0,"west",True)
    b.sp(1,4,0,"down",True)
    if init=="V":
        b.sp(1,-3,0,"up",True); b.sp(1,-1,0,"up")
    else:
        b.sp(1,-3,0,"up"); b.sp(1,-2,0,"up")
    b.sp(-1,-1,0,"east")
    # tower + arch
    b.set(-2,-1,1,S); b.set(-3,-1,1,"lever",face="wall",facing="west")
    b.set(-2,0,1,"redstone_torch"); b.set(-2,1,1,S)
    for (x,y,p) in [(-2,2,15),(-1,3,14),(0,4,13),(1,4,12),(2,4,11),(3,3,10),(4,2,9)]: b.dust(x,y,1,p)
    b.set(4,1,1,S)
    b.set(-1,3,0,"target"); b.set(0,4,0,"target"); b.set(3,3,0,"target")
    # c0
    b.dust(-2,-2,1); b.dust(-2,-2,0)
    # Q: OQ in-plane watching R1'
    b.obs(-1,-2,0,"down"); b.rep(-1,-3,0,"west",3)
    # a: relay + a-obs -> N3
    b.obs(-1,-2,1,"west"); b.obs(0,-2,1,"west"); b.set(1,-2,1,S)
    # lane -> side
    for x in (-1,0,1): b.rep(x,-3,1,"west",4,powered=lane_on)
    b.dust(2,-3,1)
    # east relay chain
    b.obs(4,-1,0,"up"); b.obs(4,-1,1,"north"); b.obs(3,-1,1,"east"); b.obs(3,-2,1,"up"); b.obs(2,-2,1,"east")
    b.obs(4,-2,1,"up"); b.set(4,-3,1,S); b.dust(4,-3,0); b.rep(3,-3,0,"east",4)
    # A stuff
    b.set(2,-3,0,"comparator",facing="east",mode="subtract"); b.set(2,-4,0,S)
    b.obs(2,-2,0,"down"); b.set(2,-1,0,S)
    print(b.save(out))
if __name__=="__main__": build()
