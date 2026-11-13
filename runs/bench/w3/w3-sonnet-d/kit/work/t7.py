exec(open('work/build2.py').read())
d=make2()
# test levers
d.set(-23,1,3,"lever",face="floor",facing="north")   # LQ
d.set(-8,4,0,"stone"); d.set(-8,5,0,"lever",face="floor",facing="north")    # LF
d.set(-3,2,0,"observer",facing="up")
for x in (-3,-4,-5): d.set(x,3,0,"redstone_wire")
d.set(-4,2,0,"stone"); d.set(-5,2,0,"stone")
d.set(-6,2,0,"stone"); d.set(-6,3,0,"lever",face="floor",facing="north")    # LR
lab=Lab(d,walls=True)
print(lab.lost)
LQ=(-23,1,3); LF=(-8,5,0); LR=(-6,3,0); LT=(-2,1,6)
def pulse(p,on=2,settle=6):
    lab.flip(*p); lab.step(on); lab.flip(*p); lab.step(settle)
def lvl(p,t=30): lab.flip(*p); lab.step(t)
def st(msg=''): print(msg, lab.doorway())
lab.rest()
lvl(LT); st('close: singles on')
for n,p in (('Q',LQ),('F',LF),('Q',LQ)):
    pulse(p); st(n)
print(lab.view(z=0).split('legend')[0])
lvl(LT); st('open: singles off')
for n,p in (('Q',LQ),('F',LF),('Q',LQ)):
    pulse(p); st(n)
lvl(LR); st('R edge1'); pulse(LQ); st('Q'); lvl(LR); st('R edge2'); pulse(LQ); st('Q')
print(lab.view(z=0).split('legend')[0])
