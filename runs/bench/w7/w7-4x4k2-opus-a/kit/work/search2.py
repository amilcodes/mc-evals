import random, time
exec(open('work/solve.py').read())
def attempt(XN):
    global FIXED
    FIXED={(XN,1):'b',(XN,0):'b',(-7,1):'d',(-7,0):'d'}
    ln={}
    for x in range(0,-7,-1): ln[(x,1)]=('r',1)
    for x in range(-6,1): ln[(x,0)]=('r',1)
    for p,k in FIXED.items(): ln[p]=(k,0)
    cand=[p for p in ORDER if p not in FIXED]
    tp=sorted(random.sample(cand,5),key=lambda p:ORDER.index(p))
    names=['A1','B3','A4','B5','A7']
    fa=feed['A'][:]; random.shuffle(fa); fb=feed['B'][:]; random.shuffle(fb)
    F={'A1':fa[0],'A4':fa[1],'A7':fa[2],'B3':fb[0],'B5':fb[1]}
    tm=dict(zip(names,tp))
    sp=[(k,T(*tm[k]),None,F[k]) for k in names]
    random.shuffle(sp)
    sp.append(('PXb',(XN,Y-2,0),(-3,-2,0),None))
    Lx,paths=make_left(ln,set(tp),XN,sp, box=((-9,-3,0),(0,Y,2)), Y=Y, verbose=False)
    if not all(v is not None for v in paths.values()): return None
    pb=paths['PXb'][1]; m=len(pb)
    best=None
    for k in range(1,m):
        sp2=[('PXt',('branch',pb[k-1]),(-3,5,0),None)]
        # rebuild with fixed paths is costly; route on top of Lx occupancy
        occ=Design(); occ.merge(Lx); center(occ,Y)
        R=Router(occ,((-9,-3,0),(0,Y,2)))
        R.forbid|=mech_moving_cells(); R.noback|=mech_moving_cells()
        R.forbid|={(-2,5,1),(-3,3,1),(-1,4,1),(-4,1,1),(-4,3,0),(-1,6,0)}
        R.forbid|=set(watched(occ).keys())
        src=pb[k-1]
        start=[add(src,v) for v in DIRS if R.free(add(src,v))]
        R.forbid.discard((-3,5,0))
        p=R.route(src,start,(-3,5,0),maxlen=40)
        if p is None: continue
        nt=k+len(p); D=2*(m-nt)
        if D<0: continue
        NLx={kk:len(v[1]) for kk,v in paths.items() if kk!='PXb'}
        tn={kk:tm[kk] for kk in names}
        r=solve(tn,NLx,0,nt,DD=D)
        if r:
            R.place(src,p)
            for c,(b,pr) in occ.blocks.items():
                if c not in Lx.blocks: Lx.set(*c,b,**pr)
            return (XN,tm,NLx,m,k,nt,D,r,Lx)
    return None
