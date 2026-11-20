import subprocess, itertools
from fast import name
from concurrent.futures import ThreadPoolExecutor
E=set(); V=set()
for l in open('pairs_results.txt'):
    m,r=l.split(); m=int(m[1:],16); bs=[i for i in range(64) if m>>i&1]; V|=set(bs)
    if int(r)>0: E.add(frozenset(bs))
V=sorted(V); adj={v:{u for u in V if frozenset((u,v)) in E} for v in V}
# enumerate all cliques (size>=2)
cl=[]
def ext(c,cand):
    for i,v in enumerate(cand):
        nc=c+[v]; cl.append(nc); ext(nc,[u for u in cand[i+1:] if u in adj[v]])
ext([],V)
print('cliques',len(cl),'max size',max(map(len,cl)))
def test(c):
    m=sum(1<<b for b in c)
    if len(c)<=2: return c, (frozenset(c) in E or len(c)==1)
    r=int(subprocess.run(['./kqk','27','45','S%x'%m],capture_output=True,text=True).stdout.split()[1]); return c,r>0
# test cliques size>=3, skipping supersets of failures
win=[c for c in cl if len(c)<=2]; bysize={}
for c in cl:
    if len(c)>=3: bysize.setdefault(len(c),[]).append(c)
fails=[]
for k in sorted(bysize):
    todo=[c for c in bysize[k] if not any(set(f)<=set(c) for f in fails)]
    with ThreadPoolExecutor(12) as ex:
        for c,ok in ex.map(test,todo):
            (win if ok else fails).append(c)
    print(k,len(todo),'win',sum(1 for c in win if len(c)==k),flush=True)
# exact min set cover over maximal winning sets
W=[frozenset(c) for c in win]
W=[w for w in W if not any(w<x for x in W)]
U=frozenset(V)
best=[None]
def rec(unc,chosen):
    if best[0] and len(chosen)>=len(best[0]): return
    if not unc: best[0]=list(chosen); return
    v=min(unc,key=lambda v:sum(1 for w in W if v in w))
    for w in sorted([w for w in W if v in w],key=lambda w:-len(w&unc)):
        rec(unc-w,chosen+[w])
rec(U,[])
print('MIN GROUPS',len(best[0]))
for w in best[0]: print(sorted(name(b) for b in w))
import json; json.dump([sorted(w) for w in W],open('maxwin.json','w'))
print('maximal winning sets',len(W))
