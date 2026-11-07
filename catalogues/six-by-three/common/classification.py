"""Exact reduction to positive circuits on the eight deterministic Bob outcomes."""

if not __debug__:
    raise RuntimeError("Run without -O or -OO: exact verification requires assertions.")
from itertools import combinations,product
from math import gcd
from functools import reduce
B=list(product((0,1),repeat=3))
def det3(M):
    (a,b,c),(d,e,f),(g,h,i)=M
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)
def normalize(a):
    g=reduce(gcd,a,0);return tuple(x//g for x in a) if g else tuple(a)
def vector(row):return tuple(sum(x*y for x,y in zip(row,(1,*b))) for b in B)
def mixed(v):
    # Four multilinear Fourier components orthogonal to affine functions.
    return tuple(sum(t*(-1)**sum(b[i] for i in J) for t,b in zip(v,B)) for J in [(0,1),(0,2),(1,2),(0,1,2)])
def atoms():
    rows=set()
    for points in combinations(B,3):
        m=[(1,*b) for b in points]
        r=normalize([(-1)**k*det3([v[:k]+v[k+1:] for v in m]) for k in range(4)])
        if any(r):rows.add(r);rows.add(tuple(-v for v in r))
    out=[]
    for r in sorted(rows):
        h=tuple(max(v,0) for v in vector(r));out.append((r,h,mixed(h)))
    for i in range(8):
        h=tuple(int(j==i) for j in range(8));out.append((None,h,mixed(h)))
    return out


import math
def det(A):
    n=len(A)
    if n==1:return A[0][0]
    if n==2:return A[0][0]*A[1][1]-A[0][1]*A[1][0]
    if n==3:return det3(A)
    return sum((-1)**i*t*det([r[:i]+r[i+1:] for r in A[1:]]) for i,t in enumerate(A[0]))
def pos_dep(cols):
    k=len(cols)
    if k==1:return (1,) if not any(cols[0]) else None
    for rows in combinations(range(4),k-1):
        M=[[q[r] for q in cols] for r in rows]
        d=normalize([(-1)**j*det([r[:j]+r[j+1:] for r in M]) for j in range(k)])
        if not any(d):continue
        if max(d)<0:d=tuple(-v for v in d)
        if min(d)>0 and all(sum(q[r]*v for q,v in zip(cols,d))==0 for r in range(4)):return d
        return None
    return None

from collections import Counter,defaultdict
from functools import lru_cache
from itertools import permutations
from math import lcm
from pathlib import Path
import json

dirs=Path(__file__).resolve().parents[1]/'entries'
def parts(k):
    if not k:yield ();return
    for p in parts(k-1):
        for j in range(max(p,default=-1)+2):yield p+(j,)
def orbit_col(q,p,s):
    J=[(0,1),(0,2),(1,2),(0,1,2)]
    return tuple(q[J.index(tuple(sorted(p[j] for j in T)))]*math.prod(s[j] for j in T) for T in J)
ops=[(p,s) for p in permutations(range(3)) for s in product((-1,1),repeat=3)]
@lru_cache(None)
def canon(C):
    # Four times all reflection coefficients. Treat a sign and its reverse
    # identically on each Alice row; then sort those rows.
    v=tuple(tuple(4*C[i][j] if i==j==0 else 0 for j in range(4)) for i in range(len(C)))
    v=[list(a) for a in v]
    for i,row in enumerate(C):
        for j,z in enumerate(row):
            if i==j==0:continue
            coeff=4*z//(2**(bool(i)+bool(j)))
            for k in ([0,i] if i else [0]):
                for l in ([0,j] if j else [0]):v[k][l]+=coeff
    g=reduce(gcd,(x for row in v for x in row),0) or 1
    v=[[x//g for x in row] for row in v]
    ans=None
    for p,s in ops:
        rr=[(w[0],*(w[i+1]*e for i,e in zip(p,s))) for w in v]
        attr=(rr[0],*sorted(min(r,tuple(-v for v in r)) for r in rr[1:] if any(r)))
        if ans is None or attr<ans:ans=attr
    return ans
def rankz(mat):
    piv={}
    for row in mat:
        for j,A in sorted(piv.items()):
            if row[j]:
                a,b=A[j],row[j]
                row=list(normalize([a*x-b*y for x,y in zip(row,A)]))
        j=next((k for k,x in enumerate(row) if x),None)
        if j is not None:piv[j]=row
    return len(piv)
def facet(C):
    k=len(C)-1
    if k==0:
        # Bob-only inequalities may define a positivity of a marginal; in
        # the full bipartite space these cannot define a facet. Check the
        # lifted representative with one named Alice setting explicitly.
        C=(*C,(0,0,0,0));k=1
    dom=[];zero=[[] for _ in range(k)]
    for b in B:
        vec=(1,*b);a=[sum(x*y for x,y in zip(row,vec)) for row in C]
        sc=a[0]+sum(max(0,x) for x in a[1:]);assert sc<=0
        if sc:continue
        dom.append([*vec,*[y*int(c>0) for c in a[1:] for y in vec]])
        for i,t in enumerate(a[1:]):
            if t==0:zero[i].append(list(vec))
    if len(dom)+sum(rankz(z) for z in zero)<4*k+3:return False
    for i,Z in enumerate(zero):
        for row in Z:dom.append([0]*(4+4*i)+row+[0]*(4*(k-i-1)))
    return rankz(dom)==4*k+3
def table(choices,weights,partition):
    # Coefficients in the circuit are relative to normalized quotient columns.
    den=[reduce(gcd,mixed(h),0) or 1 for _,h,_ in choices]
    M=lcm(*den);coeff=[w*M//g for w,g in zip(weights,den)]
    baseline=[-sum(v*t[1][i] for v,t in zip(coeff,choices)) for i in range(8)]
    assert mixed(baseline)==(0,0,0,0)
    g=[baseline[0],baseline[4]-baseline[0],baseline[2]-baseline[0],baseline[1]-baseline[0]]
    assert list(vector(g))==baseline
    R=[(w,t[0]) for w,t in zip(coeff,choices) if t[0] is not None]
    rows=[[0]*4 for _ in range(max(partition,default=-1)+1)]
    for j,(w,r) in zip(partition,R):
        for i,x in enumerate(r):rows[j][i]+=w*x
    return tuple(tuple(v) for v in [g]+[r for r in rows if any(r)])
def all_tables():
    s=defaultdict(list)
    for r,h,q in atoms():s[normalize(q)].append((r,h,q))
    for src in s.pop((0,0,0,0)):yield table([src],[1],[0])
    for k in range(2,6):
        for vv in combinations(sorted(s),k):
            dd=pos_dep(vv)
            if not dd:continue
            best=min(tuple(sorted(orbit_col(q,p,h) for q in vv)) for p,h in ops)
            if vv!=best:continue
            for parts0 in product(*(s[v] for v in vv)):
                for pp in parts(sum(t[0] is not None for t in parts0)):
                    yield table(parts0,dd,pp)
def run():
    known={}
    for f in sorted(dirs.glob('*/definition.json')):
        T=json.loads(f.read_text(encoding='utf-8'))['active_table']
        C=tuple(tuple(r+[0]*(4-len(r))) for r in T);known[canon(C)]=f.parent.name
    assert len(known)==7
    raw=set(all_tables()); checked=set(); hits=set()
    for C in raw:
        key=canon(C)
        if key in checked:continue
        checked.add(key)
        if facet(C):
            if key not in known:raise ValueError(('UNEXPECTED FACET',C,key))
            hits.add(known[key])
    assert hits==set(known.values()),hits
    print('Finite completeness calculation:',len(raw),'tables,',len(checked),'orbits tested;',sorted(hits))
if __name__=='__main__':run()
