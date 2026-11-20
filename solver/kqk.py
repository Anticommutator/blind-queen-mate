import sys, itertools
N=8
def sq(f,r): return r*8+f
def fr(s): return s%8, s//8
def name(s): f,r=fr(s); return "abcdefgh"[f]+str(r+1)
KD=[(a,b) for a in(-1,0,1) for b in(-1,0,1) if (a,b)!=(0,0)]
def kn(s):
    f,r=fr(s); return [sq(f+a,r+b) for a,b in KD if 0<=f+a<8 and 0<=r+b<8]
KN=[set(kn(s)) for s in range(64)]
def qrays(s):
    f,r=fr(s); out=[]
    for a,b in KD:
        ray=[]; x,y=f+a,r+b
        while 0<=x<8 and 0<=y<8: ray.append(sq(x,y)); x+=a;y+=b
        out.append(ray)
    return out
QR=[qrays(s) for s in range(64)]
def qatt(q,wk,ignore=None):
    # squares attacked by queen, blocked by wk (black king transparent: x-ray matters for king moves)
    A=set()
    for ray in QR[q]:
        for t in ray:
            A.add(t)
            if t==wk: break
    return A
def black_moves(wk,q,bk):
    A=qatt(q,wk)|KN[wk]
    res=[]
    for t in KN[bk]:
        if t==wk: continue
        if t==q:
            if q not in KN[wk]: res.append(t)  # capture
            continue
        if t in A: continue
        res.append(t)
    return res, (bk in qatt(q,wk))
def white_moves(wk,q,S):
    # moves legal for every bk in S
    occ=S
    mv=[]
    for t in KN[wk]:
        if t==q or t in S: continue
        if any(t in KN[b] for b in S): continue
        mv.append((t,q))
    for ray in QR[q]:
        for t in ray:
            if t==wk or t in S: break
            mv.append((wk,t))
    return mv
def step(wk,q,S):
    """returns dict move->(newstate) or None if move bad"""
    out=[]
    for (nk,nq) in white_moves(wk,q,S):
        ok=True; NS=set()
        for b in S:
            ms,chk=black_moves(nk,nq,b)
            if nq in ms: ok=False;break   # queen hangs
            if not ms:
                if chk: continue
                ok=False;break  # stalemate
            NS.update(ms)
        if ok: out.append(((nk,nq),frozenset(NS)))
    return out
