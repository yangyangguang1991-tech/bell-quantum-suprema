# Y9 · A6

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
 -1  -2  -2   0   1
 -1   1   1   0   1
 -1   1  -1   1   0
  0   0   1   1  -1
  1   1   1  -1  -1
```

**Exact quantum supremum.** f_9(x_star): unique zero of eleven rational gradient equations in certified rational box

The upper identity, Hilbert-space assumptions and construction of the attaining strategy are given in [the entry proof](PROOF.md). The data specified there are included in the local certificate.

Run `python verify.py 9` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 9 --extract proof-Y009`.
