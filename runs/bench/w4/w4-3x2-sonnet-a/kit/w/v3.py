from pdbuild import Design
exec(open("w/v2.py").read().split("d.save")[0])
# extend right chain down and across y=-3
d.set(4,-2,0,"observer",facing="up")
d.set(4,-3,0,"observer",facing="up")
d.set(3,-3,0,"observer",facing="east")
d.set(2,-3,0,"observer",facing="east")
d.set(1,-3,0,"stone")
d.save("w/v3.json")
