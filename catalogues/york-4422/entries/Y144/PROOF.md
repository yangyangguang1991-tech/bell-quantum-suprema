# Global upper bound and attainment for Y144

Use the unchanged author York144 probability coefficient row, with local bound 0.
Its Alice marginal vector is (-2, 0, -1, -2), Bob vector (-2, 0, -1, -1),
and joint matrix is [[1, 1, 0, 2], [1, -2, 1, 1], [2, 1, -1, -1], [1, 1, 2, -1]].
The constant probability coefficient is zero. All 256 deterministic assignments
give local maximum 0, with 31 tight vertices of exact homogeneous rank 24.
No party swap, setting deletion or correlator-only normalization is made.
Let x=(t,a0,a1,a2,a3,b0,b1,b2,b3). The physical two-qubit family is
 psi(x)=(|00>+t|11>)/sqrt(1+t^2),
 R(u)=((1-u^2)Z+2uX)/(1+u^2),
 A_i=R(a_i), B_j=R(b_j), i,j=0,...,3.
All eight physical observables vary and none is fixed to an identity.
The expectation f(x) is reconstructed from every original marginal and joint
coefficient. The nine rational gradient numerators and their exact denominator
definitions are frozen in selected_root_certificate.json. A strict rational
Krawczyk contraction certifies a unique zero x* in its explicit rational box.
Define q=f(x*); this is a finite selected algebraic value.

Take the specified 97 reflection words w, all of length at most 3. Their physical
action W(x) on the unnormalized vector (1,0,0,t) has four invertible pivot columns
[24,64,21,66] throughout the root box. Define N(x), of size 97x93, with its nonpivot
rows an identity and pivot rows -W_pivot(x)^-1 W_nonpivot(x). Thus WN=0 exactly,
as rational functions; N has full column rank 93. Set r=N^T w.

The complete coefficient map A(x):R^4371->R^1801 sends a real symmetric 93 Gram
matrix G to r^dagger G r. Reduction uses only A_i^2=B_j^2=I and cross-party
commutation. Real symmetric Gram matrices have equal adjoint-word coefficients;
paired-adjoint orbit coefficients vanish exactly when all oriented coefficients
vanish. No cyclic identification or same-party commutation is used.

Let L(x) be the normalized real physical expectations of these 1801 word orbits.
Let J(x)=[L(x),partial_t L(x),...,partial_b3 L(x)] have 10 columns. Fix x and
differentiate a separate strategy parameter y while keeping N(x) fixed. Every
r_i(x)psi(y) vanishes at y=x. Consequently each square expectation and polarized
real symmetric product has zero value and first derivative there, including
the normalized-state derivative. Therefore A(x)^T J(x)=0 identically wherever
the pivot inverse exists. The function coefficients N(x) are not differentiated
in this identity. This proves all ten normalized moment columns annihilate A.

For b(x)=f(x)e_identity-c_Y144, L^T b=0 and
(partial_k L)^T b=-partial_k f(x), since the identity moment equals 1. Thus
J(x*)^T b(x*)=0 at the certified stationary root.

The fixed family checker encloses all A and J entries in the same root box by
1024-bit outward integer dyadic arithmetic. A frozen dyadic preconditioner R
is used only to certify ||I-RK||_infinity<1/2, where K=AA^T+JJ^T, with outward
binary64 rounding after every scalar arithmetic operation and same-thread IEEE
guards before and after validation. Thus K is nonsingular. Since A^T J=0,
range(A) and range(J) are orthogonal and their direct sum is R^1801.
Every vector orthogonal to range(J) therefore lies in range(A).

Define the reference matrix G0 by all its explicit exact dyadic entries in
fixed_inputs.json, irrespective of its numerical discovery provenance. Exact
integer Bareiss leading minors prove G0-eta I>0 at eta=10^-5. The residual
e=b-A vec(G0) lies in range(A), since J^T b=0 and A^T J=0. K preserves the two
orthogonal ranges, so AA^T K^-1 e=e. The correction
 delta_g=A^T K^-1 e
therefore solves the COMPLETE operator coefficient identity exactly.
G=G0+unvec(delta_g) gives qI-Y144=r^dagger G r, with algebraic real coefficients.

Fraction arithmetic certifies
 ||unvec(delta_g)||_op <=93||A^T||_infinity||R||_infinity||e||_infinity/(1-d)<eta,
where d is the directed Neumann bound. The exact rational correction and
remaining strict spectral margin are computed afresh by
replay_final_bounds_fixed.py and written to implicit_sos_result.json.
No numerical eigenvalue from the discovery process is accepted as a proof.
Thus G>0. This is an exact algebraic
identity and positive Gram, not a fitted or approximate decimal identity.

The full free-reflection SOS proves Y144<=q in arbitrary dimension and every
commuting-operator representation. Private-ancilla reflection dilations cover
binary POVMs while preserving every cross-party Bell term. The selected real
two-qubit witness has score exactly q. Therefore
Q_fin(Y144)=Q_sp(Y144)=Q_com(Y144)=q.

The maximum PSD Gram rank in this specified 97-word basis is 93:
saturation on the witness forces every optimal Gram H to have WH=0, while
the constructed N G N^T has rank 93. Exact rank 10 of J must be certified at
the selected root by positive interval LDL; it is not assumed for all physical parameter values.
In particular a maximally entangled state can have an angle rotation gauge.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `selected_root_certificate.json`. The physical parametrization and contraction are implemented in `independent_root.py`, `replay_selected_root_fixed.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 144 --extract Y144-proof`.
