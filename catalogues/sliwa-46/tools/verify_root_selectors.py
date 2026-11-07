"""Verify the compact rational root selectors used in the manuscript."""
from __future__ import annotations
from fractions import Fraction as Q
from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'third_party/vendor'),str(ROOT)]
sys.dont_write_bytecode=True
import sympy as S

def require(ok,message):
    if not ok:raise ArithmeticError(message)

def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def mul(a,b):
    values=[u*v for u in a for v in b]
    return min(values),max(values)
def power(a,k):
    if not k:return Q(1),Q(1)
    lo,hi=a[0]**k,a[1]**k
    if k%2==0:return (Q(0)if a[0]<=0<=a[1]else min(lo,hi)),max(lo,hi)
    return lo,hi

def terms(poly,variables):return [(m,Q(c))for m,c in S.Poly(poly,*variables).terms()]
def bound(data,box):
    degrees=[max((m[j]for m,c in data),default=0)for j in range(len(box))]
    powers=[[power(a,k)for k in range(d+1)]for a,d in zip(box,degrees)]
    out=Q(0),Q(0)
    for m,c in data:
        term=c,c
        for j,k in enumerate(m):term=mul(term,powers[j][k])
        out=add(out,term)
    return out

def system(i,spec):
    variables=list(map(S.Symbol,spec['variables']))
    eq=list(map(S.sympify,spec['equations']))
    directory=ROOT/'entries'/f'S{i:03d}'
    config=json.loads((directory/'upper_bound/inputs.json').read_text(encoding='utf-8'))
    P=S.sympify((directory/'upper_bound'/config['characteristic_file']).read_text(encoding='utf-8'))
    q,x,y,z=S.symbols('q x y z')
    if i==28:
        quotient,remainder=S.div(P.subs(z,y),eq[0],q)
        require(remainder==0 and S.degree(eq[0],q)==6,'Incorrect S28 characteristic factor')
        require(all(S.expand(a-b)==0 for a,b in zip(eq[1:],[S.diff(eq[0],x),S.diff(eq[0],y)])),'Incorrect reduced gradient')
        definition='S28 sextic characteristic factor and its x,y derivatives'
    else:
        require(variables==[q,x,y,z],'Unexpected contact coordinates')
        require(all(S.expand(a-b)==0 for a,b in zip(eq,[P,*[S.diff(P,t)for t in(x,y,z)]])),'Incorrect full contact system')
        quotient=None;definition='P, P_x, P_y, P_z'
    return variables,eq,definition,quotient

def contraction(eq,variables,centers,radius,preconditioner=None):
    n=len(variables);point=[(a,a)for a in centers];box=[(a-radius,a+radius)for a in centers]
    J=S.Matrix(eq).jacobian(variables)
    jdata=[[terms(J[i,j],variables)for j in range(n)]for i in range(n)]
    jp=[[bound(jdata[i][j],point)[0]for j in range(n)]for i in range(n)]
    if preconditioner is None:
        inverse=S.Matrix([[S.Rational(a)for a in row]for row in jp]).inv()
        C=[[Q(inverse[i,j])for j in range(n)]for i in range(n)]
    else:C=preconditioner
    require(all(sum(C[i][k]*jp[k][j]for k in range(n))==Q(i==j)for i in range(n)for j in range(n)),'Incorrect rational inverse')
    ji=[[bound(jdata[i][j],box)for j in range(n)]for i in range(n)]
    error=[]
    for i in range(n):
        row=[]
        for j in range(n):
            acc=Q(0),Q(0)
            for k in range(n):acc=add(acc,mul((C[i][k],C[i][k]),ji[k][j]))
            row.append(add((Q(i==j),Q(i==j)),neg(acc)))
        error.append(row)
    norm=max(sum(max(abs(a),abs(b))for a,b in row)for row in error)
    f=[bound(terms(a,variables),point)[0]for a in eq]
    image=[]
    for i in range(n):
        c=centers[i]-sum(C[i][j]*f[j]for j in range(n));v=c,c
        for j in range(n):v=add(v,mul(error[i][j],(-radius,radius)))
        image.append(v)
    require(norm<1,'No strict contraction')
    require(all(box[i][0]<a<=b<box[i][1]for i,(a,b)in enumerate(image)),'No strict root inclusion')
    return C,norm,image

def check_record(r):
    i=r['id'];spec=json.loads((ROOT/'entries'/f'S{i:03d}'/'strategy_spec.json').read_text(encoding='utf-8'))
    require(r['kind']==spec['kind'],'Selector kind mismatch')
    if r['kind']=='univariate':
        require(r['polynomial']==spec['polynomial'],'Defining polynomial mismatch')
        p=S.Poly(S.sympify(r['polynomial']),S.Symbol('q'),domain=S.QQ)
        lo,hi=map(Q,r['interval']);a,b=map(Q,spec['interval'])
        require(p.eval(S.Rational(lo))!=0 and p.eval(S.Rational(hi))!=0,'A displayed interval endpoint is a root')
        require(lo<hi and p.count_roots(S.Rational(lo),S.Rational(hi))==1,'Nonunique displayed interval')
        require(p.count_roots(S.Rational(a),S.Rational(b))==1,'Nonunique original interval')
        require((a<=lo<hi<=b)or(lo<=a<b<=hi),'Root selectors are not nested')
        return {'id':i,'status':'PASS_UNIQUE_SAME_ALGEBRAIC_ROOT'}
    variables,eq,definition,quotient=system(i,spec)
    require(r['variables']==spec['variables'],'Variable order mismatch')
    centers=list(map(Q,r['centers']));radius=Q(r['radius'])
    require(len(centers)==len(variables),'Wrong selecting box dimension')
    require(radius>0,'Nonpositive radius')
    old=[tuple(map(Q,a))for a in spec['box']]
    require(all(c-radius<=a<b<=c+radius for c,(a,b)in zip(centers,old)),'Original certified root box is not contained')
    C,norm,image=contraction(eq,variables,centers,radius,[[Q(a)for a in row]for row in r['preconditioner']])
    require(r['equation_definition']==definition,'Equation definition mismatch')
    if quotient is not None:require(S.expand(S.sympify(r['complementary_factor'])-quotient)==0,'S28 quotient mismatch')
    return {'id':i,'status':'PASS_COMPACT_EXACT_CONTRACTION_AND_SAME_ROOT','contraction_upper_display':float(norm)}

def main():
    data=json.loads((ROOT/'data/compact_root_selectors.json').read_text(encoding='utf-8'))
    required=[i for i in range(1,47)if json.loads((ROOT/'entries'/f'S{i:03d}'/'strategy_spec.json').read_text())['kind']!='radicals']
    require([r['id']for r in data['records']]==required,'Incomplete compact selector catalogue')
    results=[]
    for record in data['records']:
        result=check_record(record);results.append(result)
        print(f"S{record['id']:03d}: compact exact selector PASS",flush=True)
    print(json.dumps({'status':'PASS_ALL_18_COMPACT_ROOT_SELECTORS','entries':18,'checks':results},indent=2))

if __name__=='__main__':main()
