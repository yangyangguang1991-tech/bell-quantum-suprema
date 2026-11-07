"""Enumerate rational path strategies of bounded height. Successive records tend to q_*."""

if not __debug__:
    raise RuntimeError("Run without -O or -OO: exact verification requires assertions.")
from itertools import product
from fractions import Fraction as F
from argparse import ArgumentParser
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from verify import circle,make
import json

def family(stage):
    grid=sorted({F(i,j) for i in range(stage+1) for j in range(1,stage+1)})
    best=None
    for m in range(1,stage+1):
        for u,v in product((0,None),repeat=2):
            for inner in product([*grid,None],repeat=m-1):
                labels=list(map(circle,[u,*inner,v]))
                # The Jacobi off-diagonals are nonnegative, so nonnegative
                # trial vectors suffice. Integer rays exhaust rational rays.
                for trial in product(range(stage+1),repeat=m):
                    if not any(trial):continue
                    den=sum(x*x for x in trial)
                    sc=F(0)
                    for j,x in enumerate(trial):
                        c,d=labels[j][0],labels[j+1][0]
                        sc+=x*x*(c*d+(c-d)/2-1)
                        if j+1<m:sc+=x*trial[j+1]*labels[j+1][1]
                    sc/=den
                    if best is None or sc>best[0]:best=(sc,labels,trial)
    out=make(best[1],best[2]);assert F(out['score'])==best[0]
    return out
if __name__=='__main__':
    if not __debug__:raise RuntimeError('Run without -O')
    p=ArgumentParser();p.add_argument('stage',type=int);args=p.parse_args()
    if args.stage<1:p.error('stage must be positive')
    print(json.dumps(family(args.stage),indent=2,default=str))
