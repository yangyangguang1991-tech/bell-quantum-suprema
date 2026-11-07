# Śliwa inequality 40 (S040)

## Bell expression and exact value

```text
2A + 2a + 2B - AB - aB + Ab + ab + AC + aC + 2BC - ABC - aBC + 2bC - 2AbC - 2abC + Ac - ac - 2ABc + 2aBc + Abc - abc
```

The local bound is `6`. The expression is evaluated as written, without an implicit shift or scale. Definition: [functional.json](functional.json).

The unique real root in `(8, 9)` of

```text
2891*q**11 + 150426*q**10 - 1513836*q**9 - 7160488*q**8 + 67867360*q**7 + 61979712*q**6 - 787412352*q**5 + 822897408*q**4 - 2306730240*q**3 + 9236906496*q**2 - 8585837568*q - 79792128 = 0
```

Numerical display:

```text
8.1297872420881080848592792807707013847125182197410724779660831647761251387330801
```

## Global upper-bound proof

The certificate covers arbitrary dimensions, binary POVMs and commuting-operator strategies through the [common dimension-reduction argument](../../docs/PROOF_GUIDE.md). This entry's complete upper inputs are in [upper_bound/](upper_bound/); [inputs.json](upper_bound/inputs.json) lists its characteristic polynomial and verification sequence.

[verify_40_independent.py](upper_bound/verify_40_independent.py)

[verify_40_single_field.py](upper_bound/verify_40_single_field.py)

## Exact attaining strategy

- [Exact state formula and symbolic measurements](attainment/strategy_exact.json).
- [80-digit state vector and all six measurement matrices](attainment/strategy_numeric.json).
- [Exact parameter definitions and root selectors](strategy_spec.json).

The state basis is `000,001,010,011,100,101,110,111`. The matrices are named `A,a,B,b,C,c`.

For the exact Bell matrix `M`, write `det(tI−M)=(t−q)^m R(t)`. Here `m=1`. The supplied state is the normalized fixed column `R(M)e_j` with `j=0` (zero based). The strictly positive rational interval for its squared norm is included in the exact strategy file. Thus the state is explicit, nonzero and attains `q` exactly.

## Verify this entry

From the repository root:

```text
python -S run.py verify --id 40
```

Or run `python -S entries/S040/verify.py`. To compute the supplied state's Bell score independently:

```text
python -S tools/check_strategy.py entries/S040/attainment/strategy_numeric.json
```

The [usage guide](../../docs/USAGE.md) explains CSV exports and the arithmetic-graph format.
