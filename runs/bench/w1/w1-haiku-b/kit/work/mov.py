# Relaxed 2D model where pistons are movable blocks too (retracted pistons can be pushed/pulled).
# state: frozenset of (cell, kind); kind 'S' stone, ('P',dir,sticky,ext) piston, ('H',dir) head
from collections import deque
DOOR = {(x,y) for x in range(3) for y in range(3)}
RING = {(x,-1) for x in range(3)} | {(x,3) for x in range(3)} | {(-1,y) for y in range(3)} | {(3,y) for y in range(3)}
DIRS = {'n':(0,-1),'s':(0,1),'e':(1,0),'w':(-1,0)}

def add(c,d,k=1): return (c[0]+k*DIRS[d][0], c[1]+k*DIRS[d][1])

def pistons_of(st):
    return [(c,k) for c,k in st if isinstance(k,tuple) and k[0]=='P']

def moves(st, inb):
    d = dict(st) if not isinstance(st, dict) else st
    out=[]
    for c,k in list(d.items()):
        if not (isinstance(k,tuple) and k[0]=='P'): continue
        _,dr,sticky,ext = k
        if not ext:
            F=add(c,dr)
            # extend: push chain of blocks (stones or retracted pistons) starting at F
            if F in d and not (isinstance(d[F],tuple) and d[F][0]=='H'):
                chain=[]; q=F
                while q in d and not (isinstance(d[q],tuple) and d[q][0] in ('H',)):
                    chain.append(q); q=add(q,dr)
                    if len(chain)>12: break
                # chain items must be stones or retracted pistons
                if any(isinstance(d[x],tuple) and d[x][0]=='P' and d[x][3] for x in chain): continue
                if len(chain)>12 or not inb(q) or q in d: continue
                nd=dict(d)
                for x in chain: del nd[x]
                for x in chain: nd[add(x,dr)] = d[x]
                nd[c]=('P',dr,sticky,True); nd[F]=('H',dr)
                out.append(nd)
            else:
                if F in d or not inb(F): continue
                nd=dict(d); nd[c]=('P',dr,sticky,True); nd[F]=('H',dr)
                out.append(nd)
        else:
            F=add(c,dr); B=add(c,dr,2)
            nd=dict(d); del nd[F]; nd[c]=('P',dr,sticky,False)
            if sticky and B in nd and not (isinstance(nd[B],tuple) and nd[B][0] in ('H','P') and nd[B][0]=='H'):
                if not (isinstance(nd[B],tuple) and nd[B][0]=='P' and nd[B][3]):
                    nd[F]=nd.pop(B)
            out.append(nd)
    return out

def tofs(nd): return frozenset(nd.items())
def todict(fs): return dict(fs)

def bfs(start, goal, inb, limit=3000):
    seen={start:None}; q=deque([start]); n=0
    while q and n<limit:
        s=q.popleft(); n+=1
        if goal(s): return s,n
        for nd in moves(todict(s), inb):
            f=tofs(nd)
            if f in seen: continue
            seen[f]=1; q.append(f)
    return None,n

def reach_score(pist, spares, box, limit=3000):
    (x0,x1),(y0,y1)=box
    inb=lambda c: x0<=c[0]<=x1 and y0<=c[1]<=y1
    st={}
    for c in DOOR: st[c]='S'
    for c in spares: st[c]='S'
    for c,dr,sticky in pist: st[c]=('P',dr,sticky,False)
    if len(st)!=9+len(spares)+len(pist): return -1,0
    S0=tofs(st)
    seen={S0}; q=deque([S0]); best=-1; n=0
    while q and n<limit:
        s=q.popleft(); n+=1
        dd=todict(s)
        stones={c for c,k in s if k=='S'}
        pistc={c for c,k in s if isinstance(k,tuple) and k[0]=='P'}
        sc=(9-len(DOOR&stones))+len(RING&stones)
        if sc>best: best=sc
        for nd in moves(dd,inb):
            f=tofs(nd)
            if f in seen: continue
            seen.add(f); q.append(f)
    return best, n
