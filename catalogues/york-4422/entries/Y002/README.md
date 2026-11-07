# Y2 · CHSH

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
  0   0  -1   0   0
 -1   1   1   0   0
  0  -1   1   0   0
  0   0   0   0   0
  0   0   0   0   0
```

**Exact quantum supremum.** (sqrt(2)-1)/2

Historical strict upper and attainment: B. S. Cirel’son, “Quantum generalizations of Bell’s inequality,” *Letters in Mathematical Physics* 4 (1980), 93–100. [DOI](https://doi.org/10.1007/BF00417500).

[Upper bound and attainment](PROOF.md).

Run `python verify.py 2` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 2 --extract proof-Y002`.
