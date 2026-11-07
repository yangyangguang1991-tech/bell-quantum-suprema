"""Independent exact full Sliwa-46 positivity verification.

Recomputes each polynomial directly on every leaf rectangle instead of
reusing the generator's de Casteljau coefficient propagation. Interval
evaluation uses signed power sums, rather than its Horner algorithm.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import sympy as S
import json,time,hashlib
root=Path(__file__).resolve().parent
base=root
q,x,y,z,r,u,v=S.symbols('q x y z r u v')
P=S.sympify((base/'charpoly_46_full.txt').read_text())
C=json.loads((base/'certificate_46_full_bernstein.json').read_text())
lo,hi=map(F,C['q_interval'])
def require(ok,msg):
    if not ok:raise ArithmeticError(msg)
def sr(f):return S.Rational(f.numerator,f.denominator)
polys={}
for k in range(1,8):
    ep=S.Poly(S.expand(S.diff(P,q,8-k).subs(z,1-2*r)/S.factorial(8-k)),r)
    n=ep.degree()
    for i in range(n+1):polys[f'e{k}:zBernstein{i}/{n}']=S.expand(sum(ep.nth(j)*S.Rational(comb(i,j),comb(n,j)) for j in range(i+1)))
segments=[(F(0),F(1,16)),(F(1,16),F(1,4)),(F(1,4),F(1,2)),(F(1,2),F(1))]
for si,(a,b) in enumerate(segments):
    ep=S.Poly(S.expand(P.subs(z,1-2*(sr(a)+(sr(b)-sr(a))*r))),r)
    require(ep.degree()==4,'Incorrect Charlie degree')
    for i in range(5):
        if si==0 and i==0:continue
        polys[f'e8:segment{si}:zBernstein{i}/4']=S.expand(sum(ep.nth(j)*S.Rational(comb(i,j),comb(4,j)) for j in range(i+1)))
require(set(polys)=={a['name'] for a in C['records']},'Certificate polynomial set differs')
def cover(paths,prefix=''):
    if prefix in paths:
        require(not any(p!=prefix and p.startswith(prefix) for p in paths),'Overlapping leaves')
        return
    require(any(p.startswith(prefix) for p in paths),'Missing subrectangle')
    for k in '0123':cover(paths,prefix+k)
def rectangle(path):
    ax,bx,ay,by=F(0),F(1),F(0),F(1)
    for k in path:
        require(k in '0123','Invalid quadtree path')
        mx,my=(ax+bx)/2,(ay+by)/2
        if k in '01':bx=mx
        else:ax=mx
        if k in '02':by=my
        else:ay=my
    return ax,bx,ay,by
count=0;minimum=None;start=time.monotonic()
for record in C['records']:
    paths=[a['path'] for a in record['positive_leaf_subdivision']]
    require(len(paths)==len(set(paths)),'Duplicate leaf')
    cover(set(paths))
    for path in paths:
        ax,bx,ay,by=rectangle(path)
        leaf=S.Poly(S.expand(polys[record['name']].subs({x:2*(sr(ax)+(sr(bx)-sr(ax))*u)-1,y:2*(sr(ay)+(sr(by)-sr(ay))*v)-1})),u,v,q)
        dx,dy,dq=leaf.degree_list();power=leaf.as_dict()
        for i in range(dx+1):
            for j in range(dy+1):
                coeff=[F(0)]*(dq+1)
                for (a,b,k),c in power.items():
                    if a<=i and b<=j:
                        coeff[k]+=F(int(c.p),int(c.q))*F(comb(i,a),comb(dx,a))*F(comb(j,b),comb(dy,b))
                lower=sum(c*(lo**k if c>=0 else hi**k) for k,c in enumerate(coeff))
                require(lower>0,('Nonpositive independent Bernstein coefficient',record['name'],path,i,j))
                minimum=lower if minimum is None else min(minimum,lower)
        count+=1
    print(record['name'],'independent leaf positivity PASS',len(paths),flush=True)
out={'status':'PASS_EXACT','polynomials':len(polys),'leaf_rectangles':count,'largest_subdivision_depth':max(len(a['path']) for b in C['records'] for a in b['positive_leaf_subdivision']),
     'independent_minimum_lower_bound':str(minimum),'independent_minimum_decimal_for_display':float(minimum),
     'certificate_sha256':hashlib.sha256((base/'certificate_46_full_bernstein.json').read_bytes()).hexdigest(),
     'method':'Direct rational affine substitution on every rectangle, recomputed Bernstein coefficients, signed-power q interval bounds, exact quadtree cover',
     'elapsed_seconds':time.monotonic()-start}
(root/'independent_sliwa46_bernstein_replay.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
