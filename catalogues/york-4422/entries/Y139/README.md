# Y139 · J4422^97

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
  0  -7  -2  -1   0
 -3   3   3   1   2
 -1   4  -4   1   1
  0   4   2  -4  -3
 -3   2   1   4  -3
```

**Exact quantum supremum.**

$$
q_* = \frac{-20+z^{\mathsf T}Cz+s x^{\mathsf T}Cx+2t\alpha^{\mathsf T}z}{4}
=1.158362553303224691752726414149406588918831908235\ldots.
$$

The matrix $C$, vector $\alpha$, polynomial equations, and rational isolating box defining $(x,z,s,t)$ are specified completely in [PROOF.md](PROOF.md). The displayed decimal is not the definition. The finite-dimensional, spatial, and commuting-operator suprema all equal $q_*$, and the value is attained by the explicit two-qubit state and measurements given there.

[Global upper bound and attainment](PROOF.md) · [Original coefficients](definition.json) · [Certificate descriptor](proof.json)

From the root of this York catalogue, run `python -B verify.py 139`. To read the uncompressed mathematical inputs, run `python -B verify.py 139 --extract Y139-proof`, choosing a destination that does not already exist. The included proof archive contains the exact algebraic identities, rational data, interval bounds, and independent attainment calculation. No TeX document is required.
