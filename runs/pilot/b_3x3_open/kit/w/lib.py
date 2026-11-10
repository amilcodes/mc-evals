import sys; sys.path.insert(0,'.')
from pdbuild import Design
S="stone"
def wall(x,y,z):
    if z==0: return False
    return (x in(-1,3) and 0<=y<=2) or (y in(-1,3) and 0<=x<=2)
class B:
    def __init__(s,state): s.d=Design(state)
    def set(s,x,y,z,b,**p): s.d.set(x,y,z,b,**p)
    def floor(s,x,y,z):
        if s.d.get(x,y-1,z) is None and not wall(x,y-1,z): s.d.set(x,y-1,z,S)
    def sp(s,x,y,z,f,ext=False):
        s.d.set(x,y,z,"sticky_piston",facing=f,extended=ext)
        if ext:
            dx,dy={"east":(1,0),"west":(-1,0),"up":(0,1),"down":(0,-1)}[f]
            s.d.set(x+dx,y+dy,z,"piston_head",facing=f,type="sticky")
    def dust(s,x,y,z,p=None):
        if p is None: s.d.set(x,y,z,"redstone_wire")
        else: s.d.set(x,y,z,"redstone_wire",power=p)
        s.floor(x,y,z)
    def rep(s,x,y,z,f,delay=4,powered=False):
        s.d.set(x,y,z,"repeater",facing=f,delay=delay,powered=powered); s.floor(x,y,z)
    def obs(s,x,y,z,f): s.d.set(x,y,z,"observer",facing=f)
    def door(s,closed=True):
        if closed:
            for x in range(3):
                for y in range(3): s.d.set(x,y,0,S)
    def save(s,path):
        s.d.save(path); lo,hi=s.d.bbox(); return lo,hi
