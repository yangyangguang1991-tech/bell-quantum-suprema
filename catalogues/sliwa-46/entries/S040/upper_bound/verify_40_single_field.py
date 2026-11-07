"""Exact identification of the certified S40 value as an eleventh-degree root."""
if not __debug__:
    raise RuntimeError('Run S40 field checks without Python -O: assertions must remain enabled.')
from pathlib import Path
from fractions import Fraction as F
import sympy as S,json
OUT=Path(__file__).parent
q,x,y,z=S.symbols('q x y z')
definition=json.loads((OUT/'S40_single_field_definition.json').read_text())
selected=json.loads((OUT/'S40_selected_root.json').read_text())
P=S.sympify((OUT/'S40_charpoly.txt').read_text())
h=S.sympify(definition['q_polynomial']);xf=S.sympify(definition['x']);yf=S.sympify(definition['y'])
HP=S.Poly(h,q)
assert HP.is_irreducible
assert HP.count_roots(8,9)==1
index=int(HP.count_roots(-S.oo,8))
K=S.QQ.alg_field_from_poly(HP,alias='rho',root_index=index)
qq=K([1,0])
def coeff(v):return K.from_sympy(v)
def from_q(poly):
    answer=K.zero
    for cv in S.Poly(poly,q).all_coeffs():answer=answer*qq+coeff(cv)
    return answer
xx=from_q(xf);yy=from_q(yf)
def evaluate(poly):
    answer=K.zero
    for (a,b,c),cv in S.Poly(poly,q,x,y).terms():answer+=coeff(cv)*qq**a*xx**b*yy**c
    return answer
assert from_q(h)==K.zero
for poly in [P,S.diff(P,x),S.diff(P,y),S.diff(P,z)]:assert evaluate(poly.subs(z,0))==K.zero

# Tight rational isolation based on an approximate center is accepted
# only after exact Sturm counting and exact interval arithmetic.
center=F(selected['centers'][0]);radius=F(1,10**100)
ql,qh=center-radius,center+radius
sr=lambda v:S.Rational(v.numerator,v.denominator)
assert HP.count_roots(sr(ql),sr(qh))==1
assert F(selected['box'][0][0])<ql<qh<F(selected['box'][0][1])
def interval_polynomial(poly):
    lo=hi=F(0)
    for cv in S.Poly(poly,q).all_coeffs():
        cv=F(cv);p=[lo*ql,lo*qh,hi*ql,hi*qh]
        lo=min(p)+cv;hi=max(p)+cv
    return lo,hi
xbox=interval_polynomial(xf);ybox=interval_polynomial(yf)
for i,box in enumerate([xbox,ybox],start=1):
    l,h=map(F,selected['box'][i]);assert l<box[0]<=box[1]<h
report={'status':'PASS_EXACT_ELEVENTH_DEGREE_VALUE_IDENTIFICATION',
        'q_polynomial':definition['q_polynomial'],'q_degree':11,'irreducible':True,
        'q_root_selector':'unique real root in (8,9)',
        'tight_q_interval':[str(ql),str(qh)],
        'x_y_contact_exact_in_Qq':True,'full_contact_P_Px_Py_Pz':True,
        'x_y_interval_contained_in_selected_root_box':True,
        'reason':'The eleventh-degree selected q root and exact x(q),y(q),z=0 solve all three selected-root equations inside its unique Krawczyk box. Therefore it is precisely the already globally certified value.'}
(OUT/'S40_single_field_verified.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:report[k]for k in ['status','q_degree','irreducible','q_root_selector','full_contact_P_Px_Py_Pz']},indent=2),flush=True)
