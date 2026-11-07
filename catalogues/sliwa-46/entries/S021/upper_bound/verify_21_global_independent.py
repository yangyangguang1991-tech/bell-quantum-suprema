"""Second exact global replay for S21; direct leaf substitutions, no propagation.

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
P=S.sympify((ROOT/'S21_charpoly.txt').read_text());src=ROOT/'S21_global_certificate.json';C=json.loads(src.read_text())
lo,hi=map(F,C['q_interval']);f=243*q**3+1620*q**2-8240*q-59712
def require(ok,msg):
    if not ok:raise ArithmeticError(msg)
def sr(a):return S.Rational(a.numerator,a.denominator)
def fr(a):return F(int(a.p),int(a.q))
require(f.subs(q,sr(lo))<0<f.subs(q,sr(hi)),'Cubic signs not bracketed')
require(S.diff(f,q).subs(q,4)>0 and S.diff(f,q,2).subs(q,4)>0,'Cubic unique root above4 fails')
starx=189*q*q/S.Integer(4352)+9*q/S.Integer(272)-S.Rational(553,272)
star=[starx,starx,S.Rational(1,3)]
require(C['critical_point']==list(map(str,star)),'Critical point differs')
for E in [P]+[S.diff(P,a) for a in (x,y,z)]:
    numerator=S.fraction(S.together(E.subs(dict(zip((x,y,z),star)))))[0]
    require(S.rem(S.Poly(numerator,q),S.Poly(f,q)).as_expr()==0,'Stationarity not exact')
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
# The exact critical point lies strictly inside the convex box.
sx=F(189,4352)*lo**2+F(9,272)*lo-F(553,272);sxhi=F(189,4352)*hi**2+F(9,272)*hi-F(553,272)
require(local[0][0]<sx<=sxhi<local[0][1] and local[1][0]<sx<=sxhi<local[1][1] and local[2][0]<F(1,3)<local[2][1],'Critical point outside local box')
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
out={'status':'PASS_EXACT_GLOBAL_INDEPENDENT','id':21,'q_polynomial':str(f),'root_interval':C['q_interval'],
     'all_model_upper':True,'finite_qubit_attainment_from_exact_characteristic_zero':True,
     'polynomial_count':len(expected),'positive_leaf_count':count,'independent_Hessian_DD_margins':list(map(str,dd)),
     'independent_minimum_positive_Bernstein_lower':str(minimum),'minimum_positive_decimal_display':float(minimum),
     'certificate_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'seconds':time.time()-start}
(ROOT/'S21_global_independent_replay.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='independent_minimum_positive_Bernstein_lower'},indent=2))
