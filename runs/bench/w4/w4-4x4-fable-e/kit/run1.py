exec(open("build.py").read())
d=full()
b=check(d)
print(len(d.blocks), d.bbox()); 
for x in b: print(x)
d.save("door1.json")
