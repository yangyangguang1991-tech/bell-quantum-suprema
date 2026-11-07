# Global upper bound and attainment for Y168

Neither an 8-parameter stationary root nor a numerical Gram alone proves a
global quantum optimum.

1. The literal original 25 CH coefficients are
[0,-2,0,0,0,-6,2,2,2,2,-1,2,-1,1,-1,-1,2,1,-1,-1,-2,2,-1,-1,2].
No normalization is changed. Let x=(h,a,g0,g1,g2,g3,b,c) and use the rational
rank-one/Grassmann family specified in root/family8.py. The exact root x* is
the unique solution of its 8 rational gradient equations inside the rational
box in root/selected_root8.json. Its equations are defined by differentiating
the explicit rational score. Both primary interval differentiation and an
independent symbolic derivative checker isolate the same root. Set q=f(x*).
The real 4-by 4 strategy has ranks A=(1,2,2,2), B=(3,2,2,2) and state proportional
to diag(1,1,h,h). All projections and the state are legal throughout the box.

2. Full stationarity is essential. It is not inferred from the 8 restricted
gradient equations alone. The two explicit involutions in the frozen proof
root/FULL_STATIONARITY_PROOF.txt preserve the full Bell expression. Their
fixed physical manifold has dimension 10:7 measurement coordinates and 3
normalized state coordinates. In parity order its state is diag(C,C^T), with
a real 2-by 2 matrix C. Two independent local orthogonal rotations act by
C->L C R^T and preserve the Bell value. Since 0<h<1 on the certified root box,
the singular values are positive and distinct. Smooth local singular-value
decomposition fixes these two gauge directions, leaving precisely family8.
The full fixed tangent space is therefore covered by 8 family derivatives and
two zero-value gauge derivatives. Averaging an arbitrary physical tangent
over the finite group shows that its Bell differential equals the differential
on this fixed tangent space, and is zero. This proves all 45 independent real
physical first derivatives vanish at x*. The complete geometric argument and
its independent review are included and hash-bound.

3. The actual moment derivatives use the full 45-coordinate physical chart,
not just the 8 restricted derivatives. It has 15 arbitrary real state entries
(the first fixed to 1 before normalization), and 30 arbitrary projector
coordinates with the stated ranks. Its chart is lifted rationally from x*;
all eight projector patch minors are strictly positive on the root box. The
identity reconstructing a projector from its independent pivot columns
proves the lifted chart gives the same physical strategy. Of these 45 actual
derivatives the frozen 33 indices, in their stored order, plus the normalized
moment column form J. Their independence is established by interval LDL,
not inferred from the rank of a numerical matrix.

4. In the universal reflection algebra impose only selfadjointness,
Ai^2=Bj^2=I and[Ai,Bj]=0. The 361 frozen words consist of all 217 reduced cubic
words and 144 AABB quartic words. Only adjacent equal letters within a party
are canceled. Their products give 19765 real adjoint classes. Sixteen specified
degree<=2 action columns of W(x*) are invertible on the entire root box.
Define N by identity on 345 nonpivot rows and minus W_pivot^-1 W_nonpivot on
the pivot rows. Exactly WN=0. The formal polynomials r=N^T w use all eight
universal generators; the physical witness determines only scalar coefficients.

5. For symmetric G let F vec(G) be the coefficient vector of r*G r, with
the correct factor 2 for off-diagonal entries. All terms involving a pivot
word have degree<=6. Thus the 13608 rows of degree>=7 form a constant 0/2
matrix F_H. Each of 59685 Gram coordinates occurs in at most one high row.
Exact independent enumeration finds 5832 groups of size 1 and 7776 of size 2.
Set each first coordinate to minus the sum of its companions. This defines
Z with 46077 columns, F_H Z=0 and ||Z||_infinity=1. The full reference G0
satisfies all these high cancellations exactly. Its low residual includes
ALL 59685 coordinates, including those not selected for correction.

6. For the frozen 8000 selected columns S put A=F_L Z_S. The 6157-by 34 J uses
normalized low-word moments and the 33 selected derivatives from the full 45
physical chart. Freeze N and vary a separate physical strategy y. At y=x*
each r_i psi vanishes. The expectation of every polarized quadratic product
and every first derivative is therefore zero. With F_H Z_S=0 this gives
A^T J=0 exactly. The same argument applies to the full reference polynomial
because its high coefficients vanish. The full stationarity theorem in step 2
gives J^T b=0 for b=coeff[qI-Bell]. Hence e=b-F_L vec(G0) belongs to ker J^T.

7. A strict directed Neumann bound proves K=A A^T+J J^T invertible. Together
with A^T J=0 it implies range A=ker J^T, so e is in range A. A separate exact
interval LDL verifies rank J=34 and rank A=6123. Define
delta=A^T K^-1 e and G=G0+unpack(Z_S delta).
Then A delta=e and F_H Z_S delta=0, giving the FULL universal identity
qI-Bell=r*G r in every one of the 19765 coefficient classes.

8. The exact rational reference satisfies G0-eta I>0 for eta=1/100000000000.
Primary 384-bit integer-only interval LDL and independent exact integer
characteristic-polynomial signs establish this separately. The operator norm
of the correction is at most
345 ||Z_S||_infinity ||A^T||_infinity ||R||_infinity ||e||_infinity
 /(1-||I-RK||_infinity).
All quantities are bounded outward, and exact rational comparison proves
this expression is below eta. Therefore G is positive definite. Optional
numerical refinements are frozen rational data and add no proof assumption.
The final replay never invokes a solver or modifies its fixed inputs.

9. The resulting universal positive identity gives the upper bound in every
commuting-operator model, hence in every finite or infinite tensor-product
dimension. Binary effects are included through local dilation preserving all
marginals and cross-party products. The explicit real 4-by 4 strategy attains q.
Consequently Q_fin(Y168)=Q_sp(Y168)=Q_com(Y168)=q after all gates pass. The
8-variable exact algebraic specification does not assert a short radical or
minimal univariate polynomial, and no worldwide priority claim is made.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `root/selected_root8.json`. The physical parametrization and contraction are implemented in `root/independent_root/replay.py`, `root/replay_root.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 168 --extract Y168-proof`.
