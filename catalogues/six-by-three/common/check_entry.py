"""Exact unrestricted certificate and independent literal-score replay."""

if not __debug__:
    raise RuntimeError("Run without -O or -OO: exact verification requires assertions.")
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from itertools import product
import json
from quadratic import Quad,red
from positive import positive_pivots
from matrices import R,sqrtq,check_witness
from census import check_facet,relabel
from algebra import chsh_identity, spectral_identities

def reflection_coeffs(C):
    H=defaultdict(F)
    for i,row in enumerate(C):
        for j,x in enumerate(row):
            for a in ([(),(i-1,)] if i else [()]):
                for b in ([(),(j-1,)] if j else [()]):
                    H[a,b]+=F(x,2**(bool(i)+bool(j)))
    return {k:v for k,v in H.items() if v}
def sos(C,record,q,d):
    K=record['basis'];n=len(K)
    assert all(len(t)==2 and all(type(k) is int and 0<=k<6 for k in t[0]) and all(type(k) is int and 0<=k<3 for k in t[1]) for t in K)
    assert d in (2,3)
    Y=[[Quad(*x,d) for x in row] for row in record['Y']]
    assert Y==list(map(list,zip(*Y))) and len(set((tuple(a),tuple(b)) for a,b in K))==n
    positive_pivots(Y)
    if d==2:
        assert record['bound']=='sqrt(2)-1' and q==Quad(-1,1,2)
    else:
        assert q==Quad(*record['bound'],d)
    if d==2:N=[[Quad(*x,d) for x in row] for row in record['N']]
    else:
        assert len(record['scaling_sqrt_d_powers'])==n and all(type(s) is int and s in (0,1) for s in record['scaling_sqrt_d_powers'])
        N=[[Quad(x,0,d)*(Quad(0,1,d) if s else 1) for x in r] for r,s in zip(record['N'],record['scaling_sqrt_d_powers'],strict=True)]
    assert len(N)==n and all(len(r)==len(Y) for r in N)
    nz=[[(j,v) for j,v in enumerate(r) if v] for r in N]
    T=[[sum((x*Y[j][k] for j,x in r),Quad(0,0,d)) for k in range(len(Y))] for r in nz]
    terms=defaultdict(lambda:Quad(0,0,d))
    for i,(a,b) in enumerate(K):
        for j,(c,e) in enumerate(K):
            v=sum((x*T[i][k] for k,x in nz[j]),Quad(0,0,d))
            terms[red(list(reversed(a))+c),red(list(reversed(b))+e)]+=v
    for w,v in reflection_coeffs(C).items():terms[w]+=v
    assert terms.pop(((),()))==q and not any(terms.values())
    return f'{n} words; {len(Y)} strictly positive pivots; all oriented coefficients'
def check_squares(linear,weights):
    for j in range(3):
        for k in range(3):
            if j!=k:assert sum(a*v[j]*v[k] for a,v in zip(weights,linear))==0
    assert sum(a*sum(x*x for x in v) for a,v in zip(weights,linear))==9
def spectral(C,which):
    spectral_identities(C,which)
    if which==5:
        coeff=[[-6,0,0,0],[0,1,-1,0],[1,1,1,-1],[1,-1,-1,1],[0,-1,-1,-2]]
        check_squares([[1,1,-1],[1,1,2],[1,-1,0]],[1,F(1,2),F(3,2)])
        assert 1<F(27,5)<9 and (4+F(8,3))*9==60 and 4*24<16**2
    else:
        coeff=[[-6,0,0,0],[-1,1,-1,1],[0,0,1,1],[0,1,1,0],[0,1,0,-1],[-1,-1,1,-1]]
        check_squares([[1,-1,1],[0,1,1],[1,1,0],[1,0,-1]],[1,1,1,1])
        assert 1<F(36,7)<9 and (4+3)*9==63 and 144*3<32**2
    coeffs={((i-1,) if i else (), (j-1,) if j else ()):F(x,4) for i,r in enumerate(coeff) for j,x in enumerate(r) if x}
    assert reflection_coeffs(C)==coeffs
    return 'spectral identity, scalar maximum and branch comparison'
def classical(C):
    scores=[]
    for a in product((0,1),repeat=6):
        for b in product((0,1),repeat=3):
            x=(1,)+a;y=(1,)+b
            scores.append(sum(c*x[i]*y[j] for i,r in enumerate(C) for j,c in enumerate(r)))
    assert max(scores)==0
def run(entry):
    if not __debug__:raise RuntimeError('Use Python without -O')
    data=json.loads((entry/'definition.json').read_text(encoding='utf-8'));C=data['active_table'];which=int(entry.name[:2])
    assert data['scenario']==[6,3,2,2] and data['classical_bound']==0
    assert 2<=len(C)<=7 and 2<=len(C[0])<=4 and all(len(row)==len(C[0]) and all(type(x) is int for x in row) for row in C)
    assert data['active_settings']==[len(C)-1,len(C[0])-1]
    count=check_facet(C)
    if 'brunner_gisin_table' in data:
        relabel(data['brunner_gisin_table'],C)
    if which==6:
        assert all(any(row[1:]) for row in C[1:]) and all(any(row[j] for row in C[1:]) for j in (1,2,3))
    qa,qb,d=data['exact_quadratic'];q=Quad(qa,qb,d);target=R(F(qa))+sqrtq(d)*F(qb)
    analytic_upper={0:('0','0',2),1:('-1/2','1/2',2),3:('-1','1',2),
                    4:('-1','3/4',3),5:('-3/2','1/2',15),6:('-3/2','3/4',7)}
    upper_a,upper_b,upper_d=analytic_upper[which]
    assert (q.a,q.b,q.d)==(F(upper_a),F(upper_b),upper_d), 'The displayed value must equal the proved analytic upper bound'
    if which in (3,4):
        status=sos(C,json.loads((entry/'gram.json').read_text(encoding='utf-8')),q,d)
    elif which in (5,6):
        status=spectral(C,which)
    elif which==1:
        assert reflection_coeffs(C)=={((),()):F(-1,2),((0,),(0,)):F(1,4),((0,),(1,)):F(-1,4),((1,),(0,)):F(-1,4),((1,),(1,)):F(-1,4)}
        chsh_identity(C)
        status='full oriented CHSH square identity and literal reflection form'
    else:
        assert C==[[0,0],[0,-1]]
        status='negative joint probability'
    check_witness(C,json.loads((entry/'strategy.json').read_text(encoding='utf-8')),target)
    print('PASS',data['label'],status,';',count,'saturating deterministic vertices; normalized state, nine reflections and direct CH score')
