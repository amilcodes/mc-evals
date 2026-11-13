from sim import *
from collections import deque
def bfs(st0,alpha,req,maxstates=300000):
    k0=key(st0);seen={k0:(None,None)};dq=deque([st0]);keys={k0:st0}
    hits=[]
    while dq:
        s=dq.popleft();ks=key(s)
        if all(p in s and s[p][0]=='s' for p in req):
            hits.append(ks)
        if len(seen)>maxstates: break
        for a in alpha:
            t=pulse(s,a);kt=key(t)
            if kt not in seen:
                seen[kt]=(ks,a);keys[kt]=t;dq.append(t)
    return seen,keys,hits
def path(seen,k):
    out=[]
    while seen[k][0] is not None:
        out.append(seen[k][1]);k=seen[k][0]
    return ''.join(reversed(out))
if __name__=="__main__":
    st={}
    for p in [(-1,0),(-1,1),(-1,2),(3,0),(3,1),(3,2)]: st[p]=('s',)
    st[(-2,1)]=('p','L','E');st[(4,1)]=('p','R','W')
    st[(-1,3)]=('p','A','S');st[(-1,-1)]=('p','B','N');st[(3,3)]=('p','C','S');st[(3,-1)]=('p','D','N')
    seen,keys,hits=bfs(st,['L','R','A','B','C','D'],[(0,1),(1,1),(2,1)])
    print(len(seen),len(hits))
    if hits: print(path(seen,hits[0]))
