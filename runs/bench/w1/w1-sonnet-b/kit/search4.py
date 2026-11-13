from sim import *
import itertools,sys
def search(st0,alpha,maxlen,req):
    k0=key(st0)
    for L in range(1,maxlen+1):
        found=[]
        for S in itertools.product(alpha,repeat=L):
            c=run(st0,S)
            if all(p in c and c[p][0]=='s' for p in req):
                if key(run(c,S))==k0: found.append(''.join(S))
        print(L,len(found),found[:5],flush=True)
        if found: return found
st={}
for p in [(-1,0),(-1,1),(-1,2),(3,0),(3,1),(3,2)]: st[p]=('s',)
st[(-2,1)]=('p','L','E');st[(4,1)]=('p','R','W')
st[(-1,3)]=('p','A','S');st[(-1,-1)]=('p','B','N');st[(3,3)]=('p','C','S');st[(3,-1)]=('p','D','N')
search(st,['L','R','A','B','C','D'],8,[(0,1),(1,1),(2,1)])
