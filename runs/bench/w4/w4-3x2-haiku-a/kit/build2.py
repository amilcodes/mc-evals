from pdbuild import Design
d = Design("open")
for p in [(-1,0,0),(-1,1,0),(3,0,0),(3,1,0)]:
    d.set(*p, "stone")
for x in range(3):
    d.set(x,-1,0,"stone")
    d.set(x,2,0,"stone")
for x in range(3):
    d.set(x,-2,0,"sticky_piston",facing="up")
    d.set(x,3,0,"sticky_piston",facing="down")
# lever hangs below the root observer, so its cell (outside the box) costs nothing
d.set(-2,-5,0,"lever",face="ceiling",facing="north")
for y in range(-4,6):
    d.set(-2,y,0,"observer",facing="down")
for x in range(-1,3):
    d.set(x,-4,0,"observer",facing="west")
for x in range(3):
    d.set(x,-3,0,"observer",facing="down")
for x in range(-1,3):
    d.set(x,5,0,"observer",facing="west")
for x in range(3):
    d.set(x,4,0,"observer",facing="up")
d.save("cand2.json")
print(d.bbox())
