def mk():
    d = Design()
    d.set(0,0,10,"sticky_piston",facing="east")
    d.set(1,0,10,"stone")
    d.set(0,1,10,"stone")
    d.set(0,2,10,"lever",face="floor",facing="north")
    return d
for w in (1,2,3,4,5):
    lab = Lab(mk())
    lab.flip(0,2,10)
    lab.step(w)
    lab.flip(0,2,10)
    lab.step(10)
    bl = lab.blocks()
    xs = sorted(p[0] for p,s in bl.items() if p[1]==0 and p[2]==10)
    print("pulse",w,[ (p[0],s.split('[')[0]) for p,s in sorted(bl.items()) if p[1]==0 and p[2]==10])
