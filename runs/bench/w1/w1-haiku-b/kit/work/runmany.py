import sys, time
import sa2d
K=int(sys.argv[1]); seeds=range(int(sys.argv[2]), int(sys.argv[3])); iters=int(sys.argv[4])
box=((-2,3),(-2,3))
for s in seeds:
    t0=time.time()
    b = sa2d.run(s, box, K, iters)
    print(s, K, b[0], b[1], b[2], round(time.time()-t0,1), flush=True)
