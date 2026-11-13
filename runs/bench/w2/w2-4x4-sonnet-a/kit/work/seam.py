from pdbuild import Design
import sys
blk = sys.argv[1]
d = Design("open")
for i in range(4):
    for (x,y) in [(-1,i),(4,i),(i,-1),(i,4)]:
        d.set(x,y,0,blk)
d.set(8,0,0,"stone"); d.set(8,1,0,"lever",face="floor",facing="north")
d.save("work/seam_%s.json"%blk)
