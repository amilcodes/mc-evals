import importlib, door; importlib.reload(door)
d = door.build_test()
for (x,z) in ((door.XS,-2),(door.XC,-3),(door.XR,-4)):
    d.set(x,7,z,"redstone_wire")
dS = d.copy()
dS.set(door.XS+1,7,-2,"stone"); dS.set(door.XS+1,8,-2,"lever",face="floor",facing="north")
dS.set(door.XC-1,7,-3,"stone"); dS.set(door.XC-1,8,-3,"lever",face="floor",facing="north")
dS.set(door.XR-1,7,-4,"stone"); dS.set(door.XR-1,8,-4,"lever",face="floor",facing="north")
lab = Lab(dS, walls=True); print("lost", lab.lost)
LS=(door.XS+1,8,-2); LC=(door.XC-1,8,-3); LR=(door.XR-1,8,-4)
def fire(lev, n=80):
    t0=lab.t; lab.flip(*lev); ch=lab.step(n); return t0,ch
for cyc in range(2):
    for name,lev in (("R",LR),("C",LC),("S",LS)):
        t0,ch = fire(lev); print("close",name, lab.doorway(), lab.entity)
    for name,lev in (("S",LS),("C",LC),("R",LR)):
        t0,ch = fire(lev); print("open",name, lab.doorway(), lab.entity)
print(lab.view(z=0))
