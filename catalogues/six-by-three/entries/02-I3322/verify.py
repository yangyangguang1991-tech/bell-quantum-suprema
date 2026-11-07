"""Exact path strategies for the projection form of I3322. Python 3, standard library."""

if not __debug__:
    raise RuntimeError("Run without -O or -OO: exact verification requires assertions.")
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"common"))
from algebra import i3322_identity
from census import check_facet

TABLE = [[0,-1,-2,0],[0,1,1,-1],[-1,1,1,1],[0,-1,1,0]]
def zeros(n): return [[F() for _ in range(n)] for _ in range(n)]
def make(labels, trial):
    n=len(trial)
    if n<1 or len(labels)!=n+1 or not any(trial): raise ValueError("Invalid path or vector")
    if any(c*c+s*s!=1 or s<0 for c,s in labels) or labels[0][1] or labels[-1][1]:
        raise ValueError("Invalid half-angle data or endpoints")
    z=[zeros(n),zeros(n)]; x=[zeros(n),zeros(n)]; w=[zeros(n),zeros(n)]
    for j in range(n):
        u,v=labels[j][0],labels[j+1][0]
        z[0][j][j],z[1][j][j]=(u,v) if j%2==0 else (-v,-u)
        for side in (0,1): w[side][j][j]=F(1)
    for j in range(n-1):
        side=1-j%2
        x[side][j][j+1]=x[side][j+1][j]=labels[j+1][1]
        w[1-side][j][j]=w[1-side][j+1][j+1]=F(0)
        w[1-side][j][j+1]=w[1-side][j+1][j]=F(1)
    OP=[]
    for side in (0,1):
        mats=[zeros(n) for _ in range(3)]
        for i in range(n):
            for j in range(n):
                mats[0][i][j]=(F(i==j)+z[side][i][j]-x[side][i][j])/2
                mats[1][i][j]=(F(i==j)+z[side][i][j]+x[side][i][j])/2
                mats[2][i][j]=(F(i==j)+w[side][i][j])/2
        for A in mats:
            assert all(A[i][j]==A[j][i]==sum(A[i][k]*A[k][j] for k in range(n))
                       for i in range(n) for j in range(n))
        OP.append(mats)
    I=[[F(i==j) for j in range(n)] for i in range(n)]
    raw=json.loads(Path(__file__).with_name('definition.json').read_text(encoding='utf-8'))['active_table']
    assert raw==TABLE
    i3322_identity(raw)
    gram=F(sum(t*t for t in trial))
    val=sum(raw[a][b]*sum(trial[i]*trial[j]*A[i][j]*B[i][j] for i in range(n) for j in range(n))/gram
            for a,A in enumerate([I]+OP[0]) for b,B in enumerate([I]+OP[1]))
    v=F()
    for j in range(n):
        u,vv=labels[j][0],labels[j+1][0]
        v+=trial[j]**2*(u*vv+(u-vv)/2-1)
        if j+1<n:v+=trial[j]*trial[j+1]*labels[j+1][1]
    assert v/gram==val
    return dict(dimension=n,state_diagonal=list(map(str,trial)),state_normalization_squared=str(gram),
                alice_projectors=OP[0],bob_projectors=OP[1],score=str(val))
def circle(z):
    if z is None:return F(-1),F(0)
    z=F(z)
    if z<0:raise ValueError('Half-angle parameter must be nonnegative')
    return (1-z*z)/(1+z*z),2*z/(1+z*z)
def check_record(record):
    n=record['dimension']; assert type(n) is int and n>=1
    trial=list(map(F,record['state_diagonal'])); assert len(trial)==n and any(trial)
    norm=sum(x*x for x in trial); assert norm==F(record['state_normalization_squared'])
    OP=[]
    for key in ('alice_projectors','bob_projectors'):
        assert len(record[key])==3
        mats=[[[F(x) for x in row] for row in matrix] for matrix in record[key]]
        for matrix in mats:
            assert len(matrix)==n and all(len(row)==n for row in matrix)
            assert all(matrix[i][j]==matrix[j][i]==sum(matrix[i][k]*matrix[k][j] for k in range(n)) for i in range(n) for j in range(n))
        OP.append(mats)
    identity=[[F(i==j) for j in range(n)] for i in range(n)]
    score=sum(TABLE[a][b]*sum(trial[i]*trial[j]*A[i][j]*B[i][j] for i in range(n) for j in range(n))/norm for a,A in enumerate([identity]+OP[0]) for b,B in enumerate([identity]+OP[1]))
    assert score==F(record['score'])
    return score

if __name__=='__main__':
    if not __debug__: raise RuntimeError("Run without -O")
    definition=json.loads(Path(__file__).with_name('definition.json').read_text(encoding='utf-8'))
    assert definition['active_table']==TABLE and definition['scenario']==[6,3,2,2] and definition['classical_bound']==0
    assert definition['active_settings']==[3,3]
    check_facet(TABLE); i3322_identity(TABLE)
    check_record(json.loads(Path(__file__).with_name('example.json').read_text(encoding='utf-8')))
    p=argparse.ArgumentParser();p.add_argument('--labels',help='CSV rational half-angle parameters; inf denotes the endpoint -1')
    p.add_argument('--vector',help='CSV nonzero rational Schmidt coefficients')
    p.add_argument('--export',type=Path)
    args=p.parse_args()
    if bool(args.labels)!=bool(args.vector):p.error('--labels and --vector must be supplied together')
    if args.labels:
        z=[None if v=='inf' else F(v) for v in args.labels.split(',')]
        v=list(map(F,args.vector.split(','))); result=make(list(map(circle,z)),v)
    else:
        for m in range(1,9):
            for start in [0,None]:
                for end in [0,None]:
                    z=[start]+[F(j+1,m+1) for j in range(m-1)]+[end]
                    result=make(list(map(circle,z)),[F(j+1) for j in range(m)])
        print('PASS: 32 rational paths, projections and original probability scores.')
    if args.export:args.export.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
