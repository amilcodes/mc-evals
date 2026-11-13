def mech():
    d = Design("open")
    # left side (rows 1,2): stones S1 at (-1,1),(-1,2); S0 parked (-1,0),(-1,3)
    for y in (0,1,2,3): d.set(-1,y,0,"stone")
    for y in (1,2):
        d.set(-2,y,0,"sticky_piston",facing="east")
        d.set(-3,y,0,"sticky_piston",facing="east")
    d.set(-1,4,0,"sticky_piston",facing="down")
    d.set(-1,-1,0,"sticky_piston",facing="up")
    # top/bottom pullers
    for x in range(4):
        d.set(x,4,0,"stone"); d.set(x,5,0,"sticky_piston",facing="down")
        d.set(x,-1,0,"stone"); d.set(x,-2,0,"sticky_piston",facing="up")
    return d

def levers(d):
    # direct test levers on z=-1 side via blocks
    L = {}
    def lv(name,x,y,z,face="floor"):
        L[name]=(x,y,z)
    # B: block at (-3,2,-1),(-3,1,-1)? use levers attached to pistons' back side
    d.set(-4,2,0,"lever",face="wall",facing="west"); L['B2']=(-4,2,0)   # attached to (-3,2)? lever on wall facing west attaches to block east = piston
    return L
