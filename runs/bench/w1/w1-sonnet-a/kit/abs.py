import itertools, sys
# abstract model. blocks: dict pos->name. fixed: A body (-3,1) 'A', V body (-1,3) 'V', e0 (-1,0) 'e', static door stones optionally.
def push(blocks, start, d):
    """push chain starting at cell start in direction d. returns new blocks or None if blocked"""
    chain=[]; p=start
    while p in blocks:
        if blocks[p] in ('A','V'): return None  # immovable bodies
        chain.append(p); p=(p[0]+d[0],p[1]+d[1])
        if len(chain)>12: return None
    if p in LIMITS: return None
    nb=dict(blocks)
    for q in chain: del nb[q]
    for q in chain: nb[(q[0]+d[0],q[1]+d[1])]=blocks[q]
    return nb
LIMITS=set()
def sticky(blocks, body, d, bodyname=None):
    """short pulse of sticky piston with body at body facing d. returns (newblocks, kind) kind in 'push','pull','noop' or None if blocked"""
    h=(body[0]+d[0],body[1]+d[1])
    if h in blocks:
        nb=push(blocks,h,d)
        if nb is None: return None,'blocked'
        return nb,'push'
    f=(h[0]+d[0],h[1]+d[1])
    if f in blocks and blocks[f] not in ('A','V'):
        nb=dict(blocks); b=nb.pop(f); nb[h]=b
        return nb,'pull'
    return blocks,'noop'
def pulse(blocks, el):
    if el=='A': return sticky(blocks,(-3,1),(1,0))
    if el=='V': return sticky(blocks,(-1,3),(0,-1))
    if el=='B':
        bp=[p for p,n in blocks.items() if n=='B'][0]
        # B moves with the structure
        return sticky(blocks,bp,(1,0))
def mk(S,X,Bp,extra=()):
    b={(-3,1):'A',(-1,3):'V',(-1,0):'e',Bp:'B'}
    b[S]='S'; b[X]='X'
    for e in extra: b[e]='Y'
    return b
OPEN=mk((-1,1),(-1,2),(-2,1))
CLOSED=mk((1,1),(0,1),(-2,1))
def key(b): return tuple(sorted(b.items()))
def run(seq,b):
    cur=b; log=[]
    for el in seq:
        nb,k=pulse(cur,el)
        if nb is None: return None
        log.append((el,k)); cur=nb
    return cur,log
if __name__=="__main__":
    L=int(sys.argv[1])
    sols=[]
    for n in range(1,L+1):
        for seq in itertools.product('ABV',repeat=n):
            r1=run(seq,OPEN)
            if not r1 or key(r1[0])!=key(CLOSED): continue
            r2=run(seq,CLOSED)
            if not r2 or key(r2[0])!=key(OPEN): continue
            sols.append((seq,r1[1],r2[1]))
    for s in sols[:20]: print(s)
    print(len(sols))
