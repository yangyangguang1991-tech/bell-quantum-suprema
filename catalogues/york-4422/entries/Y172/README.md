# Y172 · J4422^71

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
  0  -2   0  -1   0
 -5   2   2   2   2
  0   1  -2   1   0
 -1   1   1   1  -2
  0   1   0  -1   0
```

**Exact quantum supremum.** f_172(x_star): unique zero of nine rational gradient equations in certified rational box

The upper identity, Hilbert-space assumptions and construction of the attaining strategy are given in [the entry proof](PROOF.md). The data specified there are included in the local certificate.

Run `python verify.py 172` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 172 --extract proof-Y172`.
