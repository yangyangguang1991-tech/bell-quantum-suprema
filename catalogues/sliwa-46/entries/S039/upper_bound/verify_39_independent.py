"""Second full exact implementation for Sliwa39: matrices, field, boxes.

No Bernstein generator code is imported. Every leaf is recomputed by
direct affine substitution and signed-power q interval bounds.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import comb
import json,time
import sympy as S
R=Path(__file__).resolve().parent
q,x,y,z,t,u,v,w=S.symbols('q x y z t u v w')
P=S.sympify((R/'S39_charpoly.txt').read_text())
C=json.loads((R/'S39_full_certificate.json').read_text())
ql,qh=map(F,C['q_interval']);h=S.sympify(C['q_polynomial']);tq=S.sympify(C['overlap'])
def check(ok,msg):
    if not ok:raise ArithmeticError(msg)
def sr(f):return S.Rational(f.numerator,f.denominator)
def ff(a):a=S.Rational(a);return F(int(a.p),int(a.q))
def leaf_paths(record):
    leaves=record['leaves'];check(isinstance(leaves,list) and bool(leaves),'Nonempty leaf cover required')
    paths=[r['path'] for r in leaves]
    check(all(isinstance(p,str) and len(p)%2==0 and all(p[i] in '012' and p[i+1] in '01' for i in range(0,len(p),2)) for p in paths),'Bad leaf path')
    check(len(paths)==len(set(paths)),'Duplicate leaf')
    return set(paths)
check(0<ql<qh,'Positive q enclosure required')
check(isinstance(C['central_box'],list) and len(C['central_box'])==2,'Bad central box')
a,b=map(F,C['central_box']);box=[(a,b)]*3
check(-1<a<b<1,'Central box must lie inside the overlap cube')
expected=[]
for axis in range(3):
    for lo,hi in [(F(-1),a),(b,F(1))]:
        bb=[(a,b) if i<axis else (F(-1),F(1)) for i in range(3)];bb[axis]=(lo,hi);expected.append(bb)
check(isinstance(C['outer_boxes'],list) and len(C['outer_boxes'])==6,'All six outer slabs are required')
check([[tuple(map(F,b)) for b in rec['box']] for rec in C['outer_boxes']]==expected,'Slab coverage differs')
check(isinstance(C['elementary_coefficients'],list) and len(C['elementary_coefficients'])==7,'All seven spectral coefficients required')
indices=[rec['k'] for rec in C['elementary_coefficients']]
check(all(type(k) is int for k in indices) and set(indices)==set(range(1,8)),'Spectral coefficient indices must be 1 through 7 exactly once')
for rec in C['outer_boxes']+C['elementary_coefficients']:leaf_paths(rec)
check(S.Poly(h,q).count_roots(9,10)==1,'Root selector is not unique')
check(S.Poly(h,q).count_roots(sr(ql),sr(qh))==1,'Bad isolating interval')
check(S.expand(P-P.xreplace({x:y,y:x}))==0,'Not symmetric in xy')
check(S.expand(P-P.xreplace({y:z,z:y}))==0,'Not symmetric in yz')
diag=S.factor(P.subs({x:t,y:t,z:t}))
g=q**4-8*q**3*t-32*q**2*t**3+112*q**2*t**2+16*q**2*t-168*q**2+128*q*t**4-384*q*t**3-576*q*t**2+928*q*t+768*q+256*t**6-1024*t**5+512*t**4+3456*t**3-1856*t**2-3392*t-112
check(S.expand(diag-(q*q+4*q*t-16*t**3-32*t*t-8*t-4)**2*g)==0,'Diagonal factorization failed')
def modcompose(poly):
    answer=S.Integer(0)
    for c in S.Poly(poly,t).all_coeffs():answer=S.rem(answer*tq+c,h,q)
    return S.expand(answer)
check(modcompose(g)==0 and modcompose(S.diff(g,t))==0,'Exact determinant contact failed')
terms=[(2,'A'),(2,'B'),(-1,'AB'),(1,'aB'),(1,'Ab'),(1,'ab'),(2,'C'),(-1,'AC'),(1,'aC'),(-1,'BC'),(2,'ABC'),(-1,'aBC'),(1,'bC'),(-1,'AbC'),(-2,'abC'),(1,'Ac'),(1,'ac'),(1,'Bc'),(-1,'ABc'),(-2,'aBc'),(1,'bc'),(-2,'Abc'),(1,'abc')]
I=S.eye(2);Z=S.diag(1,-1);X=S.Matrix([[0,1],[1,0]])
grid=[(-1,0),(S.Rational(-3,5),S.Rational(4,5)),(0,1),(S.Rational(3,5),S.Rational(4,5)),(1,0)]
start=time.monotonic();points=0
for angles in product(grid,repeat=3):
    obs=[[Z,a*Z+b*X] for a,b in angles];M=S.zeros(8)
    for k,word in terms:
        local=[I,I,I]
        for ch in word:party='ABC'.index(ch.upper());local[party]=obs[party][int(ch.islower())]
        M+=k*S.kronecker_product(*local)
    check(S.expand(M.charpoly(q).as_expr()-P.subs({x:angles[0][0],y:angles[1][0],z:angles[2][0]}))==0,'Literal matrix charpoly mismatch')
    points+=1
print('125 LITERAL CHARPOLYS PASS',flush=True)
def power_interval(k,a,b):
    vals=[a**k,b**k]
    if k and a<=0<=b:vals.append(F(0))
    return min(vals),max(vals)
def scalar_range(poly,variables,bounds):
    pp=S.Poly(poly,*variables);lo=hi=F(0)
    for ms,coef in pp.terms():
        aa=bb=ff(coef)
        for k,(l,r) in zip(ms,bounds):
            c,d=power_interval(k,l,r);vals=[aa*c,aa*d,bb*c,bb*d];aa,bb=min(vals),max(vals)
        lo+=aa;hi+=bb
    return lo,hi
tr=scalar_range(tq,[q],[(ql,qh)]);check(a<tr[0]<=tr[1]<b,'Stationary point outside central box')
H=S.hessian(P,(x,y,z));hr=[]
for i in range(3):
    row=[scalar_range(H[i,j],[q,x,y,z],[(ql,qh),*box]) for j in range(3)];hr.append(row)
for i in range(3):
    off=sum(max(abs(a),abs(b)) for j,(a,b) in enumerate(hr[i]) if j!=i)
    check(hr[i][i][0]>off,'Independent Hessian interval is not diagonally dominant')
print('INDEPENDENT HESSIAN PD PASS',flush=True)
def paths_cover(paths,prefix=''):
    if prefix in paths:check(not any(p!=prefix and p.startswith(prefix) for p in paths),'Overlapping leaves');return
    extensions=[p[len(prefix):] for p in paths if p.startswith(prefix)];check(bool(extensions),'Coverage gap')
    axes={p[0] for p in extensions};check(len(axes)==1,'Incoherent split axis')
    axis=next(iter(axes));check(axis in '012','Bad split axis')
    paths_cover(paths,prefix+axis+'0');paths_cover(paths,prefix+axis+'1')
def leafbox(bounds,path):
    bounds=list(bounds);check(len(path)%2==0,'Bad leaf path')
    for i in range(0,len(path),2):
        axis=int(path[i]);side=path[i+1];check(axis in [0,1,2] and side in '01','Bad subdivision')
        lo,hi=bounds[axis];mid=(lo+hi)/2;bounds[axis]=(lo,mid) if side=='0' else (mid,hi)
    return bounds
def leaf_coeff_positive(poly,bounds):
    transformed=S.Poly(S.expand(poly.subs({xx:sr(lo)+sr(hi-lo)*yy for xx,yy,(lo,hi) in zip([x,y,z],[u,v,w],bounds)})),u,v,w,q)
    dx,dy,dz,dq=transformed.degree_list();data=transformed.as_dict();minimum=None
    for i,j,k in product(range(dx+1),range(dy+1),range(dz+1)):
        cs=[F(0)]*(dq+1)
        for (aa,bb,cc,d),coef in data.items():
            if aa<=i and bb<=j and cc<=k:
                cs[d]+=ff(coef)*F(comb(i,aa),comb(dx,aa))*F(comb(j,bb),comb(dy,bb))*F(comb(k,cc),comb(dz,cc))
        low=sum(c*(ql**d if c>=0 else qh**d) for d,c in enumerate(cs))
        check(low>0,'Nonpositive independently recomputed leaf coefficient')
        minimum=low if minimum is None else min(minimum,low)
    return minimum
count=0
for index,rec in enumerate(C['outer_boxes']):
    bounds=[tuple(map(F,r)) for r in rec['box']];check(bounds==expected[index],'Slab coverage differs')
    paths=leaf_paths(rec);paths_cover(paths)
    for path in paths:leaf_coeff_positive(P,leafbox(bounds,path));count+=1
    print('OUTER SLAB',index,'INDEPENDENT PASS',len(paths),flush=True)
for rec in C['elementary_coefficients']:
    k=rec['k'];ep=S.diff(P,q,8-k)/S.factorial(8-k);bounds=[(F(-1),F(1))]*3
    paths=leaf_paths(rec);paths_cover(paths)
    for path in paths:leaf_coeff_positive(ep,leafbox(bounds,path))
    print('ELEMENTARY',k,'PASS',flush=True)
out={'status':'PASS_EXACT_FULL_GLOBAL_INDEPENDENT','literal_matrix_grid':points,'outer_positive_leaves':count,'elementary_positive_leaves':sum(len(r['leaves']) for r in C['elementary_coefficients']),
     'root_selector':'unique root in (9,10)','local_contact_zero_and_gradient':True,'independent_Hessian_PD':True,'all_slabs_and_leaf_covers_complete':True,'exact_attainment':'M(t*,t*,t*) has algebraic eigenvalue q*; global PSD identifies it as maximum','elapsed_seconds':time.monotonic()-start}
(R/'S39_independent_replay.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
