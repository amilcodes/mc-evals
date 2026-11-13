import sys; sys.path.insert(0,'.'); sys.path.insert(0,'work')
from gen import *

def build(bounds=((-5,4),(-2,4),(-2,1)), verbose=True):
    B = Builder()
    S = "stone"
    # frame / door stones
    for c in [(-1,0,0),(-1,1,0),(-1,2,0),(3,0,0),(3,1,0),(3,2,0),(0,-1,0),(1,-1,0),(2,-1,0),(0,3,0),(1,3,0),(2,3,0)]:
        B.put(c,S)
    # mechanism
    B.put((-3,1,0),"sticky_piston",facing="east")   # M
    B.put((-2,1,0),"sticky_piston",facing="east")   # L
    B.put((-1,-1,0),"sticky_piston",facing="up")    # V
    for x in range(3):
        B.put((x,-2,0),"sticky_piston",facing="up")
        B.put((x,4,0),"sticky_piston",facing="down")
    B.put((4,1,0),"sticky_piston",facing="west")
    # reserve moving cells / doorway handled by is_hall; frame cells
    for c in [(-2,1,0),(-1,1,0),(0,1,0),(1,1,0)]: B.reserved.add(c)
    # lever + level line
    B.put((-5,2,-2),S)
    B.put((-5,1,-2),"lever",face="ceiling",facing="north")
    B.put((-5,0,-1),S); B.put((-5,1,-1),"repeater",facing="north",delay=3)
    B.put((-5,0,0),S);  B.put((-5,1,0),"repeater",facing="north",delay=3)
    B.put((-5,0,1),S);  B.put((-5,1,1),"redstone_wire")
    B.put((-4,0,1),S);  B.put((-4,1,1),"repeater",facing="west",delay=3)
    B.put((-3,0,1),S);  B.put((-3,1,1),"repeater",facing="west",delay=3)
    B.put((-2,1,1),S)   # P_L
    for c in [(-4,1,0),(-3,1,-1),(-6,1,-2)]: B.reserved.add(c)
    lever=(-5,1,-2)
    times={}
    # L1 chain
    B.obs((-4,1,-2),lever); times[(-4,1,-2)]=2
    B.obs((-3,1,-2),(-4,1,-2)); times[(-3,1,-2)]=4
    B.obs((-2,1,-2),(-3,1,-2)); times[(-2,1,-2)]=6
    B.obs((-2,1,-1),(-2,1,-2)); times[(-2,1,-1)]=8   # EO_L1 -> L
    # V window
    B.obs((-5,0,-2),lever); times[(-5,0,-2)]=2
    B.obs((-5,-1,-2),(-5,0,-2)); times[(-5,-1,-2)]=4
    B.obs((-4,-1,-2),(-5,-1,-2)); times[(-4,-1,-2)]=6
    B.obs((-3,-1,-2),(-4,-1,-2)); times[(-3,-1,-2)]=8
    B.obs((-2,-1,-2),(-3,-1,-2)); times[(-2,-1,-2)]=10
    B.put((-1,-2,-2),"glass"); B.put((-1,-1,-2),"repeater",facing="west",delay=4)
    B.obs((-1,-1,-1),(-1,-1,-2))   # EO_V -> V (20, 28)
        # M window: RM at (-3,-1,0) facing west, input (-4,-1,0); EO_M (-3,0,0) facing down
    B.put((-3,-2,0),S); B.put((-3,-1,0),"repeater",facing="west",delay=4)
    B.obs((-3,0,0),(-3,-1,0))      # EO_M -> M (b+10, b+18)
    B.reserved.add((-2,-1,0))
    # lever watcher 3
    # D for l4 and EO_L6 - placed by routes (dst)
    B.qc.add((-2,2,0))  # ensure
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
    allsrc = lambda: sorted([c for c in times if c not in [(-2,1,-1)]], key=lambda c: -times[c])
    p = do_route(allsrc(), (-5,-1,0), (-4,-1,0), 24)       # RM input -> m1=b+10, m2=b+18
    b = times[p[-1]]
    p = do_route(allsrc(), (-2,3,0), (-2,2,0), b+24)         # EO_L6
    p = do_route(allsrc(), (-1,4,0), (-1,3,0), b+14, exact=True)         # D -> W -> L@(-1,1)
    print("b",b)
    # singles chain
    p = do_route(allsrc(), (-1,4,-2), (0,4,-2), 12)
    prev=(0,4,-2)
    for c in [(1,4,-2),(2,4,-2),(3,4,-2),(4,4,-2),(4,3,-2),(4,2,-2),(4,1,-2),(4,0,-2),(4,-1,-2),(4,-2,-2),(3,-2,-2),(2,-2,-2),(1,-2,-2),(0,-2,-2)]:
        B.obs(c,prev); prev=c
    for x in range(3):
        B.obs((x,-2,-1),(x,-2,-2)); B.obs((x,4,-1),(x,4,-2))
    B.obs((4,1,-1),(4,1,-2))
    return B, times

if __name__=="__main__":
    import sys
    B,times = build()
    B.d.save(sys.argv[1] if len(sys.argv)>1 else "work/d2.json")
    print(B.d.bbox(), len(B.d.blocks))
