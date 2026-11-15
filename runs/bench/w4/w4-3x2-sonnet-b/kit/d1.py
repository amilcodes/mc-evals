d = Design("open")
# frame
for y in (0,1):
    d.set(-1,y,0,"stone"); d.set(3,y,0,"stone")
for x in range(3):
    d.set(x,2,0,"stone"); d.set(x,-1,0,"stone")
# corridor
d.set(-2,1,0,"stone")
d.set(-2,0,0,"lever",face="ceiling",facing="north")
d.set(-2,-2,0,"stone")
d.set(-2,-1,0,"redstone_wire")
d.set(-2,2,0,"redstone_wire")
# top
d.set(-1,2,0,"stone")
d.set(-1,3,0,"redstone_wire")
for x in range(3):
    d.set(x,3,0,"sticky_piston",facing="down")
    d.set(x,4,0,"redstone_wire")
# bottom
d.set(-1,-3,0,"stone")
d.set(-1,-2,0,"redstone_wire")
d.set(0,-4,0,"stone")
d.set(0,-3,0,"redstone_wire")
d.set(1,-3,0,"stone")
d.set(0,-2,0,"sticky_piston",facing="up")
d.set(1,-2,0,"sticky_piston",facing="up")
d.set(2,-3,0,"sticky_piston",facing="up")
d.set(2,-2,0,"stone")
d.save("d1.json")
lab = Lab(d, walls=True)
print(lab.lost)
print(lab.view(z=0))
lab.rest()
lab.flip(-2,0,0)
lab.rest()
print(lab.view(z=0))
print(lab.doorway())
