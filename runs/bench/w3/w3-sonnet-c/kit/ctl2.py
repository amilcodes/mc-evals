exec(open('ctl.py').read().split("def chain")[0])
def modR(d,xn,sg,delay):
    """R-type module (rear direct, side delayed). sg=+1 south, -1 north. returns output cell (x,z)"""
    zs=2*sg
    # spur
    for z in (sg,2*sg): dust(d,xn,z)
    f_in="north" if sg>0 else "south"   # comparator rear side facing toward the spur
    comp(d,xn,3*sg,f_in)
    # private repeater east of spur end, input from west (spur end)
    rep(d,xn+1,zs,"west",delay)
    dust(d,xn+2,zs); dust(d,xn+2,3*sg); dust(d,xn+1,3*sg)
    return (xn,4*sg)
def modF(d,xn,sg,delay):
    zs=2*sg
    for z in (sg,2*sg): dust(d,xn,z)
    f_in="north" if sg>0 else "south"
    rep(d,xn,3*sg,f_in,delay)
    comp(d,xn,4*sg,f_in)
    dust(d,xn+1,2*sg); dust(d,xn+1,3*sg); dust(d,xn+1,4*sg)
    return (xn,5*sg)
