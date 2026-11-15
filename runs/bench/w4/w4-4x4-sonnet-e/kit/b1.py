from sim import *
from collections import deque
def key(w): return tuple(sorted((k,v) for k,v in w.items()))
def bfs(w0,names,goal,maxn=200000):
    q=deque([(w0,())]); seen={key(w0)}; res=[]
    while q:
        w,path=q.popleft()
        if goal(w) and path: res.append((path,w)); 
        if len(res)>=1: return res
        for n in names:
            w2=pulse(w,n)
            k=key(w2)
            if k in seen: continue
            seen.add(k); q.append((w2,path+(n,)))
        if len(seen)>maxn: break
    return res
def mk(base,stones):
    w0={}
    for p,d,n in base: w0[p]=('P',d,n)
    for s in stones: w0[s]=('S',)
    return w0
def analyze(base,stones,cells,label):
    w0=mk(base,stones); names=[b[2] for b in base]
    cl=lambda w: all(w.get((x,0))==('S',) for x in cells) and all(w.get((x,0)) is None for x in range(0,4) if x not in cells)
    r=bfs(w0,names,cl)
    if not r: print(label,'no closing'); return
    path,w1=r[0]
    r2=bfs(w1,names,lambda w: key(w)==key(w0))
    print(label,'close',len(path),path,'open',len(r2[0][0]) if r2 else None, r2[0][0] if r2 else None)
analyze([((-3,0),'E','P1'),((-2,0),'E','P2'),((-1,2),'S','V1')],[(-1,0),(-1,1)],(0,1),'2deep')
analyze([((-4,0),'E','P1'),((-3,0),'E','P2'),((-2,0),'E','P3'),((-1,2),'S','V1'),((-1,-2),'N','V2')],[(-1,0),(-1,1),(-1,-1)],(0,1,2),'3deep')
