from build3 import make
d=make()
lab=Lab(d,walls=True); lab.rest()
lab.flip(-3,-2,3)
watch=[(-3,6,1),(-3,6,2),(-2,6,1),(-3,6,0),(-1,6,1),(0,6,1),(1,6,1),(1,6,0),(-3,6,3),(-3,6,-1),(-3,6,-4),(3,3,-1),(3,3,1)]
for i in range(30):
    c=lab.step(1)
    for e in c:
        if (e[1][0],e[1][1],e[1][2]) in watch:
            print(e[0]-lab.t+30 if False else e[0], e[1], e[3][:60])
