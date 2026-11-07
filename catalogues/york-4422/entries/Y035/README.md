# Y35 · N4422^3

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
 -1  -2   0   1  -3
 -4   1   1   3   3
 -2   2  -1   2  -2
  0   1   1  -2   1
  1   1  -2  -2   2
```

**Exact quantum supremum.** f(x*), with x* isolated by the exact polynomial system, box and physical chart in this entry.

The upper identity, Hilbert-space assumptions and construction of the attaining strategy are given in [the entry proof](PROOF.md). The data specified there are included in the local certificate.

Run `python verify.py 35` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 35 --extract proof-Y035`.
