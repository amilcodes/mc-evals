import itertools
exec(open('search.py').read().split("s0=")[0])
exec(open('search3.py').read().split("ACT={}")[0].split("exec(open('search.py').read().split(\"s0=\")[0])")[1])
def ext_ret_P(st):
    # M_P = P long with B domino: ExtP, ShortB (delayed), RetP, ShortB
    pos=[p for p,v in st.items() if v[0]=='P'][0]
    d=D[st[pos][2]]; head=(pos[0]+d[0],pos[1]+d[1])
    nb=st
    if head in st:
        nb=push_chain(st,head,d)
        if nb is None: return None
    # head extended: B (moved) pulse
    nb=pulse2(nb,'B')
    if nb is None: return None
    # retract: pull head+1 block into head cell
    far=(head[0]+d[0],head[1]+d[1])
    if far in nb and nb.get(far)[0]!='H':
        nb=dict(nb); v=nb.pop(far); nb[head]=v
    nb=pulse2(nb,'B')
    return nb
def run(state,seq):
    st=dict(state)
    for a in seq:
        if a=='M': st=ext_ret_P(st)
        elif a=='b': st=pulse2(st,'B')
        elif a=='a': st=pulse2(st,'A')
        elif a=='p': st=pulse2(st,'P')
        if st is None: return None
    return st
def stones(st): return {p for p,v in st.items() if v[1]=='stone'}
def isclosed(st):
    s=stones(st); return {(0,1),(1,1)}<=s and not any(p in s for p in [(-1,1),(-1,0)])
def isopen(st):
    s=stones(st); return {(-1,1)}<=s and not any(p[0]>=0 for p in s)
s0={(-3,1):('P','sp','e'),(-2,1):('B','sp','e'),(-1,1):('S','stone',None),(-1,0):('G','stone',None),(-1,-1):('A','sp','u')}
for L in range(1,9):
    res=[]
    for T in itertools.product('Mbap',repeat=L):
        cur=s0; ok=True
        for k in range(4):
            cur=run(cur,T)
            if cur is None: ok=False;break
            if k%2==0 and not isclosed(cur): ok=False;break
            if k%2==1 and not isopen(cur): ok=False;break
        if ok: res.append(''.join(T))
    print(L,len(res),res[:10])
    if res: break
