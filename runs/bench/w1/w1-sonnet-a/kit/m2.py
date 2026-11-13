exec(open('m1.py').read().split("for nm,p in")[0])
lab = Lab(d, walls=True)
def cells():
    for y in (6,5,4,3,2,1):
        print(y, [ (x, lab.block(x,y,0)) for x in (0,1,2,3) if lab.block(x,y,0)!='air'])
for nm,p in [("B",LB),("V",LV),("A",LA)]:
    pulse(p)
print("after A1"); cells()
lab.flip(*LA); 
for i in range(10):
    ch=lab.step(1)
    print(lab.t,[c for c in ch if c[1][2]==0])
    if i==1: lab.flip(*LA)
cells()
