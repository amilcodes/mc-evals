Z=10
def chain(sticky=False):
    d = Design()
    pt = "sticky_piston" if sticky else "piston"
    for x in range(0,4): d.set(x,0,Z,"stone")
    # Q4 4, O4 5, Q3 6, O3 7, Q2 8, O2 9, Q1 10
    for i,(q,o) in enumerate([(4,5),(6,7),(8,9)]):
        d.set(q,0,Z,pt,facing="west")
        d.set(o,0,Z,"observer",facing="east")
    d.set(10,0,Z,pt,facing="west")
    d.set(10,1,Z,"stone"); d.set(10,2,Z,"lever",face="floor",facing="north")
    return d
for sticky in (False,True):
    lab = Lab(chain(sticky))
    print(lab.lost)
    lab.flip(10,2,Z)
    lab.rest(max_ticks=100)
    print("sticky" if sticky else "normal", "t",lab.t)
    print(lab.view(z=Z))
