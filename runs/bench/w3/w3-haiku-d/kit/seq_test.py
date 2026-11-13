d = Design("closed")
for y in range(3):
    d.set(0,y,0,"stone"); d.set(1,y,0,"stone"); d.set(2,y,0,"stone")
    d.set(-2,y,0,"sticky_piston",facing="east")
    d.set(-3,y,0,"lever",face="wall",facing="east"); d.set(-4,y,0,"stone")
    d.set(4,y,0,"sticky_piston",facing="west")
    d.set(5,y,0,"lever",face="wall",facing="west"); d.set(6,y,0,"stone")
d.set(1,-2,0,"sticky_piston",facing="up")
d.set(2,-2,0,"lever",face="wall",facing="west"); d.set(3,-2,0,"stone")
d.set(1,-3,0,"sticky_piston",facing="up")
d.set(2,-3,0,"lever",face="wall",facing="west"); d.set(3,-3,0,"stone")
d.set(-1,-1,0,"sticky_piston",facing="east")
d.set(-2,-1,0,"lever",face="wall",facing="east"); d.set(-3,-1,0,"stone")
d.set(1,4,0,"sticky_piston",facing="down")
d.set(2,4,0,"lever",face="wall",facing="west"); d.set(3,4,0,"stone")
d.set(2,-1,0,"stone"); d.set(0,3,0,"stone"); d.set(2,3,0,"stone")
# hold levers on for closed state
hold = [(-3,y,0) for y in range(3)] + [(5,y,0) for y in range(3)] + [(2,4,0)]
