# Y13 · J4422^113

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
  0  -4  -2  -1   0
 -4   2   3   1   3
 -3   2  -3   3   1
 -1   2   2   2  -3
  0   3  -1  -3   0
```

**Exact quantum supremum.** f_13(x_star): unique zero of eight rational gradient equations in the certified rational box

The upper identity, Hilbert-space assumptions and construction of the attaining strategy are given in [the entry proof](PROOF.md). The data specified there are included in the local certificate.

Run `python verify.py 13` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 13 --extract proof-Y013`.
