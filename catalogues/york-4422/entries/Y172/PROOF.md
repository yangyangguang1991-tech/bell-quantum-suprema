# Global upper bound and attainment for Y172

The proof uses the analytic symmetry and compatibility identities below,
exact root isolation, strict Gram positivity and rigorous inverse/error bounds.
Each of these components is required for the asserted universal upper bound.

The literal original CH coefficients are
[0,-2,0,-1,0,-5,2,2,2,2,0,1,-2,1,0,-1,1,1,1,-2,0,1,0,-1,0].
For x=(t,a0,a1,a2,a3,b0,b1,b2,b3), let
R(u)=[[(1-u^2)/(1+u^2),2u/(1+u^2)],
      [2u/(1+u^2),-(1-u^2)/(1+u^2)]].
The physical witness has state (1,0,0,t)/sqrt(1+t^2), Ai=R(ai), Bj=R(bj).
Write f(x) for the original complete CH score. Its exact root certificate
isolates a unique solution x* of all nine rational gradient equations in the
specified rational box. The exact value is q=f(x*). Independent Schmidt-Pauli
expectations and Fraction intervals verify both the root and its value.

The upper-bound algebra has eight free selfadjoint involutions and only the
cross-party commutation relations. There is an exact order-two automorphism:
flip the sign of A3 (zero-based), exchange B0 with B2, and fix other generators.
It fixes the full Bell polynomial, including marginals and the constant term.
The exhaustive signed-setting/permutation/party-swap scan finds precisely this
automorphism and the identity, but only the checked involution is needed here.

Take all 217 reduced words of total length at most three. The involution gives
two integer character frames of dimensions 114 and 103. The physical word
action W(x) has four rows. Each character frame has four independently certified
invertible action pivots. Setting identity in the nonpivot rows and minus the
pivot inverse times the remaining action columns in the pivot rows defines
rational kernel matrices N. Multiplying by the character frames yields
annihilator vectors r+ and r- of lengths 110 and 99. These are exact rational
formulas on the root box. The witness need not be invariant under the symmetry.

The expansion of r+*G+ r+ + r-*G- r- is real selfadjoint and invariant under the
involution. Merge adjoint pairs using h_w=(w+w*)/2. For each signed two-class
orbit, use the average (c_w+s c_v)/2 as coefficient and the signed moment sum
L(h_w)+s L(h_v) as its dual coordinate. Positive fixed orbits retain one
coordinate; negative fixed orbits vanish by invariance. There are 3124
independent invariant coordinates. The two symmetric Gram blocks together
have 11055 independent entries, defining their exact coefficient map F(x).

J(x) consists of the normalized invariant moment sums and their nine first
physical derivatives. To verify F^T J=0, freeze the annihilator coefficients
at x and vary a second physical witness y. Every annihilator vector is zero
at y=x. Every polarized square therefore has zero expectation and zero first
derivative there. This gives F^T J=0 identically, not merely numerically.
For b(x)=coeff[f(x)I-Bell], the same pairing gives
J^T b=(0,-gradient f(x)); hence J^T b=0 at the isolated stationary root.

Exact interval LDL proves rank J=10. A guarded directed interval computation
proves K=F F^T+J J^T invertible. Therefore range F=ker J^T and rank F=3114.
Let G0 be the two frozen rational blocks. Exact principal minors and an
independent characteristic-polynomial argument prove G0-10^-10 I positive
in each block. Define e=b-Fvec(G0), delta=F^T K^-1 e, and let G be G0 plus the
two symmetric blocks specified by delta. Since e lies in range F, F delta=e
exactly. Thus qI-Bell=r+*G+ r+ + r-*G- r- is an exact polynomial identity.

The directed norm certificates and the final rational comparison prove
110 ||F^T||_infinity ||R||_infinity ||e||_infinity
    /(1-||I-RK||_infinity) < 10^-10.
This bounds the operator norm of each Gram correction. Both corrected blocks
are strictly positive. Numerical refinement steps used to choose G0 have no
logical role: all its entries are frozen exact rationals and are checked anew.

The exact identity and strict positivity proved above give the upper bound for
arbitrary-dimensional tensor and commuting models. Binary effects may be
dilated on private ancillas, preserving all original marginal and cross-party
probabilities. The two-qubit witness at x* attains q. Hence
Q_fin(Y172)=Q_sp(Y172)=Q_com(Y172)=q.
The witness coordinates never impose extra relations on competing strategies.
No claim of a radical expression or worldwide first discovery is implied.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `selected_root_certificate.json`. The physical parametrization and contraction are implemented in `family.py`, `independent_root.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 172 --extract Y172-proof`.
