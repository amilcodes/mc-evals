exec(open('gen1.py').read())
exec(open('mods.py').read())
def controller(d, lever=True):
    # chain flowing west at y=3,z=0
    n0=-11
    reps={-12:4,-14:4,-16:4}
    for x in range(-11,-20,-1):
        if x in reps: rep(d,x,0,"east",reps[x])
        else: dust(d,x,0)
    if lever:
        d.set(-10,2,0,"stone"); d.set(-10,3,0,"lever",face="floor",facing="north")
    # modules
    oR=mod(d,-11,-1,1,4,True)    # R(P) north
    oF=mod(d,-11,+1,2,1)    # F(B) south
    oP=mod(d,-19,-1,4,1,True)    # F(P) north at x=-19
    # P collector: row z=-6
    for z in range(-6,-8,-1): pass
    for z in range(-6,-9,-1): dust(d,-11,z)
    for z in range(-6,-9,-1): dust(d,-19,z)
    dust(d,-19,-5) if False else None
    for x in range(-19,-6):
        if x==-14: rep(d,x,-8,"west",1)
        else: dust(d,x,-8)
    # stairs down east
    dst(d,-6,2,-6); dst(d,-5,1,-6)
    # but (-7,3,-6) is last of row; fine
    for z in range(-5,1):
        if z==-3: rp(d,-5,1,z,"north",1)   # input from north, output south
        else: dst(d,-5,1,z)
    # F(B) collector: out cell (-11,5) -> row z=6
    for z in range(5,7): dust(d,-11,z)
    for x in range(-11,-4):
        if x==-8: rep(d,x,6,"west",1)
        else: dust(d,x,6)
    # (-4,3,6) is trunk end already
    return d
def alevel(d):
    for z in range(1,9):
        if z==4: rep(d,-15,z,"north",1)
        else: dust(d,-15,z)
    dst(d,-14,2,8); dst(d,-13,1,8); dst(d,-12,0,8); dst(d,-11,-1,8)
    for x in range(-10,-5): dst(d,x,-1,8)
    for z in range(7,-1,-1):
        if z==4: rp(d,-6,-1,z,"south",1)
        else: dst(d,-6,-1,z)
    dst(d,-5,-1,0); dst(d,-4,-1,0)
    return d
