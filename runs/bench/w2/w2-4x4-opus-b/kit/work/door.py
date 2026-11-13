from pdbuild import Design
XS = -21
XD = -10
WIRE = "redstone_wire"

def left_mech(d):
    for y in range(4): d.set(-1,y,0,"stone")
    d.set(-1,-1,0,"sticky_piston",facing="up"); d.set(-1,4,0,"sticky_piston",facing="down")
    d.set(-2,1,0,"sticky_piston",facing="east"); d.set(-2,2,0,"sticky_piston",facing="east")
    d.set(-3,1,0,"honey_block"); d.set(-4,1,0,"honey_block")
    d.set(-3,2,0,"slime_block"); d.set(-4,2,0,"slime_block")
    d.set(-5,1,0,"sticky_piston",facing="east"); d.set(-5,2,0,"sticky_piston",facing="east")
    d.set(-2,0,0,"repeater",facing="west"); d.set(-2,-1,0,"stone"); d.set(-3,0,0,"obsidian")
    d.set(-2,3,0,"obsidian"); d.set(-2,4,0,WIRE)
    # z=1 injectors
    d.set(-3,0,1,"repeater",facing="south"); d.set(-3,-1,1,"stone")
    d.set(-3,2,1,WIRE); d.set(-3,1,1,"obsidian")
    d.set(-2,2,1,"repeater",facing="west"); d.set(-2,1,1,"obsidian")
    d.set(-2,4,1,"repeater",facing="south"); d.set(-2,3,1,"stone")
    d.set(-5,2,1,"repeater",facing="south"); d.set(-5,1,1,"stone")
    d.set(-1,4,1,"repeater",facing="south")
    d.set(-1,-1,1,"repeater",facing="south"); d.set(-1,-2,1,"glass")

def pullers(d):
    for x in range(4):
        d.set(x,-2,0,"sticky_piston",facing="up"); d.set(x,-1,0,"stone")
        d.set(x,5,0,"sticky_piston",facing="down"); d.set(x,4,0,"stone")
        d.set(x,6,0,WIRE)
        d.set(x,-2,1,"repeater",facing="south"); d.set(x,-3,1,"stone")
    d.set(1,7,0,"stone"); d.set(1,7,1,"repeater",facing="south"); d.set(1,6,1,"stone")

def build_chain(times_obs, times_steady):
    """returns list of (delay, support) for repeaters, plus steady dust markers.
    elements: ('rep', delay, 'obs'|'glass') or ('dust','stone')"""
    req = sorted(set([(t,'obs') for t in times_obs] + [(t,'steady') for t in times_steady]))
    els = []; t = 0
    i = 0
    while i < len(req):
        tn, kind = req[i]
        g = tn - t
        assert g >= 0 and g % 2 == 0, (tn, t)
        if g == 0:
            # steady at same time as previous repeater: add dust
            assert kind == 'steady'
            els.append(('dust','stone')); i += 1; continue
        while g > 8:
            els.append(('rep',4,'glass')); g -= 8; t += 8
        els.append(('rep', g//2, 'obs' if kind=='obs' else 'glass')); t = tn
        if kind == 'steady':
            els.append(('dust','stone'))
        i += 1
    return els

def lane(d, k, obs, steady, xt, yt, fwd_to=1):
    els = build_chain(obs, steady)
    x = XS + 1
    xs_out = []
    for e in els:
        if e[0] == 'rep':
            d.set(x,12,k,"repeater",facing="west",delay=e[1])
            if e[2] == 'obs':
                d.set(x,11,k,"observer",facing="up"); xs_out.append(x)
            else:
                d.set(x,11,k,"glass")
        else:
            d.set(x,12,k,WIRE); d.set(x,11,k,"stone"); xs_out.append(x)
        x += 1
    lo, hi = min(xs_out), max(max(xs_out), XD)
    for xx in range(lo, hi+1):
        d.set(xx,10,k,WIRE); d.set(xx,9,k,"stone")
    # drop at XD from row 10 down
    y = 10
    while y - 2 >= yt:
        y -= 2
        d.set(XD,y,k,WIRE); d.set(XD,y-1,k,"stone")
    xx = XD + 1
    if y != yt:  # odd target: stone at yt=y-1
        assert y - 1 == yt
        d.set(xx,yt,k,"repeater",facing="west"); d.set(xx,yt-1,k,"stone"); xx += 1
    for x2 in range(xx, xt+1):
        d.set(x2,yt,k,WIRE)
        if not is_wall(x2,yt-1,k): d.set(x2,yt-1,k,"stone")
    for j in range(k-1, fwd_to-1, -1):
        if (xt,yt,j) in d.blocks: continue
        d.set(xt,yt,j,"repeater",facing="south")
        sup = (xt,yt-1,j)
        if sup not in d.blocks and not is_wall(*sup):
            d.set(*sup,"glass")

def is_wall(x,y,z):
    if z == 0: return False
    return ((x in (-1,4) and 0<=y<=3) or (y in (-1,4) and 0<=x<=3))

G = 30
def left_lanes(d):
    # R layer5 delta8: obs c
    lane(d,5,[20,22,24,26,28,30,32,46,48,50,52,54,56],[],-5,2)
    lane(d,7,[20,46,48],[],-3,2,fwd_to=2)
    lane(d,9,[54,56],[34],-2,4)
    lane(d,11,[],[28,34],-1,4)
    lane(d,13,[6,32,34],[],-3,0)
    lane(d,15,[],[18,24],-1,-1)

def spine(d, x, ks):
    for k in ks:
        d.set(x,12,k,WIRE); d.set(x,11,k,"stone")

def p_lanes(d):
    # row 12 layer 2 from XS+1 to 1
    d.set(XS+1,12,2,"repeater",facing="west"); d.set(XS+1,11,2,"stone")
    for x in range(XS+2, 2):
        if (x - (XS+2)) % 14 == 13:
            d.set(x,12,2,"repeater",facing="west")
        else:
            d.set(x,12,2,WIRE)
        d.set(x,11,2,"stone")
    # P_top drop at x=1
    d.set(1,10,2,WIRE); d.set(1,9,2,"stone"); d.set(1,8,2,WIRE); d.set(1,7,2,"stone")
    # P_bot drop at XS+3 from row 12 to row -2 dust, stone at -3
    xp = XS + 3
    y = 12
    while y > -2:
        y -= 2
        d.set(xp,y,2,WIRE); d.set(xp,y-1,2,"stone")
    x = xp + 1
    d.set(x,-3,2,"repeater",facing="west"); d.set(x,-4,2,"stone")
    for x2 in range(x+1, -1):
        if (x2 - (x+1)) % 14 == 13:
            d.set(x2,-3,2,"repeater",facing="west")
        else:
            d.set(x2,-3,2,WIRE)
        d.set(x2,-4,2,"stone")
    d.set(-1,-3,2,"repeater",facing="west"); d.set(-1,-4,2,"stone")
    d.set(0,-3,2,"stone")
    for x2 in range(4):
        d.set(x2,-2,2,WIRE)
        if x2 > 0: d.set(x2,-3,2,"stone")

def full():
    left = Design("open")
    left_mech(left); left_lanes(left)
    spine(left, XS, range(2,16))
    right = left.mirrored_x(3)
    d = Design("open")
    d.merge(left); d.merge(right)
    pullers(d); p_lanes(d)
    # transport layer 3 row 12
    d.set(XS+1,12,3,"repeater",facing="west"); d.set(XS+1,11,3,"stone")
    for x in range(XS+2, 3-XS):
        if (x - (XS+2)) % 14 == 13:
            d.set(x,12,3,"repeater",facing="west")
        else:
            d.set(x,12,3,WIRE)
        d.set(x,11,3,"stone")
    # lever
    d.set(XS-1,11,2,"stone"); d.set(XS-1,12,2,"lever",face="floor",facing="north")
    return d
