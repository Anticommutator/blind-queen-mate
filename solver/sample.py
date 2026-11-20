from fast import *
from multiprocessing import Pool
import random
LIM=60000
def job(t):
    wk,q,b=t
    p,n=solve(wk,q,1<<b,2.0,LIM)
    return (name(wk),name(q),name(b), 'MATE' if p else ('none' if n<=LIM else 'limit'), n, len(p) if p else None, fmt(p) if p else '')
if __name__=="__main__":
    random.seed(7); jobs=[]
    while len(jobs)<600:
        wk,q,b=random.sample(range(64),3)
        if (init(wk,q)>>b)&1: jobs.append((wk,q,b))
    with Pool(12) as P:
        for r in P.imap_unordered(job,jobs):
            print(*r,flush=True)
