from reach import *
st={}
for p in [(-1,0),(-1,1),(-1,2),(3,0),(3,1),(3,2)]: st[p]=('s',)
st[(-2,1)]=('p','L','E');st[(4,1)]=('p','R','W')
st[(-1,3)]=('p','A','S');st[(-1,-1)]=('p','B','N');st[(3,3)]=('p','C','S');st[(3,-1)]=('p','D','N')
alpha=['L','R','A','B','C','D']
seen,keys,hits=bfs(st,alpha,[(0,1),(1,1),(2,1)])
k0=key(st)
# for each closed state hit, BFS back to open
import collections
best=None
for h in hits[:700]:
    s0=keys[h]
    seen2,keys2,_=bfs(s0,alpha,[(99,99)],maxstates=50000)
    if k0 in seen2:
        p=path(seen2,k0)
        if best is None or len(p)<len(best[1]): best=(path(seen,h),p)
        print(path(seen,h),'->',p,flush=True)
        break
print(best)
