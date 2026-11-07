# Y124 · N4422^2

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
 -2  -3   0  -1   2
 -4   1   2   1   2
  1   1  -1   2  -3
 -3   2  -2   1   3
  1   2   1  -1  -2
```

**Exact quantum supremum.** f_124(x_star): unique zero of thirty-three rational gradient equations in certified rational box

The upper identity, Hilbert-space assumptions and construction of the attaining strategy are given in [the entry proof](PROOF.md). The data specified there are included in the local certificate.

Run `python verify.py 124` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 124 --extract proof-Y124`.
