from pdbuild import Design
SW={'east':'south','south':'east','west':'north','north':'west'}
def edge_module(d, ox=0, oy=0, oz=0, swap=False):
    """lever at (ox,oy+1,oz) on B0 (ox,oy,oz). returns (rise_cell, fall_cell). swap: exchange x/z axes."""
    def pos(x,y,z):
        return (ox+z,oy+y,oz+x) if swap else (ox+x,oy+y,oz+z)
    def S(x,y,z,b,**p):
        if swap and 'facing' in p and b!='lever': p['facing']=SW.get(p['facing'],p['facing'])
        d.set(*pos(x,y,z),b,**p)
    def floor(x,z): S(x,-1,z,"stone")
    def dust(x,z): floor(x,z); S(x,0,z,"redstone_wire")
    def rep(x,z,f,dl): floor(x,z); S(x,0,z,"repeater",facing=f,delay=dl)
    def comp(x,z,f): floor(x,z); S(x,0,z,"comparator",facing=f,mode="subtract")
    S(0,0,0,"stone"); S(0,1,0,"lever",face="floor",facing="north")
    for p in [(1,0),(2,0),(3,0),(3,1),(3,2),(3,-1),(3,-2)]: dust(*p)
    rep(0,1,"north",1); comp(0,2,"north"); rep(2,2,"east",3); dust(1,2); dust(0,3)
    rep(0,-1,"south",3); comp(0,-2,"south"); rep(2,-2,"east",1); dust(1,-2); dust(0,-3)
    return pos(0,0,3),pos(0,0,-3)
