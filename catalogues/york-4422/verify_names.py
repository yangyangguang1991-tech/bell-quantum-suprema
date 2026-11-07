#!/usr/bin/env python3
"""Independent polynomial evaluation of the supplied exact direct relabelings."""
import json,itertools,math,csv,hashlib,sys,collections
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]

def symbolic_assignments(act):
    a=[None]*4;b=[None]*4
    for i in range(4):a[act['a_perm'][i]]=('a',i,act['a_sign'][i])
    for j in range(4):b[act['b_perm'][j]]=('b',j,act['b_sign'][j])
    return (b,a) if act['exchange'] else (a,b)

def direct_map(ya,oa):
    y=symbolic_assignments(ya);o=symbolic_assignments(oa)
    reverse={}
    for side in range(2):
        for j,(c,i,s) in enumerate(y[side]):reverse[(c,i)]=(side,j,s)
    return [[dict(side='A' if reverse[(c,i)][0]==0 else 'B',index=reverse[(c,i)][1]+1,
                  sign=s*reverse[(c,i)][2]) for c,i,s in oo] for oo in o]

def expr(row):return ('-' if row['sign']<0 else '')+row['side']+str(row['index'])

def verify_row(row):
    x=row['CH25'];o=row['OBSS25'];da=row['source_A_as_Y'];db=row['source_B_as_Y']
    if sorted((d['side'],d['index']) for d in da+db)!=[(s,i) for s in ['A','B'] for i in range(1,5)]:
        raise ValueError('Not a variable bijection')
    for ab in itertools.product((-1,1),repeat=8):
        a=ab[:4];b=ab[4:];effects=[(1+t)//2 for t in ab]
        # direct CH evaluation, no reflection coefficient conversion
        lhs=x[0]+sum(x[j+1]*effects[4+j] for j in range(4))
        for i in range(4):
            lhs+=x[5+5*i]*effects[i]
            for j in range(4):lhs+=x[6+5*i+j]*effects[i]*effects[4+j]
        vals={'A':a,'B':b}
        aa=[d['sign']*vals[d['side']][d['index']-1] for d in da]
        bb=[d['sign']*vals[d['side']][d['index']-1] for d in db]
        rhs=o[0]+sum(o[i+1]*aa[i] for i in range(4))
        for j in range(4):
            rhs+=o[5+5*j]*bb[j]
            for i in range(4):rhs+=o[6+5*j+i]*aa[i]*bb[j]
        if Fraction(lhs)!=-Fraction(row['q_york_equals_minus_B_times'])*rhs:
            raise ValueError('Polynomial identity failed')
    return 256


if __name__=='__main__':
    if not __debug__:raise RuntimeError("Coefficient comparison requires ordinary Python assertion settings.")
    for k in range(1,176):
        r=json.loads((Path(__file__).parent/'entries'/f'Y{k:03}'/'definition.json').read_text(encoding='utf8'))
        cross=r['coefficient_crosswalk']
        assert k==cross['york_id']==r['york_number'] and r['traditional_name']==cross['name']
        assert cross['CH25']==[x for row in r['probability_table'] for x in row]
        verify_row(cross)
    print("PASS 175 coefficient identities, 256 deterministic assignments each.")
