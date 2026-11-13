import itertools
from abs import *
def ok(seq,start,goal):
    r=run([e for e in seq if e!='-'],start)
    return r is not None and key(r[0])==key(goal)
res=[]
for n in range(5,9):
    C=[s for s in itertools.product('ABV-',repeat=n) if ok(s,OPEN,CLOSED)]
    O=[s for s in itertools.product('ABV-',repeat=n) if ok(s,CLOSED,OPEN)]
    for c in C:
        for o in O:
            g=sum(1 for a,b in zip(c,o) if a!=b)
            res.append((g,n,c,o))
res.sort(key=lambda t:(t[0],t[1]))
for r in res[:12]: print(r)
