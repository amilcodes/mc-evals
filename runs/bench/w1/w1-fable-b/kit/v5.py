exec(open('v4.py').read().split("d4 = build4()")[0])
def build5(rw=4, r1=1, rx=4, rd=4):
    d = build4(rw, r1, rx, rd)
    # move R_w below the board; Obs_L takes its place watching the lever
    d.remove(-1,-3,1); d.remove(-1,-4,1)
    d.set(-1,-5,1,"stone"); d.set(-1,-4,1,"repeater",facing="east",delay=rw)
    d.set(-1,-3,1,"observer",facing="east")
    return d
d5 = build5(); d5.save("v5.json")
r = test(d5); print(r)
