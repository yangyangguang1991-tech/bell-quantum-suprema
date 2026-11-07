# Śliwa inequality 16 (S016)

## Bell expression and exact value

```text
A + a + AB + aB + AC + aC - 2aBC + AbC - abC + ABc - aBc - Abc + abc
```

The local bound is `4`. The expression is evaluated as written, without an implicit shift or scale. Definition: [functional.json](functional.json).

`q = 4*sqrt(1149+156*sqrt(13))/27`

Numerical display:

```text
6.1288693702808872202423760135993411335651645367992877859982543373206632822966470
```

## Global upper-bound proof

The certificate covers arbitrary dimensions, binary POVMs and commuting-operator strategies through the [common dimension-reduction argument](../../docs/PROOF_GUIDE.md). This entry's complete upper inputs are in [upper_bound/](upper_bound/); [inputs.json](upper_bound/inputs.json) lists its characteristic polynomial and verification sequence.

[verify_16_algebra.py](upper_bound/verify_16_algebra.py)

[verify_16_field_independent.py](upper_bound/verify_16_field_independent.py)

[Entry-specific proof derivation](upper_bound/PROOF.md).

## Exact attaining strategy

- [Exact state formula and symbolic measurements](attainment/strategy_exact.json).
- [80-digit state vector and all six measurement matrices](attainment/strategy_numeric.json).
- [Exact parameter definitions and root selectors](strategy_spec.json).

The state basis is `000,001,010,011,100,101,110,111`. The matrices are named `A,a,B,b,C,c`.

For the exact Bell matrix `M`, write `det(tI−M)=(t−q)^m R(t)`. Here `m=1`. The supplied state is the normalized fixed column `R(M)e_j` with `j=7` (zero based). The strictly positive rational interval for its squared norm is included in the exact strategy file. Thus the state is explicit, nonzero and attains `q` exactly.

## Verify this entry

From the repository root:

```text
python -S run.py verify --id 16
```

Or run `python -S entries/S016/verify.py`. To compute the supplied state's Bell score independently:

```text
python -S tools/check_strategy.py entries/S016/attainment/strategy_numeric.json
```

The [usage guide](../../docs/USAGE.md) explains CSV exports and the arithmetic-graph format.
