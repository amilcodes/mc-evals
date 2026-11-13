def mod(d,xn,sg,dr,ds):
    """edge module on chain node (xn,0). sg=+1 south, -1 north. rear repeater delay dr, side repeater delay ds.
       R-type: dr<ds ; F-type: dr>ds. output cell (xn,6*sg)"""
    f_in="north" if sg>0 else "south"
    for z in (1,2,3): dust(d,xn,z*sg)
    rep(d,xn,4*sg,f_in,dr)
    comp(d,xn,5*sg,f_in)
    dust(d,xn+1,3*sg); dust(d,xn+2,3*sg); dust(d,xn+2,4*sg); dust(d,xn+2,5*sg)
    rep(d,xn+1,5*sg,"east",ds)
    return (xn,6*sg)
