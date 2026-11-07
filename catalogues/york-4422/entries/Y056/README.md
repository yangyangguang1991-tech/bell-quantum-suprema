# Y56 · I4422^16

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
 -1  -2   0   0   0
 -2   0   1   1   1
  0   1  -1   1   0
  0   1   1   0  -1
  0   1   0  -2   1
```

**Exact quantum supremum.** sqrt(2)-1

[Upper bound and attainment](PROOF.md).

Run `python verify.py 56` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 56 --extract proof-Y056`.
