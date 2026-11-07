# Global upper bound and attainment for Y9

The proof combines the family identities below with exact root isolation,
Gram positivity and a rigorous inverse/error bound. The exact value q is a
rational function of the unique real
root x* isolated by c3_selected_root_certificate.json. Its 11 equations are
denominator*d(numerator)/dx_i - numerator*d(denominator)/dx_i = 0. All literal
25 probability coefficients are retained. The displayed decimal is not the
definition. The root, physical projectors and state give legal real 4x4 attainment.

Let g be the exact order-three signed measurement automorphism in the fixed
input files. In the attaining family, U is the rational 3-cycle permutation
on the first three coordinates, fixing the fourth. For every parameter in
the chart, g(A)=UAU^T, g(B)=UBU^T and (U tensor U)psi=psi. These are rational
identities of the whole family, not unproved numerical symmetries at the root.
The audit checks these identities, the signed word permutation, and its cube.

The 217-word representation splits rationally into invariant and complementary
parts. Their physical action spaces have dimensions 6 and 10. The independent
physical permutation representation proves these upper bounds; exact nonzero
determinants prove that selected physical row subsets inject on each space.
Interval inverses of the selected action pivots then construct annihilator
blocks N0,N1, with 69 and 132 columns. Thus W(x)N_b(x)=0 wherever the selected
action pivots are nonsingular, in particular throughout the certified root box.
Generic covariance also implies W(x)g^k(N_b(x)^T w)=0 for k=0,1,2 on this domain.

For each arbitrary real symmetric positive Gram block G_b, define the SOS
  S_G = (1/3) sum_{k=0}^2 sum_b [g^k(N_b^T w)]^* G_b [g^k(N_b^T w)].
The full Reynolds average is part of the certificate. Consequently no further
complex-structure or commutation condition is imposed on the 132-dimensional
standard block. The universal A_i and B_j in w are free reflections subject
only to A_i^2=B_j^2=I and [A_i,B_j]=0. Covariance constrains only the witness;
it is never a relation imposed on an arbitrary competing quantum strategy.

Let F map the 11193 upper-triangle Gram variables to 2055 averaged invariant
coefficient coordinates. The dual moment coordinates are signed orbit sums.
Let J consist of these moment values and their 11 physical derivatives.
Freeze N at x and vary an independent physical parameter y. Every annihilator
and its transformed copies vanish at y=x, so each polarized square has zero
expectation and first derivative there. Hence F(x)^T J(x)=0 analytically.
For b=q e_I-c_Bell and q=f(x*), the value column gives 0 and the 11 derivative
columns give -grad f(x*)=0. Therefore J(x*)^T b=0 exactly.

The fixed replay proves rank J=12 and invertibility of K=FF^T+JJ^T by an
outward-rounded Neumann bound, so range F=ker J^T. For e=b-F vec(G0), define
  delta=F^T K^-1 e, G=G0+unvec(delta), separately in the two Gram blocks.
Then F delta=e exactly. Exact integer Bareiss proves both blocks of
G0-(1/10000000)I positive. The final exact norm bound
  132 ||F^T||inf ||R||inf ||e||inf /(1-||I-RK||inf) < 1/10000000
proves G positive definite. Thus qI-Bell=S_G in the universal reflection
algebra, certifying the upper bound in all commuting-operator representations.
Binary POVMs are included by private simultaneous reflection dilation; this
preserves cross-party commutation. Legal real 4x4 attainment establishes
Q_fin(Y9)=Q_sp(Y9)=Q_com(Y9)=q. No worldwide priority claim is made.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `c3_selected_root_certificate.json`. The physical parametrization and contraction are implemented in `c3_family.py`, `family_r4.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 9 --extract Y009-proof`.
