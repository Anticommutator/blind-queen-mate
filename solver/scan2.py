from fast import *
from multiprocessing import Pool
import sys
LIM=int(sys.argv[1])
def job(wq):
    wk,q=wq
    S=init(wk,q)
    if S==0: return (wk,q,'nolegal',0,None)
    p,n=solve(wk,q,S,2.0,LIM)
    if p: return (wk,q,'MATE',n,(len(p),fmt(p)))
    return (wk,q,'exhausted' if n<=LIM else 'limit',n,None)
if __name__=="__main__":
    jobs=[(a,b) for a in range(64) for b in range(64) if a!=b]
    with Pool(6) as P:
        for r in P.imap_unordered(job,jobs,chunksize=8):
            print(r[0],r[1],r[2],r[3],r[4],flush=True)
