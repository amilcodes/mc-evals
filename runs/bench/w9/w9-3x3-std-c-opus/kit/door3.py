exec(open("door2.py").read())
D.remove(-3,3,-2); D.remove(-2,3,-2); D.remove(-2,3,-1)
W(-2,3,-2)   # support (-2,2,-2) exists
D.set(-2,3,-1,"comparator",facing="north",mode="subtract")   # support (-2,2,-1)
D.set(-4,3,-1,"redstone_wall_torch",facing="south")
W(-3,3,-1); D.set(-3,2,-1,"glass")
D.save("door3.json")
