from sim import *
import itertools
def closed(w): return all(w.get((x,0))==('S',) for x in (0,1)) and all(w.get((x,0)) is None for x in (2,3))
def srch(base,stones,maxn=8,name=''):
    w0={}
    for p,d,n in base: w0[p]=('P',d,n)
    for s in stones: w0[s]=('S',)
    names=[b[2] for b in base]
    for n in range(1,maxn+1):
        c=0
        for seq in itertools.product(names,repeat=n):
            w1=run(w0,seq)
            if not closed(w1): continue
            if run(w1,seq)==w0: print(name,n,seq); c+=1
            if c>3: break
        if c: return
    print(name,'none')
srch([((-3,0),'E','P1'),((-2,0),'E','P2'),((-1,2),'S','V1'),((-1,-2),'N','V2')],[(-1,0),(-1,1),(-1,-1)],8,'A')
srch([((-3,0),'E','P1'),((-2,0),'E','P2'),((-1,2),'S','V1'),((-1,-2),'N','V2')],[(-1,0),(-1,1)],8,'B')
srch([((-3,0),'E','P1'),((-2,0),'E','P2'),((0,2),'S','V1')],[(-1,0),(0,1)],8,'C')
srch([((-3,0),'E','P1'),((-2,0),'E','P2'),((-1,2),'S','V1'),((-3,2),'E','V3')],[(-1,0),(-1,1)],8,'D')
