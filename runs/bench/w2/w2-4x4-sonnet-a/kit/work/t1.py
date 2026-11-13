# one row y=0 : W pulse chain (non-sticky pistons) P1..P4, stones a..d, test closing pulses
d = Design()
y=0
# rest: P1 -8, P2 -7, P3 -6, P4 -5 facing east; stones -4..-1
for i,x in enumerate(range(-8,-4)):
    d.set(x,y,0,"piston",facing="east")
for x in range(-4,0):
    d.set(x,y,0,"stone")
# levers above each piston: lever on floor of a stone at y+1? piston top: use stone block above at y=1 and lever on it
for i,x in enumerate(range(-8,-4)):
    d.set(x,1,0,"stone")
    d.set(x,2,0,"lever",face="floor",facing="north")
lab = Lab(d)
print(lab.view(z=0))
def pulse(x):
    lab.flip(x,2,0); lab.step(4); lab.flip(x,2,0); lab.step(4)
for x in range(-8,-4):
    pulse(x)
    print(x, lab.view(z=0).split("\n")[0:0])
print(lab.view(z=0))
