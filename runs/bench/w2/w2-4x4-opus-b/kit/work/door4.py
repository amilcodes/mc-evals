exec(open("work/door3.py").read())
def flat(d, x0, x1, y, z, owner, rep_every=12, sup="stone"):
    step = 1 if x1 >= x0 else -1
    n=0
    for x in range(x0, x1+step, step):
        n+=1
        if n % rep_every == 0:
            put(d,x,y,z,"repeater",owner,facing=("west" if step==1 else "east"))
        else:
            put(d,x,y,z,WIRE,owner)
        if not is_wall(x,y-1,z): put(d,x,y-1,z,sup,owner)

def build_full(PTX=6):
    OWN.clear()
    left = Design("open")
    left_mech(left)
    for key in list(left.blocks): OWN[key]='mech'
    left_lanes3(left, 30)
    for k in range(2,19):
        if k == 16: put(left,XS,12,k,"repeater",'spine',facing="north")
        else: put(left,XS,12,k,WIRE,'spine')
        put(left,XS,11,k,"stone",'spine')
    right = left.mirrored_x(3)
    d = Design("open"); d.merge(left); d.merge(right)
    OWN2 = dict(OWN); OWN.clear()
    for key in d.blocks: OWN[key]='base'
    o='P'
    pullers(d)
    for key in d.blocks:
        if key not in OWN: OWN[key]='pull'
    # PB in layer 2
    put(d,XS+1,12,2,"repeater",o,facing="west"); put(d,XS+1,11,2,"stone",o)
    global SP2
    SP2=[(0,0),(1,0),(1,-1),(0,-1)]
    px,pz = spiral(d,XS+2,12,3,2,o)
    put(d,px+1,3,pz,"repeater",o,facing="west"); put(d,px+1,2,pz,"stone",o)
    qx,qz = spiral(d,px+2,3,-3,pz,o) if pz==2 else spiral2(d,px+2,3,-3,pz,o)
    SP2=[(0,0),(1,0),(1,1),(0,1)]
    if qz == 3:
        put(d,qx,-3,2,WIRE,o) if False else None
    flat(d,qx+1,-2,-3,qz,o,rep_every=5)
    if qz != 2:
        put(d,-2,-3,2,WIRE,o); put(d,-2,-4,2,"stone",o)
    put(d,-1,-3,2,"repeater",o,facing="west"); put(d,-1,-4,2,"stone",o)
    put(d,0,-3,2,"stone",o)
    for x in range(4):
        put(d,x,-2,2,WIRE,o)
        if x>0: put(d,x,-3,2,"stone",o)
    # P_top in layer 17
    o='PT'
    put(d,XS+1,12,17,"repeater",o,facing="west"); put(d,XS+1,11,17,"stone",o)
    flat(d,XS+2,XS+PTX-1,12,17,o)
    tx,tz = spiral(d,XS+PTX,12,6,17,o)
    for j in range(tz-1,0,-1):
        put(d,tx,6,j,"repeater",o,facing="south"); put(d,tx,5,j,"glass",o)
    flat(d,tx,-1,6,0,o,sup="glass")
    # transport layer 3 row 12
    o='T'
    put(d,XS+1,12,3,"repeater",o,facing="west"); put(d,XS+1,11,3,"stone",o)
    flat(d,XS+2,2-XS,12,3,o)
    put(d,XS-1,11,2,"stone",'lev'); put(d,XS-1,12,2,"lever",'lev',face="floor",facing="north")
    return d

def spiral2(d, X0, ytop, ybot, k, owner):
    pat=[(0,0),(1,0),(1,1),(0,1)]
    y=ytop; i=0
    while True:
        dx,dz=pat[i%4]
        put(d,X0+dx,y,k+dz,WIRE,owner); put(d,X0+dx,y-1,k+dz,"stone",owner)
        if y==ybot: return X0+dx, k+dz
        y-=1; i+=1
