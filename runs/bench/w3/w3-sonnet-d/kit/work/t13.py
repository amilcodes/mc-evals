exec(open('work/build3.py').read())
d=make3()
lab=Lab(d,walls=True)
print(lab.lost)
LT=(-2,1,6)
lab.rest()
def rows():
    out=[]
    for y in (3,2,1,0):
        r=''
        for x in range(-4,4):
            b=lab.block(x,y,0)
            if b=='air': r+='.'
            elif b=='stone': r+='#'
            elif 'sticky_piston' in b: r+= ('P' if 'extended=false' in b else 'E')
            elif 'piston_head' in b: r+='h'
            elif 'observer' in b: r+='o'
            elif 'moving' in b: r+='m'
            else: r+='?'
        out.append(r)
    return ' '.join(out)
lab.flip(*LT)
for k in range(0,16):
    lab.step(8); print(lab.t,lab.doorway(),rows())
lab.rest(); print('closed',lab.doorway())
lab.flip(*LT); t0=lab.t
for k in range(0,20):
    lab.step(8); print(lab.t-t0,lab.doorway(),rows())
lab.rest(); print('open',lab.doorway())
