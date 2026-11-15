import random
def evalline(XN, delays):
    # delays: dict pos->d (0 = dust). returns times of each element output
    t=0; T={}
    for p in ORDER:
        if p in ((XN,1),(XN,0)) or p in ((-7,1),(-7,0)): T[p]=t; continue
        t+=2*delays[p]; T[p]=t
    return T
def tsearch(XN, tm, NL, m, nt, iters=20000):
    reps=[p for p in ORDER if p not in ((XN,1),(XN,0),(-7,1),(-7,0))]
    taps=set(tm.values())
    for _ in range(iters):
        dl={}
        for p in reps:
            dl[p]=random.randint(1,4) if p in taps else random.randint(0,4)
        # forbid dust both legs same x
        if any(dl.get((x,1),1)==0 and dl.get((x,0),1)==0 for x in range(-6,1)): continue
        T=evalline(XN,dl)
        A1=T[tm['A1']]+16+2*NL['A1']; A4=T[tm['A4']]+16+2*NL['A4']; A7=T[tm['A7']]+16+2*NL['A7']
        B3=T[tm['B3']]+10+2*NL['B3']; B5=T[tm['B5']]+10+2*NL['B5']
        N1=T[(XN,1)]; N2=T[(XN,0)]
        Cto=N1+4+2*nt; Cbo=N1+4+2*m; Ctc=N2+4+2*nt; Cbc=N2+4+2*m
        if min(Cto,Cbo)>=A1+6 and max(Cto,Cbo)<=B3-4 and 6<=A4-B3<=8 and 6<=B5-A4<=8 and min(Ctc,Cbc)>=B5+6 and A7>=max(Ctc,Cbc)+4:
            return dl,dict(A1=A1,Cto=Cto,Cbo=Cbo,B3=B3,A4=A4,B5=B5,Ctc=Ctc,Cbc=Cbc,A7=A7)
    return None
