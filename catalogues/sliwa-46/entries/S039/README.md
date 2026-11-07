# Śliwa inequality 39 (S039)

## Bell expression and exact value

```text
2A + 2B - AB + aB + Ab + ab + 2C - AC + aC - BC + 2ABC - aBC + bC - AbC - 2abC + Ac + ac + Bc - ABc - 2aBc + bc - 2Abc + abc
```

The local bound is `6`. The expression is evaluated as written, without an implicit shift or scale. Definition: [functional.json](functional.json).

The unique real root in `(932534016501399318529197385054040599014920742486111/100000000000000000000000000000000000000000000000000, 29141688015668728704037418282938768719216273202691/3125000000000000000000000000000000000000000000000)` of

```text
27*q**8 - 682*q**7 - 3750*q**6 + 111824*q**5 - 445576*q**4 + 2571360*q**3 - 94816160*q**2 + 548344832*q + 1634780544 = 0
```

Numerical display:

```text
9.3253401650139931852919738505404059901492074248611165280851748386583180683808945
```

## Global upper-bound proof

The certificate covers arbitrary dimensions, binary POVMs and commuting-operator strategies through the [common dimension-reduction argument](../../docs/PROOF_GUIDE.md). This entry's complete upper inputs are in [upper_bound/](upper_bound/); [inputs.json](upper_bound/inputs.json) lists its characteristic polynomial and verification sequence.

[verify_39_independent.py](upper_bound/verify_39_independent.py)

## Exact attaining strategy

- [Exact state formula and symbolic measurements](attainment/strategy_exact.json).
- [80-digit state vector and all six measurement matrices](attainment/strategy_numeric.json).
- [Exact parameter definitions and root selectors](strategy_spec.json).

The state basis is `000,001,010,011,100,101,110,111`. The matrices are named `A,a,B,b,C,c`.

For the exact Bell matrix `M`, write `det(tI−M)=(t−q)^m R(t)`. Here `m=1`. The supplied state is the normalized fixed column `R(M)e_j` with `j=3` (zero based). The strictly positive rational interval for its squared norm is included in the exact strategy file. Thus the state is explicit, nonzero and attains `q` exactly.

## Verify this entry

From the repository root:

```text
python -S run.py verify --id 39
```

Or run `python -S entries/S039/verify.py`. To compute the supplied state's Bell score independently:

```text
python -S tools/check_strategy.py entries/S039/attainment/strategy_numeric.json
```

The [usage guide](../../docs/USAGE.md) explains CSV exports and the arithmetic-graph format.
