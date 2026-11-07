"""Bind the two deterministic Charlie branches to the full characteristic."""
from pathlib import Path
from fractions import Fraction
import json,sympy as S
if not __debug__:raise RuntimeError('Run without -O or -OO')
D=Path(__file__).resolve().parent
q,x,y,z=S.symbols('q x y z')
P=S.sympify((D/'charpoly_46_full.txt').read_text())
plus=S.sympify('q ** 4 + 48 * q * q * x * y + 48 * q * q * x + 48 * q * q * y - 296 * q * q - 576 * q * x * y - 576 * q * x - 576 * q * y + 2304 * q - 1024 * x * x * y * y + 1024 * x * x + 960 * x * y + 960 * x + 1024 * y * y + 960 * y - 4464')
minus=S.sympify('q ** 4 + 32 * q ** 2 * x * y - 32 * q ** 2 * x - 32 * q ** 2 * y - 184 * q ** 2 - 128 * q * x * y + 128 * q * x + 128 * q * y + 192 * q - 6144 * x * x * y * y + 6144 * x * x - 1920 * x * y + 1920 * x + 6144 * y * y + 1920 * y + 336')
assert S.expand(P.subs(z,1)-plus*minus)==0
C=json.loads((D/'certificate_46_full_bernstein.json').read_text())
B=json.loads((D/'certificate_46_reduced.json').read_text())
assert list(map(Fraction,C['q_interval']))==list(map(Fraction,B['isolating_interval']))
assert Fraction(C['q_interval'][0])>12
f=S.Poly(S.sympify(B['polynomial']),q)
assert f.count_roots(*map(S.Rational,B['isolating_interval']))==1
print('PASS full characteristic boundary factorization and exact-value binding')
