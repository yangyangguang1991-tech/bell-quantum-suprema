# Exact correspondence between the bipartite catalogues

All original entries remain present. The six common classes are:

- Six-by-three `00-positivity` corresponds to York Y1.
- Six-by-three `01-CHSH` corresponds to York Y2.
- Six-by-three `02-I3322` corresponds to York Y3.
- Six-by-three `03-I4322-1` corresponds to York Y5.
- Six-by-three `04-I4322-2` corresponds to York Y6.
- Six-by-three `05-I4322-3` corresponds to York Y4.

I5322 is the additional six-by-three class. It is not renamed Y176: the
historical York catalogue ends at Y175.

## Exact meaning of the maps

Let the probability coefficient table be C, with its constant in the upper
left, Alice marginals in the first column and Bob marginals in the first row.
Put the binary effects equal to (I+A_i)/2 and (I+B_j)/2. Then

    4 F = sum_(i,j) H[i,j] A_i B_j,    A_0 = B_0 = I.

The conversion includes the constant and every marginal. `CROSSWALK.json`
specifies maps from a six-by-three table to a York table. After the optional
party exchange, each target active row selects a distinct source row and a
sign; each target active column does the same. The identity is

    H_target[i,j] = a_sign[i] b_sign[j] H_source[a_index[i],b_index[j]],

with index 0 and sign +1 implicit. Only settings whose entire reflection
coefficient row or column is zero may be removed. There is no scalar shift
or rescaling in these six identities.

Setting permutations, outcome flips and party exchange map every legal
strategy to a legal strategy, with an inverse after unused settings are
restored arbitrarily. Thus the identities preserve the supremum in each
model, as well as finite attainment or approximation. The transformation
does not assume a particular state, rank, dimension or optimal score.

```console
python -B verify_crosswalk.py
```

This command binds all 182 bipartite coefficient tables and exhaustively
checks the permitted signed permutations. It reproduces the six maps and
checks that no other matches occur in this equivalence class. It is a
coefficient-identity check, not a new quantum upper-bound proof.

The 46 tripartite entries are not included in this bipartite equivalence
count. A lift between different numbers of parties is not identified with
a relabeling within one fixed scenario.
