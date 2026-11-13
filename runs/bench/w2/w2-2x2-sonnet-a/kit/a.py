d=Design("open")
for p in [(0,-1,0),(1,-1,0),(0,2,0),(1,2,0),(-1,0,0),(-1,1,0),(2,0,0),(2,1,0),(-2,2,0),(-1,2,0),(2,2,0),(3,2,0)]:
    d.set(*p,"stone")
for y in (0,1):
    d.set(-2,y,0,"sticky_piston",facing="east")
    d.set(3,y,0,"sticky_piston",facing="west")
for x in range(-2,4):
    d.set(x,3,0,"redstone_wire")
d.set(-3,2,0,"lever",face="wall",facing="west")
d.save("a.json")
print(test(d))
