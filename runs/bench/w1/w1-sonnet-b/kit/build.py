import itertools, json, sys
from collections import deque
from pdbuild import Design
from edge import edge_module

DIRN={(1,0,0):'east',(-1,0,0):'west',(0,1,0):'up',(0,-1,0):'down',(0,0,1):'south',(0,0,-1):'north'}
NB=list(DIRN.keys())
def add(a,b): return (a[0]+b[0],a[1]+b[1],a[2]+b[2])
def sub(a,b): return (a[0]-b[0],a[1]-b[1],a[2]-b[2])

def tube(c):
    x,y,z=c
    if z==0: return False
    if -1<=x<=3 and -1<=y<=3 and not ((x in(-1,3)) and (y in(-1,3))):
        return True
    return False

import random
def build(ox=-9,oy=0,oz=0,MINSTEP=3,swap=False,box=(-14,8,-6,9,-5,5),seed=None,tapsel=None,TL=12):
    rnd=random.Random(seed)
    mech={}   # pos -> (block,props)
    def M(p,b,**pr): mech[p]=(b,pr)
    for p in [(-1,1,0),(-1,2,0),(-1,0,0),(3,1,0),(3,0,0),(3,2,0)]+[(x,-1,0) for x in range(3)]+[(x,3,0) for x in range(3)]:
        M(p,"stone")
    M((-3,1,0),"sticky_piston",facing="east"); M((-2,1,0),"sticky_piston",facing="east"); M((-1,3,0),"sticky_piston",facing="down")
    for x in range(3):
        M((x,-2,0),"sticky_piston",facing="up"); M((x,4,0),"sticky_piston",facing="down")
    M((4,1,0),"sticky_piston",facing="west")
    # module
    dm=Design(); r,f=edge_module(dm,ox,oy,oz,swap)
    modblocks=dict(dm.blocks)
    lever=(ox,oy+1,oz)
    # taps: (name, W cell, dir from T to W)
    taps=[]   # list of (chain, T, dirvec, W)
    def tap(chain,T,dirv): taps.append((chain,T,dirv,add(T,dirv)))
    S=(0,0,1);N=(0,0,-1);U=(0,1,0);Dn=(0,-1,0)
    tap('A',(-2,1,-1),N); tap('A',(-1,3,-1),N); tap('A',(-3,1,-1),N)
    tap('B',(-3,1,1),S); tap('B',(-2,1,1),S); tap('B',(-1,3,1),S); tap('B',(-3,2,0),U); tap('B',(-1,-1,0),Dn); tap('B',(-3,0,0),Dn); tap('B',(-2,0,0),Dn)
    for x in (0,1,2): tap('T',(x,-2,1),S)
    tap('T',(4,1,1),S)
    for x in (2,1,0): tap('T',(x,4,1),S)
    reserved=set(mech)|set(modblocks)|{lever}
    Tcells={t[1] for t in taps}; Wcells={t[3] for t in taps}
    reserved|=Tcells
    P=(ox-1,oy+1,oz)   # observer watching lever, facing east
    Pface='east'
    reserved.add(P)
    srcs={'A':r,'B':f,'T':P}
    used=set()
    chain={'A':[],'B':[],'T':[]}
    def blocked(c,chainname):
        if c in reserved or tube(c): return True
        if c in used: return True
        if c[2]==0 and -1<=c[0]<=3 and -1<=c[1]<=3: return True
        if c in Wcells and c!=CUR[0]: return True
        if not (box[0]<=c[0]<=box[1] and box[2]<=c[1]<=box[3] and box[4]<=c[2]<=box[5]): return True
        return False
    targets_of={k:[t[3] for t in taps if t[0]==k] for k in 'ABT'}
    pist=[p for p,(b,pr) in mech.items() if 'piston' in b]
    FORB=set(pist)|{(p[0],p[1]+1,p[2]) for p in pist}
    def okback(prev,c):
        back=add(c,sub(c,prev))
        if back in FORB: return False
        if back in mech or back in modblocks: return False
        return True
    CUR=[None]
    def bfs_dist(tgt,name):
        dist={tgt:0};dq=deque([tgt])
        while dq:
            c=dq.popleft()
            for d in NB:
                n=add(c,d)
                if n in dist or blocked(n,name): continue
                dist[n]=dist[c]+1;dq.append(n)
        return dist
    def dfs(cur,tgt,L,name,dist):
        path=[];seen=set();BUD=[0]
        def rec(c,rem):
            BUD[0]+=1
            if BUD[0]>4000: return False
            nbs=list(NB); rnd.shuffle(nbs)
            for d in nbs:
                n=add(c,d)
                if n in seen: continue
                if n!=tgt and blocked(n,name): continue
                if not okback(c,n): continue
                if rem==1:
                    if n==tgt:
                        path.append(n);return True
                    continue
                if n==tgt: continue
                if dist.get(n,10**9)>rem-1: continue
                seen.add(n);path.append(n)
                if rec(n,rem-1): return True
                path.pop();seen.discard(n)
            return False
        return list(path) if rec(cur,L) else None
    import time as _t
    DEAD=[_t.time()+TL]
    def cands(cur,tgt,minlen,name):
        if _t.time()>DEAD[0]: raise Exception('timeout')
        dist=bfs_dist(tgt,name)
        out=[];seenp=set()
        nd=[dist[add(cur,d)] for d in NB if add(cur,d) in dist]
        if not nd: return out
        sh=min(nd)+1
        for L in range(max(minlen,sh),max(minlen,sh)+8):
            for _ in range(6):
                p=dfs(cur,tgt,L,name,dist)
                if p and tuple(p) not in seenp:
                    seenp.add(tuple(p));out.append(p)
        return out
    def plan(name):
        tg=targets_of[name]
        def rec(i,cur):
            if i==len(tg): return True
            CUR[0]=tg[i]
            minlen=1 if (name=='T' or not chain[name]) else MINSTEP
            for p in cands(cur,tg[i],minlen,name):
                for c in p: chain[name].append(c); used.add(c)
                if rec(i+1,tg[i]): return True
                for c in p: chain[name].pop(); used.discard(c)
                CUR[0]=tg[i]
            return False
        if not rec(0,srcs[name]): raise Exception("plan fail "+name)
    for n in 'ABT': plan(n)
    # assemble
    d=Design("open")
    for p,(b,pr) in mech.items(): d.set(*p,b,**pr)
    for p,(b,pr) in modblocks.items(): d.set(*p,b,**pr)
    d.set(*lever,"lever",face="floor",facing="north") if False else None
    # lever already in module blocks
    d.set(*P,"observer",facing=Pface)
    for (ch,T,dv,W) in taps: d.set(*T,"observer",facing=DIRN[dv])
    for name in 'ABT':
        prev=srcs[name]
        for c in chain[name]:
            d.set(*c,"observer",facing=DIRN[sub(prev,c)])
            prev=c
    return d,chain,taps
if __name__=="__main__":
    d,chain,taps=build()
    d.save("d1.json")
    print({k:len(v) for k,v in chain.items()})
    print(d.bbox())
