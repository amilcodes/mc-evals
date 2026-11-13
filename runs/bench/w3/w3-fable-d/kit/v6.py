exec(open('v5.py').read())
def build_v6():
    d = build_v5()
    S = lambda x,y,z: d.set(x,y,z,"stone")
    W = lambda x,y,z,**p: d.set(x,y,z,"redstone_wire",**p)
    # remove old bottom
    for p in [(-2,-1,2),(-2,0,2),(-2,-2,3),(-2,-1,3),(1,-3,2),(1,-2,2),(1,-3,1),(1,-2,1)]:
        d.remove(*p)
    for x in (-1,0,1):
        d.remove(x,-3,3); d.remove(x,-2,3)
    W(-2,1,1,**CROSS)
    # new bottom from right column
    W(4,1,1)
    S(4,-1,2); W(4,0,2)
    S(4,-2,3); W(4,-1,3)
    S(3,-2,3); W(3,-1,3)
    S(3,-2,2); W(3,-1,2)
    S(3,-2,1); W(3,-1,1)
    S(4,-2,1); W(4,-1,1)
    S(4,-2,0); W(4,-1,0)
    S(3,-2,0); d.set(3,-1,0,"repeater",facing="east",delay=1,powered=True)
    d.set(2,-2,0,"note_block",powered=True)
    return d
