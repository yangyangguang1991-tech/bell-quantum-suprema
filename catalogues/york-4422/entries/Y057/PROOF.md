# Global upper bound and attainment for Y57

Unrestricted real-Gram SOS from a complete complex-qubit physical chart

The proof consists of an isolated exact root, its interval-enclosed Gram
coefficient map, a rigorous inverse bound and a strictly positive corrected Gram.
The mathematical arguments and the corresponding exact checks are given below.

The physical chart has sixteen real parameters. Its state is proportional to
(1,r1+i*i1,r2+i*i2,r3+i*i3); the squared norm is 1+sum of all six state squares.
The reference measurements are A0=B0=Z, A1=R(a1,0), B1=R(b1,0), with the other
four measurements R(x,y)=((1-x^2-y^2)Z+2xX+2yY)/(1+x^2+y^2).
Only this attaining family uses these local coordinate conventions. The global
algebra retains all eight original independent reflection generators.

The Bell score f is rebuilt from all 25 original probability coefficients.
Every denominator is strictly positive. A rational Krawczyk certificate gives
a unique zero x* of all sixteen gradient numerators in a rational isolating
box. The equations are stored as exact factored polynomial numerators and
denominators; expansion into monomials is unnecessary. Isolated real roots of
this rational polynomial system have algebraic coordinates. Define q=f(x*).

Let w be the fixed 97-word column in the universal cross-commuting reflection
algebra: I, singles, all A_i B_j, ordered A_i A_j and B_i B_j, and A_i B_j B_k.
At physical x, W(x) is the complex 4-by-97 matrix with columns w_j psi. Its real
stack WR=(Re W;Im W) is 8-by-97. Eight real pivot columns are certified
invertible throughout the selected box. Solve WR*N=0 with the remaining 89
rows of N forming an identity. N is a real 97-by-89 rational matrix; hence
W*N=0 as a complex identity. Define the real-coefficient residual polynomials
r=N^T w. Both real and imaginary parts of the physical annihilation equation
are enforced; the SOS uses real-coefficient annihilators.

A maps the 4005 coordinates of a real symmetric 89-by-89 Gram to the 1801
adjoint orbits of free-word coefficients. For a real symmetric polynomial,
coefficients of an oriented word and its adjoint are equal. The orbit basis
for a non-self-adjoint word is (u+u*)/2. Equality of orbit coefficients is
therefore equality in the full complex universal star algebra. The reducer
uses only A_i^2=B_j^2=I and cross-party commutation, never same-party
commutation, finite-dimensional identities, or cyclic word equivalence.

Let L consist of the real physical moments of those orbit words, normalized
by the state norm. Let J=[L,d_1 L,...,d_16 L]. For a fixed x, hold N(x) fixed
and vary an independent physical family parameter y. Every residual
r_i(x)psi(y) vanishes at y=x. The real polarized residual products therefore
have zero value and zero first derivative at x. Thus A(x)^T J(x)=0 holds
identically on this rational chart. Neither N nor its pivot choice is
differentiated in this argument. The independent generic-point compatibility
replay checks conventions; this vanishing argument proves the full identity.

For b=f(x)e_I-c_Bell, normalization gives J^T b=(0,-gradient f). At x*, b is
therefore orthogonal to J. Interval arithmetic gives real enclosures of A,J,b
at the same algebraic root. A directed, guarded Neumann test proves
K=AA^T+JJ^T nonsingular. Orthogonal ranges of A and J then span R1801, so
range(A)=ker(J^T) exactly, without relying on numerical ranks. If the separate
17-column interval LDL check passes, rank(A)=1784 and its Gram affine kernel
dimension is 4005-1784=2221. These ranks refer only to this chosen word basis.

Let G0 be the supplied exact dyadic real symmetric reference Gram. Exact
integer Bareiss minors prove G0-eta I positive definite. Write
e=b-A vec(G0), delta=A^T K^-1 e, G=G0+unvec(delta).
As e belongs to range(A), AA^T K^-1 e=e. Hence the exact identity is
             q I-Bell=(N^T w)^* G (N^T w).
The rational bound
 ||unvec(delta)||_op <=89 ||A^T||_infinity ||R||_infinity
                         ||e||_infinity/(1-||I-RK||_infinity)<eta
proves G positive definite. Every coefficient is a well-defined real algebraic
function of the unique selected root, even though its physical witness is
complex. A real positive Gram is positive in complex Hilbert spaces.

Thus the operator upper bound holds in every dimension and every commuting
representation. Standard simultaneous private reflection dilations extend it
from binary projectors to binary POVMs while preserving the bipartite Bell
terms. The explicit two-complex-qubit witness attains q, giving
                     Q_fin=Q_sp=Q_com=q.
This argument does not assume all optimizers are qubits, real, nondegenerate,
coplanar, or covered by the chart. No extra rigidity statement is inferred.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `selected_root_certificate.json`. The physical parametrization and contraction are implemented in `family.py`, `independent_root.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 57 --extract Y057-proof`.
