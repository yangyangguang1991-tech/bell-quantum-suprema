# Śliwa inequality 24 (S024)

## Bell expression and exact value

```text
A + B + aB + Ab + ab + C + aC - BC + 2ABC - aBC - 2abC + Ac + ac - 2aBc - Abc + abc
```

The local bound is `5`. The expression is evaluated as written, without an implicit shift or scale. Definition: [functional.json](functional.json).

The `q` coordinate of the uniquely isolated real solution of the polynomial system in [strategy_spec.json](strategy_spec.json). The complete variable order, equations and selecting rational box are included there.

Numerical display:

```text
7.9401098058580475757600308253258615750597234702439552944772427122628622182588935
```

## Global upper-bound proof

The certificate covers arbitrary dimensions, binary POVMs and commuting-operator strategies through the [common dimension-reduction argument](../../docs/PROOF_GUIDE.md). This entry's complete upper inputs are in [upper_bound/](upper_bound/); [inputs.json](upper_bound/inputs.json) lists its characteristic polynomial and verification sequence.

[verify_24_independent.py](upper_bound/verify_24_independent.py)

## Exact attaining strategy

- [Exact state formula and symbolic measurements](attainment/strategy_exact.json).
- [80-digit state vector and all six measurement matrices](attainment/strategy_numeric.json).
- [Exact parameter definitions and root selectors](strategy_spec.json).

The state basis is `000,001,010,011,100,101,110,111`. The matrices are named `A,a,B,b,C,c`.

For the exact Bell matrix `M`, write `det(tI−M)=(t−q)^m R(t)`. Here `m=1`. The supplied state is the normalized fixed column `R(M)e_j` with `j=3` (zero based). The strictly positive rational interval for its squared norm is included in the exact strategy file. Thus the state is explicit, nonzero and attains `q` exactly.

## Verify this entry

From the repository root:

```text
python -S run.py verify --id 24
```

Or run `python -S entries/S024/verify.py`. To compute the supplied state's Bell score independently:

```text
python -S tools/check_strategy.py entries/S024/attainment/strategy_numeric.json
```

The [usage guide](../../docs/USAGE.md) explains CSV exports and the arithmetic-graph format.
