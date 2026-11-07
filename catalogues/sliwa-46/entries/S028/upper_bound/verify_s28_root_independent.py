"""Independent exact Krawczyk localization of the S28 algebraic contact triple.

Uses direct signed monomial power ranges and tuple intervals, rather than
the generator's interval-arithmetic power implementation. No nsolve is called.
"""
from pathlib import Path
from fractions import Fraction as Q
import sympy as s
import json,hashlib,time
if not __debug__:raise RuntimeError('Run without -O or -OO.')
ROOT=Path(__file__).resolve().parent;start=time.time();q,x,y,z=s.symbols('q x y z');vs=(q,x,y)
src=ROOT/'S28_selected_root_certificate.json';C=json.loads(src.read_text());P=s.sympify((ROOT/'S28_charpoly.txt').read_text());F=s.sympify(C['equations'][0]);eq=[F,s.diff(F,x),s.diff(F,y)]
if C['equations']!=list(map(str,eq)):raise ArithmeticError('Gradient polynomial equations changed')
quotient,remainder=s.div(P.subs(z,y),F,q)
if remainder!=0 or s.degree(F,q)!=6 or s.degree(F,x)!=3:raise ArithmeticError('Physical characteristic factor is not the defined sextic')
centers=list(map(Q,C['center_rationals']));radius=Q(C['radius']);box=[tuple(map(Q,a)) for a in C['root_box']]
if box!=[(a-radius,a+radius) for a in centers]:raise ArithmeticError('Root box is not centered as declared')
R=[list(map(Q,row)) for row in C['exact_rational_Jacobian_preconditioner']];J=s.Matrix(eq).jacobian(vs)
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[1],-a[0])
def mul(a,b):
    vals=[u*v for u in a for v in b];return min(vals),max(vals)
def power(a,k):
    if k==0:return Q(1),Q(1)
    vals=[a[0]**k,a[1]**k]
    if a[0]<=0<=a[1]:vals.append(Q(0))
    return min(vals),max(vals)
def bound(E,X):
    out=(Q(0),Q(0))
    for exps,c in s.Poly(E,*vs).terms():
        term=(Q(c),Q(c))
        for a,k in zip(X,exps):term=mul(term,power(a,k))
        out=add(out,term)
    return out
point=[(a,a) for a in centers];f0=[bound(E,point)[0] for E in eq];j0=[[bound(J[i,j],point)[0] for j in range(3)] for i in range(3)]
if any(sum(R[i][k]*j0[k][j] for k in range(3))!=Q(i==j) for i in range(3) for j in range(3)):raise ArithmeticError('Center inverse fails exact rational product')
jbox=[[bound(J[i,j],box) for j in range(3)] for i in range(3)];error=[]
for i in range(3):
    row=[]
    for j in range(3):
        accum=(Q(0),Q(0))
        for k in range(3):accum=add(accum,mul((R[i][k],R[i][k]),jbox[k][j]))
        row.append(add((Q(i==j),Q(i==j)),neg(accum)))
    error.append(row)
norm=max(sum(max(abs(a),abs(b)) for a,b in row) for row in error)
K=[]
for i in range(3):
    center=centers[i]-sum(R[i][j]*f0[j] for j in range(3));image=(center,center)
    for j in range(3):image=add(image,mul(error[i][j],(-radius,radius)))
    K.append(image)
if norm>=1 or not all(box[i][0]<K[i][0]<=K[i][1]<box[i][1] for i in range(3)):raise ArithmeticError('Independent strict Krawczyk contraction/inclusion fails')
out={'status':'PASS_EXACT_INDEPENDENT_UNIQUE_CONTACT_TRIPLE','Sliwa_id':28,'root_certificate_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
     'root_box':C['root_box'],'equations':C['equations'],'independent_Krawczyk_image':[[str(a),str(b)] for a,b in K],
     'independent_contraction_infinity_upper':str(norm),'defining_value':'q-coordinate of the unique real zero in the box',
     'scalar_minimal_polynomial_claimed':False,'seconds':time.time()-start}
(ROOT/'S28_root_independent_replay.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS independent unique S28 root; contraction',float(norm),'seconds',time.time()-start,flush=True)
