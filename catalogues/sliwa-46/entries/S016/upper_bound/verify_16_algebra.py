from pathlib import Path
import sympy as S
import itertools,json
q,r,x,y,z,t,d=S.symbols('q r x y z t d')
base=Path(__file__).parent
P=S.sympify((base/'charpoly_16_full.txt').read_text())
R=S.expand(sum(cv*r**(i[0]//2) for i,cv in S.Poly(P,q).terms()))
assert S.expand(P-R.subs(r,q*q))==0
assert S.expand(R.subs(x,1)-(r-16)**4)==0
assert S.expand(R.subs(y,1)-(r-16)**4)==0
quad=r*r-32*r+256*(y*y+z*z-y*y*z*z)
assert S.expand(R.subs(x,-1)-quad*quad)==0
quad2=r*r-32*r+256*(x*x+z*z-x*x*z*z)
assert S.expand(R.subs(y,-1)-(r-16)**2*quad2)==0
assert S.expand(R-R.xreplace({y:z,z:y}))==0

Rdiag=S.expand(R.subs(z,y))
small=r+8*x*y*y-8*x-8*y*y-8
C,rem=S.div(Rdiag,small,r)
assert rem==0
H=r+8*y*y+16*y-8
aa=-128*(y-1)**3*(y+1)*H
bb=8*(y-1)*(y+1)*(-r*r+16*r*y*y+16*r+256*y**4-768*y*y+256)
assert S.expand(S.Poly(C,x).nth(2)-aa)==0
assert S.expand(S.Poly(C,x).nth(1)-bb)==0
xf=-bb/(2*aa)
E=9*r*r*y-7*r*r+96*r*y**3-32*r*y*y-384*r*y+256*r+256*y**5-1792*y**4+2048*y**3
assert S.cancel(C.subs(x,xf)-(r-16)**2*E/(8*(y-1)*H))==0
f=243*r*r-12256*r+117504
assert S.expand(S.resultant(E,S.diff(E,y),y)-72057594037927936*r*r*(r-16)**5*f)==0
assert S.groebner([E,S.diff(E,y),f],y,r,domain=S.QQ)==S.groebner([27*r+416*y-912,f],y,r,domain=S.QQ)
ystar=(912-27*r)/416
xstar=(2320-81*r)/1664
for expression in [C,S.diff(C,x),S.diff(C,y)]:
    num=S.together(expression.subs({x:xstar,y:ystar})).as_numer_denom()[0]
    assert S.rem(num,f,r)==0
rho=(6128+832*S.sqrt(13))/243
assert S.simplify(xstar.subs(r,rho)-(1-S.sqrt(13))/6)==0
assert S.simplify(ystar.subs(r,rho)-(5-2*S.sqrt(13))/9)==0
assert 32<rho<64
assert -1<xstar.subs(r,rho)<0
assert -1<ystar.subs(r,rho)<0

ss,rr,mm=S.symmetrize(R,[y,z],formal=True)
assert rr==0
TD=S.expand(ss.subs({mm[0][0]:2*t,mm[1][0]:t*t-d/4}))
rd=S.sympify((base/'charpoly_16_derivative.txt').read_text())
assert S.expand(S.diff(TD,d)-(1-x)*rd)==0
assert S.expand(TD.subs(d,0)-Rdiag.subs(y,t))==0


print('PASS S16 boundary, stationary and asymmetry identities')
