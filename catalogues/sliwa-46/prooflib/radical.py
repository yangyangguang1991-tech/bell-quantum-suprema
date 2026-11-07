"""Exact single-entry radical-value upper verification."""
if not __debug__: raise RuntimeError('Assertions must remain enabled')
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from math import comb
import sympy as S,json,time
import re,sys
W=Path(sys.argv[1]).resolve()
ENTRY=json.loads((W.parent/'functional.json').read_text())
TABLE={ENTRY['id']:ENTRY['expression']}
def terms(k):
    output=[]
    for token in re.findall(r'[+-]?[^+-]+',TABLE[k].replace(' ','')):
        sign,num,word=re.fullmatch(r'([+-]?)(\d*)([AaBbCc]+)',token).groups()
        output.append(((-1 if sign=='-'else 1)*int(num or '1'),word))
    return output
q,x,y,z=S.symbols('q x y z');start=time.monotonic()

def characteristic(k):
    # Universal local word reduction followed by trace(AB)^n=2T_n(cosine).
    names='AaBbCc';bell={}
    for cv,wd in terms(k):
        word=tuple(tuple(names.index(c)%2 for c in wd if names.index(c)//2==i)for i in range(3))
        bell[word]=bell.get(word,0)+cv
    def mul(a,b):
        out=[]
        for va,vb in zip(a,b):
            stack=list(va)
            for c in vb:
                if stack and stack[-1]==c:stack.pop()
                else:stack.append(c)
            out.append(tuple(stack))
        return tuple(out)
    power={((),(),()):1};tr={};cs=[S.Integer(1)]
    for j in range(1,9):
        nxt=defaultdict(int)
        for a,cv in power.items():
            for b,dv in bell.items():nxt[mul(a,b)]+=cv*dv
        power={a:b for a,b in nxt.items()if b};agg=defaultdict(int)
        for a,cv in power.items():
            if any(len(t)%2 for t in a):continue
            agg[tuple(len(t)//2 for t in a)]+=8*cv
        tr[j]=S.expand(sum(cv*S.prod(S.chebyshevt(m,v)for m,v in zip(a,[x,y,z]))for a,cv in agg.items()))
        cs.append(S.expand(-sum(cs[j-i]*tr[i]for i in range(1,j+1))/j))
    return S.expand(sum(cs[j]*q**(8-j)for j in range(9)))

def ranges(ep,vs,box,ql,qh):
    ts=S.symbols('u0:'+str(len(vs)))
    pp=S.Poly(S.expand(ep.subs({v:S.Rational(lo)+S.Rational(hi-lo)*u for v,u,(lo,hi)in zip(vs,ts,box)})),*ts,q)
    ds=list(pp.degree_list());dq=ds.pop();low={};high={}
    for ix in product(*[range(d+1)for d in ds]):
        cs=[F(0)]*(dq+1)
        for powers,cv in pp.terms():
            ms=powers[:-1]
            if any(a>b for a,b in zip(ms,ix)):continue
            r=F(int(cv.p),int(cv.q))
            for a,b,d in zip(ms,ix,ds):r*=F(comb(b,a),comb(d,a))
            cs[powers[-1]]+=r
        a=b=F(0)
        for cv in reversed(cs):
            prods=[a*ql,a*qh,b*ql,b*qh];a,b=min(prods)+cv,max(prods)+cv
        low[ix]=a;high[ix]=b
    return low,high,ds

def halve(t,ds,axis):
    l={};r={};others=[i for i in range(len(ds))if i!=axis]
    for ix in product(*[range(ds[i]+1)for i in others]):
        def key(k):
            out=[0]*len(ds);out[axis]=k
            for i,j in zip(others,ix):out[i]=j
            return tuple(out)
        line=[t[key(k)]for k in range(ds[axis]+1)];left=[line[0]];right=[line[-1]]
        while len(line)>1:
            line=[(line[j]+line[j+1])/2 for j in range(len(line)-1)];left.append(line[0]);right.append(line[-1])
        for j in range(ds[axis]+1):l[key(j)]=left[j];r[key(j)]=right[-1-j]
    return l,r

def cover(ep,vs,box,ql,qh,record):
    assert isinstance(record['leaves'],list) and record['leaves'],'Nonempty leaf cover required'
    t,_,ds=ranges(ep,vs,box,ql,qh);assert ds==record['degrees']
    leaves={v['path']:F(v['lower'])for v in record['leaves']};assert len(leaves)==len(record['leaves']);visited=set()
    def visit(path,tensor):
        if path in leaves:
            assert not any(p!=path and p.startswith(path)for p in leaves)
            assert min(tensor.values())==leaves[path]>0;visited.add(path);return
        tails=[p[len(path):]for p in leaves if p.startswith(path)];assert tails and all(len(p)>=2 for p in tails)
        axes={p[0]for p in tails};assert len(axes)==1;axis=int(next(iter(axes)));assert 0<=axis<len(vs)
        a,b=halve(tensor,ds,axis);visit(path+str(axis)+'0',a);visit(path+str(axis)+'1',b)
    visit('',t);assert visited==set(leaves)
    return len(leaves)

outputs=[]
for k in [ENTRY['id']]:
    C=json.loads((W/f'S{k}_full_certificate.json').read_text());P=S.sympify((W/f'S{k}_charpoly.txt').read_text())
    classical=[sum(cv*S.prod(a['AaBbCc'.index(t)]for t in wd)for cv,wd in terms(k))for a in product([-1,1],repeat=6)]
    assert max(classical)=={5:3,18:4,23:4}[k]
    assert S.expand(characteristic(k)-P)==0
    sl,sh=map(F,C['sqrt_interval']);rad=C['sqrt_radicand'];assert 0<sl<sh and sl*sl<rad<sh*sh
    ql,qh=map(F,C['q_interval']);v=S.sympify(C['q_exact']);pt=list(map(S.sympify,C['cosines']))
    assert all(-1<=a<=1 for a in pt);sub=dict(zip([q,x,y,z],[v,*pt]));assert S.simplify(P.subs(sub))==0
    if k==5:assert v==8*S.sqrt(5)-13 and [ql,qh]==[8*sl-13,8*sh-13]
    if k==18:assert v==14-2*S.sqrt(17) and [ql,qh]==[14-2*sh,14-2*sl]
    if k==23:assert v==S.Rational(3,2)*(S.sqrt(17)-1)and [ql,qh]==[F(3,2)*(sl-1),F(3,2)*(sh-1)]
    n=0
    if k in [5,18]:
        assert all(S.simplify(S.diff(P,t).subs(sub))==0 for t in [x,y,z])
        center=[tuple(map(F,t))for t in C['central_box']]
        assert all(S.Rational(a)<t<S.Rational(b)for t,(a,b)in zip(pt,center))
        H=S.hessian(P,[x,y,z]);hr=[]
        for i in range(3):
            row=[]
            for j in range(3):
                lo,hi,_=ranges(H[i,j],[x,y,z],center,ql,qh);pair=(min(lo.values()),max(hi.values()))
                assert pair==tuple(map(F,C['hessian_ranges'][i][j]));row.append(pair)
            hr.append(row)
        for i in range(3):assert hr[i][i][0]>sum(max(abs(a),abs(b))for j,(a,b)in enumerate(hr[i])if i!=j)
        boxes=[]
        for axis in range(3):
            for interval in [(F(-1),center[axis][0]),(center[axis][1],F(1))]:
                box=[center[j]if j<axis else(F(-1),F(1))for j in range(3)];box[axis]=interval;boxes.append(box)
        assert len(C['outer_boxes'])==6
        for rec,box in zip(C['outer_boxes'],boxes):
            assert [tuple(map(F,t))for t in rec['box']]==box;n+=cover(P,[x,y,z],box,ql,qh,rec)
        assert [a['k']for a in C['elementary_coefficients']]==list(range(1,8))
        for rec in C['elementary_coefficients']:n+=cover(S.diff(P,q,8-rec['k'])/S.factorial(8-rec['k']),[x,y,z],[(F(-1),F(1))]*3,ql,qh,rec)
        assert S.simplify(S.diff(P,q).subs(sub))>0
    else:
        H=S.sympify((W/'S23_monic_quartic.txt').read_text());assert S.expand(P-H**2)==0 and S.Poly(H,q).LC()==1
        G=S.expand(H.subs(q,v));G0=G.subs(z,0);G1=G.subs(z,1);assert S.expand(G-(1-z*z)*G0-z*z*G1)==0
        s,d=S.symbols('s d');s0=(5-S.sqrt(17))/4
        positive=48*(s-s0)**2*(s+(3+S.sqrt(17))/4)*((3*S.sqrt(17)-7)/4-s)+d*d*(96*s*s+48*(1-d*d)+84*S.sqrt(17)-324)
        assert S.expand(G1.subs({x:s+d,y:s-d})-positive)==0
        assert 84*sl-324>0 and (3+sl)/4-1>0 and (3*sl-7)/4-1>0
        names=[rec['name']for rec in C['certificates']]
        assert len(names)==4 and set(names)=={'z0_constant','e1','e2','e3'},'All four S23 obligations must occur exactly once'
        for rec in C['certificates']:
            if rec['name']=='z0_constant':ep=H.subs(z,0);vs=[x,y]
            else:
                j=int(rec['name'][1:]);assert j in [1,2,3];ep=S.diff(H,q,4-j)/S.factorial(4-j);vs=[x,y,z]
            n+=cover(ep,vs,[(F(-1),F(1))]*len(vs),ql,qh,rec)
        assert S.simplify(H.subs(sub))==0 and S.simplify(S.diff(H,q).subs(sub))>0
    outputs.append({'sliwa':k,'status':'PASS_LITERAL_TRACE_CHARACTERISTIC_GLOBAL_PSD_EXACT_ATTAINMENT','leaves':n,'value':str(v),'cosines':list(map(str,pt))})
    print('PASS INDEPENDENT',k,'leaves',n,'seconds',time.monotonic()-start,flush=True)
(W/'result.json').write_text(json.dumps({'status':'PASS_EXACT_GLOBAL_UPPER_AND_ATTAINMENT','checks':outputs,'seconds':time.monotonic()-start},indent=2),encoding='utf-8')
