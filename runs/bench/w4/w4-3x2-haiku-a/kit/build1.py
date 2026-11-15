from pdbuild import Design
d = Design("open")
# permanent frame stones and moving door stones (open: moving stones sit at y=-1 and y=2)
for p in [(-1,0,0),(-1,1,0),(3,0,0),(3,1,0)]:
    d.set(*p, "stone")
for x in range(3):
    d.set(x,-1,0,"stone")
    d.set(x,2,0,"stone")
# sticky pistons, bottom row pushes up, top row pushes down
for x in range(3):
    d.set(x,-2,0,"sticky_piston",facing="up")
    d.set(x,3,0,"sticky_piston",facing="down")
# lever hangs from the root observer (ignored for volume)
d.set(-2,-6,0,"lever",face="ceiling",facing="north")
# pulse trunk: root watches lever, column runs down the left side
d.set(-2,-5,0,"observer",facing="down")
for y in range(-4,6):
    d.set(-2,y,0,"observer",facing="down")
# top trunk and feeders
for x in range(-1,3):
    d.set(x,-4,0,"observer",facing="west")
for x in range(3):
    d.set(x,-3,0,"observer",facing="down")
# bottom trunk and feeders
for x in range(-1,3):
    d.set(x,5,0,"observer",facing="west")
for x in range(3):
    d.set(x,4,0,"observer",facing="up")
d.save("cand1.json")
print(d.bbox())
