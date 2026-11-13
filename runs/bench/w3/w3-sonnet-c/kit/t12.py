for n in (2,3):
    lab=Lab(d); lab.rest()
    lab.flip(*LP); lab.step(4)
    print('n',n,'t',lab.t)
    ch=lab.flip(*LB); print('flip on',ch)
    for c in lab.step(n): print(c)
    ch=lab.flip(*LB); print('flip off',ch)
    for c in lab.step(8): 
        if c[1][1]==1 or c[1][1]>=2: print(c)
