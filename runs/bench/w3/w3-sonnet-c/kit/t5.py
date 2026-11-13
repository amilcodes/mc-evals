d = Design()
d.set(-3,1,0,"sticky_piston",facing="east")   # P
d.set(-2,1,0,"sticky_piston",facing="east")   # B
d.set(-1,1,0,"stone")  # S
d.set(-1,2,0,"stone")  # G
d.set(-1,3,0,"sticky_piston",facing="down")   # A
d.set(-3,-1,0,"stone"); d.set(-3,0,0,"lever",face="floor",facing="north")
d.set(-2,-1,0,"stone"); d.set(-2,0,0,"lever",face="floor",facing="north")
d.set(-1,4,0,"stone"); d.set(0,4,0,"lever",face="wall",facing="east")
d.set(-1,0,0,"stone")
lab = Lab(d); lab.rest()
LP,LB,LA=(-3,0,0),(-2,0,0),(0,4,0)
def pz(l,n=2,after=2):
    lab.flip(*l); lab.step(n); lab.flip(*l); lab.step(after)
def Pon(Bdelay=4,Bn=2):
    lab.flip(*LP); lab.step(Bdelay); pz(LB,Bn,2); lab.flip(*LP); lab.step(8)
# close
Pon(); pz(LB,2,0) if False else None
lab.step(4); pz(LA,2,8); pz(LB,2,6); print(lab.doorway()); 
# open
pz(LB,2,4); pz(LA,2,6); Pon(); pz(LB,2,6); print(lab.doorway()); show()
