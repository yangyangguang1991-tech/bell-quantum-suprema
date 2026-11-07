"""Exact algebraic binding and rational interval arithmetic; no numerical optimizer."""
from __future__ import annotations
import json,re
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import sympy as S
from sympy.polys.matrices import DomainMatrix

q,x,y,z=S.symbols('q x y z')
V=(q,x,y,z)
BITS=300
SCALE=1<<BITS

def require(condition,message):
    if not condition:raise ArithmeticError(message)

def load(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def expression(text):return S.sympify(text,locals=dict(zip(['q','x','y','z'],V)))

def rounded(a,b):
    a=F(a);b=F(b)
    return (F((a*SCALE).__floor__(),SCALE),F((b*SCALE).__ceil__(),SCALE))
def add(a,b):return rounded(a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[1],-a[0])
def mul(a,b):
    values=[a[i]*b[j]for i in (0,1)for j in (0,1)]
    return rounded(min(values),max(values))
def power(a,n):
    if n<0:
        require(not a[0]<=0<=a[1],'Interval division through zero')
        return power(rounded(1/a[1],1/a[0]),-n)
    if n==0:return (F(1),F(1))
    if n%2==0:
        lo=0 if a[0]<=0<=a[1] else min(a[0]**n,a[1]**n)
        return rounded(lo,max(a[0]**n,a[1]**n))
    return rounded(a[0]**n,a[1]**n)
def sqrt_interval(a):
    require(a[0]>=0,'Negative square-root interval')
    lo=isqrt((a[0]*SCALE*SCALE).__floor__())
    hi=isqrt((a[1]*SCALE*SCALE).__floor__())
    if F(hi*hi,SCALE*SCALE)<a[1]:hi+=1
    return F(lo,SCALE),F(hi,SCALE)

def interval(expr,env):
    if expr.is_Rational:
        a=F(int(expr.p),int(expr.q));return a,a
    if expr.is_Symbol:return env[expr]
    if expr.is_Add:
        result=(F(0),F(0))
        for a in expr.args:result=add(result,interval(a,env))
        return result
    if expr.is_Mul:
        result=(F(1),F(1))
        for a in expr.args:result=mul(result,interval(a,env))
        return result
    if expr.is_Pow:
        base,exponent=expr.args
        if exponent.is_Integer:return power(interval(base,env),int(exponent))
        if exponent==S.Rational(1,2):return sqrt_interval(interval(base,env))
    raise ValueError(f'Unsupported exact interval expression: {expr}')

def polynomial_value(coeff,t):
    value=F(0)
    for a in coeff:value=value*t+F(a)
    return value

def isolate(polynomial,bounds):
    polynomial=S.Poly(polynomial,q,domain=S.QQ)
    lo,hi=map(F,bounds)
    require(lo<hi,'Reversed root selector')
    require(polynomial.count_roots(S.Rational(lo),S.Rational(hi))==1,'Root selector is not unique')
    coeff=[F(a)for a in polynomial.all_coeffs()]
    fl=polynomial_value(coeff,lo);fh=polynomial_value(coeff,hi)
    require(fl*fh<0,'Selector endpoints must have opposite signs')
    while hi-lo>F(1,1<<260):
        mid=(lo+hi)/2;fm=polynomial_value(coeff,mid)
        if fm==0:return mid,mid
        if fl*fm<0:hi=mid
        else:lo=mid;fl=fm
    return lo,hi

def parameter_data(spec):
    kind=spec['kind']
    if kind=='radicals':
        qq=expression(spec['q']);overlaps=list(map(expression,spec['overlaps']))
        env={q:interval(qq,{})}
        env.update({v:interval(a,{})for v,a in zip((x,y,z),overlaps)})
        return env,dict(zip(V,[qq,*overlaps]))
    if kind=='univariate':
        qr=isolate(expression(spec['polynomial']),spec['interval'])
        env={q:qr}
        env.update({v:interval(expression(a),env)for v,a in zip((x,y,z),spec['overlaps'])})
        return env,None
    require(kind=='system','Unknown strategy parameter definition')
    raw={S.Symbol(n):tuple(map(F,b))for n,b in zip(spec['variables'],spec['box'])}
    env={q:raw[q]}
    env.update({v:interval(expression(a),raw)for v,a in zip((x,y,z),spec['overlaps'])})
    return env,None

def composition_mod(poly,spec):
    modulus=S.Poly(expression(spec['polynomial']),q,domain=S.QQ)
    coordinates=[S.Poly(q,q,domain=S.QQ),*[S.Poly(expression(a),q,domain=S.QQ)for a in spec['overlaps']]]
    parsed=S.Poly(poly,*V,domain=S.QQ)
    powers=[]
    for j,a in enumerate(coordinates):
        arr=[S.Poly(1,q,domain=S.QQ)]
        for _ in range(parsed.degree(V[j])):arr.append((arr[-1]*a).rem(modulus))
        powers.append(arr)
    result=S.Poly(0,q,domain=S.QQ)
    for exponents,c in parsed.terms():
        value=S.Poly(c,q,domain=S.QQ)
        for j,e in enumerate(exponents):value=(value*powers[j][e]).rem(modulus)
        result=(result+value).rem(modulus)
    return result.is_zero

def exact_vanishes(poly,spec,substitution=None):
    if poly==0:return True
    if spec['kind']=='radicals':
        return S.simplify(poly.subs(substitution,simultaneous=True))==0
    if spec['kind']=='univariate':return composition_mod(poly,spec)
    variables=[S.Symbol(a)for a in spec['variables']]
    replace={v:expression(a)for v,a in zip((x,y,z),spec['overlaps'])}
    target=S.Poly(S.expand(poly.subs(replace,simultaneous=True)),*variables,domain=S.QQ)
    # Every selected system includes a characteristic factor as its first equation.
    factor=S.Poly(expression(spec['equations'][0]),*variables,domain=S.QQ)
    return target.rem(factor).is_zero

def characteristic_path(directory):
    directory=Path(directory)
    config=directory/'upper_bound/inputs.json'
    if config.is_file():return directory/'upper_bound'/load(config)['characteristic_file']
    return directory/'characteristic_polynomial.txt'

def verify_binding(directory):
    directory=Path(directory);spec=load(directory/'strategy_spec.json')
    polynomial=expression(characteristic_path(directory).read_text())
    require(S.Poly(polynomial,q).degree()==8,'Characteristic polynomial must have degree 8')
    require(S.Poly(polynomial,q).LC()==1,'Characteristic polynomial must be monic')
    # Independently reconstruct the literal Bell matrix in a polynomial gauge.
    # [[t,1],[1-t^2,-t]] is similar to the physical symmetric reflection for
    # |t|<1. Polynomial identity then extends to the deterministic endpoints.
    Z=S.diag(1,-1);I=S.eye(2)
    observables=dict(zip('AaBbCc',[Z,S.Matrix([[x,1],[1-x*x,-x]]),Z,S.Matrix([[y,1],[1-y*y,-y]]),Z,S.Matrix([[z,1],[1-z*z,-z]])]))
    matrix=S.zeros(8)
    functional=load(directory/'functional.json')
    for token in re.findall(r'[+-]?[^+-]+',functional['expression'].replace(' ','')):
        match=re.fullmatch(r'([+-]?)(\d*)([AaBbCc]+)',token)
        require(match is not None,'Invalid literal Bell expression')
        sign,number,word=match.groups();c=(-1 if sign=='-'else 1)*int(number or '1')
        require(len({a.upper()for a in word})==len(word),'Duplicate party in Bell monomial')
        local=[I,I,I]
        for name in word:local['ABC'.index(name.upper())]=observables[name]
        matrix+=c*S.kronecker_product(*local)
    dm=DomainMatrix.from_Matrix(matrix).convert_to(S.ZZ.poly_ring(x,y,z))
    rebuilt=sum(dm.domain.to_sympy(c)*q**(8-j)for j,c in enumerate(dm.charpoly()))
    require(S.expand(rebuilt-polynomial)==0,'Literal Bell functional and upper/attainment characteristic polynomial disagree')
    env,sub=parameter_data(spec)
    for v in (x,y,z):require(-1<=env[v][0]<=env[v][1]<=1,f'Illegal exact overlap {v}')
    require(exact_vanishes(polynomial,spec,sub),'Selected exact value is not a characteristic zero')
    multiplicity=None
    for k in range(1,9):
        derivative=S.diff(polynomial,q,k)
        bound=interval(derivative,env)
        if bound[0]>0 or bound[1]<0:
            multiplicity=k;break
        require(exact_vanishes(derivative,spec,sub),f'Unresolved exact eigenvalue multiplicity at derivative {k}')
    require(multiplicity is not None,'No nonzero characteristic derivative')
    t=S.Symbol('t')
    pp=S.Poly(polynomial.subs(q,t),t)
    coefficients=[]
    # Synthetic division by (t-q), repeated m times.  Vanishing remainders
    # have just been checked, so this is the exact complementary factor R(t).
    for _ in range(multiplicity):
        out=[pp.all_coeffs()[0]]
        for c in pp.all_coeffs()[1:]:out.append(S.expand(c+q*out[-1]))
        pp=S.Poly.from_list(out[:-1],t)
    coefficients=[str(a)for a in pp.all_coeffs()]
    return dict(status='PASS_EXACT_ATTAINMENT_BINDING',multiplicity=multiplicity,
                complementary_factor_coefficients_descending=coefficients,
                parameter_intervals={str(a):[str(v)for v in b]for a,b in env.items()})
