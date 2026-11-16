def mech(closed=True):
    d = Design("closed" if closed else "open")
    S = "sticky_piston"
    ext = "true" if closed else "false"
    def sp(x,y,z,f):
        d.set(x,y,z,S,facing=f,extended=ext)
        if closed:
            dx,dy = {"down":(0,-1),"up":(0,1),"east":(1,0),"west":(-1,0)}[f]
            d.set(x+dx,y+dy,z,"piston_head",facing=f,type="sticky")
    for x in range(3):
        for y in range(3):
            if closed: d.set(x,y,0,"stone")
    # top
    for x in range(3): sp(x,4,0,"down")
    if not closed:
        for x in range(3): d.set(x,3,0,"stone")
    # right
    sp(4,1,0,"west"); sp(4,0,0,"west")
    if not closed: d.set(3,1,0,"stone"); d.set(3,0,0,"stone")
    d.set(3,2,0,"stone")
    # bottom
    sp(1,-2,0,"up")
    if not closed: d.set(1,-1,0,"stone")
    d.set(0,-1,0,"stone"); d.set(2,-1,0,"stone")
    # left BL
    sp(-2,0,0,"east")
    if not closed: d.set(-1,0,0,"stone")
    # center mech
    d.set(-3,1,0,S,facing="east")
    sp(-2,1,0,"east")
    sp(-1,3,0,"down")
    if not closed:
        d.set(-1,1,0,"stone"); d.set(-1,2,0,"stone")
    return d
