def lane():
    d = Design()
    for y in (1,2):
        d.set(-3,y,0,"sticky_piston",facing="east")
        d.set(-2,y,0,"sticky_piston",facing="east")
        d.set(-1,y,0,"stone")
    d.set(-1,0,0,"stone"); d.set(-1,3,0,"stone")
    d.set(-1,-1,0,"sticky_piston",facing="up")
    d.set(-1,4,0,"sticky_piston",facing="down")
    return d
d = lane()
# PA harness
d.set(-3,3,0,"stone"); d.set(-3,4,0,"redstone_wire")
d.set(-4,4,0,"observer",facing="west")
d.set(-5,3,0,"stone"); d.set(-5,4,0,"redstone_wire")
d.set(-6,3,0,"stone"); d.set(-6,4,0,"lever",face="floor",facing="north")
# PBb
d.set(-2,1,1,"stone"); d.set(-2,2,1,"redstone_wire")
d.set(-2,2,2,"observer",facing="south")
d.set(-2,1,3,"stone"); d.set(-2,2,3,"redstone_wire")
d.set(-2,1,4,"stone"); d.set(-2,2,4,"lever",face="floor",facing="north")
# PBa
d.set(-2,1,-1,"glass"); d.set(-2,2,-1,"redstone_wire")
d.set(-3,1,-1,"glass"); d.set(-3,2,-1,"redstone_wire")
d.set(-4,2,-1,"observer",facing="west")
d.set(-5,1,-1,"stone"); d.set(-5,2,-1,"redstone_wire")
d.set(-6,1,-1,"stone"); d.set(-6,2,-1,"lever",face="floor",facing="north")
# S levers
d.set(-1,4,-1,"stone"); d.set(-1,5,-1,"lever",face="floor",facing="north")
d.set(-1,-1,-1,"lever",face="ceiling",facing="north")
LA=(-6,4,0); LBb=(-2,2,4); LBa=(-6,2,-1); LS1=(-1,5,-1); LS0=(-1,-1,-1)
lab = Lab(d, walls=True)
print(lab.lost)
def show(tag):
    s = {p:b.split('[')[0] for p,b in lab.blocks().items() if p[2]==0 and -4<=p[0]<=3 and -1<=p[1]<=4}
    rows=[]
    for y in range(4,-2,-1):
        r=''
        for x in range(-3,4):
            b=s.get((x,y,0),'air')
            r+={'air':'.','stone':'#','sticky_piston':'P','piston_head':'h','moving_piston':'m'}.get(b,'?')
        rows.append(r)
    print(tag, ' '.join(rows))
def P(l, n=12):
    lab.flip(*l); lab.step(n)
show('init')
P(LA); show('cA1'); P(LBa); show('cBa'); P(LA); show('cA2'); P(LBb); show('cBb')
P(LS0,0) if False else None
lab.flip(*LS0); lab.flip(*LS1); lab.step(8); show('cS')
P(LA); show('cA3')
print('--open')
P(LA); show('oA1'); P(LBb); show('oBb')
lab.flip(*LS0); lab.flip(*LS1); lab.step(8); show('oS')
P(LA); show('oA2'); P(LBa); show('oBa'); P(LA); show('oA3'); P(LBb); show('oBb')
print(lab.entity, lab.ticks_left)
