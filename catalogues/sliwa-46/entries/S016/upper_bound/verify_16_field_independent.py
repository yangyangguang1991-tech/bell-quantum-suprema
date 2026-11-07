"""Independent full-field positivity replay: direct leaves and root intervals.

Does not import the certificate generator. Uses a rational isolating interval
for sqrt(13), rather than its exact square-comparison field-sign method.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
from itertools import product
import json,time
import sympy as S
B=Path(__file__).resolve().parent
q,r,x,y,z,t,d,u,v,w,U,V,W=S.symbols('q r x y z t d u v w U V W')
P=S.sympify((B/'charpoly_16_full.txt').read_text());C=json.loads((B/'certificate_16_field_bernstein.json').read_text())
def require(ok,msg):
    if not ok:raise ArithmeticError(msg)
def ff(a):a=S.Rational(a);return F(int(a.p),int(a.q))
def sr(a):return S.Rational(a.numerator,a.denominator)
require(all(a[0][0]%2==0 for a in S.Poly(P,q).terms()),'Odd Bell eigenvalue polynomial coefficient')
R=S.expand(sum(c*r**(i[0]//2) for i,c in S.Poly(P,q).terms()))
f=243*r*r-12256*r+117504
sq=F(int(S.floor(S.sqrt(13).evalf(90)*10**60)),10**60);sqh=sq+F(1,10**60)
require(sq*sq<13<sqh*sqh,'sqrt13 rational isolation failed')
rl=(F(6128)+832*sq)/243;rh=(F(6128)+832*sqh)/243
D=S.sympify((B/'charpoly_16_derivative.txt').read_text())
cases={}
for k in range(1,4):cases[f'shifted_e{k}_whole_cube']=(S.expand(S.diff(R,r,4-k)/S.factorial(4-k)).subs({x:2*u-1,y:2*v-1,z:2*w-1}),True)
cases['det_x_nonnegative']=(R.subs({x:u,y:2*v-1,z:2*w-1}),True)
cases['d_derivative_x_negative_t_nonnegative']=(D.subs({x:u-1,t:v,d:4*w*(1-v)**2}),False)
cases['d_derivative_x_negative_t_nonpositive']=(D.subs({x:u-1,t:-v,d:4*w*(1-v)**2}),False)
require(set(cases)=={rec['name'] for rec in C['records']},'Case set differs')
def cover(paths,prefix=''):
    if prefix in paths:require(not any(p!=prefix and p.startswith(prefix) for p in paths),'Leaf overlap');return
    require(any(p.startswith(prefix) for p in paths),'Leaf gap')
    for k in '01234567':cover(paths,prefix+k)
def rectangle(path):
    bb=[(F(0),F(1))]*3
    for ch in path:
        require(ch in '01234567','Bad octree token');a=int(ch)
        for axis,bit in enumerate([4,2,1]):
            lo,hi=bb[axis];mid=(lo+hi)/2;bb[axis]=(mid,hi) if a&bit else (lo,mid)
    return bb
def positive(expr,box,strict):
    expr=S.expand(expr.subs({p:sr(a)+sr(b-a)*vv for p,vv,(a,b) in zip([u,v,w],[U,V,W],box)}))
    expr=S.Poly(expr,r).rem(S.Poly(f,r)).as_expr()
    pp=S.Poly(expr,r,U,V,W);dr,dx,dy,dz=pp.degree_list();require(dr<=1,'Field degree not reduced');terms=pp.as_dict();zero=0
    for i,j,k in product(range(dx+1),range(dy+1),range(dz+1)):
        pair=[F(0),F(0)]
        for (e,aa,bb,cc),c in terms.items():
            if aa<=i and bb<=j and cc<=k:pair[e]+=ff(c)*F(comb(i,aa),comb(dx,aa))*F(comb(j,bb),comb(dy,bb))*F(comb(k,cc),comb(dz,cc))
        if pair==[0,0]:require(not strict,'Zero strict coefficient');zero+=1;continue
        low=pair[0]+pair[1]*(rl if pair[1]>=0 else rh)
        require(low>0,'Independent field coefficient failed positive interval bound')
    return zero
start=time.monotonic();leaves=0;zeros=0
for rec in C['records']:
    expr,strict=cases[rec['name']];require(strict==rec['strict'],'Strictness differs')
    paths={a['path'] for a in rec['leaves']};require(len(paths)==len(rec['leaves']),'Duplicate leaf');cover(paths)
    for path in paths:zeros+=positive(expr,rectangle(path),strict);leaves+=1
    print('INDEPENDENT FIELD',rec['name'],'PASS',len(paths),flush=True)
out={'status':'PASS_EXACT_FULL_FIELD_INDEPENDENT','polynomial_cases':len(cases),'leaf_boxes':leaves,'retained_exact_zero_boundary_coefficients':zeros,
     'method':'Direct affine substitution on every leaf, reduction modulo quadratic, independently isolated rational sqrt13 interval sign bounds and full octree cover',
     'elapsed_seconds':time.monotonic()-start}
(B/'verification_16_field_independent.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
