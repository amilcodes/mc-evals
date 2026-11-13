exec(open('work/build9.py').read())
d=make9()
lab=Lab(d,walls=True)
print(lab.lost)
lab.flip(-3,2,4); lab.rest()
for p in [(-3,1,4),(-3,0,3),(-3,-1,2),(-2,-2,2),(-1,-2,2),(0,-2,2),(-3,1,3),(-2,2,3),(-2,3,2),(-1,4,2),(0,4,2)]:
    print(p,lab.block(*p))
