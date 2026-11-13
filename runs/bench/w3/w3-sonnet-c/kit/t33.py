for t,p,b,a in lab.history:
    if t>=40 and p[2]==0 and -4<=p[0]<=2 and 0<=p[1]<=2: print(t,p,a[:70])
