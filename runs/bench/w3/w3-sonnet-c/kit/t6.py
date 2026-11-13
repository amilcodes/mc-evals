exec(open('m1.py').read())
d=machine()
# test levers: P: dust (-3,1,1) aimed north with (-3,1,2); lever on stone beyond
d.set(-3,0,1,"stone"); d.set(-3,1,1,"redstone_wire"); d.set(-3,0,2,"stone"); d.set(-3,1,2,"redstone_wire")
d.set(-3,0,3,"stone"); d.set(-3,1,3,"lever",face="floor",facing="north")
# B feed: dust (-2,3,1),(−2,3,2) etc
d.set(-2,2,1,"stone"); d.set(-2,3,1,"redstone_wire"); d.set(-2,2,2,"stone"); d.set(-2,3,2,"redstone_wire")
d.set(-2,2,3,"stone"); d.set(-2,3,3,"lever",face="floor",facing="north")
# A feed
d.set(-2,-1,1,"stone"); d.set(-2,0,1,"redstone_wire"); d.set(-2,-1,2,"stone"); d.set(-2,0,2,"redstone_wire")
d.set(-2,-1,3,"stone"); d.set(-2,0,3,"lever",face="floor",facing="north")
d.set(-2,1,1,"stone")  # cut diag step between P dust (-3,1,1) and A dust (-2,0,1)
lab=Lab(d); print(lab.lost); lab.rest()
LP,LB,LA=(-3,1,3),(-2,3,3),(-2,0,3)
def pz(l,n=2,after=2):
    lab.flip(*l); lab.step(n); lab.flip(*l); lab.step(after)
def Pon(Bdelay=4):
    lab.flip(*LP); lab.step(Bdelay); pz(LB,2,2); lab.flip(*LP); lab.step(8)
Pon(); lab.step(4); pz(LA,2,8); pz(LB,2,6); print(lab.doorway()); 
pz(LB,2,4); pz(LA,2,6); Pon(); pz(LB,2,6); print(lab.doorway())
print(lab.view(z=0))
