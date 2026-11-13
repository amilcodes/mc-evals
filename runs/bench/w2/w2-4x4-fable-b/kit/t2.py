from pdlab import *
d=Design()
d.set(8,8,0,"glass"); d.set(8,9,0,"lever",face="floor",facing="north")
d.set(9,8,0,"stone"); d.set(9,9,0,"redstone_wire")
d.set(8,7,0,"redstone_wire"); d.set(8,6,0,"stone")
lab=Lab(d); print(lab.lost)
print(lab.flip(8,9,0)); print(lab.block(9,9,0), lab.block(8,7,0))
