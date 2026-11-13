from build1 import make
d=make()
lab=Lab(d,walls=True)
print(lab.lost); lab.rest()
def rows():
    print(lab.view(z=0).split("legend")[0])
rows()
lab.flip(-3,-2,3); lab.rest(); rows()
lab.flip(-3,-2,3); lab.rest(); rows()
print(lab.block(-3,2,1))
