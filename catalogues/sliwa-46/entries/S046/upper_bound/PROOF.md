# S046: complete boundary and interior proof

The distributed full characteristic polynomial is `P(q,x,y,z)`. The positive candidate `q_*` is the unique root above 10 of

```text
25q³−46q²−4788q+15192 = 0,
```

isolated in the rational interval in `certificate_46_reduced.json`. In particular, `q_*>12`.

## 1. The boundary z=1

At `z=1`, Charlie's two reflections coincide. The Bell matrix splits into the sectors `C=c=+I` and `C=c=−I`. Their quartic characteristic polynomials are the `plus` and `minus` polynomials in the branch verifiers. `verify_boundary.py` checks the exact identity

```text
P(q,x,y,1) = plus(q,x,y) minus(q,x,y),
```

and binds the full certificate's rational value interval to the same selected cubic root.

Both branch polynomials are symmetric in `x,y`. Set `u=x+y`, `v=xy`. If `x≠y`, the coordinate map has nonsingular Jacobian. An interior stationary point must then have both derivatives with respect to `u,v` equal to zero.

For the plus branch, the resulting values satisfy `1+u+v=0`, equivalent to `(1+x)(1+y)=0`. For the minus branch they satisfy `1−u+v=0`, equivalent to `(1−x)(1−y)=0`. These are boundary points. Therefore an interior maximum above the boundary bound must have `x=y=t`.

This use of stationarity is valid even for a multiple Bell eigenvalue: at a global largest value `q`, the characteristic polynomial evaluated at that fixed `q` is nonnegative everywhere and has a zero at a maximizing point. Its parameter derivatives therefore vanish at an interior point.

The branch verifiers check all boundary factorizations and the diagonal cubic factorizations. Boundary eigenvalues are at most 10. The remaining linear diagonal factors also have eigenvalues at most 10. For a larger stationary eigenvalue, the cubic and its `t` derivative must vanish.

For the plus branch the exact resultant forces

```text
25q³+98q²−6068q+19736 = 0.
```

The unique root above 10 is below 12, as verified by endpoint signs and positive derivatives on that ray. Hence this branch has value at most 12.

For the minus branch the resultant forces the defining cubic of `q_*`. The same exact sign and monotonicity argument proves that it has a unique root above 10. Thus the minus branch has value at most `q_*`, which is larger than 12. Both Charlie sectors are consequently bounded by `q_*`, and `P(q_*,x,y,1)≥0` for all `x,y`.

## 2. The full overlap cube

For the shifted polynomial `det(tI+(q_*I−M))`, the independent Bernstein checker certifies the first seven elementary coefficients on the whole cube. For the determinant, it writes the polynomial in a Bernstein basis in Charlie's overlap over four adjacent segments.

Every coefficient except the constant coefficient of the first segment is strictly positive throughout the Alice/Bob overlap square, with exact rational interval bounds and complete quadtree covers. The omitted coefficient is exactly the `z=1` determinant established in Section 1. It is nonnegative. Therefore all eight shifted elementary coefficients are nonnegative everywhere, so `q_*I−M` is positive semidefinite by the common characteristic-coefficient criterion.

## 3. Exact attainment

The minus branch has a feasible stationary overlap

```text
t=(25q_*²−4q_*−3612)/4224,  0<t<1.
```

The branch verifier checks the exact characteristic and stationarity identities modulo the cubic. The entry's supplied canonical three-qubit matrices use overlaps `(t,t,1)` and its explicit finite-arithmetic normalized state attains `q_*`. This construction is independently bound to the literal full Bell matrix by the common exact layer.

The full cube upper bound and exact attainment, together with the [dimension/POVM reduction](../../../docs/PROOF_GUIDE.md), establish `Q_fin=Q_sp=Q_com=q_*`.
