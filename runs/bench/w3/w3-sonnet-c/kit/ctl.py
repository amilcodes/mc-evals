# controller test: chain flowing west along z=0 at y=3, modules north (z<0) and south (z>0)
Y=3
def sup(d,x,z,blk="stone"):
    d.set(x,Y-1,z,blk)
def dust(d,x,z):
    d.set(x,Y,z,"redstone_wire"); sup(d,x,z)
def rep(d,x,z,facing,delay=1):
    d.set(x,Y,z,"repeater",facing=facing,delay=delay); sup(d,x,z)
def comp(d,x,z,facing,mode="subtract"):
    d.set(x,Y,z,"comparator",facing=facing,mode=mode); sup(d,x,z)
def line(d,x0,x1,z):
    step=1 if x1>=x0 else -1
    for x in range(x0,x1+step,step): dust(d,x,z)
def vline(d,x,z0,z1):
    step=1 if z1>=z0 else -1
    for z in range(z0,z1+step,step): dust(d,x,z)

def chain(d, x0):
    """chain flowing west from x0. returns dict of node x positions"""
    nodes={}
    x=x0
    nodes['n0']=x; dust(d,x,0)
    # n0 -> n1 : rep d2, spacing 6
    seq=[('n1',2,6),('m1',4,5),('n2',2,5),('n3',1,6),('n4',2,6),('n5',4,6)]
    for name,delay,gap in seq:
        x-=1; rep(d,x,0,"east",delay)       # input from east
        for k in range(gap-1):
            x-=1; dust(d,x,0)
        nodes[name]=x
    return nodes
