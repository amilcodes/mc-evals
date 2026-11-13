import random, sys, time
from mov import reach_score, DOOR, RING
def cells_of(box):
    (x0,x1),(y0,y1)=box
    return [(x,y) for x in range(x0,x1+1) for y in range(y0,y1+1) if (x,y) not in DOOR]
if __name__=="__main__":
    seed=int(sys.argv[1]); K=int(sys.argv[2]); S=int(sys.argv[3]); iters=int(sys.argv[4]); lo,hi=int(sys.argv[5]),int(sys.argv[6])
    box=((lo,hi),(lo,hi))
    random.seed(seed)
    cells=cells_of(box)
    def valid(p,s):
        allc=[c for c,_,_ in p]+list(s)
        return len(set(allc))==len(allc)
    def val(p,s):
        if not valid(p,s): return -1,0
        return reach_score(p,s,box,limit=800)
    pist=[(random.choice(cells), random.choice('nsew'), random.random()<0.5) for _ in range(K)]
    spares=random.sample(cells,S)
    cur=val(pist,spares)[0]; best=(cur,list(pist),list(spares)); T=2.0; t0=time.time()
    for it in range(iters):
        p2=list(pist); s2=list(spares)
        if random.random()<0.6:
            i=random.randrange(K); c,d,st=p2[i]; m=random.random()
            if m<0.4: c=random.choice(cells)
            elif m<0.7: d=random.choice('nsew')
            else: st=not st
            p2[i]=(c,d,st)
        else:
            i=random.randrange(S); s2[i]=random.choice(cells)
        v=val(p2,s2)[0]
        if v>=cur or random.random()<pow(2.718,(v-cur)/max(T,0.05)):
            pist,spares,cur=p2,s2,v
            if cur>best[0]: best=(cur,list(pist),list(spares))
        T=max(0.05,T*0.9995)
        if best[0]==21: break
    print(seed,K,S,box,best[0],best[1],best[2],round(time.time()-t0,1),flush=True)
