exec(open('side.py').read())
LINES2 = {
  -3: ('obs',[4,2]+[1]*9),            # R_A 12 el
  -2: (None,[2,2,2,2]),               # K_A 16
  -1: (None,[3,3,3,3]),               # K_B 24
   0: ('obs',[1]*7),                  # spit 16
   1: (None,[2,2,2,2,1,1,1,1]),       # level 24
   2: ('obs',[4,4,2,2,1,1,2]),        # p1 34
   3: ('obs',[4,4,4,4,4,4,3]),        # p2 56
   6: ('obs',[4,4,3,2]+[1]*7),        # R_B 44
}
def lever_line2(d, zL=-16):
    d.remove(1,6,13); d.remove(1,5,13)
    d.set(4,8,12,"lever",face="floor",facing="north"); d.set(4,7,12,"stone")
    for z in range(11,-10,-1):
        d.set(4,8,z,"repeater",facing="south"); sup(d,4,7,z)
    d.set(4,8,-10,"redstone_wire"); sup(d,4,7,-10)
    d.set(4,7,-11,"redstone_wire"); sup(d,4,6,-11)
    d.set(4,6,-12,"redstone_wire"); sup(d,4,5,-12)
    for z in range(-13,zL,-1):
        if z==-14: d.set(4,5,z,"repeater",facing="south")
        else: d.set(4,5,z,"redstone_wire")
        sup(d,4,4,z)
    return d
def full2():
    b = base(); top_brain(b, lever=False); side_brain(b, zL=-16, lines=LINES2); lever_line2(b, zL=-16); return b
