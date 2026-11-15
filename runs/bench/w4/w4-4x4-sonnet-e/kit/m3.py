def mechS(d):
    # S1 col1
    d.set(1,-3,0,"sticky_piston",facing="up"); d.set(1,-2,0,"sticky_piston",facing="up")
    d.set(1,-1,0,"stone"); d.set(0,-1,0,"stone"); d.set(-1,-1,0,"sticky_piston",facing="east")
    # S2 col2 (mirror x about 1.5)
    d.set(2,-3,0,"sticky_piston",facing="up"); d.set(2,-2,0,"sticky_piston",facing="up")
    d.set(2,-1,0,"stone"); d.set(3,-1,0,"stone"); d.set(4,-1,0,"sticky_piston",facing="west")
def pulsegen(d, cells_line, last_dir, name):
    """cells_line: list of dust cells (x,y,z) in order from piston outward; places supports below, then observer + watch dust + lever beyond."""
    for (x,y,z) in cells_line:
        d.set(x,y-1,z,"glass"); d.set(x,y,z,"redstone_wire")
    x,y,z=cells_line[-1]; dx,dz=last_dir
    # observer beyond, facing away (back toward line)
    ox,oz=x+dx,z+dz
    face={(1,0):"east",(-1,0):"west",(0,1):"south",(0,-1):"north"}[(dx,dz)]
    d.set(ox,y,oz,"observer",facing=face)
    wx,wz=ox+dx,oz+dz
    d.set(wx,y-1,wz,"stone"); d.set(wx,y,wz,"redstone_wire")
    lx,lz=wx+dx,wz+dz
    d.set(lx,y-1,lz,"stone"); d.set(lx,y,lz,"lever",face="floor",facing="north")
    return (lx,y,lz)
def watch(d, ox,oy,oz, face, wx,wy,wz):
    d.set(ox,oy,oz,"observer",facing=face)
def inputsS(d):
    lev={}
    lev['S1P1']=pulsegen(d,[(0,-3,0),(-1,-3,0),(-2,-3,0)],(-1,0),'S1P1')
    lev['S1P2h']=pulsegen(d,[(1,-2,-1),(1,-2,-2),(1,-2,-3)],(0,-1),'S1P2h')
    for z in (-1,-2,-3,-4,-5,-6): d.set(2,-2,z,"stone")
    lev['S2P1']=pulsegen(d,[(2,-3,-1),(2,-3,-2),(2,-3,-3)],(0,-1),'S2P1')
    lev['S2P2h']=pulsegen(d,[(3,-2,0),(4,-2,0),(4,-2,-1),(4,-2,-2)],(0,-1),'S2P2h')
    # V1 tail observer (-2,-1,0) facing west, watch (-3,-1,0), then line west
    d.set(-2,-1,0,"observer",facing="west")
    for x in (-3,-4): d.set(x,-2,0,"stone"); d.set(x,-1,0,"redstone_wire")
    d.set(-5,-2,0,"stone"); d.set(-5,-1,0,"lever",face="floor",facing="north"); lev['S1V']=(-5,-1,0)
    # V2 tail observer (5,-1,0) facing east, watch (6,-1,0)
    d.set(5,-1,0,"observer",facing="east")
    for x in (6,7): d.set(x,-2,0,"stone"); d.set(x,-1,0,"redstone_wire")
    d.set(8,-2,0,"stone"); d.set(8,-1,0,"lever",face="floor",facing="north"); lev['S2V']=(8,-1,0)
    # P2f: observers (1,-2,1),(2,-2,1) down; watch dots (1,-3,1),(2,-3,1) joined; feed from east (3,-3,1)
    d.set(1,-2,1,"observer",facing="down"); d.set(2,-2,1,"observer",facing="down")
    for x in (1,2,3):
        d.set(x,-4,1,"stone"); d.set(x,-3,1,"redstone_wire")
    d.set(3,-2,1,"stone")  # cut
    d.set(4,-4,1,"stone"); d.set(4,-3,1,"lever",face="floor",facing="north"); lev['P2f']=(4,-3,1)
    return lev
d=Design(); mechS(d); LEV=inputsS(d); d.save('m3.json')
import json; json.dump({k:list(v) for k,v in LEV.items()},open('m3lev.json','w'))
