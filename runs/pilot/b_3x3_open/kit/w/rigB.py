import sys; sys.path.insert(0,'.')
from pdbuild import Design
d=Design("open")
d.set(10,0,5,"stone"); d.set(10,1,5,"lever",face="floor",facing="north")
d.set(11,-1,5,"stone"); d.set(11,0,5,"redstone_wire",north="side",south="side",east="side",west="side")
d.set(12,0,5,"piston",facing="up"); d.set(11,0,4,"piston",facing="up")
d.save("w/rigB.json")
