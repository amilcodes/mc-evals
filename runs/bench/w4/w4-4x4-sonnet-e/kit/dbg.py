import json
LEV={k:tuple(v) for k,v in json.load(open('m3lev.json')).items()}
lab=Lab('m3.json',walls=True)
def pistons():
    out=[]
    for p,s in sorted(lab.blocks().items(), key=lambda kv:(kv[0][0],kv[0][1])):
        if p[2]!=0 or not (-3<=p[1]<=3): continue
        n=s.split('[')[0]
        if n in('redstone_wire','observer','lever','stone','target'): 
            if n=='stone' and -1<=p[1]<=1 and 0<=p[0]<=3: out.append(f"({p[0]},{p[1]})S")
            continue
        out.append(f"({p[0]},{p[1]}){n[:3]}{'+' if 'extended=true' in s else ''}")
    return ' '.join(out)
def fire(n):
    if n=='P2f': lab.flip(*LEV['P2f'])
    else: lab.flip(*LEV['S1'+n]); lab.flip(*LEV['S2'+n])
    lab.rest()
    print(n, pistons())
