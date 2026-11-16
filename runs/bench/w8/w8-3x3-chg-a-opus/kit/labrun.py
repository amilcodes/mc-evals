lab=Lab(D, walls=True); print("lost", lab.lost)
print(lab.rest(), lab.doorway(), lab.entity)
for k in range(4):
    t0=lab.t; lab.flip(*LEVER)
    seq=[]
    for i in range(24):
        lab.step(5); seq.append(lab.doorway())
    r=lab.rest(300)
    print("flip",k+1, "rest",r, "door", lab.doorway(), "ent", lab.entity, "t", lab.t-t0)
    print("  ", seq[::2])
