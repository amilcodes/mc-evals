exec(open('work/build2.py').read())
d=make2()
lab=Lab(d,walls=True)
lab.rest()
lab.flip(-2,1,6)
for i in range(8):
    lab.step(8); print(lab.t, lab.doorway())
lab.rest(); print('closed', lab.doorway())
print(lab.view(z=0).split('legend')[0])
