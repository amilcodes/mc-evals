import itertools, sys
DIRS={'E':(1,0),'W':(-1,0),'N':(0,1),'S':(0,-1)}
# state: dict pos -> ('s',) stone, ('w',) wall, ('p',id,dir)
def find(st,pid):
    for p,b in st.items():
        if b[0]=='p' and b[1]==pid: return p
def pulse(st,pid):
    st=dict(st)
    p=find(st,pid); d=DIRS[st[p][2]]
    head=(p[0]+d[0],p[1]+d[1])
    if head in st:
        # push chain
        chain=[];c=head
        while c in st:
            if st[c][0]=='w': return st
            chain.append(c); c=(c[0]+d[0],c[1]+d[1])
            if len(chain)>12: return st
        if c in WALLCELLS: return st
        for c in reversed(chain):
            st[(c[0]+d[0],c[1]+d[1])]=st.pop(c)
        return st
    else:
        beyond=(head[0]+d[0],head[1]+d[1])
        if beyond in st and st[beyond][0]!='w':
            st[head]=st.pop(beyond)
        return st
WALLCELLS=set()
def key(st): return frozenset(st.items())
def run(st,seq):
    for s in seq: st=pulse(st,s)
    return st
