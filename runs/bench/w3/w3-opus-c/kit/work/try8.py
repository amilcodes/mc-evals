import sys; sys.path.insert(0,'.'); sys.path.insert(0,'work')
import build5
for seed in range(4):
    try:
        B,t = build5.build(bounds=((-5,4),(-2,4),(-2,0)), seed=seed)
    except Exception as e:
        print("fail", seed, e, flush=True); continue
    B.d.save("work/d8.json"); print("OK", seed, B.d.bbox(), flush=True); break
