src=open("t2.py").read().split("for n in [")[0]
exec(src)
def col():
    print([ (y,lab.block(0,y,0).split('[')[0][:8]+("E" if "extended=true" in lab.block(0,y,0) else "")) for y in range(-3,2)])
for n in ["Pr","Ar","Pr"]: go(n)
for n in ["Pc","Ac","Pc"]:
    n0=len(lab.history); t0=lab.t
    go(n); col()
    for h in lab.history[n0:]:
        if h[1][2]==0 and h[1][0] in (0,1,-1) and h[1][1]<2: print(h[0]-t0,h[1:])
