"""Small exact arithmetic and free-reflection algebra. Python standard library only."""

if not __debug__:
    raise RuntimeError("Run without -O or -OO: exact verification requires assertions.")

if not __debug__:
    raise RuntimeError("Run certificate checks without python -O: assertions are required.")
from fractions import Fraction as F
from dataclasses import dataclass
@dataclass(frozen=True)
class Quad:
    a:F=F(0)
    b:F=F(0)
    d:int=2
    def __post_init__(self):
        object.__setattr__(self,'a',F(self.a));object.__setattr__(self,'b',F(self.b))
    def coerce(self,o):
        if isinstance(o,Quad):
            if o.d!=self.d: raise ValueError('Different quadratic fields')
            return o
        return Quad(F(o),F(0),self.d)
    def __add__(self,o):
        o=self.coerce(o);return Quad(self.a+o.a,self.b+o.b,self.d)
    __radd__=__add__
    def __neg__(self):return Quad(-self.a,-self.b,self.d)
    def __sub__(self,o):return self+-self.coerce(o)
    def __rsub__(self,o):return self.coerce(o)+-self
    def __mul__(self,o):
        o=self.coerce(o);return Quad(self.a*o.a+self.d*self.b*o.b,self.a*o.b+self.b*o.a,self.d)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=self.coerce(o);den=o.a*o.a-self.d*o.b*o.b
        if not den:raise ZeroDivisionError
        return self*Quad(o.a/den,-o.b/den,self.d)
    def __rtruediv__(self,o):return self.coerce(o)/self
    def __bool__(self):return bool(self.a or self.b)
    def sign(self):
        a,b=self.a,self.b
        if not b:return (a>0)-(a<0)
        if not a:return (b>0)-(b<0)
        if a>0 and b>0:return 1
        if a<0 and b<0:return -1
        v=a*a-self.d*b*b
        return ((v>0)-(v<0))*(1 if a>0 else -1)
    def enc(self):return [str(self.a),str(self.b)]
    def __float__(self):return float(self.a)+float(self.b)*self.d**0.5

def red(seq):
    stack=[]
    for x in seq:
        if stack and stack[-1]==x:stack.pop()
        else:stack.append(x)
    return tuple(stack)
def word(u,v):
    a=red(tuple(reversed(u[0]))+tuple(v[0]));b=red(tuple(reversed(u[1]))+tuple(v[1]));return min((a,b),(a[::-1],b[::-1]))
IDENT=((),())
def mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(len(B))),0) for j in range(len(B[0]))] for i in range(len(A))]
def transpose(A):return [list(r) for r in zip(*A)]
def ldl_positive(A):
    n=len(A);L=[[0]*n for _ in range(n)];ds=[]
    for i in range(n):
        L[i][i]=1
        for j in range(i):L[i][j]=(A[i][j]-sum((L[i][k]*L[j][k]*ds[k] for k in range(j)),0))/ds[j]
        v=A[i][i]-sum((L[i][k]*L[i][k]*ds[k] for k in range(i)),0)
        if (v.sign() if isinstance(v,Quad) else (v>0)-(v<0))<=0:raise ArithmeticError('Nonpositive pivot '+str(i))
        ds.append(v)
    return ds
