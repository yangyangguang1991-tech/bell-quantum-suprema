# Śliwa inequality 2 (S002)

## Bell expression and exact value

```text
ABC + abC + aBc - Abc
```

The local bound is `2`. The expression is evaluated as written, without an implicit shift or scale. Definition: [functional.json](functional.json).

`q = 4`

Numerical display:

```text
4.0000000000000000000000000000000000000000000000000000000000000000000000000000000
```

## Global upper-bound proof

The certificate covers arbitrary dimensions, binary POVMs and commuting-operator strategies through the [common dimension-reduction argument](../../docs/PROOF_GUIDE.md). This entry's complete upper inputs are in [upper_bound/](upper_bound/); [inputs.json](upper_bound/inputs.json) lists its characteristic polynomial and verification sequence.

[Shared analytic algorithm](../../prooflib/analytic.py), applied only to this entry's certificate data.

## Exact attaining strategy

- [Exact state formula and symbolic measurements](attainment/strategy_exact.json).
- [80-digit state vector and all six measurement matrices](attainment/strategy_numeric.json).
- [Exact parameter definitions and root selectors](strategy_spec.json).

The state basis is `000,001,010,011,100,101,110,111`. The matrices are named `A,a,B,b,C,c`.

For the exact Bell matrix `M`, write `det(tI−M)=(t−q)^m R(t)`. Here `m=1`. The supplied state is the normalized fixed column `R(M)e_j` with `j=0` (zero based). The strictly positive rational interval for its squared norm is included in the exact strategy file. Thus the state is explicit, nonzero and attains `q` exactly.

## Verify this entry

From the repository root:

```text
python -S run.py verify --id 2
```

Or run `python -S entries/S002/verify.py`. To compute the supplied state's Bell score independently:

```text
python -S tools/check_strategy.py entries/S002/attainment/strategy_numeric.json
```

The [usage guide](../../docs/USAGE.md) explains CSV exports and the arithmetic-graph format.

## Earlier exact proof

The four signed correlators are bounded by four, and the GHZ measurements attain that bound. [N. D. Mermin, Phys. Rev. Lett. 65, 1838 (1990)](https://doi.org/10.1103/PhysRevLett.65.1838).

The Mermin case of Theorem 6 and the discussion following Eq. (26) give this bound as well. In the half-normalized three-party Mermin polynomial printed there, exchange the two settings of the third party, flip the second outcome observable of the second party, and multiply by two to obtain the literal S002 polynomial. [E. Panwar, P. Pandya and M. Wieśniak, npj Quantum Information **9**, 71 (2023)](https://doi.org/10.1038/s41534-023-00735-3).
