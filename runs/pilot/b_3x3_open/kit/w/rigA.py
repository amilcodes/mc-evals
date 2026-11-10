import sys; sys.path.insert(0,'.')
from pdbuild import Design
d=Design("open")
# lone dust test: strongly powered block B, dust next to it, pistons N and E of dust
d.set(10,0,5,"stone"); d.set(10,1,5,"lever",face="floor",facing="north")
d.set(11,-1,5,"stone"); d.set(11,0,5,"redstone_wire")
d.set(12,0,5,"piston",facing="up"); d.set(11,0,4,"piston",facing="up")
# target test: dust between target and nothing; target adjacent to piston
d.set(10,-1,7,"stone"); d.set(10,0,7,"redstone_wire")  # fed by B? (10,0,6) between
d.set(10,-1,6,"stone"); d.set(10,0,6,"redstone_wire")
d.set(10,0,8,"target"); d.set(11,0,8,"piston",facing="up")
d.set(9,0,7,"piston",facing="up")
d.save("w/rigA.json")
