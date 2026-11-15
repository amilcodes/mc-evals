from sim import *
import itertools
w0={(-3,0):('P','E','P1'),(-2,0):('P','E','P2'),(-1,0):('S',),(-1,1):('S',),(-1,2):('P','S','V')}
pist=['P1','P2','V']
def closed(w): return all(w.get((x,0))==('S',) for x in (0,1)) and all(w.get((x,0)) is None for x in (2,3))
for n in range(1,11):
    c=0
    for seq in itertools.product(pist,repeat=n):
        w1=run(w0,seq)
        if not closed(w1): continue
        w2=run(w1,seq)
        if w2==w0: print(n,seq); c+=1
    if c: break
