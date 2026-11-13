exec(open('work/build2.py').read())
d=make2()
d.set(-10,1,3,"lever",face="floor",facing="north")   # LQ
d.set(-3,2,0,"observer",facing="up")
for x in (-3,-4,-5): d.set(x,3,0,"redstone_wire")
d.set(-4,2,0,"stone"); d.set(-5,2,0,"stone")
d.set(-6,2,0,"stone"); d.set(-6,3,0,"lever",face="floor",facing="north")    # LR
lab=Lab(d,walls=True)
LQ=(-10,1,3); LR=(-6,3,0); LT=(-2,1,6)
lab.rest()
lab.flip(*LT); lab.rest(); print('closed',lab.doorway())
lab.flip(*LT); t0=lab.t
import sys
sched={24:('R',),30:('Q',),36:('R',),42:('Q',)}
for k in range(0,80):
    if k in sched:
        n=sched[k][0]
        if n=='R': lab.flip(*LR)
        else: lab.flip(*LQ)
    if k-2 in sched and sched[k-2][0]=='Q': lab.flip(*LQ)
    lab.step(1)
    if k%4==0 or k in sched: print(k,lab.doorway())
lab.rest(); print('final',lab.doorway())
print(lab.view(z=0).split('legend')[0])
