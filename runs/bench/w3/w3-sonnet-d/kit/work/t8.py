exec(open('work/build2.py').read())
d=make2()
lab=Lab(d,walls=True)
lab.flip(-2,1,6); lab.rest()
print(lab.doorway())
for p in [(-2,1,5),(-3,1,5),(-3,0,4),(-3,-1,3),(-3,-2,2),(-2,-2,2),(0,-2,2),(0,-2,1),(0,-2,0),(-2,4,2),(0,4,2),(-4,1,5)]:
    print(p,lab.block(*p))
