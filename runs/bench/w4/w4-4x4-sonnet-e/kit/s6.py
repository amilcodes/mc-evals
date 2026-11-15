from sim import *
import itertools
home={'P1':(-3,0),'P2':(-2,0),'V1':(-1,2),'V2':(-1,-2)}
def pulse2(w,name):
    pos=[p for p,b in w.items() if b[0]=='P' and b[2]==name][0]
    if pos!=home[name]: return w
    return pulse(w,name)
def run2(w,seq):
    for n in seq: w=pulse2(w,n)
    return w
def closed(w): return all(w.get((x,0))==('S',) for x in (0,1)) and all(w.get((x,0)) is None for x in (2,3))
def mk(base,stones):
    w0={}
    for p,d,n in base: w0[p]=('P',d,n)
    for s in stones: w0[s]=('S',)
    return w0
def search(base,stones,maxc=7,maxo=8):
    w0=mk(base,stones); names=[b[2] for b in base]
    cl=[]
    for n in range(1,maxc+1):
        for seq in itertools.product(names,repeat=n):
            w1=run2(w0,seq)
            if closed(w1): cl.append((seq,w1))
    print('closing seqs',len(cl))
    best=None
    for seq,w1 in cl:
        for n in range(1,maxo+1):
            for sq in itertools.product(names,repeat=n):
                if run2(w1,sq)==w0:
                    tot=len(seq)+len(sq)
                    if best is None or tot<best[0]: best=(tot,seq,sq); print(best)
                    break
    return best
print(search([((-3,0),'E','P1'),((-2,0),'E','P2'),((-1,2),'S','V1')],[(-1,0),(-1,1)],7,8))
