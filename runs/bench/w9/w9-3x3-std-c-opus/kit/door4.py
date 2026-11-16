exec(open("door3.py").read())
# remove old chain and lines
for z in range(-12,-2):
    for p in [(-4,3,z),(-4,2,z),(-6,3,z),(-6,2,z),(-2,3,z),(-2,2,z)]:
        if z <= -3 and not (p[0]==-6 and z==-3) and not (p[0]==-2 and z>=-3) and not (p[0]==-4 and z==-3 and False): D.remove(*p)
for x in (-5,-3): D.remove(x,3,-12); D.remove(x,2,-12)
for p in [(-3,4,-7),(-3,3,-7),(-2,5,-7),(-2,4,-7),(-2,5,-6),(-2,4,-6),(-2,5,-5),(-2,4,-5)]: D.remove(*p)
R(-4,3,-3,"south",4); S(-4,2,-3)
W(-4,3,-4); S(-4,2,-4)
for z in (-5,-6,-7): R(-4,3,z,"south",4); S(-4,2,z)
W(-4,3,-8); S(-4,2,-8)
W(-3,4,-4); S(-3,3,-4)
for x in (-5,-6,-3,-2): W(x,3,-8); S(x,2,-8)
for z in range(-7,-3): W(-6,3,z); S(-6,2,z)
for z in range(-7,-1): W(-2,3,z); S(-2,2,z)
D.save("door4.json")
