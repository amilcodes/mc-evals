import itertools
from abs import *
def seqvalid(seq,start,goal):
    r=run([e for e in seq if e!='-'],start)
    return r is not None and key(r[0])==key(goal)
best=[]
for n in range(3,10):
    for beta in itertools.product([0,1],repeat=n):
        nb=[i for i in range(n) if not beta[i]]
        if sum(beta)==0: continue
        # direction-specific options in non-beta slots
        def cands(start,goal):
            res=[]
            for choice in itertools.product('AV-',repeat=len(nb)):
                seq=['B']*n
                for i,c in zip(nb,choice): seq[i]=c
                if seqvalid(seq,start,goal): res.append(tuple(seq))
            return res
        c=cands(OPEN,CLOSED)
        if not c: continue
        o=cands(CLOSED,OPEN)
        if not o: continue
        best.append((n,sum(beta),beta,c[0],o[0]))
best.sort(key=lambda t:(t[0],-t[1]))
for b in best[:15]: print(b)
print(len(best))
