def mirror_props(props):
    p = dict(props)
    f = p.get("facing")
    if f in ("east","west"): p["facing"] = {"east":"west","west":"east"}[f]
    return p

def base():
    d = Design("open")
    L = []  # left-half parts, mirrored to right (x -> 3-x)
    def s(x,y,z,b,**pr): L.append((x,y,z,b,pr))
    # top-left unit
    s(0,4,0,"stone"); s(1,4,0,"stone")
    s(1,5,0,"sticky_piston",facing="down"); s(1,6,0,"sticky_piston",facing="down")
    s(-1,4,0,"sticky_piston",facing="east")
    s(1,5,1,"repeater",facing="south"); s(1,5,2,"redstone_wire")
    s(1,6,1,"glass"); s(1,7,1,"repeater",facing="south"); s(1,6,2,"glass"); s(1,7,2,"redstone_wire")
    s(-1,4,1,"repeater",facing="south"); s(-1,4,2,"redstone_wire")
    # left column E2,E3
    s(-2,2,0,"sticky_piston",facing="east"); s(-1,2,0,"stone")
    s(-2,3,0,"sticky_piston",facing="east"); s(-1,3,0,"stone")
    s(-2,3,1,"stone"); s(-2,4,1,"redstone_wire"); s(-2,3,2,"stone"); s(-2,4,2,"redstone_wire")
    # left row-1 unit
    s(-1,1,0,"stone"); s(-1,0,0,"stone")
    s(-2,1,0,"sticky_piston",facing="east"); s(-3,1,0,"sticky_piston",facing="east")
    s(-1,-1,0,"sticky_piston",facing="up")
    # A (wall feed)
    s(-2,0,1,"stone"); s(-2,1,1,"repeater",facing="west"); s(-3,0,1,"stone"); s(-3,1,1,"redstone_wire"); s(-3,0,2,"stone"); s(-3,1,2,"redstone_wire")
    # B path
    s(-2,0,-1,"glass"); s(-2,1,-1,"redstone_wire")
    s(-2,-1,-2,"stone"); s(-2,0,-2,"redstone_wire")
    s(-2,-2,-1,"stone"); s(-2,-1,-1,"redstone_wire")
    s(-2,-2,0,"stone"); s(-2,-1,0,"redstone_wire")
    s(-2,-2,1,"stone"); s(-2,-1,1,"redstone_wire")
    s(-2,-2,2,"stone"); s(-2,-1,2,"redstone_wire")
    s(-1,-1,2,"stone")  # cut
    # R1 QC feed
    s(-3,2,0,"glass"); s(-3,3,0,"redstone_wire"); s(-3,2,1,"stone"); s(-3,3,1,"redstone_wire"); s(-3,2,2,"stone"); s(-3,3,2,"redstone_wire")
    s(-3,4,0,"stone"); s(-3,4,1,"stone"); s(-3,4,2,"stone")  # cuts
    # K1 feed + bottom E
    s(-1,-2,0,"stone"); s(-1,-3,1,"stone"); s(-1,-2,1,"repeater",facing="south"); s(-1,-3,2,"stone"); s(-1,-2,2,"redstone_wire")
    for x in (0,1):
        s(x,-2,0,"sticky_piston",facing="up"); s(x,-1,0,"stone")
        s(x,-3,1,"stone"); s(x,-2,1,"repeater",facing="south"); s(x,-3,2,"stone"); s(x,-2,2,"redstone_wire")
    for (x,y,z,b,pr) in L:
        d.set(x,y,z,b,**pr)
        d.set(3-x,y,z,b,**mirror_props(pr))
    return d

def is_wall(x,y,z):
    if z == 0: return False
    return (x in (-1,4) and 0<=y<=3) or (y in (-1,4) and 0<=x<=3)
