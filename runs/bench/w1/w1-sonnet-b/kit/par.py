import sys, json, time, multiprocessing as mp
from build import build
def work(args):
    ox,oy,oz,box,seed,TL,swap=args
    try:
        d,chain,taps=build(ox,oy,oz,swap=swap,box=box,seed=seed,TL=TL)
    except Exception as e:
        return (args,None,str(e))
    bb=d.bbox(); vol=(bb[1][0]-bb[0][0]+1)*(bb[1][1]-bb[0][1]+1)*(bb[1][2]-bb[0][2]+1)
    fn=f"P_{vol}_{oz}_{seed}_{abs(hash(str(box)))%1000}.json"
    d.save(fn)
    return (args,vol,fn)
if __name__=="__main__":
    jobs=[]
    cfgs=json.loads(sys.argv[1]); TL=int(sys.argv[2]); seeds=int(sys.argv[3])
    for c in cfgs:
        for s in range(seeds):
            jobs.append((c[0],c[1],c[2],tuple(c[3]),s,TL,True))
    with mp.Pool(int(sys.argv[4]) if len(sys.argv)>4 else 6) as p:
        for r in p.imap_unordered(work,jobs):
            print(r,flush=True)
