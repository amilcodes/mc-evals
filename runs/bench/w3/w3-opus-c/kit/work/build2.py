import sys; sys.path.insert(0,'.'); sys.path.insert(0,'work')
from gen import *

def build(bounds=((-5,4),(-2,4),(-1,1)), verbose=True, order=None):
    B = Builder()
    S = "stone"
    for c in [(-1,0,0),(-1,1,0),(-1,2,0),(3,0,0),(3,1,0),(3,2,0),(0,-1,0),(1,-1,0),(2,-1,0),(0,3,0),(1,3,0),(2,3,0)]:
        B.put(c,S)
    B.put((-3,1,0),"sticky_piston",facing="east")   # M
    B.put((-2,1,0),"sticky_piston",facing="east")   # L
    B.put((-1,-1,0),"sticky_piston",facing="up")    # V
    for x in range(3):
        B.put((x,-2,0),"sticky_piston",facing="up")
        B.put((x,4,0),"sticky_piston",facing="down")
    B.put((4,1,0),"sticky_piston",facing="west")
    for c in [(-2,1,0),(-1,1,0),(0,1,0),(1,1,0)]: B.reserved.add(c)
    # lever + level line (24 ticks)
    lever=(-5,1,-1)
    B.put((-5,0,-1),S); B.put(lever,"lever",face="floor",facing="north")
    B.put((-5,0,0),S);  B.put((-5,1,0),"repeater",facing="north",delay=4)
    B.put((-5,0,1),S);  B.put((-5,1,1),"redstone_wire")
    B.put((-4,0,1),S);  B.put((-4,1,1),"repeater",facing="west",delay=4)
    B.put((-3,0,1),S);  B.put((-3,1,1),"repeater",facing="west",delay=4)
    B.put((-2,1,1),S)   # P_L
    for c in [(-4,1,0),(-3,1,-1),(-2,0,1),(-2,2,1),(-5,2,1),(-6,1,1),(-5,-1,1)]: B.reserved.add(c)
    times={}
    B.obs((-4,1,-1),lever); times[(-4,1,-1)]=2
    B.obs((-5,2,-1),lever); times[(-5,2,-1)]=2
    # V window
    B.put((-1,-1,-1),S)  # PV
    B.put((-3,-2,-1),S); B.put((-3,-1,-1),"repeater",facing="west",delay=4)  # RV
    B.obs((-2,-1,-1),(-3,-1,-1))   # V feeder (a+10, a+18)
    # M window
    B.put((-3,-2,0),S); B.put((-3,-1,0),"repeater",facing="west",delay=4)    # RM
    B.obs((-3,0,0),(-3,-1,0))      # EO_M
    # singles: power blocks behind B1,T1
    B.put((1,-2,-1),S); B.put((1,4,-1),S)
    B.put((0,4,-1),S)   # P_T0
    B.qc.add((-2,2,0))
    def do_route(srcs, dst_prev, dst, t, exact=False):
      for tt in ((t,) if exact else range(t, t+40, 2)):
        t = tt
        for s in srcs:
            n = (t - times[s])//2
            if n<1: continue
            p = B.route(s, dst_prev, dst, n, bounds)
            if p:
                B.place_chain(s, p)
                for i,c in enumerate(p): times[c]=times[s]+2*(i+1)
                if verbose: print("route", dst, "from", s, "len", len(p), "t", t)
                return p
      raise Exception(f"no route to {dst} t={t}")
    allsrc = lambda: sorted([c for c in times], key=lambda c: -times[c])
    do_route(allsrc(), (-2,3,0), (-2,2,0), 14, exact=True)      # EO_L1
    do_route(allsrc(), (-5,-1,-1), (-4,-1,-1), 10, exact=True)   # RV input -> v=20,28
    p = do_route(allsrc(), (-5,-1,0), (-4,-1,0), 24)             # RM input
    b = times[p[-1]]
    do_route(allsrc(), (-2,-1,0), (-2,0,0), b+24)                 # EO_L6
    do_route(allsrc(), (-1,4,0), (-1,3,0), b+14, exact=True)     # D
    # singles feeders
    do_route(allsrc(), (-2,-2,0), (-1,-2,0), 12)   # B0
    do_route(allsrc(), (-1,-2,-1), (0,-2,-1), 12)  # -> P_B1 (back east)
    do_route(allsrc(), (4,-2,0), (3,-2,0), 12)     # B2
    do_route(allsrc(), (-2,4,-1), (-1,4,-1), 12)   # -> P_T0
    do_route(allsrc(), (3,4,-1), (2,4,-1), 12)     # -> P_T1 (back west)
    do_route(allsrc(), (4,4,0), (3,4,0), 12)       # T2
    do_route(allsrc(), (4,3,0), (4,2,0), 12)       # R1 (facing up, back down)
    print("b", b)
    return B, times

if __name__=="__main__":
    B,times = build()
    B.d.save(sys.argv[1] if len(sys.argv)>1 else "work/d3.json")
    print(B.d.bbox(), len(B.d.blocks))
