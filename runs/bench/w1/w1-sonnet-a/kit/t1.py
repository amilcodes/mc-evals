d = Design()
def pist(x,y,face,sticky=True):
    d.set(x,y,0,"sticky_piston" if sticky else "piston",facing=face)
    d.set(x,y,2,"stone")
    d.set(x,y,1,"lever",face="wall",facing="north")
# center row subsystem
d.set(-1,1,0,"stone")   # S
d.set(-1,2,0,"stone")   # X
d.set(-1,0,0,"stone")   # e0
pist(-2,1,"east")  # B
pist(-3,1,"east")  # A
pist(-1,3,"down")  # V
lab = Lab(d)
print(lab.lost)
print(lab.view(z=0))
def pulse(pos, ticks=2, rest=8):
    lab.flip(*pos)
    lab.step(ticks)
    lab.flip(*pos)
    lab.step(rest)
for name,p in [("B",(-2,1,1)),]:
    pass
