exec(open('core.py').read())
def harness():
    d = core()
    d.set(5,1,0,"lever",face="wall",facing="east")
    d.set(-3,1,3,"observer",facing="south")
    d.set(-3,0,4,"stone"); d.set(-3,1,4,"redstone_wire"); d.set(-3,0,5,"stone"); d.set(-3,1,5,"lever",face="floor",facing="north")
    d.set(-1,-2,3,"stone"); d.set(-1,-1,3,"redstone_wire"); d.set(-1,-2,4,"stone"); d.set(-1,-1,4,"lever",face="floor",facing="north")
    return d
def show(ch, t0, allz=False):
    for t,pos,b,a in ch:
        if (pos[2]==0 and 'wire' not in a) or allz: print(t-t0,pos,b.split('[')[0],'->',a)
def row():
    return ''.join({'air':'.','stone':'#'}.get(lab.block(x,1,0),'?' ) for x in range(-3,5))+' L@(-1,2)='+lab.block(-1,2,0)
lab = Lab(harness(), walls=True)
lab.flip(5,1,0); lab.step(6)
t0=lab.t; lab.flip(-1,-1,4); ch=lab.step(12); show(ch,t0); print(row())
