exec(open('work/build8.py').read())
d=make8()
lab=Lab(d,walls=True)
lab.flip(-3,1,4); lab.rest()
for p in [(3,4,2),(4,4,2),(4,3,3),(4,2,4),(4,1,5),(4,1,4),(4,1,3),(4,1,2),(4,1,1)]:
    print(p,lab.block(*p))
