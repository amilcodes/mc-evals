exec(open('cb.py').read())
d=Design()
outs,lin=ctrl_block(d,-12,10,-8)
(x1,y,z1),(x2,y,z2)=lin
d.set(x1-1,y-1,z1,"stone"); d.set(x1-1,y,z1,"redstone_wire"); d.set(x1-2,y-1,z1,"stone"); d.set(x1-2,y,z1,"lever",face="floor",facing="north")
d.set(x2+1,y-1,z2,"stone"); d.set(x2+1,y,z2,"redstone_wire"); d.set(x2+2,y-1,z2,"stone"); d.set(x2+2,y,z2,"lever",face="floor",facing="north")
d.save('tcb.json')
import json; json.dump({'outs':outs,'l1':[x1-2,y,z1],'l2':[x2+2,y,z2]},open('tcb.json.meta','w'))
