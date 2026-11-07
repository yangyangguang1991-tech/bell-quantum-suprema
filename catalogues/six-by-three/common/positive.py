"""Rigorous fixed-point interval LDL using Python integers only.
Endpoints are integers divided by 2**bits. Every elementary result is rounded
outwards by integer floor/ceiling division. This is a positivity proof, not a
floating-point eigenvalue tolerance.
"""

if not __debug__:
    raise RuntimeError("Run without -O or -OO: exact verification requires assertions.")
from fractions import Fraction as F
from math import isqrt

def ceildiv(a,b):return -((-a)//b)

def positive_pivots(A, bits=384):
    U=1<<bits
    def cv(v):
        # v is rational or an exact a+b*sqrt(d) object.
        if hasattr(v,'a'):
            r=isqrt(v.d*U*U)
            a,b=v.a,v.b
            lo=a.numerator*U//a.denominator;hi=ceildiv(a.numerator*U,a.denominator)
            x=b.numerator*r;y=b.numerator*(r+1)
            lo+=min(x,y)//b.denominator;hi+=ceildiv(max(x,y),b.denominator)
            return lo,hi
        v=F(v);return v.numerator*U//v.denominator,ceildiv(v.numerator*U,v.denominator)
    def mul(x,y):
        z=(x[0]*y[0],x[0]*y[1],x[1]*y[0],x[1]*y[1]);return min(z)//U,ceildiv(max(z),U)
    def divpos(x,y):
        assert y[0]>0
        z=[(U*a,b) for a in x for b in y]
        return min(a//b for a,b in z),max(ceildiv(a,b) for a,b in z)
    n=len(A);S=[[cv(v) for v in row] for row in A];pivs=[]
    for k in range(n):
        p=S[k][k]
        if p[0]<=0:raise ArithmeticError(f'Interval LDL pivot {k} is not certified positive at {bits} bits.')
        pivs.append(p)
        factors=[divpos(S[i][k],p) for i in range(k+1,n)]
        for ii,i in enumerate(range(k+1,n)):
            l=factors[ii]
            for j in range(i,n):
                t=mul(l,S[j][k]);a=S[i][j];S[i][j]=S[j][i]=(a[0]-t[1],a[1]-t[0])
    return {'bits':bits,'pivot_intervals_integer':[[str(a),str(b)] for a,b in pivs],
            'common_denominator_power_of_two':bits,'all_lower_endpoints_strictly_positive':True}
