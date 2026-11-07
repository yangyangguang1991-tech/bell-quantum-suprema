# Y74 · AS2

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
 -1  -3   1   0  -1
 -3   2   2   1   1
 -1   1  -2   2   1
  0   1  -1  -2   2
  1   2  -1  -1  -2
```

**Exact quantum supremum.** sqrt(10+sqrt(2))-5/2

Historical exact solution: B. Li, “Exact values of quantum violations in low-dimensional Bell correlation inequalities,” Sections 5.2–5.3, type 4_2. The signed correlation normalization of its value is (4F+10)/10. [Paper](https://arxiv.org/abs/1712.08506).

[Upper bound and attainment](PROOF.md).

Run `python verify.py 74` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 74 --extract proof-Y074`.
