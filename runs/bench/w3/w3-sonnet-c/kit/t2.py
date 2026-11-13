d = Design()
d.set(-3,1,0,"sticky_piston",facing="east")   # P
d.set(-2,1,0,"sticky_piston",facing="east")   # B
d.set(-1,1,0,"stone")  # S
d.set(-1,2,0,"stone")  # G
d.set(-1,3,0,"sticky_piston",facing="down")   # A
d.set(-3,-1,0,"stone"); d.set(-3,0,0,"lever",face="floor",facing="north")  # lever P
d.set(-2,-1,0,"stone"); d.set(-2,0,0,"lever",face="floor",facing="north")  # lever B
d.set(-2,2,0,"stone"); d.set(-2,3,0,"lever",face="floor",facing="north")   # lever A
d.set(-1,0,0,"stone")
lab = Lab(d); print(lab.lost)
LP,LB,LA=(-3,0,0),(-2,0,0),(-2,3,0)
def pulse(l,n=2):
    lab.flip(*l); lab.step(n); lab.flip(*l)
def show(): print(lab.view(z=0))
# close sequence
lab.flip(*LP); lab.step(8); lab.flip(*LP)  # P long pulse 8
show()
