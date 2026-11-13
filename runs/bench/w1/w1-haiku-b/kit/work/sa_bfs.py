import random, sys, time
from collections import deque
from bfs2d import DOOR, RING, DIRS, toggle, make_env

def best_reach(pist, spares, box, limit=3000):
    inb = make_env(box)
    ef0 = tuple(False for _ in pist)
    S0 = (frozenset(DOOR|set(spares)), ef0)
    seen = {S0}; q=deque([S0]); best=-1; bestS=None; n=0
    while q and n < limit:
        s=q.popleft(); n+=1
        sc = (9-len(DOOR & s[0])) + len(RING & s[0])
        if sc>best: best=sc; bestS=s
        for i in range(len(pist)):
            r = toggle(s[0], s[1], pist, i, inb)
            if r is None or r in seen: continue
            seen.add(r); q.append(r)
    return best, bestS, n

def allowed(box):
    (x0,x1),(y0,y1)=box
    return [(x,y) for x in range(x0,x1+1) for y in range(y0,y1+1) if (x,y) not in DOOR and (x,y) not in RING]

def run(seed, box, K, iters, S=3):
    random.seed(seed)
    cells = allowed(box)
    pist=[(random.choice(cells), random.choice('nsew'), random.random()<0.5) for _ in range(K)]
    spares=random.sample(cells, S)
    def val(p,s):
        if len({c for c,_,_ in p})<len(p) or set(s)&{c for c,_,_ in p}: return -1, None
        return best_reach(p,s,box)[0], None
    cur,_=val(pist,spares); bestv=(cur,list(pist),list(spares))
    T=2.0
    for it in range(iters):
        p2=list(pist); s2=list(spares)
        r=random.random()
        if r<0.5:
            i=random.randrange(K); c,d,st=p2[i]
            m=random.random()
            if m<0.4: c=random.choice(cells)
            elif m<0.7: d=random.choice('nsew')
            else: st=not st
            p2[i]=(c,d,st)
        else:
            i=random.randrange(S); s2[i]=random.choice(cells)
        v,_=val(p2,s2)
        if v>=cur or random.random()<pow(2.718,(v-cur)/max(T,0.05)):
            pist,spares,cur=p2,s2,v
            if cur>bestv[0]: bestv=(cur,list(pist),list(spares))
        T=max(0.05,T*0.999)
    return bestv

if __name__=="__main__":
    seed=int(sys.argv[1]); K=int(sys.argv[2]); iters=int(sys.argv[3])
    box=((-2,3),(-2,3))
    t0=time.time()
    b=run(seed,box,K,iters)
    print(seed,K,b[0],b[1],b[2],round(time.time()-t0,1),flush=True)
