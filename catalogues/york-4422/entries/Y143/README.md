# Y143 · N4422^4

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
  0  -1  -3   0   0
 -3   1   2   2   1
 -1   1  -1   1  -1
  0   1   2  -1  -2
 -1   1   1  -1   1
```

**Exact quantum supremum.** (9*sqrt(17)-27)/16

[Upper bound and attainment](PROOF.md).

Run `python verify.py 143` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 143 --extract proof-Y143`.
