# Y87 · J4422^19

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
  0  -4   0  -1  -1
 -4   2   4   1   1
 -2   0  -2   2   2
  0   2  -1  -1   1
  0   2  -1   1  -1
```

**Exact quantum supremum.** 3*sqrt(6)/2-3

[Upper bound and attainment](PROOF.md).

Run `python verify.py 87` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 87 --extract proof-Y087`.
