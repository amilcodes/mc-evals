exec(open("v3.py").read().split("v3=build3()")[0])
def build4():
    d=build3()
    d.set(-2,3,0,"glass"); d.set(-2,4,0,"redstone_wire")
    d.set(-2,5,0,"observer",facing="down")
    return d
v4=build4(); v4.save("v4.json")
