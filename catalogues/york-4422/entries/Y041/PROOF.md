# Global upper bound and attainment for Y41

The historical pal_ filename prefix is retained for the pipeline. This proof
uses the successful Alice half-triple 169-word basis, not the unsuccessful
palindromic-triple candidate.

The construction below becomes an accepted global certificate only when all
named verification components pass with the same bound inputs. Numerical
discovery and an isolated physical root alone do not certify optimality.

1. The original 25 probability coefficients are
[-2,-5,-1,-1,0,-5,2,5,3,1,-1,3,-3,1,3,0,1,-2,3,-3,2,2,1,-3,-2].
No coefficient or constant is rescaled. Let x have 33 real coordinates, with
Schmidt vector (1,s1,s2,s3), six rank-two Grassmann projections, one rank-three
Alice projection and one rank-one Bob projection. The complete chart, exact
rational Bell value f(x), and selected rational isolating box are specified in
selected_root_certificate.json. All chart denominators are positive. The
independent root certificate proves a unique stationary point x* in this box,
with nonsingular derivative equations. Define q=f(x*) exactly. This is an
isolated real algebraic definition, not a rounded decimal identification.

2. Work in the universal algebra of eight selfadjoint involutions, imposing
only Ai^2=Bj^2=I and [Ai,Bj]=0. Words are reduced by adjacent identical letters
within each party; no same-party generators are commuted. Let w be the 169
stored words selected from total degree at most three: keep all words with
at most two letters in each party, and pure Alice triples whose first letter
is at most their last letter. The word set need not be closed under adjoint.
Its products w_i* w_j produce 4321 adjoint classes.

3. Let W(x) have columns w_j(x) psi_unnormalized(x), each a real vector of
dimension sixteen. The sixteen specified pivot columns have a square action
matrix V(x) with a certified interval inverse on the whole root box. Define
N(x) by identity on the 153 nonpivot rows and
-V(x)^(-1) W_nonpivot(x) on the pivot rows. Then W(x)N(x)=0 as a rational
identity, independently of stationarity. Put r(x)=N(x)^T w. Only this
construction of scalar coefficients uses the physical witness; the formal
polynomials r retain all eight universal generators.

4. A real symmetric 153 by 153 Gram has 11781 independent entries. Let F(x)
map those entries to the coefficients of r(x)*G r(x), in the real selfadjoint
word basis h_u=(u+u*)/2. Off-diagonal Gram variables have the corresponding
factor two after adjoint merging. Real symmetric expansion justifies this
merging exactly, without imposing an extra word relation.

Let J(x) have 34 columns: the normalized physical moments of these 4321 word
classes, followed by their derivatives in each of the 33 physical coordinates.
The replay constructs both the matrices and first derivatives using exact
outward interval arithmetic. Its only numerical inputs are explicitly frozen
exact rationals and a rational root box.

5. Freeze N(x) and vary a separate physical witness y. Every component of
r(x) psi(x) is zero. Therefore every diagonal square, every real polarized
cross term, and every first derivative of its expectation vanish at y=x.
This proves F(x)^T J(x)=0 identically wherever the pivot inverse exists.

For b(x)=coeff[f(x)I-Bell], keeping f(x) fixed while differentiating the
expectation in y, J(x)^T b(x)=(0,-gradient f(x)). Thus at x*, J^T b=0 exactly.
No numerical closeness is substituted for either of these identities.

6. The jet-rank replay proves rank J=34 by positive interval LDL pivots of
J^T J. The directed normal-map replay proves K=F F^T+J J^T invertible. Because
range F and range J are orthogonal and together span R^4321, rank F=4287 and
range F=ker J^T. In particular b and e=b-Fvec(G0) belong to range F.

7. G0 is an explicitly frozen exact rational matrix. An optional numerical
refinement is retained as an exact rational sum and contributes no assumption
to the final proof. Exact integer principal minors prove
G0-(3/100000000)I is strictly positive. Define, at x=x*,

 delta=F^T K^(-1)(b-Fvec(G0)),   G=G0+unvec(delta).

Since e lies in range F, F delta=e exactly. Hence qI-Bell=r*G r is an exact
identity, not an approximate coefficient fit. Its positivity follows from
the exact rational comparison

 153 ||F^T||_infinity ||R||_infinity ||e||_infinity
       /(1-||I-RK||_infinity) < 3/100000000.

The left-hand side bounds the operator norm of the symmetric Gram correction.
All norms are bounded outward, and the final inequality is rational.

8. After acceptance, the universal positive identity applies in arbitrary
dimension, including commuting operator models. Binary effects can be dilated
on private local ancillas preserving marginals and cross products. The real
four-dimensional bipartite strategy specified by x* attains q. Consequently
Q_fin(Y41)=Q_sp(Y41)=Q_com(Y41)=q. No four-dimensional assumption is imposed
on competing strategies, and no worldwide novelty claim follows from this
internal certificate.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `selected_root_certificate.json`. The physical parametrization and contraction are implemented in `family.py`, `family_r4.py`, `independent_root.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 41 --extract Y041-proof`.
