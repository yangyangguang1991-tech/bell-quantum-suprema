# Global upper bound and attainment for Y69

Scope and definition

The original 25 probability coefficients are fixed literally by the archived
York catalogue. R=(0,-2,-1,0,0), and C has rows
(-3,1,1,1,2), (0,1,-1,0,0), (-1,1,1,1,-2), (0,1,1,-1,0).
No affine renormalization is made. All 256 deterministic assignments give
classical maximum zero. The 44 saturating vertices have homogeneous rank 24.

Let t be the unique root of t^8-6t^6+22t^4-30t^2+5 in the rational interval
specified in certificate.json, near 0.438687079877003896586526.
Define
q=(-3t^7+17t^5-63t^3+85t)/16-3/2.
Equivalently q is the unique root in (0.5147829042000097,0.5147829042000098)
of the irreducible polynomial
32q^8+384q^7+1776q^6+3888q^5+3794q^4+732q^3-990q^2-432q-59.
The selected-root binding and resultant are checked by exact rational arithmetic.

Explicit physical attainment

Set u=(1-t^2)/(1+t^2), w=2t/(1+t^2), c=u/w, s=c/(1+2u).
Then u^2+w^2=c^2+s^2=1, and u is the unique root in
(0.67722429877498,0.67722429877499) of 8u^4+8u^3-u^2-4u-1.
For |Phi+> use A=(uZ+wX,X,uZ-wX,Z), B=(cZ+sX,cZ-sX,I,X).
Every operator is a legal self-adjoint reflection. Direct exact substitution
into all 25 original probability terms gives q. B3=I belongs to this attaining
strategy only; it is never imposed on arbitrary competing strategies.

Universal upper bound

The certificate contains 97 reflection words, the sparse 97x85 matrix N,
and every upper-triangular entry of a symmetric 85x85 matrix G in Q(t).
Field coordinates are rational coefficients of 1,t,...,t^7.
Write r=N^T w. The certificate proves
             q I - Bell_Y69 = r^dagger G r,       G > 0.
Word normalization ONLY cancels adjacent repeated same-party letters and
commutes Alice letters past Bob letters. It never commutes distinct letters
of one party and never uses cyclic trace equivalences.
The first checker independently expands all 3457 directed word classes using
integer common-denominator quotient-ring arithmetic. The second checker
uses SymPy ANP arithmetic and checks all 1801 adjoint-paired real classes.
This pairing is lossless for this real symmetric Gram, as the first checker
also independently confirms the complete directed identity.

Positivity is proved twice. First, exact Bareiss leading minors certify
G0-10^-6 I>0 and 768-bit outward rational intervals bound
||G-G0||_op by the maximum absolute row sum, strictly below 10^-6.
Second, direct 1024-bit outward interval LDL of the algebraic G itself
certifies all 85 pivots strictly positive. Neither proof uses floating
eigenvalues as a positivity criterion.

Only A_i^2=B_j^2=I and [A_i,B_j]=0 enter the universal identity. Hence the
bound holds for arbitrary-dimensional commuting reflection models. Separate
private Halmos dilation of Alice and Bob contractions preserves all marginal
and cross-party moments and also covers binary POVMs. Finite two-qubit
attainment proves Q_fin=Q_sp=Q_com=q.

Discovery versus proof

Complex attaining phase families exposed a larger real word-action span.
Numerical facial searches located an interior Gram; exact sparse elimination
over Q(t) then constructed the explicit field entries. No numeric optimizer,
discovery pickle, first-jet range assumption or fitted equality is needed
to replay this certificate. The standard stationary-root/normal-matrix
proof family used elsewhere in this catalogue is not invoked for Y69.
No optimal-strategy uniqueness or globally minimal Hilbert dimension is claimed.

Replay

Python 3.11 or later with SymPy is sufficient. Run run_fixed_acceptance.py.
Its manifest binds every input, checker and this proof before and after
execution. Three checks run: directed identity/attainment/positivity/facet;
independent paired identity/direct algebraic positivity; minimal value
polynomial and unique-root binding. Actual logs are retained.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `certificate.json`. The physical parametrization and contraction are implemented in `check.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 69 --extract Y069-proof`.
