exec(open('m1.py').read())
d=machine()
# P feed from back
for x in (-4,-5): d.set(x,0,0,"stone"); d.set(x,1,0,"redstone_wire")
d.set(-6,0,0,"stone"); d.set(-6,1,0,"lever",face="floor",facing="north")
# B feed via z
d.set(-2,2,1,"stone"); d.set(-2,3,1,"redstone_wire"); d.set(-2,2,2,"stone"); d.set(-2,3,2,"redstone_wire")
d.set(-2,2,3,"stone"); d.set(-2,3,3,"lever",face="floor",facing="north")
# A feed
d.set(-2,-1,1,"stone"); d.set(-2,0,1,"redstone_wire"); d.set(-2,-1,2,"stone"); d.set(-2,0,2,"redstone_wire")
d.set(-2,-1,3,"stone"); d.set(-2,0,3,"lever",face="floor",facing="north")
lab=Lab(d); print(lab.lost); lab.rest()
LP,LB,LA=(-6,1,0),(-2,3,3),(-2,0,3)
def pz(l,n=2,after=2):
    lab.flip(*l); lab.step(n); lab.flip(*l); lab.step(after)
def Pon(Bdelay=4):
    lab.flip(*LP); lab.step(Bdelay); pz(LB,2,2); lab.flip(*LP); lab.step(8)
Pon(); lab.step(4); pz(LA,2,8); pz(LB,2,6); print(lab.doorway()); 
pz(LB,2,4); pz(LA,2,6); Pon(); pz(LB,2,6); print(lab.doorway())
print(lab.view(z=0))
