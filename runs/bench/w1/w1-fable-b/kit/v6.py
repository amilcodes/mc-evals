exec(open('v4.py').read().split("d4 = build4()")[0])
def build6(rw=4, r1=1, rx=4, rd=4):
    d = build4(rw, r1, rx, rd)
    d.set(0,-3,1,"stone")                                  # Lb, strongly powered by the lever under it
    d.set(0,-4,1,"lever",face="ceiling",facing="north")
    d.set(-1,-4,1,"observer",facing="east")                # Obs_L watches the lever, supports R_w
    return d
d6 = build6(); d6.save("v6.json")
r = test(d6); print(r)
