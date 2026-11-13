exec(open('ctl2.py').read())
def ctrl():
    d=Design("open")
    N={'n0':-10,'n1':-15,'n2':-20,'n3':-25,'n4':-30,'n5':-35}
    # chain
    reps={-11:2,-16:4,-18:2,-21:1,-26:2,-31:4}
    for x in range(-10,-36,-1):
        if x in reps: rep(d,x,0,"east",reps[x])
        else: dust(d,x,0)
    # lever
    d.set(-9,Y-1,0,"stone"); d.set(-9,Y,0,"lever",face="floor",facing="north")
    outs=[]
    # B modules south
    spec=[('n0','F',1),('n1','R',1),('n3','R',1),('n4','F',1),('n5','F',1)]
    for n,t,dl in spec:
        xn=N[n]
        o=(modR if t=='R' else modF)(d,xn,+1,dl)
        outs.append((xn,o[1],+1))
    # P modules north
    for n,t in [('n0','R'),('n3','F')]:
        xn=N[n]
        o=(modR if t=='R' else modF)(d,xn,-1,4)
        outs.append((xn,o[1],-1))
    for xn,z0,sg in outs:
        # vline from z0 to 9*sg ; dummy repeater for modules east of -22
        dummy = xn>-22
        for z in range(z0, 9*sg+sg, sg):
            if dummy and z==z0+sg:
                rep(d,xn,z,"north" if sg>0 else "south",1)
            else: dust(d,xn,z)
    for sg in (+1,-1):
        for x in range(-35,-5):
            if x in (-22,-8): rep(d,x,9*sg,"west",1)
            else: dust(d,x,9*sg)
    return d
