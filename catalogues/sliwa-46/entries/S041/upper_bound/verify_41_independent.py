"""Independent full matrix/box/leaf checks: imports no Bernstein generator."""
if not __debug__:
    raise RuntimeError('Run S41 certificate checks without Python -O/-OO: assertions must remain enabled.')
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import comb
import re,json,time
import sympy as S
OUT=Path(__file__).resolve().parent
q,x,y,z,u,v,w=S.symbols('q x y z u v w')
P=S.sympify((OUT/'S41_charpoly.txt').read_text())
C=json.loads((OUT/'S41_full_certificate.json').read_text())
RC=json.loads((OUT/'S41_selected_root.json').read_text())
ql,qh=map(F,C['q_interval'])
def check(ok,msg):
    if not ok:raise ArithmeticError(msg)
def sr(v):return S.Rational(v.numerator,v.denominator)
def ff(v):v=S.Rational(v);return F(int(v.p),int(v.q))
check(len(RC['equations'])==4,'Exactly four root equations required')
check(RC['variables']==['q','x','y','z'],'Root variable ordering mismatch')
check(len(RC['centers'])==len(RC['box'])==4,'Exactly four root coordinates required')
check(C['q_interval']==RC['box'][0],'Global q interval must equal selected-root q box')
check(0<ql<qh,'Positive ordered q interval required')
check(len(C['outer_boxes'])==6,'Exactly six outer slabs required')
check(len(C['elementary_coefficients'])==7 and {r['k']for r in C['elementary_coefficients']}==set(range(1,8)),'Exactly k=1,...,7 required')
check(len(C['central_box'])==3,'Three central coordinates required')
check(all(-1<F(a)<F(b)<1 for a,b in C['central_box']),'Central box must be inside overlap cube')
system=[P,S.diff(P,x),S.diff(P,y),S.diff(P,z)]
check(all(S.expand(S.sympify(a)-b)==0 for a,b in zip(RC['equations'],system)),'Wrong selected-root equations')


class RI:
    scale=1<<384
    __slots__=('a','b')
    def __init__(self,a=0,b=None):
        a=F(a);b=F(a if b is None else b)
        self.a=F(a.numerator*self.scale//a.denominator,self.scale)
        self.b=F(-((-b.numerator*self.scale)//b.denominator),self.scale)
    @staticmethod
    def c(v):return v if isinstance(v,RI)else RI(v)
    def __add__(self,v):v=self.c(v);return RI(self.a+v.a,self.b+v.b)
    __radd__=__add__
    def __neg__(self):return RI(-self.b,-self.a)
    def __sub__(self,v):return self+-self.c(v)
    def __rsub__(self,v):return self.c(v)+-self
    def __mul__(self,v):
        v=self.c(v);p=[self.a*v.a,self.a*v.b,self.b*v.a,self.b*v.b];return RI(min(p),max(p))
    __rmul__=__mul__
    def inv(self):check(not self.a<=0<=self.b,'division interval zero');return RI(1/self.b,1/self.a)
    def __truediv__(self,v):return self*self.c(v).inv()
    def __rtruediv__(self,v):return self.c(v)*self.inv()
    def __pow__(self,k):
        check(int(k)==k,'noninteger power');k=int(k)
        if k<0:return self.inv()**(-k)
        ans=RI(1)
        while k:
            if k&1:ans=ans*self
            self=self*self;k>>=1
        return ans
centers=list(map(F,RC['centers']));radius=F(RC['radius'])
check(radius>0,'Positive root radius required')
check(all([c-radius,c+radius]==list(map(F,b)) for c,b in zip(centers,RC['box'])),'Root centers plus or minus radius must equal stored box')
bounds=[RI(a-radius,a+radius)for a in centers]
J=S.Matrix(system).jacobian([q,x,y,z]);fun=S.lambdify((q,x,y,z),[*system,*list(J)],modules='math',cse=True)
f0=list(map(RI.c,fun(*map(RI,centers))));fx=list(map(RI.c,fun(*bounds)))
R=[[F(v)for v in row]for row in RC['preconditioner']]
Kmat=[[RI(int(i==j))-sum(R[i][k]*fx[4+4*k+j]for k in range(4))for j in range(4)]for i in range(4)]
image=[RI(centers[i])-sum(R[i][j]*f0[j]for j in range(4))+sum(Kmat[i][j]*RI(-radius,radius)for j in range(4))for i in range(4)]
check(all(bounds[i].a<image[i].a<=image[i].b<bounds[i].b for i in range(4)),'Independent root strict inclusion failed')
check(all(centers[i]-radius<image[i].a<=image[i].b<centers[i]+radius for i in range(4)),'Root image outside unrounded stored rational box')
contraction=max(sum(max(abs(v.a),abs(v.b))for v in row)for row in Kmat)
check(contraction<1,'Independent root contraction failed')
print('INDEPENDENT SELECTED ROOT PASS',flush=True)

source='A + B + AB + C + aC - 3ABC - aBC + bC - AbC - 2abC + Ac - ac + Bc - 4ABc + aBc - bc + Abc + 2abc'
terms=[]
for term in re.findall(r'[+-]?[^+-]+',source.replace(' ','')):
    sign,num,word=re.fullmatch(r'([+-]?)(\d*)([AaBbCc]+)',term).groups()
    terms.append(((-1 if sign=='-' else 1)*(int(num)if num else 1),word))
I=S.eye(2);Z=S.diag(1,-1);X=S.Matrix([[0,1],[1,0]])
grid=[(-1,0),(S.Rational(-3,5),S.Rational(4,5)),(0,1),(S.Rational(3,5),S.Rational(4,5)),(1,0)]
start=time.monotonic();points=0
for angles in product(grid,repeat=3):
    obs=[[Z,a*Z+b*X]for a,b in angles];M=S.zeros(8)
    for cv,word in terms:
        local=[I,I,I]
        for ch in word:local['ABC'.index(ch.upper())]=obs['ABC'.index(ch.upper())][int(ch.islower())]
        M+=cv*S.kronecker_product(*local)
    check(M.charpoly().all_coeffs()==S.Poly(P.subs({x:angles[0][0],y:angles[1][0],z:angles[2][0]}),q).all_coeffs(),'Literal matrix charpoly mismatch')
    points+=1
print('125 LITERAL CHARPOLYS PASS',flush=True)

def power_range(k,a,b):
    vals=[a**k,b**k]
    if k and a<=0<=b:vals.append(F(0))
    return min(vals),max(vals)
def scalar_range(poly,variables,bounds):
    pp=S.Poly(poly,*variables);lo=hi=F(0)
    for ms,coef in pp.terms():
        aa=bb=ff(coef)
        for k,(l,r)in zip(ms,bounds):
            c,d=power_range(k,l,r);products=[aa*c,aa*d,bb*c,bb*d];aa,bb=min(products),max(products)
        lo+=aa;hi+=bb
    return lo,hi
central=[tuple(map(F,b))for b in C['central_box']]
for axis in range(3):
    l,h=map(F,RC['box'][axis+1]);check(central[axis][0]<l<h<central[axis][1],'Root outside central box')

def centered_range(poly):
    mids=[(a+b)/2 for a,b in central]
    radii=[(b-a)/2 for a,b in central]
    shifted=S.Poly(S.expand(poly.subs({a:sr(m)+b for a,b,m in zip([x,y,z],[u,v,w],mids)})),u,v,w)
    low=high=F(0)
    for ms,coefficient in shifted.terms():
        aa,bb=scalar_range(coefficient,[q],[(ql,qh)])
        for degree,radius in zip(ms,radii):
            l,h=power_range(degree,-radius,radius)
            ps=[aa*l,aa*h,bb*l,bb*h];aa,bb=min(ps),max(ps)
        low+=aa;high+=bb
    return low,high
T=S.Matrix(C['hessian_congruence']);check(T.det()!=0,'Singular Hessian congruence');H=T.T*S.hessian(P,(x,y,z))*T;hr=[[centered_range(H[i,j])for j in range(3)]for i in range(3)]
for i in range(3):
    off=sum(max(abs(a),abs(b))for j,(a,b)in enumerate(hr[i])if j!=i)
    check(hr[i][i][0]>off,'Independent unshifted Hessian interval failed')
print('INDEPENDENT HESSIAN PD PASS',flush=True)

def paths_cover(paths,prefix=''):
    if prefix in paths:
        check(not any(p!=prefix and p.startswith(prefix)for p in paths),'Overlapping leaves');return
    tails=[p[len(prefix):]for p in paths if p.startswith(prefix)]
    check(bool(tails),'Coverage gap');axes={p[0]for p in tails};check(len(axes)==1,'Incoherent axis')
    axis=next(iter(axes));check(axis in '012','Bad axis')
    paths_cover(paths,prefix+axis+'0');paths_cover(paths,prefix+axis+'1')
def leafbox(box,path):
    box=list(box);check(len(path)%2==0,'Bad path length')
    for i in range(0,len(path),2):
        a=int(path[i]);side=path[i+1];check(a in [0,1,2]and side in '01','Bad split')
        l,h=box[a];mid=(l+h)/2;box[a]=(l,mid)if side=='0'else(mid,h)
    return box
def leaf_positive(poly,box):
    expr=S.Poly(S.expand(poly.subs({a:sr(l)+sr(h-l)*b for a,b,(l,h)in zip([x,y,z],[u,v,w],box)})),u,v,w,q)
    dx,dy,dz,dq=expr.degree_list();data=expr.as_dict();minimum=None
    for i,j,k in product(range(dx+1),range(dy+1),range(dz+1)):
        cs=[F(0)]*(dq+1)
        for(a,b,c,d),coef in data.items():
            if a<=i and b<=j and c<=k:cs[d]+=ff(coef)*F(comb(i,a),comb(dx,a))*F(comb(j,b),comb(dy,b))*F(comb(k,c),comb(dz,c))
        low=sum(cv*(ql**d if cv>=0 else qh**d)for d,cv in enumerate(cs))
        check(low>0,'Nonpositive independently recomputed Bernstein leaf')
        minimum=low if minimum is None else min(minimum,low)
    return minimum
expected=[]
for axis in range(3):
    a,b=central[axis]
    for l,h in [(F(-1),a),(b,F(1))]:
        bb=[central[i]if i<axis else(F(-1),F(1))for i in range(3)];bb[axis]=(l,h);expected.append(bb)
count=0
for index,record in enumerate(C['outer_boxes']):
    bb=[tuple(map(F,b))for b in record['box']];check(bb==expected[index],'Slab cover differs')
    paths={r['path']for r in record['leaves']};check(len(paths)==len(record['leaves']),'Repeated leaf');paths_cover(paths)
    for path in paths:leaf_positive(P,leafbox(bb,path));count+=1
    print('OUTER SLAB',index,'PASS',len(paths),flush=True)
for record in C['elementary_coefficients']:
    k=record['k'];ep=S.diff(P,q,8-k)/S.factorial(8-k)
    paths={r['path']for r in record['leaves']};check(len(paths)==len(record['leaves']),'Repeated elementary leaf');paths_cover(paths)
    for path in paths:leaf_positive(ep,leafbox([(F(-1),F(1))]*3,path))
    print('ELEMENTARY',k,'PASS',flush=True)
data={'status':'PASS_INDEPENDENT_EXACT_FULL_GLOBAL_S41',
      'selected_root_replayed_independently':True,'outward_bits':384,
      'root_box_and_q_interval_bindings_checked':True,'exactly_six_slabs_and_seven_elementary_coefficients':True,
      'literal_matrix_grid':points,'outer_positive_leaves':count,
      'elementary_positive_leaves':sum(len(r['leaves'])for r in C['elementary_coefficients']),
      'independent_hessian_PD':True,'all_slab_and_leaf_covers_complete':True,
      'exact_attainment':'Selected full root imposes P(q*,x*,y*,z*)=P_x=P_y=P_z=0; complete PSD proves this physical qubit eigenvalue is global maximum',
      'seconds':time.monotonic()-start}
(OUT/'S41_independent_replay.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print(json.dumps(data,indent=2),flush=True)
