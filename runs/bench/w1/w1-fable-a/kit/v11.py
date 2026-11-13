def v11(dl=(2,1,1), **kw):
    d = v9(cross=False, dl=dl, **kw)
    d.set(3,-2,0,"target")
    rep(d,3,1,"east",1)
    dust(d,4,0)
    return d
d11 = v11(); d11.save("v11.json")
r = test(d11); print(r.text[:700])
if not r.valid: show(d11, keys=["(3,-1,0)","(2,-1,0)","(3,-2,1)","(1,-1,0) ","(1,-2,1)","(1,-2,0)","(2,-2,1)","(4,-2,0)"], width=170)
else: print(robust(d11,(-2,4,1)))
