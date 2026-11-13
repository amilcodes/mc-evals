exec(open('work/t10.py').read().split("import sys")[0])
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
sched={24:'R',30:'Q',36:'R',42:'Q'}
for k in range(0,60):
    if k in sched:
        lab.flip(*(LR if sched[k]=='R' else LQ))
    if k-2 in sched and sched[k-2]=='Q': lab.flip(*LQ)
    lab.step(1)
    if k%3==0: print(k,rows())
