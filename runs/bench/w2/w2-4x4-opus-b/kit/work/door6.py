PB_END=[-3]
PB_MID=[3]
exec(open("work/door5.py").read())
def base_mech(d):
    for y in range(4): d.set(-1,y,0,"stone")
    d.set(-1,-1,0,"sticky_piston",facing="up"); d.set(-1,4,0,"sticky_piston",facing="down")
    d.set(-2,1,0,"sticky_piston",facing="east"); d.set(-2,2,0,"sticky_piston",facing="east")
    d.set(-3,1,0,"honey_block"); d.set(-4,1,0,"honey_block")
    d.set(-3,2,0,"slime_block"); d.set(-4,2,0,"slime_block")
    d.set(-5,1,0,"sticky_piston",facing="east"); d.set(-5,2,0,"sticky_piston",facing="east")
    d.set(-2,3,0,"obsidian"); d.set(-2,4,0,WIRE)
    # front injectors: SDLB, SDLT, R
    d.set(-3,1,-1,WIRE); d.set(-3,0,-1,"stone")
    d.set(-2,1,-1,"repeater",facing="west"); d.set(-2,0,-1,"stone")
    d.set(-3,2,1,WIRE); d.set(-3,1,1,"obsidian")
    d.set(-2,2,1,"repeater",facing="west"); d.set(-2,1,1,"obsidian")
    d.set(-5,2,1,"repeater",facing="south"); d.set(-5,1,1,"stone")
    # back injectors: SR, KLT, KLB
    d.set(-2,4,-1,"repeater",facing="north"); d.set(-2,3,-1,"stone")
    d.set(-1,4,-1,"repeater",facing="north")
    d.set(-1,-1,-1,"repeater",facing="north"); d.set(-1,-2,-1,"glass")

SPINE_REPS = {8:'north', 16:'north', -3:'south', -11:'south'}
SPINE_LO=-19
SPINE_HI=18
def spine_delay(k):
    n=0
    for z,f in SPINE_REPS.items():
        if f=='north' and 2 < z < k: n+=1
        if f=='south' and k < z < 2: n+=1
    return 2*n

def lane6(d, k, obs, steady, xt, yt, fwd_to=1, owner=None):
    s = 1 if k > 0 else -1
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
        if xx in stones: put(d,xx,11,k,WIRE,owner); put(d,xx,10,k,"stone",owner)
        else: put(d,xx,10,k,WIRE,owner); put(d,xx,9,k,"stone",owner)
    X0 = hi+2+EXTRA[0]
    for xx in range(hi+1, X0-1):
        put(d,xx,10,k,WIRE,owner); put(d,xx,9,k,"stone",owner)
    put(d,X0-1,10,k,"repeater",owner,facing="west"); put(d,X0-1,9,k,"stone",owner)
    y=10; i=0
    pat=[(0,0),(1,0),(1,s),(0,s)]
    while True:
        dx,dz = pat[i%4]
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
    end = fwd_to*s
    j = pz - s
    while (j >= end) if s>0 else (j <= end):
        if (xt,yt,j) in d.blocks and abs(j)==1: j -= s; continue
        put(d,xt,yt,j,"repeater",owner,facing=("south" if s>0 else "north"))
        sup=(xt,yt-1,j)
        if sup not in d.blocks and not is_wall(*sup): put(d,*sup,"glass",owner)
        j -= s
    return pz

def lane6_try(d,*a,**kw):
    last=None
    for extra in range(0,12):
        sb=dict(d.blocks); so=dict(OWN)
        try:
            EXTRA[0]=extra; return lane6(d,*a,**kw)
        except Coll as e:
            d.blocks=sb; OWN.clear(); OWN.update(so); last=e
    raise last

def pz6(k, yt):
    s = 1 if k>0 else -1
    pat=[(0,0),(1,0),(1,s),(0,s)]
    return k + pat[(10-yt)%4][1]

def lanes6(d, G, L):
    def D(k, yt, extra=0):
        return 2*(abs(pz6(k,yt))-1) + 2 + 2*extra + spine_delay(k)
    dl = D(L['SDLB'],0,1); lane6_try(d,L['SDLB'],[G+4-dl-2, G+30-dl-2, G+32-dl-2],[],-3,0)
    dl = D(L['KLB'],-1); lane6_try(d,L['KLB'],[],[G+18-dl, G+24-dl],-1,-1)
    dl = D(L['SDLT'],2); lane6_try(d,L['SDLT'],[G+4-dl-2, G+30-dl-2, G+32-dl-2],[],-3,2,fwd_to=2)
    dl = D(L['R'],2); lane6_try(d,L['R'],[G+a-dl-2 for a in range(0,14,2)]+[G+a-dl-2 for a in range(26,38,2)],[],-5,2)
    dl = D(L['SR'],4); lane6_try(d,L['SR'],[G+42-dl-2, G+44-dl-2],[G+20-dl],-2,4)
    dl = D(L['KLT'],4); lane6_try(d,L['KLT'],[],[G+18-dl, G+24-dl],-1,4)

TL=[3]
PBD=[1]
PBX=[4]
def PB_OLD(d, PTZ=1):
    global SP2
    o='P'
    for key in d.blocks:
        if key not in OWN: OWN[key]='pull'
    global SP2
    put(d,XS+1,CR,2,"repeater",o,facing="west"); put(d,XS+1,CR-1,2,"stone",o)
    SP2=[(0,0),(1,0),(1,-1),(0,-1)]
    MID = PB_MID[0]
    px,pz = spiral(d,XS+2,CR,MID,2,o)
    put(d,px+1,MID,pz,"repeater",o,facing="west"); put(d,px+1,MID-1,pz,"stone",o)
    qx,qz = spiral(d,px+2,MID,PB_END[0],pz,o)
    SP2=[(0,0),(1,0),(1,1),(0,1)]
    if PB_END[0] == -3:
        flat(d,qx+1,-2,-3,qz,o,rep_every=5)
        d.set(-2,-3,qz,WIRE)
        if qz != 2:
            put(d,-2,-3,2,WIRE,o); put(d,-2,-4,2,"stone",o)
        put(d,-1,-3,2,"repeater",o,facing="west"); put(d,-1,-4,2,"stone",o)
        put(d,0,-3,2,"stone",o)
        for x in range(4):
            put(d,x,-2,2,WIRE,o)
            if x>0: put(d,x,-3,2,"stone",o)
    else:
        flat(d,qx+1,-3,-2,qz,o,rep_every=5)
        d.set(-3,-2,qz,WIRE)
        if qz == 0: raise Coll("PB ends in layer 0")
        if qz != 2:
            put(d,-3,-2,2,WIRE,o); put(d,-3,-3,2,"stone",o)
        for x in range(-2,4):
            put(d,x,-2,2,WIRE,o); put(d,x,-3,2,"stone",o)
    o='T'
    put(d,XS+1,CR,3,"repeater",o,facing="west"); put(d,XS+1,CR-1,3,"stone",o)
    flat(d,XS+2,2-XS,CR,3,o)
    d.set(2-XS,CR,3,"repeater",facing="west")
    if d.blocks.get((1-XS,CR,3),("",))[0]=="repeater": d.set(1-XS,CR,3,WIRE)
    if PTZ:
        if CR == 12:
            path=[(1,11,2),(2,10,2),(2,9,3),(1,8,3),(1,7,2)]
        elif CR == 8:
            path=[(1,7,2)]
        elif CR == 6:
            path=[(3,6,2)]
            del d.blocks[(1,7,1)]; del d.blocks[(1,6,1)]; del d.blocks[(1,7,0)]
            d.set(3,6,1,"repeater",facing="south"); d.set(3,5,1,"stone")
        elif CR == 7:
            path=[(3,7,2)]
            del d.blocks[(1,7,1)]; del d.blocks[(1,6,1)]; del d.blocks[(1,7,0)]
            d.set(3,7,1,"repeater",facing="south"); d.set(3,6,1,"stone"); d.set(3,7,0,"stone")
        else:
            path=[(1,9,2),(2,8,2),(3,7,2)]
            del d.blocks[(1,7,1)]; del d.blocks[(1,6,1)]; del d.blocks[(1,7,0)]
            d.set(3,7,1,"repeater",facing="south"); d.set(3,6,1,"stone"); d.set(3,7,0,"stone")
        for (x,y,z) in path:
            put(d,x,y,z,WIRE,'T'); put(d,x,y-1,z,"stone",'T')

def build6(L, G=36, PTX=3, PTZ=17):
    OWN.clear()
    left = Design("open"); base_mech(left)
    for key in list(left.blocks): OWN[key]='mech'
    lanes6(left, G, L)
    for k in range(SPINE_LO, SPINE_HI+1):
        if k in SPINE_REPS: put(left,XS,CR,k,"repeater",'spine',facing=SPINE_REPS[k])
        else: put(left,XS,CR,k,WIRE,'spine')
        put(left,XS,CR-1,k,"stone",'spine')
    right = left.mirrored_x(3)
    d = Design("open"); d.merge(left); d.merge(right)
    OWN.clear()
    for key in d.blocks: OWN[key]='base'
    o='P'
    pullers(d)
    for key in d.blocks:
        if key not in OWN: OWN[key]='pull'
    if TL[0]==3:
        PB_OLD(d, PTZ)
    else:
        # transport in layer 2, PB branches from it
        o='T'
        put(d,XS+1,CR,2,"repeater",o,facing="west"); put(d,XS+1,CR-1,2,"stone",o)
        xb = XS+PBX[0]
        flat(d,XS+2,2-XS,CR,2,o)
        for xx in range(max(xb-2,XS+2), xb+1):
            d.set(xx,CR,2,WIRE)
        if xb-3 > XS+1: d.set(xb-3,CR,2,"repeater",facing="west")
        d.set(2-XS,CR,2,"repeater",facing="west")
        if d.blocks.get((1-XS,CR,2),("",))[0]=="repeater": d.set(1-XS,CR,2,WIRE)
        global SP2
        o='P'
        SP2=[(0,0),(1,0),(1,PBD[0]),(0,PBD[0])]
        MID=PB_MID[0]
        px,pz = spiral(d,xb,CR-1,MID,1,o)
        put(d,px+1,MID,pz,"repeater",o,facing="west"); put(d,px+1,MID-1,pz,"stone",o)
        SP2=[(0,0),(1,0),(1,PBD[0]),(0,PBD[0])] if pz==1 else [(0,0),(1,0),(1,-PBD[0]),(0,-PBD[0])]
        qx,qz = spiral(d,px+2,MID,-2,pz,o)
        SP2=[(0,0),(1,0),(1,1),(0,1)]
        flat(d,qx+1,-3,-2,qz,o,rep_every=5)
        d.set(-3,-2,qz,WIRE)
        if qz == 0: raise Coll("PB ends in layer 0")
        if qz != 2:
            put(d,-3,-2,2,WIRE,o); put(d,-3,-3,2,"stone",o)
        for x in range(-2,4):
            put(d,x,-2,2,WIRE,o); put(d,x,-3,2,"stone",o)
        # top pullers: injector (3,7,1) reads transport dust (3,7,2)
        del d.blocks[(1,7,1)]; del d.blocks[(1,6,1)]; del d.blocks[(1,7,0)]
        if CR == 7:
            d.set(3,7,1,"repeater",facing="south"); d.set(3,6,1,"stone"); d.set(3,7,0,"stone")
        else:
            d.set(3,CR,1,"repeater",facing="south"); d.set(3,CR-1,1,"stone")
        if d.blocks.get((3,CR,2),("",))[0]!=WIRE: raise Coll("transport not dust at x=3")
    put(d,XS-1,CR-1,2,"lever",'lev',face="wall",facing="west")
    return d
