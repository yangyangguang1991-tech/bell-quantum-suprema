# Y158 · N4422^11

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
  0  -3   0   0   0
 -6   3   1   2   3
 -1   2  -1   1  -1
 -1   3  -2  -3   1
 -3   3   3  -1  -2
```

**Exact quantum supremum.** (3*sqrt(19)-10)/4

The upper identity, Hilbert-space assumptions and construction of the attaining strategy are given in [the entry proof](PROOF.md). The data specified there are included in the local certificate.

Run `python verify.py 158` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 158 --extract proof-Y158`.
