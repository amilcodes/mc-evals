# control block: rows along x at z = z0 - 2*j ; pulse lines exit toward +z
DELAY=2
TAPS={'T1':(1,8),'T2':(2,12),'T3':(3,4),'T4':(4,14),'T5':(5,6),'T6':(6,10)}  # k, xT
def ctrl_block(d, X0, Yb, Z0):
    """returns dict of output cells (x,y,z) for groups P2h,P1,V,P2f (pulse dust / level dust), and lever-input cell for L"""
    XBL,XBR=-1,26
    rows=sorted(TAPS)
    for j,name in enumerate(rows):
        k,xT=TAPS[name]; w=Z0-2*j
        a0=xT-k; b1=xT+13-k
        # west stub: dust from XBL+1 .. a0-1 ; A repeaters a0..xT-1 facing west(input west)
        for x in range(XBL, a0):
            d.set(X0+x,Yb-1,w,"stone"); d.set(X0+x,Yb,w,"redstone_wire")
        d.set(X0+XBL+1,Yb,w,"repeater",facing="west",delay=1)
        for x in range(a0,xT):
            d.set(X0+x,Yb-1,w,"stone"); d.set(X0+x,Yb,w,"repeater",facing="west",delay=DELAY)
        d.set(X0+xT,Yb-1,w,"stone"); d.set(X0+xT,Yb,w,"redstone_wire")
        for x in range(xT+1,b1+1):
            d.set(X0+x,Yb-1,w,"stone"); d.set(X0+x,Yb,w,"repeater",facing="east",delay=DELAY)
        for x in range(b1+1, XBR+1):
            d.set(X0+x,Yb-1,w,"stone"); d.set(X0+x,Yb,w,"redstone_wire")
        d.set(X0+XBR-1,Yb,w,"repeater",facing="east",delay=1)
    zlast=Z0-2*(len(rows)-1)
    # buses along z at x=XBL and XBR (fill gaps)
    for x in (XBL,XBR):
        for w in range(zlast,Z0+1):
            d.set(X0+x,Yb-1,w,"stone"); d.set(X0+x,Yb,w,"redstone_wire")
    # observers and pulse lines
    zexit=Z0+2
    outs={}
    for j,name in enumerate(rows):
        k,xT=TAPS[name]; w=Z0-2*j
        if name=='T3':
            # level: staircase up
            d.set(X0+xT,Yb,w+1,"stone") if False else None
            d.set(X0+xT,Yb,w+1,"stone"); d.set(X0+xT,Yb+1,w+1,"redstone_wire")
            d.set(X0+xT,Yb+1,w+2,"stone"); d.set(X0+xT,Yb+2,w+2,"redstone_wire")
            start=w+3
        else:
            d.set(X0+xT,Yb+1,w,"observer",facing="down")
            d.set(X0+xT,Yb+2,w,"redstone_wire")
            start=w+1
        for ww in range(start,zexit+1):
            d.set(X0+xT,Yb+1,ww,"stone"); d.set(X0+xT,Yb+2,ww,"redstone_wire")
    # merges at exit row zexit
    def link(xa,xb):
        for x in range(xa+1,xb):
            d.set(X0+x,Yb+1,zexit,"stone"); d.set(X0+x,Yb+2,zexit,"redstone_wire")
    link(8,10); link(12,14)
    outs={'P2h':(X0+9,Yb+2,zexit),'P1':(X0+13,Yb+2,zexit),'V':(X0+6,Yb+2,zexit),'P2f':(X0+4,Yb+2,zexit)}
    zmid=Z0-5
    return outs, ((X0+XBL,Yb,zmid),(X0+XBR,Yb,zmid))
