import sys, random; sys.path.insert(0,'.'); sys.path.insert(0,'work')
from gen import *

class Fail(Exception): pass

def build(bounds=((-5,4),(-2,4),(-2,0)), verbose=False, seed=0, corridor=None, l1order=0):
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
    # L level: RL fed by redstone block toggled by PR
    B.put((-2,0,-1),S); B.put((-2,1,-1),"repeater",facing="north",delay=1)
    B.put((-2,2,-2),"redstone_block"); B.put((-2,3,-2),"sticky_piston",facing="down")  # PR
    B.reserved.add((-2,1,-2))
    # lever
    lever=(-3,0,-2)
    B.put((-3,1,-2),S)
    B.put(lever,"lever",face="ceiling",facing="north")
    B.obs((-3,0,-1),lever); B.obs((-2,0,-2),lever)
    times={(-3,0,-1):2,(-2,0,-2):2}
    # V window RV at (-1,-1,-2) on observer (-1,-2,-2) (singles ring start), EO_V (-1,-1,-1)
    B.reserved.add((-1,-1,-2)); B.reserved.add((-1,-2,-2))
    B.obs((-1,-1,-1),(-1,-1,-2))
    # M window
    B.put((-3,2,0),"observer",facing="up"); B.put((-3,3,0),"repeater",facing="north",delay=4)
    B.fronts.add((-3,3,0))
    B.put((-3,3,-1),S)   # BM block feeding RM
    B.qc.add((-2,2,0))
    rnd = random.Random(seed)
    def do_route(dst_prev, dst, ts):
        for tt in ts:
            srcs = sorted([c for c in times], key=lambda c: (rnd.random() if seed%2 else 0, -times[c], rnd.random()))
            for s in srcs:
                n = (tt - times[s])//2
                if n<1: continue
                p = B.route(s, dst_prev, dst, n, bounds)
                if p:
                    B.place_chain(s, p)
                    for i,c in enumerate(p): times[c]=times[s]+2*(i+1)
                    if verbose: print("route", dst, "from", s, "len", len(p), "t", tt)
                    return tt
        raise Fail(f"no route to {dst} {list(ts)[:3]}")
    # L1: via (-2,0,0) facing down (pred (-2,-1,0)) or (-2,2,0) facing up (pred (-2,3,0))
    import copy as _cp
    base0=(_cp.deepcopy(B), dict(times))
    done=False
    for P in range(16, 60, 2):
        for (dp,dd) in [((-4,3,-2),(-3,3,-2)),((-2,5,-2),(-2,4,-2))]:
            B, t0 = _cp.deepcopy(base0[0]), dict(base0[1]); times.clear(); times.update(t0)
            try:
                do_route(dp, dd, [P])
                a = P-10
                do_route((-3,-1,-2), (-2,-1,-2), [a])
                l1=None
                for (dp2,dd2) in [((-2,3,0),(-2,2,0)),((-2,-1,0),(-2,0,0))]:
                    try:
                        l1 = do_route(dp2, dd2, range(4, a+6, 2)); L1face=dd2; break
                    except Fail: pass
                if l1 is None: raise Fail("L1")
                done=True; break
            except Fail: pass
        if done: break
    if not done: raise Fail("PR/a/L1")
    v1=a+10; v2=a+18
    B.reserved.add((-1,-1,-2)); B.reserved.add((-1,-2,-2))
    # M: RM input observer (-3,3,-1) facing north, pred (-3,3,-2); b >= v2-4
    import copy
    L6 = ((-2,3,0),(-2,2,0)) if L1face==(-2,0,0) else ((-2,-1,0),(-2,0,0))
    B.put((-1,3,0),"redstone_wire")
    if corridor is None:
        corridor = [(-2,-1,0),(-2,-2,0),(-3,-2,0),(-2,-2,-1)] if L1face==(-2,2,0) else [(-2,3,-1),(-2,4,-1),(-2,2,-1),(-2,3,0),(-3,4,-1),(-4,4,-1),(-3,4,0),(-2,4,0)]
    for c in corridor:
        if c not in B.used: B.reserved.add(c)
    l6 = 200
    b=None
    base = (copy.deepcopy(B), dict(times))
    for bb in range(v2-4, l6-24+1, 2):
        for (dp,dd) in [((-3,1,-1),(-3,2,-1))]:
            B, t0 = copy.deepcopy(base[0]), dict(base[1])
            times.clear(); times.update(t0)
            try:
                do_route(dp, dd, [bb])
                do_route((-1,3,-2), (-1,3,-1), [bb+14])
                b = bb; break
            except Fail: pass
        if b is not None: break
    if b is None: raise Fail("RM/D")
    for c in corridor: B.reserved.discard(c)
    do_route(L6[0], L6[1], range(b+24, b+80, 2))
    v1=a+10
    B.reserved.discard((-1,-1,-2)); B.reserved.discard((-1,-2,-2))
    # singles ring start observer at (-1,-2,-2) (supports RV)
    do_route((-2,-2,-2), (-1,-2,-2), range(6,60,2)) if B.free((-2,-2,-2),bounds) else do_route((-1,-2,-1), (-1,-2,-2), range(6,60,2))
    B.put((-1,-1,-2),"repeater",facing="west",delay=4); B.fronts.add((-1,-1,-2))
    prev=(-1,-2,-2)
    for c in [(0,-2,-2),(1,-2,-2),(2,-2,-2),(3,-2,-2),(4,-2,-2),(4,-1,-2),(4,0,-2),(4,1,-2),(4,2,-2),(4,3,-2),(4,4,-2),(3,4,-2),(2,4,-2),(1,4,-2),(0,4,-2)]:
        B.obs(c,prev); prev=c
    for x in range(3):
        B.obs((x,-2,-1),(x,-2,-2)); B.obs((x,4,-1),(x,4,-2))
    B.obs((4,1,-1),(4,1,-2))
    return B, times

if __name__=="__main__":
    for seed in range(int(sys.argv[2]) if len(sys.argv)>2 else 1):
        try:
            B,times = build(seed=seed)
            B.d.save(sys.argv[1]); print("ok seed",seed, B.d.bbox(), len(B.d.blocks)); break
        except (Fail, AssertionError) as e:
            print("seed",seed,"fail",e)
