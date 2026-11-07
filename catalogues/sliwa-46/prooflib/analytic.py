"""Exact single-entry algebraic and Bernstein upper verification."""
if not __debug__: raise RuntimeError('Exact replay requires Python without -O/-OO')
import json,re,time,hashlib,itertools
from pathlib import Path
from fractions import Fraction as F
from math import comb
from functools import cmp_to_key
import sympy as S
from sympy.polys.matrices import DomainMatrix
import sys
D=Path(sys.argv[1]).resolve()
ENTRY=json.loads((D.parent/'functional.json').read_text())
q,x,y,z=S.symbols('q x y z');VS=[x,y,z]
R0=(F(0),F(0))
def plus(a,b):return(a[0]+b[0],a[1]+b[1])
def times(a,t):return(a[0]*t,a[1]*t)
def sg(a,d):
 u,v=a
 if not v:return (u>0)-(u<0)
 if not u:return (v>0)-(v<0)
 if u*v>0:return (u>0)-(u<0)
 h=u*u-d*v*v
 return ((h>0)-(h<0))*((u>0)-(u<0))
def conv(a,d):
 a=S.expand(a);v=a.coeff(S.sqrt(d))if d else 0;u=S.expand(a-v*S.sqrt(d))if d else a
 return F(u),F(v)
def poly(expr,d,parity=None):
 p=S.Poly(S.expand(expr),*VS);ts={ms:conv(c,d)for ms,c in p.terms()}
 if parity:
  assert all(all(m%2==0 for ms in ts for m,pa in zip(ms,parity)if pa)for _ in[0])
  ts={tuple(m//2 if pa else m for m,pa in zip(ms,parity)):v for ms,v in ts.items()}
 deg=[max(ms[j]for ms in ts)for j in range(3)];return ts,deg

def coefficient_tensor(expr,d,box,parity=None):
 # Direct closed formula at every leaf, no de Casteljau recurrence.
 ts,deg=poly(expr,d,parity);out=[]
 transforms={}
 for ax in range(3):
  a,b=box[ax]
  for n in range(deg[ax]+1):
   for m in range(deg[ax]+1):
    transforms[ax,n,m]=sum(F(comb(m,j))*a**(m-j)*(b-a)**j*F(comb(n,j),comb(deg[ax],j))for j in range(min(m,n)+1))
 for ns in itertools.product(*[range(dd+1)for dd in deg]):
  acc=R0
  for ms,cv in ts.items():
   f=F(1)
   for ax in range(3):f*=transforms[ax,ns[ax],ms[ax]]
   acc=plus(acc,times(cv,f))
  out.append(acc)
 return out

def cover_ok(paths):
 assert len(paths)==len(set(paths))
 def visit(ps):
  if ''in ps:assert len(ps)==1;return
  assert ps;axis=ps[0][0];assert axis in'012'and all(len(p)>=2 and len(p)%2==0 and p[0]==axis and p[1]in'01'for p in ps)
  visit([p[2:]for p in ps if p[1]=='0']);visit([p[2:]for p in ps if p[1]=='1'])
 visit(paths)
def prove_cover(expr,d,box,paths,parity=None):
 cover_ok(paths)
 for path in paths:
  b=list(box)
  for i in range(0,len(path),2):
   axis=int(path[i]);side=int(path[i+1]);a,c=b[axis];m=(a+c)/2;b[axis]=(a,m)if not side else(m,c)
  cc=coefficient_tensor(expr,d,b,parity);assert all(sg(t,d)>=0 for t in cc),(path,b)
 return len(paths)
def interval(expr,d,box):
 a=coefficient_tensor(expr,d,box);key=cmp_to_key(lambda u,v:sg(plus(u,times(v,-1)),d));return min(a,key=key),max(a,key=key)
def maxabs(a,b,d):
 a=a if sg(a,d)>=0 else times(a,-1);b=b if sg(b,d)>=0 else times(b,-1)
 return a if sg(plus(a,times(b,-1)),d)>=0 else b

def terms(lit):
 out=[]
 for t in re.findall(r'[+-]?[^+-]+',lit.replace(' ','')):
  a,n,w=re.fullmatch(r'([+-]?)(\d*)([AaBbCc]+)',t).groups();out.append(((-1 if a=='-'else 1)*(int(n)if n else 1),w))
 return out

def matrix(lit,values=None):
 I=S.eye(2);Z=S.diag(1,-1)
 obs={}
 for party,t in zip('ABC',VS if values is None else values):
  obs[party]=Z;obs[party.lower()]=S.Matrix([[t,1],[1-t*t,-t]])if values is None else S.Matrix([[t,S.sqrt(1-t*t)],[S.sqrt(1-t*t),-t]])
 M=S.zeros(8)
 for cv,w in terms(lit):
  loc=[I,I,I]
  for a in w:loc['ABC'.index(a.upper())]=obs[a]
  M+=cv*S.kronecker_product(*loc)
 return M

def exact_identity(k,P,v):
 if k==6:
  f=[a for a,m in S.factor_list(P)[1]if S.degree(a,q)==4][0];f=S.Poly(f,q).monic().as_expr()
  assert S.expand(P-(q+5)*(q-3)**3*f)==0
  assert S.expand(f.subs(q,v)-64*(1-z*z)*(x*y+x+y-1)**2-256*z*z)==0
  assert sg(conv(v-3,2),2)>0 and sg(conv(v+5,2),2)>0
 elif k==9:
  vv=y*y;w=z*z
  rhs=16384*((1-vv)**2*(w*x-w+x+1)**2+4*vv*(1-vv)*((1-w)*(x+1)+w*(x*x+1))+4*vv**2)
  assert S.expand(P.subs(q,v)-rhs)==0
 elif k==13:
  f=S.Poly(S.factor_list(P)[1][0][0],q).monic().as_expr();assert S.expand(P-f*f)==0
  assert [S.simplify(S.diff(f,q,4-i).subs(q,v)/S.factorial(4-i))for i in[1,2,3]]==[16*S.sqrt(2),160,256*S.sqrt(2)]
  assert S.expand(f.subs(q,v)-64*(1-y*y)*(x*z-x-z-1)**2-256*y*y)==0
 else:raise AssertionError(k)

def elementary(k,lit):
 # Free algebra on reflections, commuting only across parties.
 def product(a,b):
  out={}
  for v,c in a.items():
   for w,d in b.items():
    rt=[]
    for aa,bb in zip(v,w):
     acc=list(aa)
     for t in bb:
      if acc and acc[-1]==t:acc.pop()
      else:acc.append(t)
     rt.append(tuple(acc))
    key=tuple(rt);out[key]=S.expand(out.get(key,0)+c*d)
  return {a:b for a,b in out.items()if b!=0}
 def add(*args):
  out={}
  for a in args:
   for v,c in a.items():out[v]=S.expand(out.get(v,0)+c)
  return {a:b for a,b in out.items()if b!=0}
 def scale(a,c):return{v:S.expand(w*c)for v,w in a.items()if w*c!=0}
 I={((),(),()):S.Integer(1)}
 O={a: {tuple((int(a.islower()),)if i=='ABC'.index(a.upper())else()for i in range(3)):S.Integer(1)}for a in'AaBbCc'}
 def word(w):
  a=I
  for t in w:a=product(a,O[t])
  return a
 M=add(*[scale(word(w),cv)for cv,w in terms(lit)])
 if k==1:
  rhs=product(product(add(I,scale(O['A'],-1)),add(I,scale(O['B'],-1))),add(I,scale(O['C'],-1)))
  assert add(I,scale(M,-1))==rhs
 elif k==2:
  assert all(cv in[-1,1]and len(w)==3 for cv,w in terms(lit))and len(terms(lit))==4
  for cv,w in terms(lit):assert product(word(w),word(w))==I
 elif k==3:
  dd=word('BC');ee=word('bc');r1=add(O['A'],scale(add(dd,ee),-1/S.sqrt(2)));r2=add(O['a'],scale(add(dd,scale(ee,-1)),-1/S.sqrt(2)))
  assert add(scale(I,2*S.sqrt(2)),scale(M,-1))==scale(add(product(r1,r1),product(r2,r2)),1/S.sqrt(2))
 elif k==4:
  T=add(word('BC'),word('bC'),word('Bc'),scale(word('bc'),-1));assert M==add(scale(O['A'],2),product(add(I,scale(O['A'],-1)),T))
  r1=add(O['B'],scale(add(O['C'],O['c']),-1/S.sqrt(2)));r2=add(O['b'],scale(add(O['C'],scale(O['c'],-1)),-1/S.sqrt(2)))
  assert add(scale(I,2*S.sqrt(2)),scale(T,-1))==scale(add(product(r1,r1),product(r2,r2)),1/S.sqrt(2))
 else:raise AssertionError(k)

start=time.time();C=json.loads((D/'certificate.json').read_text());result=[];leafcount=0
assert [r['id']for r in C['rows']]==[ENTRY['id']]
for row in C['rows']:
 k=row['id'];d=row['q_field_d'];v=S.sympify(row['quantum_value']);P=S.sympify((D/f'S{k:02d}_charpoly.txt').read_text());M=matrix(row['literal']);DM=DomainMatrix.from_Matrix(M).convert_to(S.ZZ.poly_ring(x,y,z));pc=DM.charpoly();PP=S.expand(sum(DM.domain.to_sympy(a)*q**(8-i)for i,a in enumerate(pc)));assert S.expand(PP-P)==0
 assert S.Poly(P,q).LC()==1 and S.Poly(P,q).degree()==8 and all(S.degree(P,t)<=4 for t in VS)
 vals=[sum(cv*S.prod(a['AaBbCc'.index(c)]for c in w)for cv,w in terms(row['literal']))for a in itertools.product([-1,1],repeat=6)];assert max(vals)==row['local_bound']
 if row['method']=='elementary_operator':
  assert S.simplify(v-{1:S.Integer(1),2:S.Integer(4),3:2*S.sqrt(2),4:4*S.sqrt(2)-2}[k])==0
  elementary(k,row['literal'])
 else:
  expected=set(map(str,range(1,7 if k==13 else 8 if k in[6,7,8,9,15,26]else 9)))
  assert set(row['elementary_coefficients'])==expected
  assert ('identity_determinant'in row)==(k in[6,9,13])
  assert ('interior_determinant'in row)==(k in[7,8,15,26])
  for i,cert in row['elementary_coefficients'].items():
   i=int(i);E=S.expand(S.diff(P,q,8-i).subs(q,v)/S.factorial(8-i))
   if i==8 and k in[11,12,14]:
    unit,fac=S.factor_list(E,extension=True);assert all(m%2==0 for _,m in fac);E=S.expand(unit)
   pa=cert['parity'];box=[(F(0),F(1))if a else(F(-1),F(1))for a in pa]
   leafcount+=prove_cover(E,d,box,cert['leaves'],pa)
  if 'identity_determinant'in row:exact_identity(k,P,v)
  if 'interior_determinant'in row:
   inc=row['interior_determinant'];c=list(map(S.sympify,inc['center']));H=[tuple(map(F,b))for b in inc['H']];E=S.expand(P.subs(q,v));ss=dict(zip(VS,c));assert S.simplify(E.subs(ss))==0 and all(S.simplify(S.diff(E,t).subs(ss))==0 for t in VS)
   for j in range(3):
    assert -1<=H[j][0]<c[j]<H[j][1]<=1
    diag=interval(S.diff(E,VS[j],2),d,H)[0]
    for j2 in range(3):
     if j2!=j:diag=plus(diag,times(maxabs(*interval(S.diff(E,VS[j],VS[j2]),d,H),d),-1))
    assert sg(diag,d)>0
   assert {(b['axis'],b['side'])for b in inc['outer']}==set(itertools.product(range(3),range(2)))
   for cert in inc['outer']:
    a,b=cert['axis'],cert['side'];box=[(F(-1),F(1))]*3
    for j in range(a):box[j]=H[j]
    box[a]=(F(-1),H[a][0])if b==0 else(H[a][1],F(1));assert box==[tuple(map(F,z))for z in cert['box']]
    leafcount+=prove_cover(E,d,box,cert['leaves'])
 overlap=list(map(S.sympify,row['overlaps']));assert all(-1<=t<=1 for t in overlap)
 p1=S.expand(P.subs(dict(zip(VS,overlap))));assert S.simplify(p1.subs(q,v))==0
 multiplicity=next(j for j in range(1,9)if S.simplify(S.diff(p1,q,j).subs(q,v))!=0)
 result.append(dict(id=k,value=str(v),global_upper='PASS',exact_attainment='PASS',local_maximum=int(max(vals)),canonical_overlaps=row['overlaps'],top_eigenvalue_multiplicity=multiplicity))
 print('PASS',k,'elapsed',round(time.time()-start,2),flush=True)
out=dict(status='PASS_EXACT_GLOBAL_UPPER_AND_ATTAINMENT',values=result,bernstein_leaf_count=leafcount,seconds=time.time()-start,certificate_sha256=hashlib.sha256((D/'certificate.json').read_bytes()).hexdigest())
(D/'result.json').write_text(json.dumps(out,indent=2));print(out['status'],leafcount,flush=True)
