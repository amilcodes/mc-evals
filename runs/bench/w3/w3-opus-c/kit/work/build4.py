import sys, random; sys.path.insert(0,'.'); sys.path.insert(0,'work')
from gen import *

def build(bounds=((-4,4),(-2,4),(-2,1)), verbose=True, seed=0, bmin=22):
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
    # lever + level line: 22 ticks
    lever=(-4,1,-2)
    B.put((-4,2,-2),S); B.put(lever,"lever",face="ceiling",facing="north")
    B.put((-4,0,-1),S); B.put((-4,1,-1),"repeater",facing="north",delay=4)
    B.put((-4,0,0),S);  B.put((-4,1,0),"repeater",facing="north",delay=4)
    B.put((-4,0,1),S);  B.put((-4,1,1),"redstone_wire")
    B.put((-3,0,1),S);  B.put((-3,1,1),"repeater",facing="west",delay=3)
    B.put((-2,1,1),S)   # P_L
    for c in [(-3,1,-1)]: B.reserved.add(c)
    times={}
    # L1 chain: lever watcher (-3,1,-2) facing west
    B.obs((-3,1,-2),lever); times[(-3,1,-2)]=2
    B.obs((-2,1,-2),(-3,1,-2)); times[(-2,1,-2)]=4
    B.obs((-2,1,-1),(-2,1,-2)); times[(-2,1,-1)]=6   # EO_L1 -> L (l1=6)
    # V window: RV fed at 8 -> v1=18, v2=26
    B.obs((-4,0,-2),lever); times[(-4,0,-2)]=2
    B.obs((-4,-1,-2),(-4,0,-2)); times[(-4,-1,-2)]=4
    B.obs((-3,-1,-2),(-4,-1,-2)); times[(-3,-1,-2)]=6
    B.obs((-2,-1,-2),(-3,-1,-2)); times[(-2,-1,-2)]=8
    B.reserved.add((-1,-2,-2))
    B.obs((-1,-1,-1),(-1,-1,-2))   # EO_V
    B.fronts.discard((-1,-1,-2))
    # M window: RM at (-3,3,0) facing north (input (-3,3,-1)), EO_M (-3,2,0) facing up
    B.put((-3,2,0),"observer",facing="up"); B.used.discard((-3,2,0)); B.used.add((-3,2,0))
    B.put((-3,3,0),"repeater",facing="north",delay=4)
    B.fronts.add((-3,3,0))
    B.qc.add((-2,2,0))
    rnd = random.Random(seed)
    nodouble = set()
    def do_route(dst_prev, dst, t, exact=False, span=40):
      for tt in ((t,) if exact else range(t, t+span, 2)):
        srcs = sorted([c for c in times if c != (-2,1,-1)], key=lambda c: (-times[c], rnd.random()))
        for s in srcs:
            n = (tt - times[s])//2
            if n<1: continue
            p = B.route(s, dst_prev, dst, n, bounds)
            if p:
                B.place_chain(s, p)
                for i,c in enumerate(p): times[c]=times[s]+2*(i+1)
                if verbose: print("route", dst, "from", s, "len", len(p), "t", tt)
                return tt
      raise Exception(f"no route to {dst} t={t}")
    b = do_route((-3,3,-2), (-3,3,-1), bmin)          # RM input
    do_route((-1,4,0), (-1,3,0), b+14, exact=True)    # l4 via W
    do_route((-2,3,0), (-2,2,0), b+24)                # l6
    # singles chain (reverse) along z=-2
    B.reserved.discard((-1,-2,-2))
    for pv in [(-2,-2,-2),(-1,-2,-1)]:
        try:
            do_route(pv, (-1,-2,-2), 12); break
        except Exception as e: last=e
    else: raise last
    B.put((-1,-1,-2),"repeater",facing="west",delay=4)   # RV on observer
    B.fronts.add((-1,-1,-2))
    prev=(-1,-2,-2)
    for c in [(0,-2,-2),(1,-2,-2),(2,-2,-2),(3,-2,-2),(4,-2,-2),(4,-1,-2),(4,0,-2),(4,1,-2),(4,2,-2),(4,3,-2),(4,4,-2),(3,4,-2),(2,4,-2),(1,4,-2),(0,4,-2)]:
        B.obs(c,prev); prev=c
    for x in range(3):
        B.obs((x,-2,-1),(x,-2,-2)); B.obs((x,4,-1),(x,4,-2))
    B.obs((4,1,-1),(4,1,-2))
    print("b",b)
    return B, times

if __name__=="__main__":
    for seed in range(int(sys.argv[2]) if len(sys.argv)>2 else 1):
        try:
            B,times = build(seed=seed)
            B.d.save(sys.argv[1]); print("ok seed",seed, B.d.bbox(), len(B.d.blocks)); break
        except Exception as e:
            print("seed",seed,"fail",e)
