import itertools
D={'U':(0,1),'E':(1,0),'W':(-1,0),'N':(0,-1)}
def add(p,d): return (p[0]+d[0],p[1]+d[1])
# world: dict pos -> ('stone',name) | ('pis',name) | ('head',name) | ('static',)
# pistons: name -> dict(facing, sticky, ext) ; positions tracked by world
def find(w,name):
    for p,v in w.items():
        if v[0]=='pis' and v[1]==name: return p
def push(w,start,d,forbid):
    chain=[];p=start
    while p in w:
        v=w[p]
        if v[0] in ('static','head'): return False
        if v[0]=='pis' and ext[v[1]]: return False
        chain.append(p);p=add(p,d)
        if len(chain)>12: return False
    if p in forbid: return False
    for q in reversed(chain): w[add(q,d)]=w.pop(q)
    return True
def act(w,ext_,name,kind,forbid,facing):
    global ext
    ext=ext_
    p=find(w,name); d=D[facing[name]]; f=add(p,d)
    if kind=='pulse':
        if ext[name]: return False
        if f in w:
            return push(w,f,d,forbid)
        g=add(f,d)
        if g in w and w[g][0] in ('stone','pis') and not (w[g][0]=='pis' and ext[w[g][1]]):
            w[f]=w.pop(g)
        return True
    if kind=='ext':
        if ext[name]: return True
        if f in w:
            if not push(w,f,d,forbid): return False
        w[f]=('head',name); ext[name]=True; return True
    if kind=='ret':
        if not ext[name]: return True
        del w[f]; ext[name]=False
        g=add(f,d)
        if g in w and w[g][0] in ('stone','pis') and not (w[g][0]=='pis' and ext[w[g][1]]):
            w[f]=w.pop(g)
        return True
facing={'B':'U','B2':'U','K':'E'}
pos0={'B':(1,-2),'B2':(1,-3),'K':(-1,-1)}
forbid_close={(1,2)}; forbid_open={(1,2),(1,3)}
def build(extc):
    w={(2,-1):('static',),(1,0):('stone','S1'),(1,1):('stone','S2')}
    ext={}
    for n,p in pos0.items():
        w[p]=('pis',n); ext[n]=False
    for n in extc:
        f=add(pos0[n],D[facing[n]])
        if f in w: return None
        w[f]=('head',n); ext[n]=True
    return w,ext
def isopen(w):
    return (1,0) not in w and (1,1) not in w and w.get((1,-1),('',))[0]=='stone' and w.get((0,-1),('',))[0]=='stone'
def isclosed(w):
    return w.get((1,0),('',))[0]=='stone' and w.get((1,1),('',))[0]=='stone'
names=['B','B2','K']
found=[]
for modes in itertools.product(['pulse','sc','so'],repeat=3):  # sc: extended when closed; so: extended when open
    md=dict(zip(names,modes))
    statep=[n for n in names if md[n]!='pulse']
    pulsep=[n for n in names if md[n]=='pulse']
    extc=[n for n in names if md[n]=='sc']
    exto=[n for n in names if md[n]=='so']
    for n in range(1,8):
        # sequence: slots containing pulses (any pulsed piston) and each state piston exactly once
        for seq in itertools.product(pulsep+['S:'+s for s in statep],repeat=n):
            if any(seq.count('S:'+s)!=1 for s in statep): continue
            ok=True
            for start_closed in (True,):
                b=build(extc)
                if b is None: ok=False;break
                w,e=b; w=dict(w); e=dict(e)
                # open
                for a in seq:
                    if a.startswith('S:'):
                        nm=a[2:]; kind='ret' if md[nm]=='sc' else 'ext'
                    else: nm=a;kind='pulse'
                    if not act(w,e,nm,kind,forbid_open,facing): ok=False;break
                if not ok or not isopen(w): ok=False;break
                for a in seq:
                    if a.startswith('S:'):
                        nm=a[2:]; kind='ext' if md[nm]=='sc' else 'ret'
                    else: nm=a;kind='pulse'
                    if not act(w,e,nm,kind,forbid_close,facing): ok=False;break
                if not ok: break
                b2=build(extc)
                if sorted(w.items())!=sorted(b2[0].items()) or e!=b2[1]: ok=False
            if ok: found.append((md,seq))
        if any(f[0]==md for f in found): break
for f in found[:40]: print(f)
print(len(found))
