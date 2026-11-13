import random, sys, time
from sa_bfs import best_reach, allowed
if __name__=="__main__":
    seed=int(sys.argv[1]); K=int(sys.argv[2]); S=int(sys.argv[3]); iters=int(sys.argv[4])
    lo,hi=int(sys.argv[5]),int(sys.argv[6])
    box=((lo,hi),(lo,hi))
    import sa_bfs
    random.seed(seed)
    cells=allowed(box)
    pist=[(random.choice(cells), random.choice('nsew'), random.random()<0.5) for _ in range(K)]
    spares=random.sample(cells,S)
    def val(p,s):
        if len({c for c,_,_ in p})<len(p) or len(set(s))<len(s) or set(s)&{c for c,_,_ in p}: return -1,None
        b=best_reach(p,s,box,limit=3000)
        return b[0], b
    cur,_=val(pist,spares); best=(cur,list(pist),list(spares))
    T=2.0; t0=time.time()
    for it in range(iters):
        p2=list(pist); s2=list(spares)
        if random.random()<0.5:
            i=random.randrange(K); c,d,st=p2[i]; m=random.random()
            if m<0.4: c=random.choice(cells)
            elif m<0.7: d=random.choice('nsew')
            else: st=not st
            p2[i]=(c,d,st)
        else:
            i=random.randrange(S); s2[i]=random.choice(cells)
        v,_=val(p2,s2)
        if v>=cur or random.random()<pow(2.718,(v-cur)/max(T,0.05)):
            pist,spares,cur=p2,s2,v
            if cur>best[0]: best=(cur,list(pist),list(spares))
        T=max(0.05,T*0.9993)
    print(seed,K,S,box,best[0],best[1],best[2],round(time.time()-t0,1),flush=True)
