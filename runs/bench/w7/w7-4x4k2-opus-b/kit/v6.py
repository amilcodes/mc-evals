import v5
from v1 import dust, rep, obs
def left():
    d=v5.left()
    Y=v5.Y
    for p in [(-7,Y,0),(-7,Y-1,0),(-7,2,0),(-6,2,0),(-6,1,0)]+[(-7,y,0) for y in range(Y+1,2)]:
        d.remove(*p)
    d.remove(-6,1,-1)  # support replaced by column top observer
    for y in range(Y+1,2): obs(d,-6,y,-1,"down")
    return d
