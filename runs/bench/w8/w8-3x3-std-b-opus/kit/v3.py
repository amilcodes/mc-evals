def build3(cfg=None):
    c = dict(ps=[4,4,4,4,3], psl=1, s_side=[1,1,1,1], main=[4,4], a28=[4,4], qo_side=2, x1=3, x2=3, w1side=1, stretch=2)
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
    # bus column x=-8
    for z in [-3,-2,-1]: dust(-8,1,z)
    S(-9,0,-3,"lever",face="wall",facing="west")
    rep(-8,1,0,"north",c['main'][0]); rep(-8,1,1,"north",c['main'][1])
    # z=-3 P_s rear row
    for i,x in enumerate([-7,-6,-5,-4,-3]): rep(x,1,-3,"west",c['ps'][i])
    dust(-2,1,-3); rep(-2,1,-2,"north",c['psl']); cmp(-2,1,-1,"north")
    # z=-2 S side row
    for i,x in enumerate([-7,-6,-5,-4]): rep(x,1,-2,"west",c['s_side'][i])
    dust(-3,1,-2); cmp(-3,1,-1,"west"); rep(-4,1,-1,"west",1)
    # z=-1 pulse
    S(-7,1,-1,"observer",facing="west"); sup(-7,1,-1)
    rep(-6,1,-1,"west",c['stretch']); dust(-5,1,-1)
    # z=0 A28
    dust(-5,1,0); cmp(-4,1,0,"west")
    rep(-7,1,1,"south",c['a28'][0]); dust(-7,1,0); rep(-6,1,0,"west",c['a28'][1])
    # N row z=2
    dust(-8,1,2); dust(-7,1,2); rep(-6,1,2,"west",1)
    for x in [-5,-4,-3]: dust(x,1,2)
    rep(-4,1,1,"south",c['qo_side'])
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
    dust(0,4,4); dust(0,4,3)
    for x in [0,1,2]: dust(x,4,2); rep(x,4,1,"south",1)
    dust(3,3,2); dust(4,2,2); rep(4,1,1,"south",1)
    return d
