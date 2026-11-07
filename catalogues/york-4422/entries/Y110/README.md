# Y110 · I4422^12

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
  0  -3  -1   0   0
 -3   1   1   1   2
 -1   2  -2   0   1
 -1   2   1   1  -2
  0   1   1  -1   0
```

**Exact quantum supremum.** q=f(x*), unique zero of the complete listed rational-gradient system in the rational isolation box; denominators nonzero there

The upper identity, Hilbert-space assumptions and construction of the attaining strategy are given in [the entry proof](PROOF.md). The data specified there are included in the local certificate.

Run `python verify.py 110` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 110 --extract proof-Y110`.
