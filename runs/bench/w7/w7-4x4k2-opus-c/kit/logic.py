from pdbuild import Design
W="redstone_wire"
def left_logic(d):
    s=d.set
    s(-3,6,-2,"observer",facing="up"); s(-2,6,-2,"note_block")
    s(-1,6,-2,"repeater",facing="east",delay=4); s(0,6,-2,W); s(1,6,-2,"stone")
    s(-3,6,-1,W); s(-2,6,-1,"observer",facing="east"); s(-1,6,-1,"observer",facing="up")
    s(0,6,-1,"glass"); s(1,6,-1,"glass")
    s(-3,7,-2,"observer",facing="up"); s(-2,7,-2,W); s(-1,7,-2,"stone"); s(0,7,-2,"stone"); s(1,7,-2,W)
    s(-3,7,-1,"observer",facing="up"); s(-2,7,-1,"repeater",facing="south",delay=4)
    s(-1,7,-1,W); s(0,7,-1,W); s(1,7,-1,W)
    s(-2,7,0,"stone"); s(-3,7,0,"stone"); s(-4,7,0,"stone"); s(-4,7,-1,"stone")
    s(-3,8,-2,"observer",facing="up"); s(-2,8,-2,"stone"); s(-1,8,-2,"stone"); s(0,8,-2,W)
    s(-4,8,-2,"stone")
    s(-3,8,-1,"observer",facing="up")
    s(-4,8,-1,"repeater",facing="north",delay=4)   # R5
    s(-4,8,0,W); s(-3,8,0,"repeater",facing="west",delay=4)  # R6
    s(-2,8,0,W)
    s(-2,8,-1,"observer",facing="down")            # W1 watches C_l rep
    s(-3,9,-2,"repeater",facing="east",delay=4)    # R2
    s(-2,9,-2,"repeater",facing="east",delay=4)    # R1
    s(-1,9,-2,W); s(-4,9,-2,W)
    s(-3,9,-1,"observer",facing="up")
    s(-2,9,-1,"observer",facing="down")            # W2
    s(-2,10,-1,"observer",facing="down")           # W3
    s(-1,10,-1,"observer",facing="west")           # W3a
    s(-1,10,-2,"observer",facing="south")          # W3b
    s(-2,10,-2,"observer",facing="east")           # W3c
    s(-3,10,-2,"observer",facing="east")           # W3d
    s(-3,10,-1,"observer",facing="north")          # W4
    return d
def left_half():
    import door2, importlib; importlib.reload(door2)
    d=Design("closed"); door2.mech_left(d); d.remove(-1,-2,0)
    left_logic(d)
    d.set(1,6,-3,"lever",face="wall",facing="north")
    return d
