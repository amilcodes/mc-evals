def v10(**kw):
    d = v9(cross=False, **kw)
    d.set(3,-2,0,"target")
    return d
d10 = v10(); d10.save("v10.json")
r = test(d10); print(r.text[:700])
if not r.valid: show(d10, keys=["(3,-1,0)","(2,-1,0)","(3,-2,1)","(1,-1,0) ","(1,-2,1)","(1,-2,0)"], width=200)
else: print(robust(d10,(-2,4,1)))
