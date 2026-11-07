# Śliwa inequality 21 (S021)

## Bell expression and exact value

```text
A + a + B + AB + b - ab + AC + aC + BC - 2ABC - aBC + bC - AbC + ABc - aBc - Abc + abc
```

The local bound is `4`. The expression is evaluated as written, without an implicit shift or scale. Definition: [functional.json](functional.json).

The unique real root in `(5, 6)` of

```text
243*q**3+1620*q**2-8240*q-59712 = 0
```

Numerical display:

```text
5.9554569186959206519525393738959897602866559884803332268443758338631243131432317
```

## Global upper-bound proof

The certificate covers arbitrary dimensions, binary POVMs and commuting-operator strategies through the [common dimension-reduction argument](../../docs/PROOF_GUIDE.md). This entry's complete upper inputs are in [upper_bound/](upper_bound/); [inputs.json](upper_bound/inputs.json) lists its characteristic polynomial and verification sequence.

[verify_21_global_independent.py](upper_bound/verify_21_global_independent.py)

## Exact attaining strategy

- [Exact state formula and symbolic measurements](attainment/strategy_exact.json).
- [80-digit state vector and all six measurement matrices](attainment/strategy_numeric.json).
- [Exact parameter definitions and root selectors](strategy_spec.json).

The state basis is `000,001,010,011,100,101,110,111`. The matrices are named `A,a,B,b,C,c`.

For the exact Bell matrix `M`, write `det(tI−M)=(t−q)^m R(t)`. Here `m=1`. The supplied state is the normalized fixed column `R(M)e_j` with `j=7` (zero based). The strictly positive rational interval for its squared norm is included in the exact strategy file. Thus the state is explicit, nonzero and attains `q` exactly.

## Verify this entry

From the repository root:

```text
python -S run.py verify --id 21
```

Or run `python -S entries/S021/verify.py`. To compute the supplied state's Bell score independently:

```text
python -S tools/check_strategy.py entries/S021/attainment/strategy_numeric.json
```

The [usage guide](../../docs/USAGE.md) explains CSV exports and the arithmetic-graph format.
