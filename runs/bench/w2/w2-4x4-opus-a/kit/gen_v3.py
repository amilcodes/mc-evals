import json
def is_wall(x,y,z):
    if z==0: return False
    return ((x in (-1,4)) and 0<=y<=3) or ((y in (-1,4)) and 0<=x<=3)
class B:
    def __init__(s): s.b={}; s.err=[]
    def put(s,p,id,**pr):
        if is_wall(*p): s.err.append(("wall",p,id)); return
        if p in s.b and s.b[p][0]!=id: s.err.append(("dup",p,id,s.b[p][0]))
        s.b[p]=(id,pr)
    def sup(s,p):
        q=(p[0],p[1]-1,p[2])
        if is_wall(*q): return
        if q in s.b:
            if s.b[q][0] not in ("stone",): s.err.append(("supconf",q,s.b[q][0]))
            return
        s.b[q]=("stone",{})
    def dust(s,p): s.put(p,"redstone_wire"); s.sup(p)
    def rep(s,p,f,d=1): s.put(p,"repeater",facing=f,delay=str(d)); s.sup(p)
    def obs(s,p,f): s.put(p,"observer",facing=f)
    def blk(s,p): s.put(p,"stone")
MIR={"east":"west","west":"east"}
def mech(bd):
    for y in (0,1,2,3): bd.blk((-1,y,0))
    for y in (1,2):
        bd.put((-2,y,0),"sticky_piston",facing="east"); bd.put((-3,y,0),"sticky_piston",facing="east")
    bd.put((-1,4,0),"sticky_piston",facing="down"); bd.put((-1,-1,0),"sticky_piston",facing="up")

ZB=-22; ZM=-8; BUSX0=-16; BUSX1=19
BUSREP=[-9,-1,14]
def busdelay(x): return 2*sum(1 for r in BUSREP if r<x)

class Side:
    def __init__(s,bd,mir): s.bd=bd; s.mir=mir
    def T(s,p): return (3-p[0],p[1],p[2]) if s.mir else p
    def F(s,f): return MIR.get(f,f) if s.mir else f
    def dust(s,p): s.bd.dust(s.T(p))
    def rep(s,p,f,d=1): s.bd.rep(s.T(p),s.F(f),d)
    def obs(s,p,f): s.bd.obs(s.T(p),s.F(f))
    def put(s,p,id,**pr):
        if "facing" in pr: pr["facing"]=s.F(pr["facing"])
        s.bd.put(s.T(p),id,**pr)

def run(side, cells, forced=None):
    """cells: list of (pos, dir) where dir is travel direction 'S' (+z) or 'E' (+x) or None (turn->dust).
    places dust, with repeaters every 12 straight cells. returns delay ticks"""
    delay=0; cnt=0
    forced=forced or {}
    for i,(p,d) in enumerate(cells):
        if p in forced:
            f,dl=forced[p]; side.rep(p,f,dl); delay+=2*dl; cnt=0; continue
        cnt+=1
        if d is not None and cnt>=12:
            side.rep(p,{"S":"north","E":"west"}[d],1); delay+=2; cnt=0
        else:
            side.dust(p)
    return delay

def column(side, X, y, kind, tgt, post):
    """build a column from bus to merge at ZM; returns nothing. kind: ('level',) or ('pulse',k)"""
    bd=side.T((X,0,0))[0]
    internal = tgt - busdelay(bd) - post
    side.rep((X,5,ZB+1),"north",1)
    side.dust((X,5,ZB+2))
    z=ZB+3
    for k in range(1,5-y+1):
        side.dust((X,5-k,z)); z+=1
    rem = internal - 2   # tap
    elems=[]
    if kind[0]=='pulse':
        kk=kind[1]; pre = rem - 2 - 2*kk
        assert pre>=0 and pre%2==0, (X,y,kind,tgt,pre)
        steps=pre//2
        while steps>0:
            d=min(4,steps); elems.append(('R',d)); steps-=d
        elems.append(('O',)); elems.append(('R',kk))
    else:
        assert rem>=2 and rem%2==0, (X,y,kind,tgt,rem)
        steps=rem//2
        while steps>0:
            d=min(4,steps); elems.append(('R',d)); steps-=d
    start = ZM - len(elems)
    assert start>=z, ("column too long",X,y,start,z)
    while z<start:
        side.dust((X,y,z)); z+=1
    for e in elems:
        if e[0]=='R': side.rep((X,y,z),"north",e[1])
        else: side.obs((X,y,z),"north")
        z+=1
    side.dust((X,y,ZM))

T0=40
SIG={ 'K':[('level',),10,('level',),26],
      'Fb':[('level',),16],
      'B':[('pulse',2),2,('pulse',4),30,('pulse',4),34],
      'Ff':[('pulse',2),30],
      'Pb':[('level',),0]}
def S(p0,p1,z0,z1):  # south run along z at (x,y) from z0..z1 inclusive
    return [((p0,p1,z),'S') for z in range(z0,z1+1)]
def E(y,z,x0,x1):
    return [((x,y,z),'E') for x in range(x0,x1+1)]

def side_build(bd, mir, with_pbot):
    sd=Side(bd,mir)
    # mechanism
    for y in (0,1,2,3): sd.put((-1,y,0),"stone")
    for y in (1,2):
        sd.put((-2,y,0),"sticky_piston",facing="east"); sd.put((-3,y,0),"sticky_piston",facing="east")
    sd.put((-1,4,0),"sticky_piston",facing="down"); sd.put((-1,-1,0),"sticky_piston",facing="up")
    lanes={}
    def lane_Fb():
        d=run(sd, [((-6,2,ZM+1),'S')], {(-6,2,ZM+1):("north",1)})
        d+=run(sd, [((-6,2,-6),None)]+E(2,-6,-5,-3)+[((-2,2,-6),None)])
        fr={p:("north",1) for p,_ in S(-2,2,-5,-1)}
        fr[(-2,2,-5)]=("north",2)
        d+=run(sd, S(-2,2,-5,-1), fr)
        return d
    def lane_B():
        d=run(sd, [((-8,2,ZM+1),'S')], {(-8,2,ZM+1):("north",1)})
        d+=run(sd, S(-8,2,ZM+2,-5)+[((-8,2,-4),None)]+E(2,-4,-7,-4)+[((-3,2,-4),None)])
        fr={p:("north",1) for p,_ in S(-3,2,-3,-1)}; fr[(-3,2,-3)]=("north",2)
        d+=run(sd, S(-3,2,-3,-1), fr)
        # Ff branch: T at (-8,2,-4) continue south
        run(sd, [((-8,2,-3),'S'),((-8,2,-2),None)]+E(2,-2,-7,-5)+[((-4,2,-2),None)]+S(-4,2,-1,0)+[((-4,2,1),None)])
        sd.rep((-3,2,1),"west",1); sd.rep((-2,2,1),"west",1)
        # Fb branch from B segment at (-6,2,-4) into Fb turn (-6,2,-6)
        sd.rep((-6,2,-5),"south",4)
        return d
    def lane_K():
        X=-14; y=4
        d0=run(sd, [((X,y,ZM+1),'S')], {(X,y,ZM+1):("north",1)})
        # K_hi path
        dh=run(sd, S(X,y,ZM+2,-1)+[((X,y,0),None)]+E(y,0,X+1,-4), {(-4,y,0):("west",1)})
        # K_lo branch from (X,4,ZM+2) west then down along z at x=-19
        br=[((X-1,4,ZM+2),None)]
        yy=4; z=ZM+2
        while yy>-1:
            yy-=1; z+=1; br.append(((X-1,yy,z),'S'))
        br+= S(X-1,-1,z+1,-1)+[((X-1,-1,0),None)]+E(-1,0,X,-4)
        dl=run(sd, br, {(-4,-1,0):("west",1)})
        # equalize
        global KDIFF
        KDIFF=(dh,dl)
        sd.rep((-3,y,0),"west",1+max(0,(dl-dh)//2)); sd.rep((-2,y,0),"west",1)
        sd.rep((-3,-1,0),"west",1+max(0,(dh-dl)//2)); sd.rep((-2,-1,0),"west",1)
        return d0+max(dh,dl)+4
    def lane_Pb():
        X=-4
        d=run(sd, [((X,-2,ZM+1),'S')], {(X,-2,ZM+1):("north",1)})
        d+=run(sd, [((X,-2,-6),None)]+E(-2,-6,X+1,0)+[((1,-2,-6),None)]+S(1,-2,-5,-3))
        for x in range(4):
            sd.dust((x,-2,-2)); sd.rep((x,-2,-1),"north",1)
            sd.put((x,-2,0),"sticky_piston",facing="up"); sd.put((x,-1,0),"stone")
        return d+2
    specs=[('Fb',lane_Fb,[-6],2),('B',lane_B,[-8,-10,-12],2),
           ('K',lane_K,[-14,-16],4)]
    if with_pbot: specs.append(('Pb',lane_Pb,[-4],-2))
    for name,lf,cols,y in specs:
        post=lf()
        sg=SIG[name]
        for i,X in enumerate(cols):
            column(sd,X,y,sg[2*i],sg[2*i+1]+T0,post)
        # bridge
        if len(cols)>1:
            for x in range(min(cols),max(cols)+1):
                sd.dust((x,y,ZM))
        lanes[name]=post
    return lanes

def build():
    bd=B()
    side_build(bd,False,True)
    side_build(bd,True,False)
    # bus
    bd.put((BUSX0,4,ZB-1),"stone"); bd.put((BUSX0,5,ZB-1),"lever",face="floor",facing="north")
    for x in range(BUSX0,BUSX1+1):
        if x in BUSREP: bd.rep((x,5,ZB),"west",1)
        else: bd.dust((x,5,ZB))
    # P_top lane at x=1
    sd=Side(bd,False)
    cells=S(1,5,ZB+1,-3)
    run(sd,cells,{(1,5,ZB+1):("north",1)})
    for x in range(4):
        bd.dust((x,5,-2)); bd.rep((x,5,-1),"north",1)
        bd.put((x,5,0),"sticky_piston",facing="down"); bd.put((x,4,0),"stone")
    return bd

def save(bd,path):
    d=Design("open")
    for p,(id,pr) in bd.b.items(): d.set(*p,id,**pr)
    d.save(path); return d
