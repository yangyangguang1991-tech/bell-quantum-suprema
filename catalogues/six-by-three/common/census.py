"""Facet rank in the full scenario and relabellings of the conventional tables."""

if not __debug__:
    raise RuntimeError("Run without -O or -OO: exact verification requires assertions.")
from fractions import Fraction as F
from itertools import product,permutations
def rank(A):
    prime=1009
    piv={}
    for row in A:
        for j,t in sorted(piv.items()):
            if row[j]:
                c=row[j];row=[(u-c*v)%prime for u,v in zip(row,t)]
        j=next((k for k,x in enumerate(row) if x%prime),None)
        if j is not None:
            inv=pow(row[j],-1,prime);piv[j]=[u*inv%prime for u in row]
    return len(piv)
def check_facet(C):
    sat=[]; scores=[]
    for a in product((0,1),repeat=6):
        for b in product((0,1),repeat=3):
            aa=(1,)+a;bb=(1,)+b
            f=sum(v*aa[i]*bb[j] for i,r in enumerate(C) for j,v in enumerate(r))
            scores.append(f)
            if f==0:sat.append([1,*a,*b,*[x*y for x in a for y in b]])
    assert max(scores)==0 and rank(sat)==27
    return len(sat)
def signed(C):
    n=len(C[0])-1;m=len(C)-1;s=[[0]*(n+1) for _ in range(m+1)]
    for i,r in enumerate(C):
        for j,v in enumerate(r):
            a=[0,i] if i else [0];b=[0,j] if j else [0]
            for k in a:
                for l in b:s[k][l]+=4*v//(len(a)*len(b))
    return s
def relabel(src,dst):
    A=signed(src);B=signed(dst); m,n=len(A)-1,len(A[0])-1
    for pa in permutations(range(1,m+1)):
        for pb in permutations(range(1,n+1)):
            for sa in product((-1,1),repeat=m):
                for sb in product((-1,1),repeat=n):
                    if all(x*y*A[i][j]==B[u][v] for u,(x,i) in enumerate(zip((1,)+sa,(0,)+pa))
                           for v,(y,j) in enumerate(zip((1,)+sb,(0,)+pb))):
                        return dict(alice_permutation=pa,bob_permutation=pb,alice_signs=sa,bob_signs=sb)
    raise ValueError("No signed relabelling including the constant and marginals.")
