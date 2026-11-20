# bitboard version
import heapq, sys
from kqk import sq, name, KN, QR
KB=[sum(1<<t for t in KN[s]) for s in range(64)]
def qatt(q,wk):
    A=0
    for ray in QR[q]:
        for t in ray:
            A|=1<<t
            if t==wk: break
    return A
QA={}
def qa(q,wk):
    k=(q,wk)
    if k not in QA: QA[k]=qatt(q,wk)
    return QA[k]
def bits(S):
    while S:
        l=S&-S; yield l.bit_length()-1; S^=l
def dilate(S):
    # king-neighbourhood of set S
    notA=0xfefefefefefefefe; notH=0x7f7f7f7f7f7f7f7f; M=(1<<64)-1
    h=S|((S<<1)&notA)|((S>>1)&notH)
    return (h|(h<<8)|(h>>8))&M
def step(wk,q,S):
    out=[]
    adjS=dilate(S)  # squares adjacent to (or in) S
    cand=[]
    for t in KN[wk]:
        if t!=q and not (adjS>>t)&1: cand.append((t,q))
    for ray in QR[q]:
        for t in ray:
            if t==wk or (S>>t)&1: break
            cand.append((wk,t))
    for nk,nq in cand:
        prot=(KB[nk]>>nq)&1
        if not prot and (adjS>>nq)&1: continue   # queen could be captured
        A=qa(nq,nk)|KB[nk]|(1<<nk)
        free=~A & ((1<<64)-1)
        NS=0; ok=True
        for b in bits(S):
            m=KB[b]&free & ~(1<<nq)
            if m==0:
                if not (A>>b)&1: ok=False;break  # stalemate
            NS|=m
        if ok: out.append((nk,nq,NS))
    return out
def init(wk,q):
    A=qa(q,wk)|KB[wk]|(1<<wk)|(1<<q)
    return ((1<<64)-1)&~A
def solve(wk,q,S,W=2.0,limit=10**7):
    st=(wk,q,S); par={st:None}; pq=[(0,0,st)]; n=0
    while pq:
        f,d,st=heapq.heappop(pq); n+=1
        if n>limit: return None,n
        for nk,nq,NS in step(*st):
            ns=(nk,nq,NS)
            if ns in par: continue
            par[ns]=(st,(nk,nq))
            if NS==0:
                path=[];cur=ns
                while par[cur]: p,m=par[cur]; path.append((p,m)); cur=p
                return path[::-1],n
            heapq.heappush(pq,(d+1+W*bin(NS).count('1'),d+1,ns))
    return None,n
def fmt(path):
    return " ".join(("K"+name(m[0])) if m[0]!=p[0] else ("Q"+name(m[1])) for p,m in path)
if __name__=="__main__":
    a=sys.argv
    wk=int(a[1]);q=int(a[2]);W=float(a[3]); bk=a[4] if len(a)>4 else None
    S=init(wk,q) if bk is None else 1<<int(bk)
    p,n=solve(wk,q,S,W)
    print(n, None if p is None else (len(p),fmt(p)))
