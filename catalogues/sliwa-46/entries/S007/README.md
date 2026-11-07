# Śliwa inequality 7 (S007)

## Bell expression and exact value

```text
3ABC + aBC + AbC - abC + ABc - aBc - Abc + abc
```

The local bound is `4`. The expression is evaluated as written, without an implicit shift or scale. Definition: [functional.json](functional.json).

`q = 20/3`

Numerical display:

```text
6.6666666666666666666666666666666666666666666666666666666666666666666666666666667
```

## Global upper-bound proof

The certificate covers arbitrary dimensions, binary POVMs and commuting-operator strategies through the [common dimension-reduction argument](../../docs/PROOF_GUIDE.md). This entry's complete upper inputs are in [upper_bound/](upper_bound/); [inputs.json](upper_bound/inputs.json) lists its characteristic polynomial and verification sequence.

[Shared analytic algorithm](../../prooflib/analytic.py), applied only to this entry's certificate data.

## Exact attaining strategy

- [Exact state formula and symbolic measurements](attainment/strategy_exact.json).
- [80-digit state vector and all six measurement matrices](attainment/strategy_numeric.json).
- [Exact parameter definitions and root selectors](strategy_spec.json).

The state basis is `000,001,010,011,100,101,110,111`. The matrices are named `A,a,B,b,C,c`.

For the exact Bell matrix `M`, write `det(tI−M)=(t−q)^m R(t)`. Here `m=1`. The supplied state is the normalized fixed column `R(M)e_j` with `j=3` (zero based). The strictly positive rational interval for its squared norm is included in the exact strategy file. Thus the state is explicit, nonzero and attains `q` exactly.

## Verify this entry

From the repository root:

```text
python -S run.py verify --id 7
```

Or run `python -S entries/S007/verify.py`. To compute the supplied state's Bell score independently:

```text
python -S tools/check_strategy.py entries/S007/attainment/strategy_numeric.json
```

The [usage guide](../../docs/USAGE.md) explains CSV exports and the arithmetic-graph format.

## Earlier exact proof

Panwar, Pandya and Wieśniak explicitly identify this representative as Śliwa’s seventh inequality in the discussion accompanying Eqs. (26)–(27). Their qubit block and anti-diagonal reduction gives the exact maximum $20/3$. [E. Panwar, P. Pandya and M. Wieśniak, npj Quantum Information **9**, 71 (2023)](https://doi.org/10.1038/s41534-023-00735-3). The remaining scalar optimization can be checked directly as follows.

The anti-diagonal entries have the form $4+(u-1)(v-1)(w-1)$ for unit complex $u,v,w$. The operator norm of each two-dimensional block is the absolute value of its anti-diagonal entry. Fix $u,v$ and put $K=(u-1)(v-1)$. Maximizing over $w$ gives $|4-K|+|K|$. Write $u=e^{2ix}$ and $v=e^{2iy}$, where $0\leq x,y\leq\pi$. Set $t=\cos(x+y)$ and $s=\sin x\sin y$. The result divided by four is
$$
\sqrt{1+2st+s^2}+s .
$$
For fixed $x+y$, the triangle inequality shows that this expression is nondecreasing in $s$: the modulus $|1+s e^{i(x+y)}|$ can decrease by at most the increase in $s$. Also $s=(\cos(x-y)-t)/2\leq(1-t)/2$, with equality at $x=y$. Substitute $t=1-2s$. For $0\leq s\leq1$, $5/3-s$ is positive and
$$
(5/3-s)^2-(1+2s-3s^2)=4(s-2/3)^2 .
$$
The bound is therefore $4(5/3)$, with equality at $s=2/3$ and $\cos(2x)=-1/3$. The numbered certificate and explicit state above give a second global proof and a direct realization in the archive’s tensor basis.
