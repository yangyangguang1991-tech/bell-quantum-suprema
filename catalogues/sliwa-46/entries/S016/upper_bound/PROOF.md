# S016: complete upper-bound reduction

Let `P(q,x,y,z)` be the distributed eight-dimensional characteristic polynomial. The algebra checker proves that it is even in `q` and writes it as `R(r,x,y,z)` with `r=q²`, where `R` is monic of degree four in `r`. Since the physical Bell matrix is self-adjoint, the roots of `R` are real, nonnegative squared eigenvalues.

Set

```text
rho = (6128+832 sqrt(13))/243,
q_* = sqrt(rho) = 4 sqrt(1149+156 sqrt(13))/27.
```

The field certificate checks the first three shifted elementary coefficients of `R` throughout the cube. It also proves `R(rho,x,y,z)≥0` when `x≥0`. It remains to justify the determinant bound when `x≤0`.

## 1. Equal-overlap slice

On `z=y`, the algebra checker factors

```text
R(r,x,y,y) = small(r,x,y) C(r,x,y),
small = r+8xy²−8x−8y²−8.
```

The root of `small` is `8[(1+x)+(1−x)y²]≤16`. On every boundary edge of the square `(x,y)∈[-1,1]²`, the remaining squared eigenvalues are at most 32. These claims follow from the boundary factorizations verified in `verify_16_algebra.py`.

Suppose the maximum squared eigenvalue on this slice were `r_*>rho>32`. It would occur in the interior. For the fixed value `r_*`, all roots of `C` at every point of the square are at most `r_*`, so `C(r_*,x,y)≥0` everywhere and vanishes at a maximizing point. Thus `C=C_x=C_y=0` there. This stationary argument does not assume differentiability or simplicity of the largest eigenvalue.

Write `C=aa x²+bb x+cc`. The checker proves

```text
aa = −128(y−1)³(y+1) H,
H = r+8y²+16y−8.
```

For an interior `y` and `r>32`, `aa>0` because `H=r+8(y+1)²−16>0`. Therefore `x=−bb/(2aa)`. Substitution gives

```text
C(r,−bb/(2aa),y) = (r−16)² E(r,y)/(8(y−1)H).
```

The denominator is nonzero, so stationarity implies `E=E_y=0`. The exact resultant identity is

```text
resultant_y(E,E_y)
 = 72057594037927936 r²(r−16)^5 (243r²−12256r+117504).
```

For `r>32`, the only possible roots are the roots of the displayed quadratic. Its larger root is precisely `rho`. This contradicts `r_*>rho`, proving the equal-overlap slice bound.

## 2. Unequal overlaps

Use `t=(y+z)/2` and `d=(y−z)²`. The physical domain satisfies

```text
−1≤t≤1,  0≤d≤4(1−|t|)².
```

The exact symmetry and derivative identity checked by the algebra program is

```text
partial_d R(r,x,t+sqrt(d)/2,t−sqrt(d)/2) = (1−x) D(r,x,t,d),
```

where `D` is the distributed derivative polynomial. At `r=rho`, the independent field verifier proves `D≥0` on the whole domain for `−1≤x≤0`, using the two substitutions `t=±v`, `d=4w(1−v)²`. It follows that

```text
R(rho,x,y,z) ≥ R(rho,x,t,t) ≥ 0.
```

Combined with the `x≥0` determinant certificate and the first three shifted elementary coefficients, this proves that every squared Bell eigenvalue is at most `rho`. Consequently `M≤q_* I` throughout the full overlap cube.

## 3. Attainment and model scope

The exact point

```text
x=(1−sqrt(13))/6,
y=z=(5−2sqrt(13))/9
```

is feasible and is a characteristic zero at `q_*`. The entry's explicit normalized state construction proves attainment. The common reflection/POVM/dimension-reduction argument in the [proof guide](../../../docs/PROOF_GUIDE.md) promotes the cube bound to all dimensions and the commuting-operator model.
