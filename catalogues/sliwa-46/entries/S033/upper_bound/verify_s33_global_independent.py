"""Second exact global replay for S33; direct leaf substitutions, no propagation.

Uses signed-power coefficient interval bounds instead of generator Horner, and
recomputes every Bernstein coefficient on every final leaf rectangle.
"""
from fractions import Fraction as F
from math import comb
from itertools import product
from pathlib import Path
import json,time,hashlib
import sympy as S
if not __debug__:raise RuntimeError('Exact certificate checks require ordinary Python; do not use -O or -OO.')
ROOT=Path(__file__).resolve().parent
q,x,y,z,u,v,w=S.symbols('q x y z u v w')
P=S.sympify((ROOT/'S33_charpoly.txt').read_text());src=ROOT/'S33_global_certificate.json';C=json.loads(src.read_text())
lo,hi=map(F,C['q_interval']);point=json.loads((ROOT/'S33_exact_algebraic_point.json').read_text())
f=S.sympify(point['q_minimal_polynomial']);tp=S.sympify(point['common_measurement_cosine_rational_polynomial'])
def require(ok,msg):
    if not ok:raise ArithmeticError(msg)
def sr(a):return S.Rational(a.numerator,a.denominator)
def fr(a):return F(int(a.p),int(a.q))
require(C['root_certificate_sha256']==hashlib.sha256((ROOT/'S33_exact_algebraic_point.json').read_bytes()).hexdigest(),'Algebraic-point binding changed')
require(C['charpoly_sha256']==hashlib.sha256((ROOT/'S33_charpoly.txt').read_bytes()).hexdigest(),'Characteristic binding changed')
require(C['q_interval']==point['q_root_isolating_interval'],'Root interval mismatch')
require(S.Poly(f,q).count_roots(sr(lo),sr(hi))==1,'Scalar algebraic root is not uniquely isolated')
t=S.Symbol('t');diag=S.expand(P.subs({x:t,y:t,z:t}))
Fpoly=next(a for a,b in S.factor_list(diag)[1] if S.degree(a,q)==4)
for E in [Fpoly,S.diff(Fpoly,t)]:
    numerator,denominator=S.fraction(S.together(E.subs(t,tp)))
    require(S.rem(numerator,f,q)==0 and denominator!=0,'Exact algebraic stationary composition failed')
quotient,remainder=S.div(diag,Fpoly,q);require(remainder==0,'Diagonal factorization failed')
require(S.expand(P-P.xreplace({x:y,y:x}))==0 and S.expand(P-P.xreplace({x:z,z:x}))==0,'Permutation symmetry failed')
for a in (x,y,z):require(S.expand(3*S.diff(P,a).subs({x:t,y:t,z:t})-S.diff(diag,t))==0,'Full three-variable stationarity identity failed')
local=list(map(lambda r:tuple(map(F,r)),C['local_convexity_box']));full=[(F(-1),F(1))]*3
def direct_bounds(expr,box):
    E=S.Poly(S.expand(expr.subs({x:sr(box[0][0])+sr(box[0][1]-box[0][0])*u,
                               y:sr(box[1][0])+sr(box[1][1]-box[1][0])*v,
                               z:sr(box[2][0])+sr(box[2][1]-box[2][0])*w})),u,v,w,q)
    dx,dy,dz,dq=E.degree_list();power=E.as_dict();bounds=[]
    for i,j,k in product(range(dx+1),range(dy+1),range(dz+1)):
        co=[F(0)]*(dq+1)
        for (a,b,c,t),cv in power.items():
            if a<=i and b<=j and c<=k:co[t]+=fr(cv)*F(comb(i,a),comb(dx,a))*F(comb(j,b),comb(dy,b))*F(comb(k,c),comb(dz,c))
        low=sum(cv*(lo**t if cv>=0 else hi**t) for t,cv in enumerate(co))
        high=sum(cv*(hi**t if cv>=0 else lo**t) for t,cv in enumerate(co));bounds.append((low,high))
    return min(a for a,b in bounds),max(b for a,b in bounds)
H=S.hessian(P,(x,y,z));hb={}
for i in range(3):
    for j in range(i,3):hb[i,j]=direct_bounds(H[i,j],local)
dd=[]
for i in range(3):
    margin=hb[i,i][0]-sum(max(abs(a),abs(b)) for j in range(3) if j!=i for a,b in [hb[min(i,j),max(i,j)]])
    require(margin>0,'Independent local Hessian diagonal dominance failed');dd.append(margin)
# Enclose t(q*) by independent signed-power evaluation of its degree11 polynomial.
cotp=S.Poly(tp,q)
sx=sum(fr(cotp.nth(k))*(lo**k if cotp.nth(k)>=0 else hi**k) for k in range(cotp.degree()+1))
sxhi=sum(fr(cotp.nth(k))*(hi**k if cotp.nth(k)>=0 else lo**k) for k in range(cotp.degree()+1))
require(all(a<sx<=sxhi<b for a,b in local),'Algebraic critical point outside local box')
def cover(paths,prefix=()):
    if prefix in paths:
        require(not any(a!=prefix and a[:len(prefix)]==prefix for a in paths),'Overlapping certificate leaves');return
    below=[p for p in paths if p[:len(prefix)]==prefix];require(bool(below),'Missing rectangle')
    axes={a[len(prefix)][0] for a in below};require(len(axes)==1,'Inconsistent split axes')
    axis=next(iter(axes));require(axis in (0,1,2),'Invalid split axis')
    cover(paths,prefix+((axis,0),));cover(paths,prefix+((axis,1),))
def rectangle(box,path):
    box=list(box)
    for axis,side in path:
        require(axis in (0,1,2) and side in (0,1),'Invalid split token');a,b=box[axis];mid=(a+b)/2
        box[axis]=(a,mid) if side==0 else (mid,b)
    return box
a,b=local[0];c,d=local[2]
boxes=[[(F(-1),a),full[1],full[2]],[(b,F(1)),full[1],full[2]],
       [local[0],(F(-1),a),full[2]],[local[0],(b,F(1)),full[2]],
       [local[0],local[1],(F(-1),c)],[local[0],local[1],(d,F(1))]]
expected={f'P_q_derivative_order_{i}':(S.diff(P,q,i)/S.factorial(i),full) for i in range(1,9)}
expected.update({f'P_exterior_box_{i}':(P,box) for i,box in enumerate(boxes)})
require(set(expected)=={r['name'] for r in C['records']},'Polynomial cover differs')
start=time.time();count=0;minimum=None
for rec in C['records']:
    expr,box=expected[rec['name']];require(rec['box']==[[str(a),str(b)] for a,b in box],'Initial rectangle differs')
    paths=[tuple(map(tuple,v['path'])) for v in rec['positive_leaf_cover']];require(len(paths)==len(set(paths)),'Duplicate leaf');cover(set(paths))
    for path in paths:
        low,unused=direct_bounds(expr,rectangle(box,path));require(low>0,('Independent leaf not positive',rec['name'],path))
        minimum=low if minimum is None else min(minimum,low);count+=1
    print(rec['name'],'PASS',len(paths),flush=True)
out={'status':'PASS_EXACT_GLOBAL_INDEPENDENT','id':33,'q_polynomial':str(f),'root_interval':C['q_interval'],
     'all_model_upper':True,'finite_qubit_attainment_from_exact_characteristic_zero':True,'algebraic_point_definition':'degree12 isolated q root, t(q) degree11',
     'polynomial_count':len(expected),'positive_leaf_count':count,'independent_Hessian_DD_margins':list(map(str,dd)),
     'independent_minimum_positive_Bernstein_lower':str(minimum),'minimum_positive_decimal_display':float(minimum),
     'certificate_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'seconds':time.time()-start}
(ROOT/'S33_global_independent_replay.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='independent_minimum_positive_Bernstein_lower'},indent=2))
