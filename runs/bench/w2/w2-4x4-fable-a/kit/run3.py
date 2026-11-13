exec(open('build3.py').read())
d = door3(); d.save("door3.json")
lab = Lab(d, walls=True)
print("lost", lab.lost)
def run(n=100, grep=None):
    t0=lab.t; lab.flip(*LEV); ch=lab.step(n)
    for t,p,b,a in ch:
        s="+%d %s %s -> %s"%(t-t0,p,b.split('[')[0],a)
        if grep is not None and any(g in s for g in grep): print("  ",s)
    print(lab.doorway(), lab.entity, "last change +%d"%(ch[-1][0]-t0) if ch else "")
