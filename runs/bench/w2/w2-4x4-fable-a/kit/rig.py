exec(open('build.py').read())
d = door("open")
d.set(1,5,-3,"redstone_wire"); d.set(1,5,-2,"observer",facing="north"); d.set(1,5,-4,"stone"); d.set(1,6,-4,"lever",face="floor",facing="north")
d.set(1,5,3,"repeater",facing="south"); d.set(1,5,4,"stone"); d.set(1,6,4,"lever",face="floor",facing="north")
d.set(1,6,1,"stone"); d.set(1,7,1,"lever",face="floor",facing="north")
d.set(-1,-2,0,"stone"); d.set(-1,-3,0,"lever",face="ceiling",facing="north")
d.set(4,-2,0,"stone"); d.set(4,-3,0,"lever",face="ceiling",facing="north")
F=(1,6,-4); R=(1,6,4); U=(1,7,1); UB1=(-1,-3,0); UB2=(4,-3,0)
lab = Lab(d, walls=True)
print("lost", lab.lost)
def show(tag=""):
    print(tag, "t=%d"%lab.t, lab.doorway(), sorted((p[0],p[1],s.split('[')[0][:6]) for p,s in lab.blocks().items() if p[2]==0 and -3<=p[0]<=1 and -1<=p[1]<=4 and s!='air' and 'observer' not in s and 'repeater' not in s))
def act(lev, n=12, verbose=False, zf=None):
    t0=lab.t
    lab.flip(*lev)
    ch=lab.step(n)
    if verbose:
        for t,p,b,a in ch:
            if 'wire' not in a and p[0]<2: print("   +%d"%(t-t0), p, b.split('[')[0], "->", a)
def Uf(n=14, v=False):
    lab.flip(*UB1); lab.flip(*UB2); act(U, n, v)
