exec(open("build7.py").read())
d=full()
from collections import Counter
for ax,name in ((0,"x"),(1,"y"),(2,"z")):
    c=Counter(p[ax] for p in d.blocks)
    print(name, sorted(c.items()))
def show(ax,val):
    for p,b in sorted(d.blocks.items()):
        if p[ax]==val: print(p,b[0],b[1].get("facing",""))
print("--- y=6"); show(1,6)
print("--- z=4"); show(2,4)
