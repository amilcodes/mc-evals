from build3 import make
d=make()
lab=Lab(d,walls=True)
print(lab.lost)
lab.rest()
print(lab.doorway())
lab.flip(-3,-2,3); lab.rest(); print("closed?", lab.doorway())
lab.flip(-3,-2,3); lab.rest(); print("open?", lab.doorway())
print(lab.view(z=0).split("legend")[0])
