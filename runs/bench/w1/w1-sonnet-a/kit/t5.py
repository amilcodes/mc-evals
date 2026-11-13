def run_spaced(seq, spacing):
    # seq: list of lever positions; pulse of 2 ticks at times 0, spacing, 2*spacing ...
    t=0
    events=[]
    for i,p in enumerate(seq):
        events.append((i*spacing,'on',p)); events.append((i*spacing+2,'off',p))
    events.sort(key=lambda e:(e[0], 0 if e[1]=='off' else 1))
    cur=0
    for tt,kind,p in events:
        if tt>cur: lab.step(tt-cur); cur=tt
        lab.flip(*p)
    lab.step(10)
    print(row())
# B position depends on state, so give both levers each time: pulse both B1 and B2 levers when B pulse
def Bp(): return [B1,B2]
d2 = d
lab = Lab(d2)
# closing: B,V,A,A  using spacing
def seqrun(names, spacing):
    cur=0; ev=[]
    for i,n in enumerate(names):
        ps={'A':[A],'B':[B1,B2],'V':[V]}[n]
        for p in ps:
            ev.append((i*spacing,1,p)); ev.append((i*spacing+2,0,p))
    ev.sort(key=lambda e:(e[0],e[1]))
    for tt,k,p in ev:
        if tt>cur: lab.step(tt-cur); cur=tt
        lab.flip(*p)
    lab.step(12)
    print(row())
for sp in (4,):
    lab=Lab(d2)
    print("spacing",sp,"closing B,V,A,A"); seqrun("BVAA",sp)
    print("opening B,V,A,B,A,B"); seqrun("BVABAB",sp)
