"""Second exact global replay for S27; direct leaf substitutions, no propagation.

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
P=S.sympify((ROOT/'S27_charpoly.txt').read_text());src=ROOT/'S27_global_certificate.json';C=json.loads(src.read_text())
lo,hi=map(F,C['q_interval']);point=json.loads((ROOT/'S27_exact_algebraic_point.json').read_text())
f=S.sympify(point['q_minimal_polynomial']);xp=S.sympify(point['x_coordinate_rational_polynomial']);yp=S.sympify(point['y_coordinate_rational_polynomial'])
def require(ok,msg):
    if not ok:raise ArithmeticError(msg)
def sr(a):return S.Rational(a.numerator,a.denominator)
def fr(a):return F(int(a.p),int(a.q))
require(C['root_certificate_sha256']==hashlib.sha256((ROOT/'S27_exact_algebraic_point.json').read_bytes()).hexdigest(),'Algebraic-point binding changed')
require(C['charpoly_sha256']==hashlib.sha256((ROOT/'S27_charpoly.txt').read_bytes()).hexdigest(),'Characteristic binding changed')
require(C['q_interval']==point['q_root_isolating_interval'],'Root interval mismatch')
require(S.Poly(f,q).count_roots(sr(lo),sr(hi))==1,'Scalar algebraic root is not uniquely isolated')
# Independent nested-Horner composition in Q[q]/(f), without the generator's
# table of separately precomputed field powers.
mod=S.Poly(f,q);qx=S.Poly(q,q);px=S.Poly(xp,q);py=S.Poly(yp,q)
require(mod.degree()==17 and mod.is_irreducible,'Degree17 minimal-polynomial claim failed')
require(px.degree()==16 and py.degree()==16,'Coordinate-polynomial degrees changed')
def field_compose(E):
    poly=S.Poly(E,q,x,y);dq,dx,dy=poly.degree_list();terms=poly.as_dict();out=S.Poly(0,q)
    for i in range(dq,-1,-1):
        a=S.Poly(0,q)
        for j in range(dx,-1,-1):
            b=S.Poly(0,q)
            for k in range(dy,-1,-1):b=(b*py+S.Poly(terms.get((i,j,k),0),q)).rem(mod)
            a=(a*px+b).rem(mod)
        out=(out*qx+a).rem(mod)
    return out
for E in [P,S.diff(P,x),S.diff(P,y),S.diff(P,z)]:
    require(field_compose(E.subs(z,y)).is_zero,'Full algebraic contact identity failed')
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
# Signed-power q interval bounds for the two degree16 coordinate polynomials.
def coordinate_bounds(p):
    co=S.Poly(p,q)
    low=sum(fr(co.nth(k))*(lo**k if co.nth(k)>=0 else hi**k) for k in range(co.degree()+1))
    high=sum(fr(co.nth(k))*(hi**k if co.nth(k)>=0 else lo**k) for k in range(co.degree()+1))
    return low,high
sx,sxhi=coordinate_bounds(xp);sy,syhi=coordinate_bounds(yp)
require(local[0][0]<sx<=sxhi<local[0][1] and all(a<sy<=syhi<b for a,b in local[1:]),'Algebraic critical point outside local box')
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
a0,b0=local[0];a1,b1=local[1];a2,b2=local[2]
boxes=[[(F(-1),a0),full[1],full[2]],[(b0,F(1)),full[1],full[2]],
       [local[0],(F(-1),a1),full[2]],[local[0],(b1,F(1)),full[2]],
       [local[0],local[1],(F(-1),a2)],[local[0],local[1],(b2,F(1))]]
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
out={'status':'PASS_EXACT_GLOBAL_INDEPENDENT','id':27,'q_polynomial':str(f),'root_interval':C['q_interval'],
     'all_model_upper':True,'finite_qubit_attainment_from_exact_characteristic_zero':True,'algebraic_point_definition':'degree17 isolated q root, x(q),y(q) degree16; z=y',
     'polynomial_count':len(expected),'positive_leaf_count':count,'independent_Hessian_DD_margins':list(map(str,dd)),
     'independent_minimum_positive_Bernstein_lower':str(minimum),'minimum_positive_decimal_display':float(minimum),
     'certificate_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'seconds':time.time()-start}
(ROOT/'S27_global_independent_replay.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='independent_minimum_positive_Bernstein_lower'},indent=2))
