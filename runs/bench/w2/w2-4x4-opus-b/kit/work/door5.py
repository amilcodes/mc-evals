exec(open("work/door4.py").read())
_put_orig = put
def put(d, x,y,z, b, owner, **p):
    if b == WIRE:
        for dx,dy,dz in [(1,0,0),(-1,0,0),(0,0,1),(0,0,-1),(0,1,0),(0,-1,0),(1,1,0),(-1,1,0),(1,-1,0),(-1,-1,0),(0,1,1),(0,1,-1),(0,-1,1),(0,-1,-1)]:
            q=(x+dx,y+dy,z+dz)
            if q in d.blocks and d.blocks[q][0]==WIRE and OWN.get(q) not in (owner,):
                if OWN.get(q) in ('spine',) and owner in ('spine',): continue
                if {OWN.get(q), owner} in ({'PT','pull'},{'P','T'},{'PT','T'},{'P','PT'}): continue
                if {OWN.get(q), owner} == {'T','base'} and (q[0] == 3-XS or x == 3-XS): continue
                raise Coll(f"dust adj {q} ({OWN.get(q)}) vs {(x,y,z)} ({owner})")
    return _put_orig(d,x,y,z,b,owner,**p)
import copy
def lane_try(d, *a, **kw):
    for extra in range(0,10):
        snap_b = dict(d.blocks); snap_o = dict(OWN); snap_x = dict(X0S)
        try:
            EXTRA[0] = extra
            return lane2(d,*a,**kw)
        except Coll as e:
            d.blocks = snap_b; OWN.clear(); OWN.update(snap_o); X0S.clear(); X0S.update(snap_x)
            last = e
    raise last
EXTRA=[0]
