exec(open('work/build5.py').read())
def logic6(d):
    for z in range(-6,7): wire(d,M,Y0,z)
    d.set(M+1,Y0-1,0,"lever",face="wall",facing="east")
    branch5(d,-2,-1,3,[('r',4),('r',4),('r',1)],-2)
    branch5(d,-4,-1,3,[('r',4),('r',4),('r',3)],-3)
    branch5(d,-6,-3,1,[('r',2)],-3)
    branch5(d,2,-2,2,[('r',4),('r',4),('r',3)],2)
    branch5(d,4,-2,2,[('r',4),('r',4),('r',4),('o',),('r',4)],3,first=4)
    branch5(d,6,-2,-3,[('r',4),('r',4),('r',4),('r',2)],1,((4,1),))
    wire(d,0,-3,-4); rep(d,0,-3,-3,"north",4); wire(d,0,-3,-2); wire(d,0,-3,-1)
def full8():
    d=Design("open"); core(d); feeds5(d); logic6(d); simple5(d); return d
