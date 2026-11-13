d = Design()
d.set(4,1,0,"sticky_piston",facing="west"); d.set(3,1,0,"stone")
d.set(4,2,0,"sticky_piston",facing="west"); d.set(3,2,0,"stone")
# tower z=+1
d.set(4,-2,1,"stone"); d.set(4,-1,1,"redstone_torch"); d.set(4,0,1,"stone"); d.set(4,1,1,"redstone_torch")
d.set(5,-2,1,"lever",face="wall",facing="east")
# tower z=-1 for R2
d.set(4,-1,-1,"stone"); d.set(4,0,-1,"redstone_torch"); d.set(4,1,-1,"stone"); d.set(4,2,-1,"redstone_torch")
d.set(5,-1,-1,"lever",face="wall",facing="east")
lab=Lab(d, walls=True)
print(lab.lost)
lab.rest()
def show():
    print([ (p,lab.block(*p)[:30]) for p in [(4,-1,1),(4,1,1),(4,0,-1),(4,2,-1),(3,1,0),(4,1,0),(3,2,0),(4,2,0)]])
show()
lab.flip(5,-2,1); lab.flip(5,-1,-1); lab.rest(); show()
lab.flip(5,-2,1); lab.flip(5,-1,-1); lab.rest(); show()
