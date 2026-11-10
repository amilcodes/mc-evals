from pdbuild import Design
from v1 import mech, logic, dust, rep
CROSS=dict(north="side",south="side",east="side",west="side")
def singles(d):
    for x in (0,1):
        d.set(x,-2,0,"sticky_piston",facing="up"); d.set(x,-1,0,"stone")
        d.set(x,4,0,"sticky_piston",facing="down"); d.set(x,3,0,"stone")
    d.set(2,-1,0,"stone"); d.set(2,3,0,"stone")
    for y in (0,1,2):
        d.set(4,y,0,"sticky_piston",facing="west"); d.set(3,y,0,"stone")
def sdist(d):
    d.set(0,-2,1,"stone"); d.set(1,-2,1,"lever",face="wall",facing="east")
    for x in (2,3,4): dust(d,x,-2,1)
    for (y,z) in ((-1,2),(0,1),(1,2),(2,1),(3,2),(4,1)):
        d.set(4,y-1,z,"glass"); d.set(4,y,z,"redstone_wire")
    dust(d,3,4,1); d.set(2,4,1,"repeater",facing="east"); d.set(1,4,1,"stone")
    d.set(0,4,1,"redstone_wire",**CROSS)
if __name__=="__main__":
    d=Design("open"); mech(d); logic(d); singles(d); sdist(d)
    d.remove(-1,-1,6); d.remove(-1,-2,6)
    for z in range(2,7): dust(d,1,-2,z)
    dust(d,0,-2,6); dust(d,-1,-2,6); dust(d,-2,-1,6)
    d.save("v1full.json")
