# Śliwa inequality 33 (S033)

## Bell expression and exact value

```text
A + a + B - aB + b - Ab + C - aC + 2aBC - bC + 2AbC + abC + c - Ac - Bc + 2ABc + aBc + Abc - 3abc
```

The local bound is `6`. The expression is evaluated as written, without an implicit shift or scale. Definition: [functional.json](functional.json).

The unique real root in `(1957970663654534598478605853855605685092019509/200000000000000000000000000000000000000000000, 1957970663654534598478605853856005685092019509/200000000000000000000000000000000000000000000)` of

```text
54*q**12 + 9032*q**11 + 908421*q**10 + 45607668*q**9 + 1209126020*q**8 + 3264069312*q**7 - 205380507744*q**6 - 827904633984*q**5 + 10254570689664*q**4 - 11023382264832*q**3 - 62255513288448*q**2 + 158439706850304*q - 104196893322240 = 0
```

Numerical display:

```text
9.7898533182726729923930292692790284254600975449844152846001543339147808524421687
```

## Global upper-bound proof

The certificate covers arbitrary dimensions, binary POVMs and commuting-operator strategies through the [common dimension-reduction argument](../../docs/PROOF_GUIDE.md). This entry's complete upper inputs are in [upper_bound/](upper_bound/); [inputs.json](upper_bound/inputs.json) lists its characteristic polynomial and verification sequence.

[verify_s33_global_independent.py](upper_bound/verify_s33_global_independent.py)

## Exact attaining strategy

- [Exact state formula and symbolic measurements](attainment/strategy_exact.json).
- [80-digit state vector and all six measurement matrices](attainment/strategy_numeric.json).
- [Exact parameter definitions and root selectors](strategy_spec.json).

The state basis is `000,001,010,011,100,101,110,111`. The matrices are named `A,a,B,b,C,c`.

For the exact Bell matrix `M`, write `det(tI−M)=(t−q)^m R(t)`. Here `m=1`. The supplied state is the normalized fixed column `R(M)e_j` with `j=7` (zero based). The strictly positive rational interval for its squared norm is included in the exact strategy file. Thus the state is explicit, nonzero and attains `q` exactly.

## Verify this entry

From the repository root:

```text
python -S run.py verify --id 33
```

Or run `python -S entries/S033/verify.py`. To compute the supplied state's Bell score independently:

```text
python -S tools/check_strategy.py entries/S033/attainment/strategy_numeric.json
```

The [usage guide](../../docs/USAGE.md) explains CSV exports and the arithmetic-graph format.
