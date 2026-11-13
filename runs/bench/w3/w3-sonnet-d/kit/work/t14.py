exec(open('work/build3.py').read())
d=make3()
lab=Lab(d,walls=True)
print(lab.lost)
for p in [(-15,1,4),(-15,1,3),(-14,1,3),(-13,1,3),(-12,1,3),(-11,1,3),(-15,2,4),(-15,1,5),(-16,1,3),(-17,1,3)]:
    print(p,lab.block(*p))
