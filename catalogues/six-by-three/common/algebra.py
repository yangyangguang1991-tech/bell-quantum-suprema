"""Oriented free-reflection polynomials with exact rational coefficients."""

if not __debug__:
    raise RuntimeError("Run without -O or -OO: exact verification requires assertions.")

from fractions import Fraction as F
from collections import defaultdict

def reduce_word(word):
    stack=[]
    for letter in word:
        if stack and stack[-1]==letter:stack.pop()
        else:stack.append(letter)
    return tuple(stack)
def clean(p):return {w:F(c) for w,c in p.items() if c}
def add(*polys):
    out=defaultdict(F)
    for p in polys:
        for w,c in p.items():out[w]+=c
    return clean(out)
def scale(c,p):return clean({w:F(c)*x for w,x in p.items()})
def mul(p,q):
    out=defaultdict(F)
    for (a,b),x in p.items():
        for (c,d),y in q.items():out[reduce_word(a+c),reduce_word(b+d)]+=x*y
    return clean(out)
ONE={((),()):F(1)}
def A(i):return {((i,),()):F(1)}
def B(j):return {((),(j,)):F(1)}
def square(p):return mul(p,p)
def comm(p,q):return add(mul(p,q),scale(-1,mul(q,p)))
def from_table(C):
    out={}
    for i,row in enumerate(C):
        for j,c in enumerate(row):
            p=ONE if i==0 else scale(F(1,2),add(ONE,A(i-1)))
            q=ONE if j==0 else scale(F(1,2),add(ONE,B(j-1)))
            out=add(out,scale(c,mul(p,q)))
    return out
def chsh_identity(C):
    S=add(mul(A(0),add(B(0),scale(-1,B(1)))),scale(-1,mul(A(1),add(B(0),B(1)))))
    assert scale(4,from_table(C))==add(scale(-2,ONE),S)
    assert square(S)==add(scale(4,ONE),scale(-1,mul(comm(A(0),A(1)),comm(B(0),B(1)))))
def spectral_identities(C,which):
    if which==5:
        U=add(B(0),B(1),scale(-1,B(2))); V=add(B(0),B(1),scale(2,B(2))); T=add(B(0),scale(-1,B(1)))
        assert add(square(U),scale(F(1,2),square(V)),scale(F(3,2),square(T)))==scale(9,ONE)
        expr=add(scale(-6,ONE),mul(A(0),T),mul(A(1),add(U,ONE)),mul(A(2),add(scale(-1,U),ONE)),scale(-1,mul(A(3),V)))
        radius2=F(9); alpha2=F(4); gamma2=F(8,3); max2=F(60); contact2=F(27,5)
        # (2+2 sqrt(6))^2=28+8 sqrt(6)<60, since 6<16.
        assert F(6)<F(16) and 28+8*4==max2
    elif which==6:
        U=add(B(0),scale(-1,B(1)),B(2)); T=[add(B(1),B(2)),add(B(0),B(1)),add(B(0),scale(-1,B(2)))]
        assert add(square(U),*(square(t) for t in T))==scale(9,ONE)
        expr=add(scale(-6,ONE),mul(A(0),add(U,scale(-1,ONE))),mul(A(4),add(scale(-1,U),scale(-1,ONE))),*(mul(A(i+1),t) for i,t in enumerate(T)))
        radius2=F(9); alpha2=F(4); gamma2=F(3); max2=F(63); contact2=F(36,7)
        # (2+3 sqrt(3))^2=31+12 sqrt(3)<63, since 3<(8/3)^2.
        assert F(3)<F(64,9) and 31+12*F(8,3)==max2
    else:raise ValueError('Unknown spectral proof')
    assert scale(4,from_table(C))==expr
    # Exact two-coordinate Cauchy--Schwarz maximum on the high branch.
    assert radius2*(alpha2+gamma2)==max2
    assert contact2==radius2*alpha2/(alpha2+gamma2) and 1<contact2<radius2
def i3322_identity(C):
    ZA=scale(F(1,2),add(A(0),A(1))); XA=scale(F(1,2),add(A(1),scale(-1,A(0)))); WA=A(2)
    ZB=scale(F(1,2),add(B(0),B(1))); XB=scale(F(1,2),add(B(1),scale(-1,B(0)))); WB=B(2)
    for Z,X,W in ((ZA,XA,WA),(ZB,XB,WB)):
        assert add(mul(X,Z),mul(Z,X))=={}
        assert add(square(X),square(Z))==ONE and square(W)==ONE
    expr=add(mul(ZA,ZB),scale(F(1,2),ZA),scale(F(-1,2),ZB),scale(-1,ONE),scale(F(1,2),mul(XA,WB)),scale(F(1,2),mul(WA,XB)))
    assert from_table(C)==expr
