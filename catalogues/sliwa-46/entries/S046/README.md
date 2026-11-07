# Śliwa inequality 46 (S046)

## Bell expression and exact value

```text
3A + a + 3B - 2AB - aB + b - Ab - 2ab + 2AC - 2aC + BC - 3ABC + 4aBC + bC - AbC + 2abC + Ac + ac + 2Bc - 3ABc - aBc - 2bc + 4Abc + 2abc
```

The local bound is `10`. The expression is evaluated as written, without an implicit shift or scale. Definition: [functional.json](functional.json).

The unique real root in `(12985173496317373/1000000000000000, 6492586748158687/500000000000000)` of

```text
25*q**3 - 46*q**2 - 4788*q + 15192 = 0
```

Numerical display:

```text
12.985173496317373300203056007388254090234326872115076742715018242988463116660844
```

## Global upper-bound proof

The certificate covers arbitrary dimensions, binary POVMs and commuting-operator strategies through the [common dimension-reduction argument](../../docs/PROOF_GUIDE.md). This entry's complete upper inputs are in [upper_bound/](upper_bound/); [inputs.json](upper_bound/inputs.json) lists its characteristic polynomial and verification sequence.

[verify_46_plus.py](upper_bound/verify_46_plus.py)

[verify_46_reduced.py](upper_bound/verify_46_reduced.py)

[verify_boundary.py](upper_bound/verify_boundary.py)

[verify_sliwa46_bernstein_independent.py](upper_bound/verify_sliwa46_bernstein_independent.py)

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
python -S run.py verify --id 46
```

Or run `python -S entries/S046/verify.py`. To compute the supplied state's Bell score independently:

```text
python -S tools/check_strategy.py entries/S046/attainment/strategy_numeric.json
```

The [usage guide](../../docs/USAGE.md) explains CSV exports and the arithmetic-graph format.
