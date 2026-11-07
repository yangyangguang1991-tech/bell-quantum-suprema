# Y6 · I4322^2

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
  0  -1   0  -1   0
 -2   1   1   0   1
  0   1  -1   1   0
 -1   0   1   1  -1
  0   0   0   0   0
```

**Exact quantum supremum.** (3*sqrt(3)-4)/4

[Upper bound and attainment](PROOF.md).

Run `python verify.py 6` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 6 --extract proof-Y006`.
