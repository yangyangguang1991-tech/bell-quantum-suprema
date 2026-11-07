# Y3 · I3322

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
  0  -1  -2   0   0
 -1   1   1   1   0
  0  -1   1   0   0
  0   1   1  -1   0
  0   0   0   0   0
```

**Exact quantum supremum.** The Jacobi path constant $q_*$ defined in [PROOF.md](PROOF.md), with

$$
Q_{\mathrm{fin}}=Q_{\mathrm{sp}}=Q_{\mathrm{com}}=q_*.
$$

The proof includes an unrestricted commuting-operator upper bound and a sequence of legal finite-dimensional strategies approaching the same value. Finite-dimensional nonattainment and normal infinite-dimensional spatial attainment are established in the [cited exact-value literature](REFERENCES.md). The proof distinguishes the literal York coordinates from the enclosed source program's equivalent three-setting convention. Only the fourth setting of each party is unused in the York table.

Run `python verify.py 3` from the root of this York catalogue. To inspect the uncompressed mathematical inputs, run `python verify.py 3 --extract proof-Y003`.
