def v8(p1d=4, cd=(4,4,4,1), hd=1):
    d = v7(p1d, cd, hd)
    d.set(1,-3,1,"stone"); d.set(1,-2,1,"stone")
    fl(d,2,1,"observer",facing="east"); dust(d,3,1); dust(d,4,1)
    return d
d8 = v8(); d8.save("v8.json")
r = test(d8); print(r.text[:900])
if not r.valid: show(d8, keys=KEYS+["(2,-2,0)","(1,-2,1)","(2,-2,1)","(0,-2,1)"])
else: print(robust(d8,(1,4,1)))
