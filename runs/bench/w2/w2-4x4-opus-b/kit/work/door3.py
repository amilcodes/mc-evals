exec(open("work/door2.py").read())
def pz_of(k, yt):
    i = 10 - yt
    return k + SPIRAL[i%4][1]
def left_lanes3(d, G):
    L=LAYERS
    def D(k, yt, extra=0): return 2*(pz_of(k,yt)-1) + 2 + 2*extra
    dl = D(L['SDLB'],0,1)
    lane_try(d,L['SDLB'],[G+4-dl-2, G+30-dl-2, G+32-dl-2],[],-3,0)
    dl = D(L['KLB'],-1); lane_try(d,L['KLB'],[],[G+18-dl, G+24-dl],-1,-1)
    dl = D(L['SDLT'],2); lane_try(d,L['SDLT'],[G+4-dl-2, G+30-dl-2, G+32-dl-2],[],-3,2,fwd_to=2)
    dl = D(L['R'],2); lane_try(d,L['R'],[G+a-dl-2 for a in range(0,14,2)]+[G+a-dl-2 for a in range(26,38,2)],[],-5,2)
    dl = D(L['SR'],4); lane_try(d,L['SR'],[G+42-dl-2, G+44-dl-2],[G+20-dl],-2,4)
    dl = D(L['KLT'],4); lane_try(d,L['KLT'],[],[G+18-dl, G+24-dl],-1,4)

SP2=[(0,0),(1,0),(1,1),(0,1)]
def spiral(d, X0, ytop, ybot, k, owner):
    y=ytop; i=0
    while True:
        dx,dz=SP2[i%4]
        put(d,X0+dx,y,k+dz,WIRE,owner); put(d,X0+dx,y-1,k+dz,"stone",owner)
        if y==ybot: return X0+dx, k+dz
        y-=1; i+=1

def p_lanes3(d):
    o='P'
    # P_top: spine (XS,12,2) -> repeater (XS+1,12,2) -> spiral at XS+2 from 12 to 6
    put(d,XS+1,12,2,"repeater",o,facing="west"); put(d,XS+1,11,2,"stone",o)
    px,pz = spiral(d,XS+2,12,6,2,o)
    # forward to z=0 at (px,6)
    for j in range(pz-1,-1,-1):
        put(d,px,6,j,"repeater",o,facing="south"); put(d,px,5,j,"glass",o)
    # at z=0: repeater at (px,6,0) outputs into (px,6,-1)! fix: last forward at j=1 outputs into (px,6,0)
    return px,pz
