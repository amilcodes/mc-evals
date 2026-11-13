X0S = {}
EXTRA=[0]
exec(open("work/door.py").read())
class Coll(Exception): pass
OWN = {}
def put(d, x,y,z, b, owner, **p):
    key=(x,y,z)
    if key in d.blocks and (OWN.get(key) != owner or d.blocks[key][0] != b):
        raise Coll(f"collision at {key}: {d.blocks[key][0]} ({OWN.get(key)}) vs {b} ({owner})")
    if is_wall(x,y,z): raise Coll(f"wall at {key} ({owner})")
    d.set(x,y,z,b,**p); OWN[key]=owner

def build_chain2(times_obs, times_steady):
    req = sorted(set([(t,'obs') for t in times_obs] + [(t,'steady') for t in times_steady]))
    els=[]; t=0
    for tn,kind in req:
        g=tn-t
        if g==0:
            assert kind=='steady'; els.append(('stone',)); continue
        while g>8: els.append(('rep',4,'glass')); g-=8; t+=8
        els.append(('rep',g//2,'obs' if kind=='obs' else 'glass')); t=tn
        if kind=='steady': els.append(('stone',))
    return els

SPIRAL=[(0,0),(1,0),(1,1),(0,1)]
def lane2(d, k, obs, steady, xt, yt, fwd_to=1, owner=None):
    owner = owner or f"lane{k}"
    els = build_chain2(obs, steady)
    x = XS+1; outs=[]; stones=[]
    for e in els:
        if e[0]=='rep':
            put(d,x,12,k,"repeater",owner,facing="west",delay=e[1])
            if e[2]=='obs': put(d,x,11,k,"observer",owner,facing="up"); outs.append(x)
            else: put(d,x,11,k,"glass",owner)
        else:
            put(d,x,12,k,"stone",owner); stones.append(x); outs.append(x)
        x+=1
    lo, hi = min(outs), max(outs)
    for xx in range(lo, hi+1):
        if xx in stones:
            put(d,xx,11,k,WIRE,owner); put(d,xx,10,k,"stone",owner)
        else:
            put(d,xx,10,k,WIRE,owner); put(d,xx,9,k,"stone",owner)
    X0 = hi+2+EXTRA[0]
    while any(abs(X0 - v) < 3 for kk,v in X0S.items() if abs(kk-k)==2):
        X0 += 1
    X0S[k] = X0
    for xx in range(hi+1, X0-1):
        put(d,xx,10,k,WIRE,owner); put(d,xx,9,k,"stone",owner)
    put(d,X0-1,10,k,"repeater",owner,facing="west"); put(d,X0-1,9,k,"stone",owner)
    y=10; i=0
    while True:
        dx,dz = SPIRAL[i%4]
        put(d,X0+dx,y,k+dz,WIRE,owner); put(d,X0+dx,y-1,k+dz,"stone",owner)
        if y==yt: break
        y-=1; i+=1
    px, pz = X0+dx, k+dz
    step = -1 if xt < px else 1
    xx = px
    while xx != xt:
        xx += step
        put(d,xx,yt,pz,WIRE,owner)
        if not is_wall(xx,yt-1,pz): put(d,xx,yt-1,pz,"stone",owner)
    for j in range(pz-1, fwd_to-1, -1):
        if (xt,yt,j) in d.blocks and j==1: continue
        if (xt,yt,j) in d.blocks and OWN.get((xt,yt,j)) is None: continue
        put(d,xt,yt,j,"repeater",owner,facing="south")
        sup=(xt,yt-1,j)
        if sup not in d.blocks and not is_wall(*sup): put(d,*sup,"glass",owner)
    return pz

LAYERS = dict(SDLB=5, KLB=7, SDLT=9, R=11, SR=13, KLT=15)
def deltas():
    L=LAYERS
    # forward repeaters from pz (lane layer or +1) ... approximated with lane layer; spiral top +1
    return None

def left_lanes2(d, G):
    L=LAYERS
    def D(k, extra=0): return 2*(k-1) + 2 + 2*extra   # fwd reps (k-1) + spiral top rep
    # SD-LB: A [G+4,G+6) u [G+30,G+34); extra mech repeater 1
    dl = D(L['SDLB'],1); o=lambda a: a-dl
    lane2(d,L['SDLB'],[o(G+4)-2, o(G+30)-2, o(G+32)-2],[],-3,0)
    dl = D(L['KLB']); lane2(d,L['KLB'],[],[G+18-dl, G+24-dl],-1,-1)
    dl = D(L['SDLT']) - 2  # forward stops at z=2, then repeater (-2,2,1): same count
    dl = D(L['SDLT']); lane2(d,L['SDLT'],[G+4-dl-2, G+30-dl-2, G+32-dl-2],[],-3,2,fwd_to=2)
    dl = D(L['R']); lane2(d,L['R'],[G+a-dl-2 for a in range(0,14,2)]+[G+a-dl-2 for a in range(26,38,2)],[],-5,2)
    dl = D(L['SR']); lane2(d,L['SR'],[G+42-dl-2, G+44-dl-2],[G+20-dl],-2,4)
    dl = D(L['KLT']); lane2(d,L['KLT'],[],[G+18-dl, G+24-dl],-1,4)
