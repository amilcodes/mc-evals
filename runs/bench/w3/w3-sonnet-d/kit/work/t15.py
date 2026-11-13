exec(open('work/build6.py').read())
d=make6()
lab=Lab(d,walls=True)
LT=(-3,1,4)
lab.flip(*LT); lab.rest()
lab.flip(*LT); lab.rest()
for p in [(4,1,0),(4,2,0),(4,3,0),(4,3,1),(3,1,0),(2,1,0),(4,0,0),(5,1,0),(4,2,1),(3,2,0)]:
    print(p,lab.block(*p))
