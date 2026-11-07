# Y25 · AS1

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
  0  -2   0   0  -1
 -2   1   1   1   1
 -1   1  -1   1   1
  0   1   0   0  -1
  0   1   0  -2   1
```

**Exact quantum supremum.** (5*sqrt(6)-9)/6

Historical exact solution: B. Li, “Exact values of quantum violations in low-dimensional Bell correlation inequalities,” Sections 5.2–5.3, type 4_1. The signed correlation normalization of its value is (4F+6)/6. [Paper](https://arxiv.org/abs/1712.08506).

[Upper bound and attainment](PROOF.md).

Run `python verify.py 25` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 25 --extract proof-Y025`.
