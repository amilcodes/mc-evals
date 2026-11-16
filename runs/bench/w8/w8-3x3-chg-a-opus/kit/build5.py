# Polarity A: lever on = closed. Initial open, everything retracted.
D = Design("open")
used = {}
def put(x,y,z,b,**p):
    if (x,y,z) in used: raise Exception(f"conflict at {(x,y,z)}: {used[(x,y,z)]} vs {b}")
    used[(x,y,z)] = b; D.set(x,y,z,b,**p)
def dust(x,y,z,sup="stone"):
    put(x,y,z,"redstone_wire");
    if sup: put(x,y-1,z,sup)
def rep(x,y,z,facing,delay=1,sup="stone"):
    put(x,y,z,"repeater",facing=facing,delay=delay)
    if sup: put(x,y-1,z,sup)
SP="sticky_piston"
# --- open-state frame stones ---
for p in [(0,-1,0),(1,-1,0),(2,-1,0),(3,0,0),(3,1,0),(3,2,0),(0,3,0),(1,3,0),(2,3,0),(-1,0,0),(-1,1,0),(-1,2,0)]:
    put(*p,"stone")
# pistons
for x in range(3): put(x,-2,0,SP,facing="up"); put(x,4,0,SP,facing="down")
put(4,1,0,SP,facing="west")
put(-1,-1,0,SP,facing="up")   # H2 (L goes down)
put(-2,1,0,SP,facing="east")  # V
put(-3,1,0,SP,facing="east")  # W
# --- P / V-high / V-low cross ---
# P at top: observers under dust at y=4
put(-2,3,0,"observer",facing="up"); put(-2,4,0,"redstone_wire")
put(-1,3,0,"observer",facing="up"); put(-1,4,0,"redstone_wire")
rep(-3,4,0,"west",1); put(-4,3,0,"glass"); put(-4,4,0,"redstone_wire")
dust(-5,3,0); put(-4,2,0,"redstone_wire")          # W-copy: dust on W power block
# --- W cluster (z=0) ---
put(-4,1,0,"stone")                                # W power block
rep(-5,1,0,"west",1)                               # SR
dust(-6,1,0)
rep(-6,1,-1,"north",4)                             # ST (input from z=-2)
# --- chain ---
put(-6,-2,0,"stone"); put(-7,-2,0,"lever",face="wall",facing="west")   # lever attached to LB (-6,-2,0)
dust(-5,-2,0)                                      # dot next to LB, watched by O_T1
put(-5,-1,0,"observer",facing="down")              # O_T1 -> SR support block (-5,0,0)
dust(-5,0,-1)                                      # trigger path up to (-5,1,-2)
rep(-6,-2,-1,"south",4); put(-6,-2,-2,"stone")    # c1 -> block
rep(-5,-2,-2,"west",4); rep(-4,-2,-2,"west",4); dust(-3,-2,-2)   # c2, c4, b
dust(-6,1,-2); dust(-5,1,-2,sup=None); put(-5,0,-2,"stone")
put(-4,0,-2,"observer",facing="east")            # O_T2 watches climb dust (-3,0,-2)
put(-3,-2,0,"stone"); rep(-2,-2,0,"west",1); put(-1,-2,0,"stone")  # OR blk, r2, D
rep(-3,-2,-1,"north",1)   # short (from b)
dust(-2,-1,-2); put(-3,-1,-2,"glass"); dust(-3,0,-2,sup=None); put(-2,0,-2,"glass"); dust(-2,1,-2,sup=None)
rep(-2,1,-1,"north",3)    # V
dust(-3,0,-1); rep(-2,-1,-1,"west",4); put(-1,-1,-1,"stone")   # long path into H2 from z=-1
# --- S line to right ---
dust(-1,-2,-1); dust(-1,-2,-2); put(-1,-1,-2,"stone")
dust(0,-2,-2); rep(1,-2,-2,"west",1); rep(2,-2,-2,"west",1); dust(3,-2,-2)
dust(4,-2,-1)
rep(3,-2,-1,"east",1); put(2,-2,-1,"stone"); put(1,-2,-1,"redstone_wire",north="side",south="side",east="side",west="side"); put(1,-3,-1,"stone")
# right climb x=4, z in {-1,-2}
put(4,-2,-2,"stone"); put(4,-1,-2,"redstone_wire")
for dp,gp in [((4,0,-1),(4,-1,-1)),((4,1,-2),(4,0,-2)),((4,2,-1),(4,1,-1))]:
    put(*gp,"glass"); put(*dp,"redstone_wire")
put(4,2,0,"stone"); put(4,3,0,"redstone_wire")
put(4,3,-1,"glass"); put(4,4,-1,"redstone_wire")
rep(3,4,-1,"east",1); put(2,4,-1,"stone"); put(1,4,-1,"redstone_wire",north="side",south="side",east="side",west="side"); put(0,4,-1,"stone")
LEVER=(-7,-2,0)
D.save(OUT)
print("blocks", len(D.blocks), D.bbox())
