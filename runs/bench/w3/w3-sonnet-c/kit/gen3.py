exec(open('gen1.py').read())
exec(open('mods.py').read())
def controller(d, lever=True):
    reps={-12:4,-14:4,-16:4}
    for x in range(-11,-20,-1):
        if x in reps: rep(d,x,0,"east",reps[x])
        else: dust(d,x,0)
    if lever:
        d.set(-10,2,0,"stone"); d.set(-10,3,0,"lever",face="floor",facing="north")
    mod(d,-11,-1,1,3)   # R(P)
    mod(d,-11,+1,3,1)   # F(B)
    mod(d,-19,-1,3,1)   # F(P)
    # P collector
    for z in (-6,-7,-8): dust(d,-11,z)
    for z in (-6,-7,-8): dust(d,-19,z)
    for x in range(-19,-7):
        if x==-9: rep(d,x,-8,"west",4)      # stretch + delay
        else: dust(d,x,-8)
    dst(d,-7,3,-8); dst(d,-6,2,-8); dst(d,-5,1,-8)
    for z in range(-7,1):
        if z==-4: rp(d,-5,1,z,"south",1) if False else rp(d,-5,1,z,"north",1)
        else: dst(d,-5,1,z)
    # F(B) collector
    dust(d,-11,6); dust(d,-11,7)
    for x in range(-11,-1):
        if x==-8: rep(d,x,7,"west",1)
        else: dust(d,x,7)
    return d
def alevel(d):
    for z in range(1,9):
        if z==4: rep(d,-15,z,"north",1)
        else: dust(d,-15,z)
    dst(d,-14,2,8); dst(d,-13,1,8); dst(d,-12,0,8); dst(d,-11,-1,8)
    for x in range(-10,-5):
        if x==-8: rp(d,x,-1,8,"west",1)
        else: dst(d,x,-1,8)
    for z in range(7,-1,-1):
        if z==4: rp(d,-6,-1,z,"south",1)
        else: dst(d,-6,-1,z)
    dst(d,-5,-1,0); dst(d,-4,-1,0)
    return d
def trunk(d):
    for z in range(1,8): dst(d,-1,3,z,sup=None)
def full():
    d=build(); trunk(d); controller(d); alevel(d); return d
