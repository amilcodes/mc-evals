from b1 import *
from collections import deque
def allpaths(w0,names,maxlen):
    # BFS shortest path to every state
    q=deque([(w0,())]); seen={key(w0):()}
    out=[]
    while q:
        w,p=q.popleft()
        if len(p)>=maxlen: continue
        for n in names:
            w2=pulse(w,n); k=key(w2)
            if k in seen: continue
            seen[k]=p+(n,); q.append((w2,p+(n,)))
    return seen
def run(base,stones,cells=(0,1)):
    w0=mk(base,stones); names=[b[2] for b in base]
    cl=lambda w: all(w.get((x,0))==('S',) for x in cells) and all(w.get((x,0)) is None for x in range(0,4) if x not in cells)
    fw=allpaths(w0,names,12)
    best=[]
    for k,p in fw.items():
        w={a:b for a,b in k}
        if not cl(w): continue
        # shortest return
        bw=allpaths(w,names,12)
        kk=key(w0)
        if kk in bw: best.append((max(len(p),len(bw[kk])),len(p),len(bw[kk]),p,bw[kk]))
    best.sort(key=lambda t:(t[0],t[1]+t[2]))
    return best[:6]
for b in run([((-3,0),'E','P1'),((-2,0),'E','P2'),((-1,2),'S','V1')],[(-1,0),(-1,1)]): print(b)
