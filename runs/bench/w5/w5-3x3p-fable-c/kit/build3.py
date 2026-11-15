exec(open("build2.py").read().split("d2 = build2()")[0])
def build3():
    d = build2()
    W = "redstone_wire"
    for z in (1,-1):
        d.set(3,3,z,W); d.set(2,4,z,W)
    return d
d3 = build3(); d3.save("d3.json")
print(d3.bbox())
print(trace(d3, flips=2, limit=0))
