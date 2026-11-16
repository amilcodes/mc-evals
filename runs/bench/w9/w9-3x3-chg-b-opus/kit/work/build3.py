exec(open('work/build2.py').read())
def feeds3(d):
    feeds2(d)
    for p in [(2,-4,0),(3,-4,0),(4,-4,0),(4,-5,0)]: d.remove(*p)
    d.set(3,-2,0,"observer",facing="up"); d.set(3,-3,0,"stone")
    d.set(2,-3,0,"repeater",facing="east",delay=3); d.set(2,-4,0,"stone")
def logic3(d):
    for z in range(-6,9): wire(d,M,-4,z)
    d.set(M+1,-5,0,"lever",face="wall",facing="east")
    branch2(d,-2,-1,3,[('r',4),('r',4),('r',1)],-2)
    branch2(d,-4,-1,3,[('r',4),('r',4),('r',3)],-3)
    branch2(d,-6,-4,1,[('r',2)],-3)
    branch2(d,2,-2,2,[('r',4),('r',4),('r',3)],2)
    branch2(d,4,-2,2,[('r',4),('r',4),('r',4),('r',3),('o',),('r',4)],3)
    branch2(d,6,-3,0,[('r',4),('r',2)],1)
    branch2(d,8,-2,-3,[('r',4),('r',4),('r',4),('r',2)],1,((4,1),))
def full4():
    d=Design("open"); core(d); feeds3(d); logic3(d); simple(d); return d
