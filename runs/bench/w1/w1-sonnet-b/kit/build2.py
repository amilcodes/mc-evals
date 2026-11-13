import random, time
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
    return -1<=x<=3 and -1<=y<=3 and not ((x in(-1,3)) and (y in(-1,3)))
S=(0,0,1);N=(0,0,-1);U=(0,1,0);Dn=(0,-1,0);E=(1,0,0);W=(-1,0,0)
def alts(piston,dirs):
    # T = piston - dirv ... T adjacent to piston, dirv points from T away from piston
    out=[]
    for dv in dirs:
        T=sub(piston,dv)   # T + dv = piston ?? no: T's back = piston => piston = T - dv => T = piston + dv
    return out
def tapalts(piston,dvs):
    # observer T at piston+(-dv)... T faces dv (watches T+dv); back = T-dv = piston => T = piston+dv
    return [(add(piston,dv),dv) for dv in dvs]
ALL=[S,N,U,Dn,E,W]
def build(ox=0,oy=-3,oz=-2,MINSTEP=3,swap=True,box=(-3,4,-2,4,-2,2),seed=None,TL=20,nowrite=False,order='BA',fixedT=True):
    rnd=random.Random(seed)
    mech={}
    def M(p,b,**pr): mech[p]=(b,pr)
    for p in [(-1,1,0),(-1,2,0),(-1,0,0),(3,1,0),(3,0,0),(3,2,0)]+[(x,-1,0) for x in range(3)]+[(x,3,0) for x in range(3)]:
        M(p,"stone")
    M((-3,1,0),"sticky_piston",facing="east"); M((-2,1,0),"sticky_piston",facing="east"); M((-1,3,0),"sticky_piston",facing="down")
    for x in range(3):
        M((x,-2,0),"sticky_piston",facing="up"); M((x,4,0),"sticky_piston",facing="down")
    M((4,1,0),"sticky_piston",facing="west")
    dm=Design(); r,f=edge_module(dm,ox,oy,oz,swap)
    modblocks=dict(dm.blocks)
    lever=(ox,oy+1,oz)
    Y=(-3,1,0);X=(-2,1,0);V=(-1,3,0)
    def ya(dvs=(S,N,U,Dn,W)): return tapalts(Y,dvs)
    def xa(dvs=(S,N,U,Dn)): return tapalts(X,dvs)
    def va(dvs=(S,N,W,U)): return tapalts(V,dvs)
    X2=[((-1,-1,0),Dn)]
    seqs={'A':[xa(),va(),ya()],
          'B':[ya(),xa(),va(),ya(),X2,ya(),xa()],
          'T':[tapalts((x,-2,0),(S,N)) for x in (0,1,2)]+[tapalts((4,1,0),(S,N,E,U,Dn))]+[tapalts((x,4,0),(S,N,U)) for x in (2,1,0)]}
    reserved=set(mech)|set(modblocks)|{lever}
    P=(ox-1,oy+1,oz); reserved.add(P)
    srcs={'A':r,'B':f,'T':P}
    used=set(); chain={'A':[],'B':[],'T':[]}; taps=[]
    def blocked(c):
        if c in reserved or tube(c) or c in used: return True
        if c[2]==0 and -1<=c[0]<=3 and -1<=c[1]<=3: return True
        return not (box[0]<=c[0]<=box[1] and box[2]<=c[1]<=box[3] and box[4]<=c[2]<=box[5])
    pist=[p for p,(b,pr) in mech.items() if 'piston' in b]
    FORB=set(pist)|{(p[0],p[1]+1,p[2]) for p in pist}
    def okback(prev,c):
        back=add(c,sub(c,prev))
        return not (back in FORB or back in mech or back in modblocks)
    DEAD=time.time()+TL
    def bfs_dist(tgt):
        dist={tgt:0};dq=deque([tgt])
        while dq:
            c=dq.popleft()
            for d in NB:
                n=add(c,d)
                if n in dist or blocked(n): continue
                dist[n]=dist[c]+1;dq.append(n)
        return dist
    def dfs(cur,tgt,L,dist):
        path=[];seen=set();BUD=[0]
        def rec(c,rem):
            BUD[0]+=1
            if BUD[0]>3000: return False
            nbs=list(NB); rnd.shuffle(nbs)
            for d in nbs:
                n=add(c,d)
                if n in seen: continue
                if n!=tgt and blocked(n): continue
                if not okback(c,n): continue
                if rem==1:
                    if n==tgt: path.append(n);return True
                    continue
                if n==tgt: continue
                if dist.get(n,10**9)>rem-1: continue
                seen.add(n);path.append(n)
                if rec(n,rem-1): return True
                path.pop();seen.discard(n)
            return False
        return list(path) if rec(cur,L) else None
    def cands(cur,tgt,minlen):
        if time.time()>DEAD: raise Exception('timeout')
        dist=bfs_dist(tgt)
        out=[];seenp=set()
        nd=[dist[add(cur,d)] for d in NB if add(cur,d) in dist]
        if not nd: return out
        sh=min(nd)+1
        for L in range(max(minlen,sh),max(minlen,sh)+6):
            for _ in range(4):
                p=dfs(cur,tgt,L,dist)
                if p and tuple(p) not in seenp:
                    seenp.add(tuple(p));out.append(p)
            if len(out)>=6: break
        return out
    if fixedT:
        Tcells=[(0,-2,-2),(1,-2,-2),(2,-2,-2),(3,-2,-2),(4,-2,-2),(4,-1,-2),(4,0,-2),(4,1,-2),(4,2,-2),(4,3,-2),(4,4,-2),(3,4,-2),(2,4,-2),(1,4,-2),(0,4,-2)]
        for c in Tcells: chain['T'].append(c); used.add(c)
        for (T_,dv_) in [((x,-2,-1),N) for x in (0,1,2)]+[((4,1,-1),N)]+[((x,4,-1),N) for x in (2,1,0)]:
            reserved.add(T_); taps.append(('T',T_,dv_,add(T_,dv_)))
    flat=[]
    for name in order:
        for k,al in enumerate(seqs[name]): flat.append((name,k,al))
    def rec(i,cur):
        if i==len(flat): return True
        name,k,al0=flat[i]
        if k==0: cur=srcs[name]
        al=list(al0); rnd.shuffle(al)
        for (T,dv) in al:
            Wc=add(T,dv)
            if T in reserved or T in used or Wc in reserved or Wc in used or blocked(Wc) or tube(T) or (T[2]==0 and -1<=T[0]<=3 and -1<=T[1]<=3): continue
            if not (box[0]<=T[0]<=box[1] and box[2]<=T[1]<=box[3] and box[4]<=T[2]<=box[5]): continue
            reserved.add(T)
            minlen=1 if (name=='T' or k==0) else MINSTEP
            for p in cands(cur,Wc,minlen):
                for c in p: chain[name].append(c); used.add(c)
                taps.append((name,T,dv,Wc))
                if rec(i+1,Wc): return True
                taps.pop()
                for c in p: chain[name].pop(); used.discard(c)
            reserved.discard(T)
        return False
    if not rec(0,None): raise Exception("plan fail")
    d=Design("open")
    for p,(b,pr) in mech.items(): d.set(*p,b,**pr)
    for p,(b,pr) in modblocks.items(): d.set(*p,b,**pr)
    d.set(*P,"observer",facing='east')
    for (ch,T,dv,Wc) in taps: d.set(*T,"observer",facing=DIRN[dv])
    for name in 'ABT':
        prev=srcs[name]
        for c in chain[name]:
            d.set(*c,"observer",facing=DIRN[sub(prev,c)]); prev=c
    return d,chain,taps
