exec(open('work/build.py').read())
def back(c,facing): return sub(c,VEC[facing])
def make_left(line, taps, xn, specs, box=((-8,-3,0),(0,9,1)), verbose=True, Y=9):
    L=Design("closed"); mech.mech_left(L); heads_left(L)
    for (x,z),(kind,dl) in line.items():
        if kind=='r': L.set(x,Y,z,"repeater",facing=("east" if z==1 else "west"),delay=dl)
        elif kind=='d': L.set(x,Y,z,"redstone_wire")
        elif kind=='b': L.set(x,Y,z,"stone")
        if x==xn: continue
        if (x,z) in taps: L.set(x,Y-1,z,"observer",facing="up")
        else: L.set(x,Y-1,z,"stone")
    L.set(xn,Y-1,1,"redstone_wire",north="side",south="side",east="side",west="side"); L.set(xn,Y-1,0,"note_block")
    L.remove(-4,5,0); L.set(-4,5,0,"note_block")
    L.set(xn,Y-2,1,"glass"); L.set(xn,Y-2,0,"observer",facing="up")
    occ=Design(); occ.merge(L); center(occ, Y)
    R=Router(occ, box)
    R.forbid |= mech_moving_cells(); R.noback |= mech_moving_cells()
    R.forbid |= {(-2,5,1),(-3,3,1),(-1,4,1),(-4,1,1),(-4,3,0),(-1,6,0)}
    paths={}
    FEED={(-3,6,1),(-4,7,1),(-5,6,1),(-4,6,0),(-5,5,0)}
    R.forbid |= FEED
    for name,src,goal,feeder in specs:
        R.forbid |= set(watched(occ).keys())
        if isinstance(src,tuple) and len(src)==2 and src[0]=='branch':
            src=src[1]
            start=[add(src,v) for v in DIRS if R.free(add(src,v))]
        else:
            sf=occ.blocks[src][1]['facing']
            start=[back(src,sf)]
        goalcell=goal
        if feeder:
            fpos,ff=feeder; goalcell=add(fpos,VEC[ff])
        R.forbid.discard(goalcell)
        for st in start: R.forbid.discard(st)
        if goalcell==src:
            p=[]
        elif goalcell in occ.blocks:
            p=None
        else:
            p=R.route(src,start,goalcell,maxlen=40)
        if p is None:
            if verbose: print("FAIL",name)
            paths[name]=None; continue
        R.place(src,p)
        if feeder: occ.set(*fpos,"observer",facing=ff)
        paths[name]=(src,p)
        if verbose: print(name,len(p),p)
    for c,(b,pr) in occ.blocks.items():
        if c not in L.blocks: L.set(*c,b,**pr)
    for c in list(L.blocks):
        pass
    return L,paths
