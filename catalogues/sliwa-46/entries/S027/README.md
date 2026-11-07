# Śliwa inequality 27 (S027)

## Bell expression and exact value

```text
2A + a + B - AB + Ab + ab + C - AC + 2ABC - 2aBC + bC - AbC + Ac + ac + Bc - ABc + bc - 2Abc - abc
```

The local bound is `5`. The expression is evaluated as written, without an implicit shift or scale. Definition: [functional.json](functional.json).

The unique real root in `(6954655832892835349916432033539220817176226839/1000000000000000000000000000000000000000000000, 6954655832892835349916432033541220817176226839/1000000000000000000000000000000000000000000000)` of

```text
10849707*q**17 - 150960591*q**16 - 2050185384*q**15 + 42149662632*q**14 - 7397849916*q**13 - 3449841500628*q**12 + 16815103176776*q**11 + 69584416756216*q**10 - 692349592440238*q**9 + 196002544695094*q**8 + 11657605749300776*q**7 - 26991280436896424*q**6 - 60390083350535068*q**5 + 292083434523950668*q**4 - 285077706709744456*q**3 - 85515321733308280*q**2 + 149822598004120667*q + 38413632053782177 = 0
```

Numerical display:

```text
6.9546558328928353499164320335402208171762268391790800168245532724274061305510212
```

## Global upper-bound proof

The certificate covers arbitrary dimensions, binary POVMs and commuting-operator strategies through the [common dimension-reduction argument](../../docs/PROOF_GUIDE.md). This entry's complete upper inputs are in [upper_bound/](upper_bound/); [inputs.json](upper_bound/inputs.json) lists its characteristic polynomial and verification sequence.

[verify_s27_global_independent.py](upper_bound/verify_s27_global_independent.py)

## Exact attaining strategy

- [Exact state formula and symbolic measurements](attainment/strategy_exact.json).
- [80-digit state vector and all six measurement matrices](attainment/strategy_numeric.json).
- [Exact parameter definitions and root selectors](strategy_spec.json).

The state basis is `000,001,010,011,100,101,110,111`. The matrices are named `A,a,B,b,C,c`.

For the exact Bell matrix `M`, write `det(tI−M)=(t−q)^m R(t)`. Here `m=1`. The supplied state is the normalized fixed column `R(M)e_j` with `j=5` (zero based). The strictly positive rational interval for its squared norm is included in the exact strategy file. Thus the state is explicit, nonzero and attains `q` exactly.

## Verify this entry

From the repository root:

```text
python -S run.py verify --id 27
```

Or run `python -S entries/S027/verify.py`. To compute the supplied state's Bell score independently:

```text
python -S tools/check_strategy.py entries/S027/attainment/strategy_numeric.json
```

The [usage guide](../../docs/USAGE.md) explains CSV exports and the arithmetic-graph format.
