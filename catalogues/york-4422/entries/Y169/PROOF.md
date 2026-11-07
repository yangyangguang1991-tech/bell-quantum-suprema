# Global upper bound and attainment for Y169

The literal probability coefficient vector, in the order constant, Bob
marginals, then four rows of (Alice marginal, four joint probabilities), is
[0,-1,0,0,0,-3,1,1,1,1,-2,1,-1,1,1,0,1,0,0,-1,-1,1,0,-1,1].
It agrees with row 169 of the frozen 175 catalogue. All 256 deterministic
assignments give maximum 0; the 48 saturating homogeneous vertices have rank 24.

Exact value and attainment.
Let x=(b,u,v,t,h) be the unique zero of the five exact gradient polynomial
numerators in selected_reduced_root.json in that file's rational box, whose
radius is 10^-55 about its listed rational centre. Existence and uniqueness
are proved by a strict Krawczyk inclusion and contraction estimate, using
independently reconstructed direct probabilities and outward rounded rational
interval automatic differentiation. Put q=f(x), with f the literal Bell score.
This is an exact real algebraic definition with a selected isolating box;
q begins 0.28786830453211939337852775922077018130202507411522.
No short radical expression or minimal polynomial is asserted.

Explicitly let r=(1-t^2)/(1+t^2), s=2t/(1+t^2), a=-b*r*v/s and
psi=(|00>+a|11>+b|22>)/sqrt(1+a^2+b^2).
The four Alice vectors are (u,1,v),(-u,1,v),(1,r,s),(0,1,h).
The four Bob vectors are (-u,1,-v),(1,r,-s),(0,1,-h),(u,1,-v).
Normalize every vector. The projectors are its rank-one projector for ranks
[1,1,1,2,2,1,1,2], replacing it by its orthogonal complement when rank 2.
These are legal projective measurements on C^3 tensor C^3. Their direct
probabilities give f(x), hence q is attained without a limiting strategy.

Universal coefficient map.
Only Ai^2=Bj^2=I and [Ai,Bj]=0 are imposed, with Pi=(I+Ai)/2 and
Qj=(I+Bj)/2. The 97 word vector w consists of 1, Ai, Bj, AiBj, ordered
AiAk (i!=k), orderedBjBl(j!=l), andAiBjBl(j!=l). The frozen exact
rational-function matrix N has size 97x56. Its columns are split into four
characters of a verified Z2xZ2 symmetry group, with block sizes 23,15,15,3.
All 224 character identities and all four original Bell invariances are
verified exactly. Expanding (N^T w)^dagger G(N^T w) for real symmetric
character-block Gram matrices defines F with 463 invariant coefficient rows
and 522 independent Gram coordinates. Adjoint word canonicalization and
signed-orbit compression are lossless for this invariant real polynomial.

Exact rank and compatibility.
Let L be the 15 coefficient rows of degree<=2 and H the other 448 rows.
Exact Gaussian elimination over Q(b,u,v,t,h) proves rank(F_H)=294,
including 228 exactly zero reductions. This rational-function upper bound
holds at every point where the original F is defined: all 295-minors are
identically zero rational functions, regardless of whether an intermediate
elimination pivot vanishes at that point. The root-box interval evaluation
checks all original N denominators and a300x300 full-map minor.

Direct symbolic qutrit word evaluation gives WN=0 (all 504 entries).
Fix N at the selected point. Expectation and first physical variations of
the squared norm of N^T w psi therefore annihilate every Gram polynomial.
Use expectation, all 9 real unnormalized state variations, and all 24 real
local rotation variations. Their 34 real moment functionals form J.
The low restriction J_L has rank at least 9, certified by a strict rational
interval 9x9 inverse estimate. Real variations suffice for this real linear
coefficient problem; the final operator identity applies equally on complex
Hilbert spaces.

The literal probability score and all five gradient rational functions are
checked against the root definition. All 18 unconstrained real chart
derivatives reduce exactly to those five gradients. Off-diagonal state
variations are expressed through local rotations using the nonzero Schmidt
square gaps; the remaining chain-rule denominator a_t is also strictly
nonzero throughout the root box. Every one of the 34 contractions of
bvec=qI-Bell is checked exactly. Thus J^T bvec=0 at the selected root.

Now range(F) intersect L is contained in ker(J_L^T), of dimension at most 6.
Hence rankF <= rankF_H+6 <=300. The strict 300-minor gives equality. It
follows that rankF_H=294 and both range(F) intersect L and ker(J_L^T)
have dimension 6, so these spaces agree. Since bvec is supported in L and
has zero J contraction, bvec lies exactly in range(F). This dimension
argument uses exact rank identities and strict minors, never a fitted zero.

Positive exact Gram and upper bound.
The frozen rational block Gram G0 satisfies G0>10^-7 I by strict outward
rounded rational LDL. Let R,S be the certified 300 row/column selections,
C=F[R,S], and e=bvec-F vecG0. Set delta_S=C^-1 e_R and all other
coordinates of delta to zero. RankF=300 and exact range compatibility imply
F delta=e in all 463 rows. Thus the algebraic Gram G=G0+unvec(delta)
satisfies the exact universal identity
 qI-Bell = (N^T w)^dagger G(N^T w).
The strict inverse Neumann bound is below 9.04e-11, the inverse infinity
bound below 91.134, and the total operator correction bound below 6.911e-11.
It follows that G>(10^-7-6.911e-11)I>0.

Consequently Bell<=qI in every Hilbert-space representation of the universal
bipartite reflection algebra, including arbitrary dimension and commuting
operator models. Binary effects can be dilated projectively with separate
local ancillas, preserving cross-party commutation and all Bell probabilities.
The explicit qutrit strategy attains q. Therefore
 Q_fin(Y169)=Q_sp(Y169)=Q_com(Y169)=q.

This is a project-internal certification of the original frozen inequality.
It makes no claim of worldwide historical priority. Discovery solvers,
finite-field rank estimates, and failed symbolic branches are not proof
inputs. The exact-only portable checkers reconstruct the relevant arithmetic
from frozen rational data and reject changed coefficients or failed gates.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `selected_reduced_root.json`. The physical parametrization and contraction are implemented in `independent_interval_ad.py`, `verify_reduced_root.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 169 --extract Y169-proof`.
