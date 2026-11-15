from pdbuild import Design
def left_mech(d):
    for y in (1,2):
        d.set(-2,y,0,"sticky_piston",facing="east")
        d.set(-3,y,0,"sticky_piston",facing="east")
        d.set(-3,y,1,"observer",facing="north")
        d.set(-2,y,1,"observer",facing="west")
    # sliders extended (closed)
    d.set(-1,4,0,"sticky_piston",facing="down",extended="true")
    d.set(-1,3,0,"piston_head",facing="down",type="sticky")
    d.set(-1,-1,0,"sticky_piston",facing="up",extended="true")
    d.set(-1,0,0,"piston_head",facing="up",type="sticky")
    # hi drivers: repeaters at z=-1 on stone supports
    for x in (-2,-3):
        d.set(x,1,-1,"stone")
        d.set(x,2,-1,"repeater",facing="north")
        d.set(x,1,-2,"stone")
    return d
