import itertools
D={'e':(1,0),'w':(-1,0),'u':(0,1),'d':(0,-1)}
def push_chain(blocks, start, d):
    chain=[]; p=start
    while p in blocks:
        chain.append(p); p=(p[0]+d[0],p[1]+d[1])
        if len(chain)>12: return None
    new=dict(blocks)
    items=[(q,blocks[q]) for q in chain]
    for q,_ in items: del new[q]
    for q,v in items: new[(q[0]+d[0],q[1]+d[1])]=v
    return new
def pulse2(blocks,n):
    pos=[p for p,v in blocks.items() if v[0]==n][0]
    d=D[blocks[pos][2]]
    head=(pos[0]+d[0],pos[1]+d[1])
    if head in blocks:
        return push_chain(blocks, head, d)
    far=(head[0]+d[0],head[1]+d[1])
    if far in blocks:
        nb=dict(blocks); v=nb.pop(far); nb[head]=v; return nb
    return blocks
s0={(-3,1):('P','sp','e'),(-2,1):('B','sp','e'),(-1,1):('S','stone',None),(-1,2):('G','stone',None),(-1,3):('A','sp','d')}
def run(state, seq):
    st=dict(state)
    for n in seq:
        st=pulse2(st,n)
        if st is None: return None
    return st
def closed(st):
    d={v[0]:p for p,v in st.items()}
    return d.get('S')==(1,1) and d.get('G')==(0,1)
res=[]
for L in range(1,10):
    for T in itertools.product('PBA',repeat=L):
        a=run(s0,T)
        if a is None or not closed(a): continue
        b=run(a,T)
        if b is None: continue
        if b==s0: res.append(T)
    if res: print(L,[''.join(t) for t in res[:20]]); break
print('done',len(res))
def stones(st): return {p for p,v in st.items() if v[1]=='stone'}
def isclosed(st):
    s=stones(st); return {(0,1),(1,1)}<=s and not any(p in s for p in [(-1,1),(-1,2)])
def isopen(st):
    s=stones(st); return {(-1,1),(-1,2)}<=s and not any(p[0]>=0 for p in s)
res=[]
for L in range(1,11):
    for T in itertools.product('PBA',repeat=L):
        cur=s0; ok=True
        for k in range(4):
            cur=run(cur,T)
            if cur is None: ok=False;break
            if k%2==0 and not isclosed(cur): ok=False;break
            if k%2==1 and not isopen(cur): ok=False;break
        if ok: res.append(''.join(T))
    if res: print(L,res[:30]); break
print('done2')
