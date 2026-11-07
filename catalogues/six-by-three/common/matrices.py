"""Exact arithmetic in rational linear combinations of real square roots and i."""

if not __debug__:
    raise RuntimeError("Run without -O or -OO: exact verification requires assertions.")
from fractions import Fraction as F
from math import gcd,isqrt

class R:
    def __init__(self,terms=0):
        if isinstance(terms,R):terms=terms.term
        if not isinstance(terms,dict):terms={(1,0):F(terms)}
        self.term={k:F(v) for k,v in terms.items() if v}
    def __add__(self,b):
        t=self.term.copy()
        for k,v in R(b).term.items():t[k]=t.get(k,0)+v
        return R(t)
    __radd__=__add__
    def __neg__(self):return R({k:-v for k,v in self.term.items()})
    def __sub__(self,b):return self+-R(b)
    def __rsub__(self,b):return R(b)+-self
    def __mul__(self,b):
        t={}
        for (r,i),v in self.term.items():
            for (s,j),w in R(b).term.items():
                g=gcd(r,s);k=(r*s//g**2,(i+j)%2)
                t[k]=t.get(k,0)+v*w*g*(-1 if i*j else 1)
        return R(t)
    __rmul__=__mul__
    def conj(self):return R({(r,i):(-1 if i else 1)*v for (r,i),v in self.term.items()})
    def __eq__(self,b):return self.term==R(b).term
    def export(self):return [[str(v),r,i] for (r,i),v in sorted(self.term.items())]
    @staticmethod
    def read(encoded):
        if not isinstance(encoded,list):raise ValueError('An exact scalar must be a list of triples')
        terms={}
        for item in encoded:
            if not isinstance(item,list) or len(item)!=3:raise ValueError('Invalid scalar triple')
            v,r,i=item
            if type(r) is not int or r<1 or type(i) is not int or i not in (0,1):raise ValueError('Invalid radical or imaginary parity')
            if any(r%(k*k)==0 for k in range(2,isqrt(r)+1)):raise ValueError('Radicand must be squarefree')
            if (r,i) in terms:raise ValueError('Duplicate radical term')
            terms[r,i]=F(v)
        return R(terms)
def sqrtq(x):
    x=F(x); assert x>=0
    if not x:return R()
    n=x.numerator*x.denominator;factor=1;squarefree=1;p=2
    while p*p<=n:
        multiplicity=0
        while n%p==0:n//=p;multiplicity+=1
        factor*=p**(multiplicity//2)
        if multiplicity%2:squarefree*=p
        p=3 if p==2 else p+2
    return R({(squarefree*n,0):F(factor,x.denominator)})
I=R({(1,1):1})
UNIT=[[R(1),R()],[R(),R(1)]]
def pauli(v):
    x,y,z=v
    return [[z,x-I*y],[x+I*y,-z]]
def tr(A):return [list(row) for row in zip(*A)]
def adj(A):return [[v.conj() for v in row] for row in tr(A)]
def mul(A,B):return [[sum((a*b for a,b in zip(row,col)),R()) for col in tr(B)] for row in A]
def effect(A,sign):return [[(UNIT[i][j]+sign*A[i][j])*F(1,2) for j in range(2)] for i in range(2)]
def tensor(A,B):return [[A[i][j]*B[k][l] for j in range(2) for l in range(2)] for i in range(2) for k in range(2)]
def expect(v,M):return sum((v[i].conj()*M[i][j]*v[j] for i in range(4) for j in range(4)),R())
def vectors_from_gram(G):
    n=len(G);L=[[F(0)]*n for _ in range(n)];p=[]
    for i in range(n):
        L[i][i]=1
        for j in range(i):L[i][j]=(G[i][j]-sum(L[i][k]*L[j][k]*p[k] for k in range(j)))/p[j]
        p.append(G[i][i]-sum(L[i][k]**2*p[k] for k in range(i)))
        assert p[-1]>0
    return [[L[i][j]*sqrtq(p[j]) for j in range(n)] for i in range(n)]
def decode_matrix(m):
    if not isinstance(m,list) or len(m)!=2 or any(not isinstance(row,list) or len(row)!=2 for row in m):raise ValueError('A qubit matrix must be 2 by 2')
    return [[R.read(x) for x in row] for row in m]
def check_witness(table,record,target):
    A=list(map(decode_matrix,record['alice_reflections']));B=list(map(decode_matrix,record['bob_reflections']))
    v=list(map(R.read,record['state']))
    assert len(v)==4 and len(A)==6 and len(B)==3 and sum(t.conj()*t for t in v)==1
    for T in A+B:assert adj(T)==T and mul(T,T)==UNIT
    A=[UNIT]+[effect(T,1) for T in A];B=[UNIT]+[effect(T,1) for T in B]
    result=sum(table[i][j]*expect(v,tensor(A[i],B[j])) for i in range(len(table)) for j in range(len(table[i])))
    assert result==target
    return result
