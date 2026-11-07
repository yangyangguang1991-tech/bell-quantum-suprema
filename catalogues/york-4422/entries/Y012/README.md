# Y12 · J4422^9

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
  0  -3  -2  -2   0
 -1   0   1   1   1
 -1   1  -1   1   1
 -1   2   1  -2   1
  0   2   1   2  -2
```

**Exact quantum supremum.** 1/2

[Upper bound and attainment](PROOF.md).

Run `python verify.py 12` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 12 --extract proof-Y012`.
