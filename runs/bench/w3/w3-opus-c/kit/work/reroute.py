import sys, json; sys.path.insert(0,'.'); sys.path.insert(0,'work')
from gen import *
D6={"east":(1,0,0),"west":(-1,0,0),"up":(0,1,0),"down":(0,-1,0),"south":(0,0,1),"north":(0,0,-1)}
d=json.load(open('work/best216.json'))
blk={tuple(b['pos']):(b['id'],b.get('props',{})) for b in d['blocks']}
obs={p:add(p,D6[pr['facing']]) for p,(i,pr) in blk.items() if i=='observer'}
watchers={}
for o,w in obs.items(): watchers.setdefault(w,[]).append(o)
lever=[p for p,(i,_) in blk.items() if i=='lever'][0]
# times
t={}
for o,w in obs.items():
    if w==lever: t[o]=2
changed=True
while changed:
    changed=False
    for o,w in obs.items():
        if o not in t and w in t and blk.get(w,('',))[0]=='observer':
            t[o]=t[w]+2; changed=True
def chain_back(end):
    ch=[end]; c=end
    while True:
        w=obs[c]
        if w in obs and len(watchers.get(w,[]))==1 and w not in [o for o in obs if obs[o]==lever]:
            ch.append(w); c=w
        else: break
    return ch, obs[ch[-1]]
ends={'L6':(-2,2,0),'D':(-1,4,-1)}
info={}
for k,e in ends.items():
    ch,src=chain_back(e)
    info[k]=(ch,src)
    print(k,'len',len(ch),'src',src,'t_end',t.get(e),'t_src',t.get(src), 'ys',sorted(set(c[1] for c in ch)))
# RM feeder: observer whose back is (-3,3,-1)
for o,w in obs.items():
    back=sub(o,sub(w,o))
    if back==(-3,3,-1): print('RM feeder',o,t.get(o))
json.dump({'t':{str(k):v for k,v in t.items()}},open('work/times216.json','w'))

# remove L6 chain, D chain, and trunk to (-1,5,-1)
rm=set(info['L6'][0])|set(info['D'][0])
trunk,tsrc=chain_back((-1,5,-1))
keep=[]
for c in trunk:   # trunk is ordered from (-1,5,-1) backwards
    back=sub(c,sub(obs[c],c))
    if back in blk and blk[back][0]!='observer':
        break
    keep.append(c)
trunk=keep
rm|=set(trunk)
print('trunk',len(trunk),'from',tsrc, t.get(tsrc), 'removed',len(rm))
import random
best=None
for seed in range(16):
    B=Builder()
    for p,(i,pr) in blk.items():
        if p in rm: continue
        B.put(p,i,**pr)
    for o,w in obs.items():
        if o not in rm: B.fronts.add(w)
    B.reserved.add((-2,1,-2))
    times={o:v for o,v in t.items() if o not in rm}
    rnd=random.Random(seed)
    bounds=((-4,4),(-2,4),(-2,0))
    def do_route(dp,dd,ts):
        for tt in ts:
            srcs=sorted(times,key=lambda c:(rnd.random() if seed>=2 else 0,-times[c]))
            for s in srcs:
                n=(tt-times[s])//2
                if n<1: continue
                p=B.route(s,dp,dd,n,bounds)
                if p:
                    B.place_chain(s,p)
                    for k,c in enumerate(p): times[c]=times[s]+2*(k+1)
                    return tt
        raise Exception("noroute %s"%(dd,))
    try:
        # reserve L6 corridor during D routing
        if seed%2==0:
            do_route((-2,3,0),(-2,2,0),range(46,120,2))
            do_route((-1,4,-2),(-1,4,-1),[34])
        else:
            do_route((-1,4,-2),(-1,4,-1),[34])
            do_route((-2,3,0),(-2,2,0),range(46,120,2))
    except Exception as e:
        print('seed',seed,'fail',e); continue
    B.d.save('work/rr.json'); print('OK',B.d.bbox()); break
