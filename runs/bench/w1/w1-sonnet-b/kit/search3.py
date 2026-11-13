from sim import *
from search1 import search
from search2 import layouts
import sys
for n in sys.argv[1:]:
    st=layouts[n]
    alpha=sorted({b[1] for b in st.values() if b[0]=='p'})
    r=search(st,alpha,9)
    print(n,r[:10],flush=True)
