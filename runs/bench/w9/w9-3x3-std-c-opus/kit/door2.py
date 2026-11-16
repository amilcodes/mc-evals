exec(open("door.py").read())
# remove old lever/chain
for p in [(-7,0,-3),(-7,1,-3),(-7,1,-2),(-7,0,-2),(-8,1,-1),(-8,0,-1),(-8,1,-3),(-8,0,-3),(-9,1,-3),(-9,0,-3),
          (-9,2,-4),(-9,1,-4),(-9,3,-5),(-9,2,-5),(-9,4,-6),(-9,3,-6),(-9,5,-7),(-9,4,-7)]:
    D.remove(*p)
for x in range(-8,0): D.remove(x,5,-7); D.remove(x,4,-7)
for z in (-6,-5): D.remove(-5,5,z); D.remove(-5,4,z)
for x in (-5,-4,-3): D.remove(x,5,-4); D.remove(x,4,-4)
# lever + K'
S(-4,3,-2); D.set(-4,4,-2,"lever",face="floor",facing="north")
D.set(-3,3,-2,"redstone_wall_torch",facing="east")
D.set(-2,3,-2,"comparator",facing="north",mode="subtract"); S(-2,2,-2)
R(-2,3,-1,"north"); S(-2,2,-1)
D.set(-2,2,0,"sticky_piston",facing="east")
# A_trig from lever
R(-5,3,-2,"east"); S(-5,2,-2); W(-6,3,-2); S(-6,2,-2); W(-7,2,-2); S(-7,1,-2)
R(-6,3,-3,"north"); S(-6,2,-3)
# chain
R(-4,3,-3,"south"); S(-4,2,-3)
for z in (-4,-5,-6): R(-4,3,z,"south",4); S(-4,2,z)
W(-4,3,-7); S(-4,2,-7)
for z in (-8,-9,-10,-11): R(-4,3,z,"south",4); S(-4,2,z)
W(-4,3,-12); S(-4,2,-12)
# L24 to P line
W(-3,4,-7); S(-3,3,-7); W(-2,5,-7); S(-2,4,-7)
for z in (-6,-5): W(-2,5,z); S(-2,4,z)
# L_late
for x in (-5,-6,-3,-2): W(x,3,-12); S(x,2,-12)
for z in range(-11,-3): W(-6,3,z); S(-6,2,z)
for z in range(-11,-2): W(-2,3,z); S(-2,2,z)
# simple pistons
for x in (0,1,2):
    D.set(x,-2,0,"sticky_piston",facing="up"); R(x,-2,1,"south"); S(x,-3,1)
    W(x,-2,2); S(x,-3,2)
for x in (1,2):
    D.set(x,4,0,"sticky_piston",facing="down"); R(x,4,1,"south"); W(x,4,2)
D.set(4,1,0,"sticky_piston",facing="west"); R(4,1,1,"south"); S(4,0,1)
# bus from (-4,1,2) down to bottom
W(-4,1,3); S(-4,0,3); W(-3,0,3); S(-3,-1,3); W(-2,-1,3); S(-2,-2,3); W(-1,-2,3); S(-1,-3,3)
W(-1,-2,2); S(-1,-3,2)
R(3,-2,2,"west"); S(3,-3,2); W(4,-2,2); S(4,-3,2)
W(5,-1,2); S(5,-2,2); W(5,0,3); S(5,-1,3); D.set(5,0,2,"glass")
W(5,1,2); W(4,1,2); S(4,0,2)
D.set(5,1,3,"glass"); W(5,2,3); D.set(5,2,2,"glass"); W(5,3,2); D.set(5,3,3,"glass"); W(5,4,3)
W(4,4,3); S(4,3,3); W(4,4,2); S(4,3,2); W(3,4,2); S(3,3,2)
D.save("door2.json")
