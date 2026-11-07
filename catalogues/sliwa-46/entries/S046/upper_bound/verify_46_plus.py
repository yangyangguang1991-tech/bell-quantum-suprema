"""Exact replay of the auxiliary C=c=+I branch upper bound <=12."""
import sympy as S
import json
from pathlib import Path
q,t,x,y,u,v=S.symbols('q t x y u v')
P=q**4+48*q*q*x*y+48*q*q*x+48*q*q*y-296*q*q-576*q*x*y-576*q*x-576*q*y+2304*q-1024*x*x*y*y+1024*x*x+960*x*y+960*x+1024*y*y+960*y-4464
Puv=q**4-296*q*q+2304*q+1024*u*u+(48*q*q-576*q+960)*u-1024*v*v+(48*q*q-576*q-1088)*v-4464
assert S.expand(Puv.subs({u:x+y,v:x*y})-P)==0
ustar=(-3*q*q+36*q-60)/128
vstar=(3*q*q-36*q-68)/128
assert S.simplify(S.diff(Puv,u).subs(u,ustar))==0
assert S.simplify(S.diff(Puv,v).subs(v,vstar))==0
assert S.simplify(1+ustar+vstar)==0
assert S.expand(P.subs(y,1)-(q-10)*(q-2)*(q*q+12*q+96*x-124))==0
assert S.expand(P.subs(y,-1)-(q-10)**2*(q-2)*(q+22))==0
p=q**3+(-4*t+6)*q*q+(64*t*t+48*t-260)*q-256*t**3-384*t*t+176*t+744
assert S.expand(P.subs({x:t,y:t})-(q+4*t-6)*p)==0
g=25*q**3+98*q*q-6068*q+19736
assert S.expand(S.resultant(p,S.diff(p,t),t)+16777216*(q-10)*(q-2)*(q+22)*g)==0
assert g.subs(q,10)<0<g.subs(q,12)
assert S.diff(g,q).subs(q,10)>0
assert S.diff(g,q,2).subs(q,10)>0
data={'scope':'C=c=+I Sliwa-46 branch, full two-party maximization upper bound <=12',
      'logic':'All boundary eigenvalues <=10; an interior eigenvalue maximum q>10 has x=y, and resultant forces g(q)=0; g is increasing on [10,infinity), its unique root >10 lies below 12.',
      'result':'PASS'}
Path(__file__).with_name('verification_46_plus.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print(json.dumps(data,indent=2))
