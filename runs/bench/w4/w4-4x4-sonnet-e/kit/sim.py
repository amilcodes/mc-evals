import itertools
D={'E':(1,0),'W':(-1,0),'N':(0,1),'S':(0,-1)}
def pulse(w,name):
    w=dict(w); pos=[p for p,b in w.items() if b[0]=='P' and b[2]==name][0]; b=w[pos]
    d=D[b[1]]; h=(pos[0]+d[0],pos[1]+d[1])
    if h in w:
        chain=[];c=h
        while c in w:
            chain.append(c); c=(c[0]+d[0],c[1]+d[1])
            if len(chain)>12: return w
        if w[chain[-1]][0]=='O': return w
        for c in chain:
            if w[c][0]=='O': return w
        for c in reversed(chain):
            n=(c[0]+d[0],c[1]+d[1]); w[n]=w.pop(c)
        return w
    else:
        t=(h[0]+d[0],h[1]+d[1])
        if t in w and w[t][0]!='O':
            w[h]=w.pop(t)
        return w
def run(w,seq):
    for p in seq: w=pulse(w,p)
    return w
