RD=3;SD=[4,4,4];KD=[4,4,2]
exec(open("door10.py").read())
for p in list(d.blocks):
    if p[0]==5: d.remove(*p)
d.remove(4,4,5); d.remove(4,3,5)
S(4,2,5); S(4,3,5,W); S(4,1,4); S(4,2,4,W); S(4,3,4,"glass")
d.save("door11.json")
