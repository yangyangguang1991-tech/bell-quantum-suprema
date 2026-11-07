"""Verify exact local relabelings between the two bipartite catalogues."""
from pathlib import Path
import hashlib
import itertools
import json

ROOT = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def reflection(c):
    """Return H with 4 F = sum H[i,j] A_i B_j, A_0 = B_0 = I."""
    m, n = len(c) - 1, len(c[0]) - 1
    if any(len(row) != n + 1 for row in c) or any(type(x) is not int for row in c for x in row):
        raise ValueError('The coefficient table must be a rectangular integer matrix.')
    h = [[0] * (n + 1) for _ in range(m + 1)]
    h[0][0] = 4*c[0][0] + 2*sum(c[i][0] for i in range(1,m+1)) + 2*sum(c[0][1:]) + sum(sum(r[1:]) for r in c[1:])
    for i in range(1,m+1):
        h[i][0] = 2*c[i][0] + sum(c[i][1:])
    for j in range(1,n+1):
        h[0][j] = 2*c[0][j] + sum(c[i][j] for i in range(1,m+1))
    for i in range(1,m+1):
        for j in range(1,n+1):
            h[i][j] = c[i][j]
    return h


def trim(h):
    a = [i for i in range(1,len(h)) if any(h[i])]
    b = [j for j in range(1,len(h[0])) if any(r[j] for r in h)]
    return [[h[i][j] for j in [0]+b] for i in [0]+a], a, b


def invariant(h):
    return (len(h), len(h[0]), h[0][0],
            tuple(sorted(abs(x) for r in h[1:] for x in r[1:])),
            tuple(sorted(abs(r[0]) for r in h[1:])),
            tuple(sorted(abs(x) for x in h[0][1:])))


def find(source, target):
    s, sa, sb = trim(source)
    t, ta, tb = trim(target)
    for exchange in (False, True):
        v = [list(r) for r in zip(*s)] if exchange else s
        if invariant(v) != invariant(t):
            continue
        m,n = len(t)-1,len(t[0])-1
        for perm in itertools.permutations(range(1,m+1)):
            if any(abs(t[i+1][0]) != abs(v[perm[i]][0]) for i in range(m)):
                continue
            for signs in itertools.product((1,-1), repeat=m):
                if any(t[i+1][0] != signs[i]*v[perm[i]][0] for i in range(m)):
                    continue
                columns = {}
                for j in range(1,n+1):
                    c = (v[0][j],)+tuple(signs[i]*v[perm[i]][j] for i in range(m))
                    columns.setdefault(c, []).append((j,1))
                    columns.setdefault(tuple(-x for x in c), []).append((j,-1))
                bmap=[]
                used=set()
                for j in range(1,n+1):
                    wanted=tuple(t[i][j] for i in range(m+1))
                    options=[x for x in columns.get(wanted, []) if x[0] not in used]
                    if not options:
                        break
                    chosen=options[0]
                    bmap.append(chosen)
                    used.add(chosen[0])
                if len(bmap) != n:
                    continue
                pi=[0]+list(perm)
                pj=[0]+[x[0] for x in bmap]
                si=[1]+list(signs)
                sj=[1]+[x[1] for x in bmap]
                if not all(t[i][j] == si[i]*sj[j]*v[pi[i]][pj[j]] for i in range(m+1) for j in range(n+1)):
                    raise ValueError('A proposed relabeling fails coefficient equality.')
                ai,bi=(sb,sa) if exchange else (sa,sb)
                return {'party_exchange':exchange, 'target_active_alice':ta,
                        'target_active_bob':tb,
                        'source_alice_indices':[ai[x-1] for x in perm],
                        'alice_signs':list(signs),
                        'source_bob_indices':[bi[x[0]-1] for x in bmap],
                        'bob_signs':[x[1] for x in bmap]}
    return None


def calculate():
    six=ROOT/'catalogues/six-by-three/entries'
    york=ROOT/'catalogues/york-4422/entries'
    inputs={}
    sources={}
    targets={}
    for f in sorted(six.glob('*/definition.json')):
        sources[f.parent.name]=reflection(read(f)['active_table'])
        inputs[f.relative_to(ROOT).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
    for f in sorted(york.glob('Y*/definition.json')):
        d=read(f)
        targets[d['york_number']]=reflection(d['probability_table'])
        inputs[f.relative_to(ROOT).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
    if len(sources)!=7 or sorted(targets)!=list(range(1,176)):
        raise ValueError('Incomplete bipartite catalogue definitions.')
    matches=[]
    for label,source in sources.items():
        for number,target in targets.items():
            mapping=find(source,target)
            if mapping is not None:
                matches.append({'six_by_three_entry':label, 'york_number':number, 'map':mapping})
    pairs=[(r['six_by_three_entry'],r['york_number']) for r in matches]
    expected=[('00-positivity',1),('01-CHSH',2),('02-I3322',3),
              ('03-I4322-1',5),('04-I4322-2',6),('05-I4322-3',4)]
    if pairs!=expected:
        raise ValueError('The exact catalogue overlap differs from the specified six classes.')
    return {'convention':'4F = sum H[i,j] A_i B_j; A_0=B_0=I; effects=(I+A_i)/2 and (I+B_j)/2.',
            'scope':'Setting permutations, local outcome flips, party exchange and removal of wholly unused settings; scale one and zero added scalar. No identification of tripartite and bipartite classes.',
            'definition_sha256':inputs, 'matches':matches}


if __name__ == '__main__':
    actual=calculate()
    expected=read(ROOT/'CROSSWALK.json')
    if actual!=expected:
        raise ValueError('Crosswalk data, coefficient definitions or exact transformations differ.')
    print('PASS six exact bipartite correspondences, all 182 original coefficient tables and the absence of additional matches in this relabeling class.')
