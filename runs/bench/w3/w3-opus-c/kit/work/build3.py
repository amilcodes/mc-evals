import sys, random; sys.path.insert(0,'.'); sys.path.insert(0,'work')
from gen import *

def build(bounds=((-5,4),(-2,4),(-1,1)), verbose=True, seed=0, m1=36):
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
    lever=(-5,1,-1)
    B.put((-5,0,-1),S); B.put(lever,"lever",face="floor",facing="north")
    B.put((-5,0,0),S);  B.put((-5,1,0),"repeater",facing="north",delay=4)
    B.put((-5,0,1),S);  B.put((-5,1,1),"redstone_wire")
    B.put((-4,0,1),S);  B.put((-4,1,1),"repeater",facing="west",delay=4)
    B.put((-3,0,1),S);  B.put((-3,1,1),"repeater",facing="west",delay=4)
    B.put((-2,1,1),S)   # P_L
    for c in [(-4,1,0),(-2,0,1),(-2,2,1),(-5,2,1),(-6,1,1),(-5,-1,1)]: B.reserved.add(c)
    times={}
    B.obs((-4,1,-1),lever); times[(-4,1,-1)]=2
    B.obs((-5,2,-1),lever); times[(-5,2,-1)]=2
    B.obs((-5,2,0),(-5,1,0)); times[(-5,2,0)]=10
    B.obs((-4,2,1),(-4,1,1)); times[(-4,2,1)]=18
    B.put((-2,1,-1),S)   # P_L2
    B.obs((-3,1,-1),(-4,1,-1)); times[(-3,1,-1)]=4   # l1 = 4
    B.put((-1,-1,-1),S)  # PV
    B.put((-1,-1,1),S)   # PV'
    B.put((1,-2,-1),S); B.put((1,4,-1),S); B.put((0,4,-1),S)
    B.qc.add((-2,2,0))
    rnd = random.Random(seed)
    def do_route(dst_prev, dst, t, exact=False, span=40):
      for tt in ((t,) if exact else range(t, t+span, 2)):
        srcs = sorted(times, key=lambda c: (rnd.random() if seed>=3 else 0, -times[c], rnd.random()))
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
    do_route((-3,-1,-1), (-2,-1,-1), 18, exact=True)    # v1 via PV
    do_route((-3,-1,1), (-2,-1,1), 30, exact=True)      # v2 via PV'
    for m in range(m1, m1+30, 2):
        try:
            t = do_route((-3,-1,0), (-3,0,0), m, exact=True)
        except Exception: continue
        break
    do_route((-1,4,0), (-1,3,0), t+4, exact=True)       # l4 via W
    do_route((-3,3,0), (-3,2,0), t+8, exact=True)       # m2
    do_route((-2,3,0), (-2,2,0), t+14)                  # l6
    do_route((-2,-2,0), (-1,-2,0), 12)   # B0
    do_route((-1,-2,-1), (0,-2,-1), 12)  # P_B1
    do_route((4,-2,0), (3,-2,0), 12)     # B2
    do_route((-2,4,-1), (-1,4,-1), 12)   # P_T0
    do_route((3,4,-1), (2,4,-1), 12)     # P_T1
    do_route((4,4,0), (3,4,0), 12)       # T2
    do_route((4,3,0), (4,2,0), 12)       # R1
    return B, times

if __name__=="__main__":
    for seed in range(int(sys.argv[2]) if len(sys.argv)>2 else 1):
        try:
            B,times = build(seed=seed)
            B.d.save(sys.argv[1]); print("ok seed",seed, B.d.bbox(), len(B.d.blocks)); break
        except Exception as e:
            print("seed",seed,"fail",e)
