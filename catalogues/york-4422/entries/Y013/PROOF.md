# Global upper bound and attainment for Y13

1. Original functional and exact value definition.
Use the 25 probability coefficients
[0,-4,-2,-1,0,-4,2,3,1,3,-3,2,-3,3,1,-1,2,2,2,-3,0,3,-1,-3,0].
There is no rescaling or constant translation. Set
R(t)=[[(1-t^2)/(1+t^2),2t/(1+t^2)],
      [2t/(1+t^2),-(1-t^2)/(1+t^2)]].
For x=(s1,s2,s3,a0,a3,b0,b1,b3), the physical witness is
psi=(1,s1,s2,s3)/sqrt(1+s1^2+s2^2+s3^2),
A=(R(a0),-I,Z,R(a3)), B=(R(b0),R(b1),Z,R(b3)).
Let f(x) be the original 25-term score evaluated on this witness.
The exact value q is f(x*) where x* is the unique zero of all eight rational
gradient equations in the rational box in selected_root_certificate.json.
Two independently implemented interval Krawczyk replays establish existence,
uniqueness, nonsingularity and the claimed enclosing interval. All denominators
are nonzero on the box. This specifies an exact real algebraic value, whether
or not a short radical expression or univariate minimal polynomial is known.

2. Universal algebra and the exact symmetry.
The upper-bound algebra has eight free selfadjoint generators satisfying only
A_i^2=B_j^2=I and [A_i,B_j]=0. Same-party generators do not commute in it.
With zero-based indices, p=(2,1,0,3), s=(1,1,1,-1), the map
sigma(A_i)=s_i B_{p_i}, sigma(B_i)=s_i A_{p_i}
is an involutive star automorphism that fixes the full Bell polynomial.
It does not impose any relation on an arbitrary competing strategy.

3. Character annihilators.
Let w be all 217 distinct reduced bipartite words of total length at most 3.
In each party only adjacent identical letters cancel. Fix the order in the
input file. The signed permutation induced by sigma has rational character
frames T_+ and T_-. Each column is e_i for an appropriate fixed word or
e_i +/- s_i e_j for a two-word orbit. The independent audit reconstructs these
frames rather than trusting the stored arrays.
Let W(x) have columns w_j(x) psi_unnormalized(x), a four-component physical
action. In each character space, select the four pivot columns recorded in
the frozen data. Their determinants are certified nonzero throughout the box.
Writing V_epsilon=W T_epsilon, define N_epsilon by identity in the nonpivot
rows and -V_pivot^(-1) V_nonpivot in the pivot rows. Then
U_epsilon=T_epsilon N_epsilon, W U_epsilon=0, and
sigma(U_epsilon^T w)=epsilon U_epsilon^T w
as rational identities wherever the pivot matrix is invertible.
The two vectors r_epsilon=U_epsilon^T w have lengths 107 and 102.

4. The invariant coefficient map and its dual moments.
Expand r_+^dagger G_+ r_+ + r_-^dagger G_- r_- in the universal algebra.
Each real symmetric block produces a sigma-invariant selfadjoint polynomial.
First merge adjoint word pairs; real symmetric coefficients make this exact.
For a signed two-orbit (v,sigma(v)), record the averaged coefficient
(c_v + sign*c_sigma(v))/2. For a positive fixed orbit record its coefficient;
a negative fixed orbit vanishes by invariance. This gives 3105 coordinates.
The linear map F has 11031 symmetric block variables (diagonals once and
off-diagonals with factor two).
The dual moment coordinate is the signed orbit SUM, not its average.
Thus coefficient-moment pairing equals the actual physical expectation.
Let J consist of these normalized moment sums and their eight physical
derivatives. The exact interval implementation recomputes them from the
physical matrices, without treating a numerical Gram as exact data.

5. Exact compatibility; why first derivatives suffice.
Fix x in the box and freeze U_epsilon(x). Vary an independent witness y.
Every r_epsilon(x) annihilates psi(x). Consequently the expectation of each
polarized square and its first y-derivatives vanish at y=x. Hence
F(x)^T J(x)=0 identically. This is an analytic identity, not a conclusion
inferred from finitely many numerical tests.
Let b(x) be the invariant coefficient vector of f(x) I minus Bell, where
f(x) is kept fixed when differentiating the witness expectation in y. Then
J(x)^T b(x)=(0,-partial_1 f(x),...,-partial_8 f(x)).
Therefore J(x*)^T b(x*)=0 by the isolated stationary root equations.
Interval LDL of J^T J proves rank J=9. Directed, guarded arithmetic certifies
K=F F^T+J J^T invertible. It follows that ker F^T=range J and rank F=3096.
Indeed ker F^T contains range J; invertibility of K excludes any additional
vector orthogonal to range J. Thus range F=ker J^T and b lies in range F.

6. An exact positive Gram, not an approximate identity.
The frozen matrices G0 are exact rational numbers (binary64 values converted
to rational numbers). Both G0 blocks minus eta I, eta=1/10^7, are positive
definite by exact integer principal minors and a separate independent check.
Define e=b-F vec(G0), delta=F^T K^(-1)e, and
G=G0+block_unvec(delta), at x=x*.
Because e is orthogonal to J, F delta=e EXACTLY. This proves the operator
identity; there is no residual tolerance in the mathematical conclusion.
The enclosure calculation proves
max_block ||Delta G||_op <=
107 ||F^T||_infinity ||R||_infinity ||e||_infinity /
    (1-||I-RK||_infinity) < eta.
All bounds are outward and converted back to exact rationals for the final
comparison. Hence both exact corrected blocks G are strictly positive.
We have the universal identity
q I - Bell = r_+^dagger G_+ r_+ + r_-^dagger G_- r_- >= 0.

7. Models and conclusion after acceptance.
The operator identity holds in every representation of the universal
bipartite reflection algebra, including infinite-dimensional commuting
models. Binary positive contractions can be dilated to reflections on private
ancillas while preserving all original marginal and cross-party products.
The explicit two-qubit witness reaches q. Consequently
Q_fin(Y13)=Q_sp(Y13)=Q_com(Y13)=q.
The constants and anchors constrain the attaining witness only. They are
never substituted into the universal upper-bound algebra.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `selected_root_certificate.json`. The physical parametrization and contraction are implemented in `family.py`, `independent_root.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 13 --extract Y013-proof`.
