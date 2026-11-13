from pdlab import *
from pdbuild import Design
def rig(pist, stones, extra=None):
    """pist: dict id->(x,y,facing); stones: list of (x,y). Each piston gets a lever at z=2."""
    d=Design()
    for (x,y) in stones: d.set(x,y,0,"stone")
    levers={}
    for k,(x,y,f) in pist.items():
        d.set(x,y,0,"sticky_piston",facing=f)
        d.set(x,y,1,"stone")
        d.set(x,y,2,"lever",face="wall",facing="south")
        levers[k]=(x,y,2)
    if extra:
        for (x,y,z,b,pr) in extra: d.set(x,y,z,b,**pr)
    return d,levers
def pulse(lab,lev,gap=6):
    lab.flip(*lev); lab.step(2); lab.flip(*lev)
    if gap>0: lab.step(gap)
def row(lab,y=1,x0=-5,x1=4,z=0):
    s=''
    for x in range(x0,x1+1):
        b=lab.block(x,y,z)
        s+= '#' if b=='stone' else ('.' if b=='air' else ('P' if 'piston' in b else '?'))
    return s
