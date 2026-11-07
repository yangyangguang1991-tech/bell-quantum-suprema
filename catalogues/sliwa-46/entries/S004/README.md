# Śliwa inequality 4 (S004)

## Bell expression and exact value

```text
2A + BC - ABC + bC - AbC + Bc - ABc - bc + Abc
```

The local bound is `2`. The expression is evaluated as written, without an implicit shift or scale. Definition: [functional.json](functional.json).

`q = 4*sqrt(2)-2`

Numerical display:

```text
3.6568542494923801952067548968387923142786875015077922927067189519629299138484282
```

## Global upper-bound proof

The certificate covers arbitrary dimensions, binary POVMs and commuting-operator strategies through the [common dimension-reduction argument](../../docs/PROOF_GUIDE.md). This entry's complete upper inputs are in [upper_bound/](upper_bound/); [inputs.json](upper_bound/inputs.json) lists its characteristic polynomial and verification sequence.

[Shared analytic algorithm](../../prooflib/analytic.py), applied only to this entry's certificate data.

## Exact attaining strategy

- [Exact state formula and symbolic measurements](attainment/strategy_exact.json).
- [80-digit state vector and all six measurement matrices](attainment/strategy_numeric.json).
- [Exact parameter definitions and root selectors](strategy_spec.json).

The state basis is `000,001,010,011,100,101,110,111`. The matrices are named `A,a,B,b,C,c`.

For the exact Bell matrix `M`, write `det(tI−M)=(t−q)^m R(t)`. Here `m=1`. The supplied state is the normalized fixed column `R(M)e_j` with `j=4` (zero based). The strictly positive rational interval for its squared norm is included in the exact strategy file. Thus the state is explicit, nonzero and attains `q` exactly.

## Verify this entry

From the repository root:

```text
python -S run.py verify --id 4
```

Or run `python -S entries/S004/verify.py`. To compute the supplied state's Bell score independently:

```text
python -S tools/check_strategy.py entries/S004/attainment/strategy_numeric.json
```

The [usage guide](../../docs/USAGE.md) explains CSV exports and the arithmetic-graph format.

## Earlier exact proof

Let H = BC + bC + Bc − bc. The literal expression satisfies S4 − 2I = (I−A)(H−2I). This is twice the CHSH functional H−2I conditioned on the event A=−1. The party-lifting theorem of Jebarathinam, Hung, Chen and Liang (Section III.C, Observation 1), together with the exact CHSH bound, gives S4 ≤ (4√2−2)I. In the A=+1 sector the value is 2. The A=−1 sector with a CHSH-maximizing pair attains 4√2−2. This identifies the specialization and normalization of the earlier theorem. [Party lifting](https://doi.org/10.1103/PhysRevResearch.1.033073) · [CHSH quantum bound](https://doi.org/10.1007/BF00417500).

The same specialization already follows from the tight composite-bound theorem of D. Rosset, J.-D. Bancal and N. Gisin, Section II.4 and Appendix C.2, Proposition 4 (2014). Take the additive constant to be 2 and the two factors to be I−A and H−2I. Their endpoint bounds are [0,2] and [−2√2−2,2√2−2]; the upper endpoint product gives 4√2−2, attained by A=−1 and a CHSH-maximizing pair. [Earlier composite-bound theorem](https://doi.org/10.1088/1751-8113/47/42/424022).
