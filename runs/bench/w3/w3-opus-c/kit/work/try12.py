import sys, importlib; sys.path.insert(0,'.'); sys.path.insert(0,'work')
mod, x0, x1, y1, seeds = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
m=importlib.import_module(mod)
for seed in range(seeds):
    try:
        B,t = m.build(bounds=((x0,x1),(-2,y1),(-2,0)), seed=seed)
    except Exception as e:
        print("fail", mod, seed, str(e)[:40], flush=True); continue
    fn=f"work/r_{mod}_{x0}_{x1}_{y1}.json"; B.d.save(fn); print("OK", fn, B.d.bbox(), flush=True); break
