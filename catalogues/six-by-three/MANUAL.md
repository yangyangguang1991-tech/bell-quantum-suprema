# Reproduction manual

## Requirements and commands

Python 3.10 or later and its standard library are sufficient. There is no operating-system-specific arithmetic engine, compiler, package installer, or external mathematical data dependency. Extract or clone the complete repository. Run commands from its root:

```console
python -B verify.py
python -B verify.py 0
python -B verify.py 1
python -B verify.py 2
python -B verify.py 3
python -B verify.py 4
python -B verify.py 5
python -B verify.py 6
python -B verify_files.py
```

The first command executes all seven proof checks and the complete facet enumeration. The numbered commands execute the indicated entry and its full-scenario facet check. Each entry can also be run through its own `verify.py`, for example `python -B entries/04-I4322-2/verify.py`. The commands resolve input paths relative to the files, so they also work with an absolute script path from another working directory. Verification rejects disabled assertions, malformed data, failed identities and nonpositive certified pivots. A child-process failure propagates to the root command. Do not run Python with `-O`, `-OO` or a nonzero `PYTHONOPTIMIZE` setting.

`verify_files.py` checks the listed files against `SHA256SUMS.txt`; it checks transfer integrity, not the mathematical theorem. The mathematical checks are the proof commands above. They do not modify the supplied inputs. `-B` suppresses bytecode caches. I3322 example exports are written only when explicitly requested.

## File framework

Every entry contains `README.md`, `definition.json`, `PROOF.md`, `proof.json` and `verify.py`. The metadata identifies the proof method and local materials, not a saved execution verdict. The six finite-attainment entries include `strategy.json`. The two Gram entries also include `gram.json`. I3322 instead supplies `example.json` and `sequence.py`. CHSH and I3322 include `REFERENCES.md` for identified historical exact unrestricted results. Other relevant historical sources are recorded globally; an entry does not cite a numerical estimate as a prior proof of its exact value.

`common/` contains only shared local arithmetic, polynomial expansion and facet-enumeration code. Keep this directory when moving individual entries. Every certificate and strategy for an entry is local; no other entry's proof data is required.

## Probability conventions and model coverage

For positive-outcome projections $P_i,Q_j$, the table specifies

$$F=C_{00}I+\sum_i C_{i0}P_i+\sum_j C_{0j}Q_j+\sum_{ij}C_{ij}P_iQ_j.$$

The first column contains Alice marginals and the first row Bob marginals. Append zero rows or columns to reach six and three settings. Strategies restrict to the active table, and conversely extend by identity measurements, so padding preserves every quantum supremum.

The upper proofs assume only cross-party commutation. Same-party measurements need not commute. For a binary effect $E$, the projection with blocks $E,\sqrt{E(I-E)},\sqrt{E(I-E)},I-E$ compresses to $E$. Distinct ancillary factors for the measurements and disjoint factors for the parties preserve each marginal and cross-party product. Thus projection upper bounds cover all binary POVMs. Explicit finite strategies prove the reverse inequality for six entries. For I3322 a proved convergent family establishes equality of suprema; separate external theorems address finite nonattainment and normal infinite-dimensional attainment.

## Exact finite strategies

Each scalar in `strategy.json` is a list of triples $[c,d,j]$, interpreted as the sum of $c\sqrt d\,i^j$, where $c$ is rational, $d$ is a squarefree positive integer and $j=0$ or $1$. An empty list represents zero. Matrix multiplication and conjugation use exact rational arithmetic. The state has four coordinates in basis order $00,01,10,11$. Each file stores all six Alice and three Bob $2\times2$ reflections. The verifier checks state normalization and all Hermitian involution identities, forms $(I+R)/2$, and contracts every constant, marginal and joint term of the literal table. These checks give an exact attaining Bell score.

## Gram identities and strict positivity

For I4322^(1), $Y$ is a $16\times16$ symmetric matrix over $\mathbb Q(\sqrt2)$, with a $20\times16$ factor $N$. For I4322^(2), $Y$ is $46\times46$ over $\mathbb Q(\sqrt3)$, $N$ is rational $50\times46$, and the row multiplier is $D_{ii}=(\sqrt3)^{s_i}$. The identities are respectively $qI-F=w^*NYN^{\mathsf T}w$ and $qI-F=w^*DNYN^{\mathsf T}Dw$.

The word reducer cancels adjacent equal reflection letters within each party and commutes letters only across parties. Every oriented coefficient is checked exactly. In particular, reversing a word is not silently identified with the original word.

For positivity, start with interval enclosures of the entries of $Y$. At step $k$, enclose the pivot $p=S_{kk}$, require its lower endpoint to be positive, then update

$$S_{ij}\leftarrow S_{ij}-S_{ik}S_{jk}/p\qquad(i,j>k).$$

Every interval endpoint is an integer multiple of $2^{-384}$. Addition, multiplication and positive-denominator division round outwards by exact floor or ceiling division. Integer square roots provide an enclosing interval for the positive field embedding. Induction proves that each interval contains the exact Schur entry. Positive lower endpoints certify every exact pivot, hence $Y\succ0$. This certificate uses no floating-point eigenvalue tolerance.

## Spectral proofs and I3322

The CHSH checker expands its full square identity. The I4322^(3) and I5322 checkers expand their Bell polynomials and weighted square identities, and verify the scalar branch comparisons exactly. The operator inequalities and their dimension-independent hypotheses are proved in each `PROOF.md`; the exact supplied strategies independently match their values.

I3322's verifier expands the exact Bell/Jacobi reduction, checks the stored example as a literal probability experiment, and constructs 32 finite rational path strategies. To export another path and to enumerate one stage of the approaching family:

```console
python -B entries/02-I3322/verify.py --labels 0,1/3,1/2,inf --vector 1,2,1 --export path.json
python -B entries/02-I3322/sequence.py 2
```

The unnormalized Schmidt coefficients are in `state_diagonal`; divide by the square root of `state_normalization_squared`. The three reported projectors per party are in the literal entry convention. Add three identity Alice settings. A finite run proves only the stated finite identities. The written Riccati argument proves the unrestricted upper bound; the density argument proves convergence of the enumeration. Replaying finite examples does not independently reproduce the external theorem constructing a normal infinite-dimensional maximizer.

## Facet completeness

Every entry is checked on all 512 deterministic assignments in the full 27-dimensional probability space. Its homogeneous saturating vertices have rank 27 modulo a prime, giving a rational lower bound of 27; the supporting hyperplane gives the matching upper bound. The complete enumeration in [FACETS.md](FACETS.md) generates 2,431 candidate tables and 98 candidate orbits, and identifies exactly these seven facet classes. Run it separately with `python -B common/classification.py`.
