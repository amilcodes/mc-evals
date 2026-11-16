d=build()
for p in [(1,7,0),(2,7,0),(1,6,0),(2,6,0),(6,6,1),(6,5,1),(7,6,1),(8,6,1),(8,7,1),(7,7,1),(6,7,1),(5,7,1),(4,7,1),(4,6,1)]:
    d.remove(*p)
d.set(2,6,0,"redstone_wire")              # aims west into (1,6) -> B QC
d.set(4,6,1,"repeater",facing="west",delay=4)   # input from (3,6,1), output east into (5,6,1)
d.set(0,6,1,"observer",facing="down")
d.set(1,6,1,"observer",facing="west"); d.set(2,6,1,"observer",facing="west"); d.set(3,6,1,"observer",facing="west")
d.save("d2.json")
