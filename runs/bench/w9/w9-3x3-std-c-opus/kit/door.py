D = Design("open")
S = lambda x,y,z: D.set(x,y,z,"stone")
W = lambda x,y,z: D.set(x,y,z,"redstone_wire")
def R(x,y,z,f,d=1): D.set(x,y,z,"repeater",facing=f,delay=d)
# frame statics
for p in [(-1,0,0),(3,2,0),(3,0,0)]: S(*p)
# door storage blocks (open)
for p in [(-1,1,0),(0,3,0),(-1,2,0),(1,3,0),(2,3,0),(3,1,0),(0,-1,0),(1,-1,0),(2,-1,0)]: S(*p)
# A-DPE
D.set(-3,1,0,"sticky_piston",facing="east"); D.set(-2,1,0,"sticky_piston",facing="east")
R(-2,1,-1,"west"); S(-2,0,-1)
S(-2,0,0); R(-3,0,0,"west"); S(-3,-1,0)
W(-5,1,-1); S(-5,0,-1); W(-4,1,-1); S(-4,0,-1); W(-3,1,-1); S(-3,0,-1)
W(-4,0,0); S(-4,-1,0)
D.set(-4,1,0,"observer",facing="east")       # OA2 watches T_A
W(-5,1,0); S(-5,0,0)
D.set(-6,1,-1,"observer",facing="west")      # OA1 watches A_trig
R(-3,1,1,"south"); S(-3,0,1)
# lever and A_trig
S(-7,0,-3); D.set(-7,1,-3,"lever",face="floor",facing="north")
R(-7,1,-2,"north"); S(-7,0,-2)
for z in (-1,0,1,2): W(-7,1,z); S(-7,0,z)
R(-6,1,2,"west",4); S(-6,0,2)
for x in (-5,-4,-3): W(x,1,2); S(x,0,2)
R(-8,1,-1,"west"); S(-8,0,-1)   # L48 into A_trig, input (-9,1,-1)
# delay chain: L -> (-9,1,-3) staircase up north to y5 z-7
R(-8,1,-3,"east"); S(-8,0,-3)
W(-9,1,-3); S(-9,0,-3)
W(-9,2,-4); S(-9,1,-4); W(-9,3,-5); S(-9,2,-5); W(-9,4,-6); S(-9,3,-6); W(-9,5,-7); S(-9,4,-7)
for x in (-8,-7,-6): R(x,5,-7,"west",4); S(x,4,-7)
W(-5,5,-7); S(-5,4,-7)
for x in (-4,-3,-2): R(x,5,-7,"west",4); S(x,4,-7)
W(-1,5,-7); S(-1,4,-7)   # L48
# P_trig line from (-5,5,-7) south to z-4 then east to x=0
for z in (-6,-5,-4): W(-5,5,z); S(-5,4,z)
for x in (-4,-3,-2,-1,0): W(x,5,-4); S(x,4,-4)
# P-DPE
D.set(0,5,0,"sticky_piston",facing="down"); D.set(0,4,0,"sticky_piston",facing="down")
R(0,4,-1,"north")             # on wall (0,3,-1)
S(0,4,-2); W(0,5,-2)
D.set(0,5,-3,"observer",facing="north")   # OP1
D.set(0,5,-1,"observer",facing="south")   # OP2 watches T_P
# T_P via QC: branch from (-2,5,-4)
R(-2,5,-3,"north",4); S(-2,4,-3)
W(-2,5,-2); S(-2,4,-2)
W(-2,6,-1); S(-2,5,-1)
W(-2,6,0); S(-2,5,0)
R(-1,6,0,"west"); S(-1,5,0)
D.save("door.json")
