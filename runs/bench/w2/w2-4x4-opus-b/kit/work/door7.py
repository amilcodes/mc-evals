exec(open("work/door6.py").read())
NREP = {}
RCL=[14]
FLIP=set()
CR = 12
def lane7(d, k, obs, steady, xt, yt, fwd_to=1, owner=None, west=False):
    s = 1 if k > 0 else -1
    owner = owner or f"lane{k}"
    els = build_chain2(obs, steady)
    x = XS+1; outs=[]; stones=[]
    for e in els:
        if e[0]=='rep':
            put(d,x,CR,k,"repeater",owner,facing="west",delay=e[1])
            if e[2]=='obs': put(d,x,CR-1,k,"observer",owner,facing="up"); outs.append(x)
            else: put(d,x,CR-1,k,"glass",owner)
        else:
            put(d,x,CR,k,"stone",owner); stones.append(x); outs.append(x)
        x+=1
    lo, hi = min(outs), max(outs)
    for xx in range(lo, hi+1):
        if xx in stones: put(d,xx,CR-1,k,WIRE,owner); put(d,xx,CR-2,k,"stone",owner)
        else:
            put(d,xx,CR-2,k,WIRE,owner)
            if not is_wall(xx,CR-3,k): put(d,xx,CR-3,k,"stone",owner)
    nrep = 1
    if not west:
        X0 = hi+2+EXTRA[0]
        for xx in range(hi+1, X0-1):
            put(d,xx,CR-2,k,WIRE,owner); put(d,xx,CR-3,k,"stone",owner)
        put(d,X0-1,CR-2,k,"repeater",owner,facing="west"); put(d,X0-1,CR-3,k,"stone",owner)
        sd = -s if k in FLIP else s
        pat=[(0,0),(1,0),(1,sd),(0,sd)]
    else:
        X0 = lo-2
        if X0-1 < XS: raise Coll("west spiral outside spine")
        put(d,X0+1,CR-2,k,"repeater",owner,facing="east"); put(d,X0+1,CR-3,k,"stone",owner)
        sd = -s if k in FLIP else s
        pat=[(0,0),(-1,0),(-1,sd),(0,sd)]
    y=CR-2; i=0
    while True:
        dx,dz = pat[i%4]
        put(d,X0+dx,y,k+dz,WIRE,owner)
        if not is_wall(X0+dx,y-1,k+dz): put(d,X0+dx,y-1,k+dz,"stone",owner)
        if y==yt: break
        y-=1; i+=1
    px, pz = X0+dx, k+dz
    step = -1 if xt < px else 1
    xx = px; n=0; strength = 15 - (CR-2-yt)
    while xx != xt:
        xx += step; n+=1; strength -= 1
        if strength <= 1 and abs(xt-xx) >= 1:
            put(d,xx,yt,pz,"repeater",owner,facing=("west" if step==1 else "east")); nrep += 1; strength = 16
        else:
            put(d,xx,yt,pz,WIRE,owner)
        if not is_wall(xx,yt-1,pz): put(d,xx,yt-1,pz,"stone",owner)
    end = fwd_to*s
    j = pz - s
    while (j >= end) if s>0 else (j <= end):
        nrep += 1
        if (xt,yt,j) in d.blocks and abs(j)==1: j -= s; continue
        put(d,xt,yt,j,"repeater",owner,facing=("south" if s>0 else "north"))
        sup=(xt,yt-1,j)
        if sup not in d.blocks and not is_wall(*sup): put(d,*sup,"glass",owner)
        j -= s
    NREP[k] = nrep
    return pz

def lane7_try(d,*a,**kw):
    last=None
    for west in (False, True):
        for extra in (range(0,8) if not west else [0]):
            sb=dict(d.blocks); so=dict(OWN)
            try:
                EXTRA[0]=extra; return lane7(d,*a,west=west,**kw)
            except Coll as e:
                d.blocks=sb; OWN.clear(); OWN.update(so); last=e
    raise last

NR_GUESS = {}
def lanes7(d, G, L):
    def D(name, k, extra=0):
        n = NR_GUESS.get(name, abs(k))
        return 2*n + 2*extra + spine_delay(k)
    def go(name, obs_a, st_a, xt, yt, fwd_to=1, extra=0):
        k=L[name]; dl=D(name,k,extra)
        obs=[G+a-dl-2 for a in obs_a]; st=[G+a-dl for a in st_a]
        lane7_try(d,k,obs,st,xt,yt,fwd_to=fwd_to)
        NR_GUESS[name+'_got']=NREP[k]
    go('SDLB',[4,30,32],[],-3,1,fwd_to=2,extra=1)
    go('KLB',[],[18,24],-1,-1)
    go('SDLT',[4,30,32],[],-3,2,fwd_to=2,extra=1)
    go('R',list(range(0,RCL[0],2))+list(range(26,38,2)),[],-5,2)
    go('SR',[42,44],[20],-2,4)
    go('KLT',[],[18,24],-1,4)
