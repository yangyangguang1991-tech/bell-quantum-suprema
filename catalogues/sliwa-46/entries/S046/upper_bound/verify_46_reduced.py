"""Exact replay of the unrestricted TWO-PARTY reduced Sliwa-46 branch.

This is not a certificate of the complete unrestricted tripartite Sliwa-46
maximum. No floating-point equality is used for any assertion.
"""
import itertools
import json
import hashlib
from pathlib import Path
import sympy as S

if not __debug__:
    raise RuntimeError('Run S46 exact checks without -O or -OO')

q,t,x,y,sx,sy,u,v=S.symbols('q t x y sx sy u v')
Z=S.Matrix([[1,0],[0,-1]])
X=S.Matrix([[0,1],[1,0]])
I=S.eye(2)
A=x*Z+sx*X
B=y*Z+sy*X
M=2*S.kronecker_product(Z,I)+2*S.kronecker_product(I,Z)+4*S.kronecker_product(A,B)-4*S.kronecker_product(Z,B)-4*S.kronecker_product(A,Z)-6*S.kronecker_product(Z,Z)

def reduce_reflection(expr):
    expr=S.Poly(expr,sx).rem(S.Poly(sx*sx-(1-x*x),sx)).as_expr()
    expr=S.Poly(expr,sy).rem(S.Poly(sy*sy-(1-y*y),sy)).as_expr()
    return S.expand(expr)

P=q**4+32*q**2*x*y-32*q**2*x-32*q**2*y-184*q**2-128*q*x*y+128*q*x+128*q*y+192*q-6144*x*x*y*y+6144*x*x-1920*x*y+1920*x+6144*y*y+1920*y+336
assert reduce_reflection((q*S.eye(4)-M).det()) == P
Puv=q**4-184*q*q+192*q+6144*u*u+u*(-32*q*q+128*q+1920)-6144*v*v+v*(32*q*q-128*q-14208)+336
assert S.expand(Puv.subs({u:x+y,v:x*y})-P)==0
assert S.expand(S.diff(P,x)-S.diff(P,y)-32*(x-y)*(-q*q+4*q+384*x*y+444))==0
ustar=(q*q-4*q-60)/384
vstar=(q*q-4*q-444)/384
assert S.simplify(S.diff(Puv,u).subs(u,ustar))==0
assert S.simplify(S.diff(Puv,v).subs(v,vstar))==0
assert S.simplify(1-ustar+vstar)==0

# All four boundary edges have eigenvalues <=10. By symmetry only y=+/-1.
assert S.expand(P.subs(y,1)-(q-10)**2*(q+6)*(q+14))==0
assert S.expand(P.subs(y,-1)-(q-10)*(q+6)*(q*q+4*q-64*x-76))==0
# The other two roots on y=-1 are -2 +/- sqrt(80+64x), hence <=10
# because x in [-1,1] gives 80+64x in [16,144].

ptrip=q**3+(8*t+2)*q*q+(96*t*t-32*t-180)*q+768*t**3-192*t*t-1248*t-168
assert S.expand(P.subs({x:t,y:t})-(q-8*t-2)*ptrip)==0
f=25*q**3-46*q*q-4788*q+15192
resultant=S.resultant(ptrip,S.diff(ptrip,t),t)
assert S.expand(resultant-301989888*(q-10)*(q+6)*(q+14)*f)==0

# Attaining branch t is a rational polynomial in q*. These polynomial
# identities assert both the eigenvalue equation and stationary condition.
tformula=(25*q*q-4*q-3612)/4224
assert S.rem(S.together(ptrip.subs(t,tformula)).as_numer_denom()[0],f,q)==0
assert S.rem(S.together(S.diff(ptrip,t).subs(t,tformula)).as_numer_denom()[0],f,q)==0

lo=S.Rational(12985173496317373,10**15)
hi=S.Rational(12985173496317374,10**15)
assert 10<lo<hi<13
assert f.subs(q,lo)<0<f.subs(q,hi)
assert S.diff(f,q).subs(q,10)>0
assert S.diff(f,q,2).subs(q,10)>0
# f''=150q-92>0 for q>=10, so f'>0 throughout that ray;
# these two endpoint signs isolate the unique q*>10.
assert 0<tformula.subs(q,lo)<tformula.subs(q,hi)<1

# Exact substitution from Table I #46. Formal symbols commute here only
# to extract coefficients across parties; each monomial has <=1 setting
# from each party, so no same-party ordering is erased.
aa,aaa,bb,bbb,cc,ccc=S.symbols('A a B b C c')
full=(3*aa+aaa+3*bb-2*aa*bb-aaa*bb+bbb-aa*bbb-2*aaa*bbb+
      2*aa*cc-2*aaa*cc+bb*cc-3*aa*bb*cc+4*aaa*bb*cc+
      bbb*cc-aa*bbb*cc+2*aaa*bbb*cc+aa*ccc+aaa*ccc+
      2*bb*ccc-3*aa*bb*ccc-aaa*bb*ccc-2*bbb*ccc+
      4*aa*bbb*ccc+2*aaa*bbb*ccc)
red=2*aaa+2*bbb+4*aa*bb-4*aaa*bb-4*aa*bbb-6*aaa*bbb
assert S.expand(full.subs({cc:-1,ccc:-1})-red)==0
assert max(full.subs(dict(zip([aa,aaa,bb,bbb,cc,ccc],row))) for row in itertools.product([-1,1],repeat=6))==10
assert max(red.subs(dict(zip([aa,aaa,bb,bbb],row))) for row in itertools.product([-1,1],repeat=4))==10

data={
  'scope':'Exact unrestricted two-party value of T=S46|C=c=-I; an exact lower bound, not a full tripartite S46 upper bound.',
  'polynomial':str(f),
  'root_selection':'unique real root q>10',
  'isolating_interval':[str(lo),str(hi)],
  'attaining_t':str(tformula),
  'attaining_measurements':'a=b=Z, A=B=tZ+sqrt(1-t^2)X; third party C=c=-I',
  'exact_checks':[
    'original S46 substitution',
    'local bounds by all 64 and 16 deterministic assignments',
    '4x4 characteristic polynomial under exact reflection identities',
    'x,y symmetric polynomial and all edge factorisations',
    'interior critical-point gradient identities (no presumed optimizer symmetry)',
    'diagonal factorisation and exact resultant',
    'attainment t(q) identities modulo cubic',
    'rational isolation and t in (0,1)'
  ],
  'result':'PASS'
}
certificate=Path(__file__).with_name('certificate_46_reduced.json')
supplied=json.loads(certificate.read_text(encoding='utf-8'))
if S.Poly(S.sympify(supplied['polynomial']),q,domain=S.QQ)!=S.Poly(f,q,domain=S.QQ):
    raise ArithmeticError('S46 reduced input polynomial differs from the derived exact target')
if tuple(map(S.Rational,supplied['isolating_interval']))!=(lo,hi):
    raise ArithmeticError('S46 reduced input interval differs from the derived exact selector')
if not S.Poly(S.sympify(supplied['attaining_t'])-tformula,q,domain=S.QQ).is_zero:
    raise ArithmeticError('S46 reduced input attaining overlap differs from the exact formula')
data['input_binding']='PASS_EXACT_REDUCED_INPUT_BINDING'
data['certificate_sha256']=hashlib.sha256(certificate.read_bytes()).hexdigest()
Path(__file__).with_name('verification_46_reduced.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(data,ensure_ascii=False,indent=2))
