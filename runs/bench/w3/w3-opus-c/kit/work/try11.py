import sys; sys.path.insert(0,'.'); sys.path.insert(0,'work')
import build6w as m
for seed in range(4):
    try:
        B,t = m.build(bounds=((-5,4),(-2,4),(-2,0)), seed=seed)
    except Exception as e:
        print("fail", seed, e, flush=True); continue
    B.d.save("work/d11.json"); print("OK", B.d.bbox(), flush=True); break
