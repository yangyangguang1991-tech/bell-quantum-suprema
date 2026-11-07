# Śliwa inequality 22 (S022)

## Bell expression and exact value

```text
A + a + B + AB + b - ab + C + AC + BC - 2ABC - aBC - AbC + abC + c - ac - ABc + aBc - bc + Abc
```

The local bound is `4`. The expression is evaluated as written, without an implicit shift or scale. Definition: [functional.json](functional.json).

The unique real root in `(11611869448169517237733206769741/1873498979564783417543254600986, 4155329092868420420864835450739/670435096604712748770505419233)` of

```text
27*q**5 - 972*q**4 + 8608*q**3 + 107904*q**2 - 865536*q + 357376 = 0
```

Numerical display:

```text
6.1979587791753010059357828996695158685903903555328873478822554568074711900542590
```

## Global upper-bound proof

The certificate covers arbitrary dimensions, binary POVMs and commuting-operator strategies through the [common dimension-reduction argument](../../docs/PROOF_GUIDE.md). This entry's complete upper inputs are in [upper_bound/](upper_bound/); [inputs.json](upper_bound/inputs.json) lists its characteristic polynomial and verification sequence.

[verify_22_independent.py](upper_bound/verify_22_independent.py)

## Exact attaining strategy

- [Exact state formula and symbolic measurements](attainment/strategy_exact.json).
- [80-digit state vector and all six measurement matrices](attainment/strategy_numeric.json).
- [Exact parameter definitions and root selectors](strategy_spec.json).

The state basis is `000,001,010,011,100,101,110,111`. The matrices are named `A,a,B,b,C,c`.

For the exact Bell matrix `M`, write `det(tI−M)=(t−q)^m R(t)`. Here `m=1`. The supplied state is the normalized fixed column `R(M)e_j` with `j=7` (zero based). The strictly positive rational interval for its squared norm is included in the exact strategy file. Thus the state is explicit, nonzero and attains `q` exactly.

## Verify this entry

From the repository root:

```text
python -S run.py verify --id 22
```

Or run `python -S entries/S022/verify.py`. To compute the supplied state's Bell score independently:

```text
python -S tools/check_strategy.py entries/S022/attainment/strategy_numeric.json
```

The [usage guide](../../docs/USAGE.md) explains CSV exports and the arithmetic-graph format.
