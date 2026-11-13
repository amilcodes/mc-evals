exec(open('work/build2.py').read())
d=make2()
lab=Lab(d,walls=True)
print(lab.lost)
for z in (5,3,0,-1):
    print(lab.view(z=z).split('legend')[0])
