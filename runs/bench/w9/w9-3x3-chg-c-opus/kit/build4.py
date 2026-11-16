d=Design.load("d2.json")
for p in [(5,4,0),(5,4,1),(5,5,1),(5,5,0),(5,6,0),(4,6,1),(0,6,1),(1,6,1),(2,6,1),(3,6,1),(4,4,0),(4,4,1),(4,5,1)]:
    d.remove(*p)
d.set(4,5,1,"stone")                                   # A
d.set(5,5,1,"lever",face="wall",facing="east")
d.set(4,6,1,"sticky_piston",facing="west"); d.set(3,6,1,"stone")   # G + conductor
d.set(1,6,1,"repeater",facing="west",delay=4)
d.set(0,6,1,"observer",facing="west"); d.set(-1,6,1,"observer",facing="west"); d.set(-2,6,1,"observer",facing="down")
d.set(3,5,1,"observer",facing="up")
d.set(3,4,1,"observer",facing="up")
d.set(4,4,1,"observer",facing="west"); d.set(4,4,0,"observer",facing="south")
d.set(2,4,1,"observer",facing="east"); d.set(1,4,1,"stone")
d.save("d4.json")
