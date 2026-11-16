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
put(-2,0,1,"stone"); put(-2,1,1,"redstone_wire",north="side",south="side",east="side",west="side")
put(-3,0,1,"observer",facing="west")             # O_P watches R_P, outputs into (-2,0,1)
rep(-4,0,1,"west",2)                              # R_P
dust(-5,0,1); dust(-6,0,1)
# --- W cluster (z=0) ---
put(-4,1,0,"stone")                                # W power block
rep(-5,1,0,"west",1)                               # SR
dust(-6,1,0)
rep(-6,1,-1,"north",4)                             # ST (input from z=-2)
# --- z=-2 control plane ---
put(-9,-2,-2,"stone"); put(-9,-1,-2,"lever",face="floor",facing="north")
rep(-8,-2,-2,"west",4); rep(-7,-2,-2,"west",4); rep(-6,-2,-2,"west",4)
dust(-5,-2,-2); rep(-4,-2,-2,"west",2); dust(-3,-2,-2)
put(-8,-1,-2,"observer",facing="west")            # O_T1 watches lever
put(-7,-1,-2,"stone"); dust(-7,0,-2,sup=None)
put(-6,-1,-2,"observer",facing="down")            # O_T2 watches c3
put(-6,0,-2,"stone"); dust(-6,1,-2,sup=None)
# short delivery
dust(-5,-2,-1); dust(-5,-2,0)
rep(-4,-2,0,"west",1); put(-3,-2,0,"stone"); rep(-2,-2,0,"west",1); put(-1,-2,0,"stone")  # D
# long delivery
rep(-3,-2,-1,"north",1)
# late2 climb to V
dust(-2,-1,-2); put(-3,-1,-2,"glass"); dust(-3,0,-2,sup=None); put(-2,0,-2,"glass"); dust(-2,1,-2,sup=None)
rep(-2,1,-1,"north",1)
# --- S line to right ---
dust(-1,-2,1); dust(0,-2,1); rep(1,-2,1,"west",1); dust(2,-2,1); dust(3,-2,1)
dust(3,-2,0); dust(4,-2,0); dust(4,-2,-1)
rep(3,-2,-1,"east",1); put(2,-2,-1,"stone"); put(1,-2,-1,"redstone_wire",north="side",south="side",east="side",west="side"); put(1,-3,-1,"stone")
# right climb
cl=[((4,-1,1),(4,-2,1)),((4,0,0),(4,-1,0)),((4,1,1),(4,0,1)),((5,2,1),(5,1,1)),((4,3,1),(4,2,1)),((4,4,0),(4,3,0))]
for dp,gp in cl:
    put(*gp,"glass"); put(*dp,"redstone_wire")
put(3,3,0,"stone"); put(3,4,0,"redstone_wire")
for x in range(0,3): put(x,5,0,"redstone_wire")
LEVER=(-9,-1,-2)
D.save("v1.json")
print("blocks", len(D.blocks), D.bbox())
