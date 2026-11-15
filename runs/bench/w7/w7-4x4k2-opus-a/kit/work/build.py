import sys, importlib
sys.path.insert(0,'work')
import mech, route; importlib.reload(mech); importlib.reload(route)
from pdbuild import Design
from route import Router, DIRS, add, sub
VEC={v:k for k,v in DIRS.items()}

def heads_left(d):
    # A head dust + feeders, B head dust + feeders, chain parts from mech_left already: Q_A etc
    # A delivery chains (from earlier design)
    d.set(-4,5,1,"observer",facing="up")    # Q_A watches A head (-4,6,1)
    d.set(-3,5,1,"observer",facing="west")  # watches Q_A
    d.set(-3,4,1,"observer",facing="up")    # watches (-3,5,1)
    d.remove(-2,4,1); d.set(-2,4,1,"observer",facing="west")  # watches (-3,4,1)
    d.set(-4,4,1,"observer",facing="up"); d.set(-4,3,1,"observer",facing="up"); d.set(-4,2,1,"observer",facing="up")
    d.remove(-3,2,1); d.remove(-3,1,1); d.set(-3,2,1,"observer",facing="west")  # watches (-4,2,1), back into rep (-2,2,1)
    d.set(-4,6,1,"redstone_wire")           # A head
    # B: (-4,4,0) obs up watches (-4,5,0) B head dust; (-3,4,0) obs W watches (-4,4,0)
    d.set(-4,4,0,"observer",facing="up")
    d.set(-4,5,0,"redstone_wire")
    # C top source (-3,5,0) end of chain (router)
def watched(d):
    w={}
    for p,(b,pr) in d.blocks.items():
        if b=="observer": w[add(p,VEC[pr["facing"]])]=p
    return w

def center(d, Y=9, initial="closed"):
    if initial=="closed": d.fill(0,0,0,3,3,0,"stone")
    for x in range(4):
        d.set(x,5,0,"sticky_piston",facing="down"); d.set(x,6,0,"redstone_wire")
        d.set(x,-2,0,"sticky_piston",facing="up")
    d.set(1,Y-1,1,"stone"); d.set(1,Y,1,"lever",face="floor",facing="north")
    d.set(2,Y-1,1,"stone"); d.set(2,Y,1,"redstone_wire")

def mech_moving_cells():
    s=set()
    for x in range(-3,7):
        for y in range(-2,6):
            s.add((x,y,0))
    return s

def build_left(line, taps, xn, routes_spec, box=((-8,-3,0),(0,9,1))):
    """line: dict x->(kind,delay) for z=1 leg and z=0 leg: keys (x,z). kind 'r' or 'd' or 'b'"""
    L=Design("closed"); mech.mech_left(L); heads_left(L)
    occ=Design(); occ.merge(L); center(occ)
    # line elements
    for (x,z),(kind,dl) in line.items():
        if kind=='r': L.set(x,9,z,"repeater",facing=("east" if z==1 else "west"),delay=dl)
        elif kind=='d': L.set(x,9,z,"redstone_wire")
        elif kind=='b': L.set(x,9,z,"stone")
        # support
        if (x,z) in taps: L.set(x,8,z,"observer",facing="up")
        elif x==xn: pass
        else: L.set(x,8,z,"stone")
    # X dust + PX observers
    L.set(xn,8,1,"redstone_wire"); L.set(xn,8,0,"redstone_wire")
    L.set(xn,7,1,"observer",facing="up"); L.set(xn,7,0,"observer",facing="up")
    occ=Design(); occ.merge(L); center(occ)
    R=Router(occ, box)
    R.forbid |= set(watched(occ).keys())
    R.forbid |= mech_moving_cells()
    R.noback |= mech_moving_cells()
    R.forbid |= {(-2,5,1),(-3,3,1),(-1,4,1),(-4,1,1),(-4,3,0),(-1,6,0),(-1,6,1)}
    R.noback |= {(-1,6,0),(-1,6,1)}
    paths={}
    for name,(src,goal,feeder) in routes_spec.items():
        start=[add(src,v) for v in DIRS]
        goalcell=goal
        if feeder:
            fpos,ffacing=feeder
            goalcell=add(fpos,VEC[ffacing])
            R.forbid.discard(goalcell)
        p=R.route(src,start,goalcell,maxlen=30)
        if p is None:
            print("FAIL",name); paths[name]=None; continue
        R.place(src,p)
        if feeder: occ.set(*fpos,"observer",facing=ffacing)
        paths[name]=p
        R.forbid |= set(watched(occ).keys())
    # copy chain observers into L
    for c,(b,pr) in occ.blocks.items():
        if c not in L.blocks and b=="observer": L.set(*c,b,**pr)
    return L, paths
