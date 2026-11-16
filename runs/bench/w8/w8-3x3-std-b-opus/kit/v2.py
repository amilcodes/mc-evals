def build2(cfg=None):
    c = dict(ps=[4,4,4,4,4], a28=[4,4,4,4], s_side=[1,1,1,1], main=[4,4], qo_side=2, x1=3, x2=3, w1side=1, stretch=2)
    if cfg: c.update(cfg)
    d = mech()
    def S(x,y,z,b="stone",**p): d.set(x,y,z,b,**p)
    def wall(x,y,z):
        if z==0: return False
        return ((x in(-1,3)) and 0<=y<=2) or ((y in(-1,3)) and 0<=x<=2)
    def sup(x,y,z):
        if d.get(x,y-1,z) is None and not wall(x,y-1,z): S(x,y-1,z)
    def dust(x,y,z): S(x,y,z,"redstone_wire"); sup(x,y,z)
    def rep(x,y,z,f,dl=1): S(x,y,z,"repeater",facing=f,delay=dl); sup(x,y,z)
    def cmp(x,y,z,f): S(x,y,z,"comparator",facing=f,mode="subtract"); sup(x,y,z)
    # lever on side of bus start support
    for x in range(-8,-1): dust(x,1,-7)
    S(-9,0,-7,"lever",face="wall",facing="west")
    # x=-2 P_s rear
    for i,z in enumerate([-6,-5,-4,-3,-2]): rep(-2,1,z,"north",c['ps'][i])
    cmp(-2,1,-1,"north")
    for i,z in enumerate([-6,-5,-4,-3]): rep(-3,1,z,"north",c['s_side'][i])
    dust(-3,1,-2); cmp(-3,1,-1,"west"); rep(-4,1,-1,"west",1)
    for i,z in enumerate([-6,-5,-4,-3]): rep(-5,1,z,"north",c['a28'][i])
    for z in [-2,-1,0]: dust(-5,1,z)
    cmp(-4,1,0,"west")
    # main column x=-8: dust then repeaters
    for z in range(-6,0): dust(-8,1,z)
    rep(-8,1,0,"north",c['main'][0]); rep(-8,1,1,"north",c['main'][1])
    dust(-8,1,2); dust(-7,1,2); rep(-6,1,2,"west",1)
    for x in [-5,-4,-3]: dust(x,1,2)
    rep(-4,1,1,"south",c['qo_side'])
    # pulse: observer watching main dust (-8,1,-1)
    S(-7,1,-1,"observer",facing="west"); sup(-7,1,-1)
    rep(-6,1,-1,"west",c['stretch'])
    # N net down to D line + V
    dust(-2,0,2); dust(-2,-1,3); dust(-1,-2,3); dust(-1,-2,2)
    for x in [0,1,2]: dust(x,-2,2); rep(x,-2,1,"south",1)
    rep(-1,-2,1,"south",1); S(-1,-2,0)
    # W1 path
    dust(-7,2,3); dust(-7,3,4)
    rep(-6,3,4,"west",c['x1']); dust(-5,3,4)
    for p in [(-5,3,3),(-5,3,2),(-4,3,2),(-3,3,2)]: dust(*p)
    rep(-2,3,2,"west",c['w1side'])
    rep(-4,3,4,"west",c['x2'])
    for p in [(-3,3,4),(-2,3,4),(-1,3,4),(-1,3,3)]: dust(*p)
    cmp(-1,3,2,"south"); dust(-1,3,1); dust(-1,3,0)
    # G top fed from W1 rear lane
    dust(0,4,4); dust(0,4,3)
    for x in [0,1,2]: dust(x,4,2); rep(x,4,1,"south",1)
    dust(3,3,2); dust(4,2,2); rep(4,1,1,"south",1)
    return d
