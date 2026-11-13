Z=10
for face in ("west","east"):
    d=Design()
    if face=="west":
        for x in range(0,4): d.set(x,0,Z,"stone")
        ps=range(4,8)
    else:
        for x in range(12,16): d.set(x,0,Z,"stone")
        ps=range(8,12)
    for x in ps: d.set(x,0,Z,"piston",facing=face)
    for x in range(-1,17): d.set(x,1,Z,"stone")
    for x in range(-1,17): d.set(x,2,Z,"redstone_wire")
    d.set(17,1,Z,"stone"); d.set(17,2,Z,"lever",face="floor",facing="north")
    d.set(17,2,Z,"lever",face="floor",facing="north")
    lab=Lab(d); lab.flip(17,2,Z); lab.rest(max_ticks=100)
    print(face, lab.view(z=Z).split("\n")[3:9])
