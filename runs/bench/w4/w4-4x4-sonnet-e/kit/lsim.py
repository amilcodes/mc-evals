import itertools
D={'E':(1,0),'W':(-1,0),'N':(0,1),'S':(0,-1)}
# world: dict pos -> ('S',) stone | ('P',dir,sticky,name,ext) | ('H',name)
def add(p,d,k=1): return (p[0]+d[0]*k,p[1]+d[1]*k)
def find(w,name):
    for p,b in w.items():
        if b[0]=='P' and b[3]==name: return p
def movable(b): 
    if b[0]=='S': return True
    if b[0]=='P': return not b[4]
    return False
def setp(w,name,on):
    w=dict(w); pos=find(w,name); b=w[pos]
    if b[4]==on: return w
    d=D[b[1]]; h=add(pos,d)
    if on:
        if h in w:
            chain=[];c=h
            while c in w:
                if not movable(w[c]) or len(chain)>=12: return w
                chain.append(c); c=add(c,d)
            for c in reversed(chain):
                w[add(c,d)]=w.pop(c)
        w[h]=('H',name); w[pos]=b[:4]+(True,)
    else:
        w.pop(h,None); w[pos]=b[:4]+(False,)
        if b[2]:
            t=add(h,d)
            if t in w and movable(w[t]): w[h]=w.pop(t)
    return w
