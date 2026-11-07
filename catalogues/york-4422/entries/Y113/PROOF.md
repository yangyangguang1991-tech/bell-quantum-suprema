# Global upper bound and attainment for Y113

All 25 coefficients belong to York entry Y113; original_york_4422_CG.json contains that single row. Local bound zero
and facet rank are independently verified on all 256 deterministic strategies.
Let x* be the unique root of all eighteen partial derivatives of the complete
original probability function f in the rational box selected_root_certificate.json.
The rational family is the state vec(diag(1,s1,s2)) divided by its positive norm,
with eight independent rank-one or rank-two qutrit projectors. Each projector is
vv^T/(v^T v), or its complement, with one fixed coordinate of v equal to 1 and
two independent real coordinates. These denominator norms are strictly positive.
The root certificate specifies eighteen exact numerator/denominator polynomial
equations, strict interval Krawczyk inclusion and contraction. Thus x* and q=f(x*)
are precisely selected real algebraic quantities. Printed value enclosures locate
q; their width is not an optimization gap.

A second physical strategy applies the full Bell automorphism frozen in
fixed_inputs.json. Exact integer coefficient comparison includes the constant,
all eight marginals and all sixteen joint terms; it proves f2(x)=f1(x) on the
entire physical chart. This automorphism swaps parties as well as relabelling
settings and signs. On the diagonal Schmidt state the tensor SWAP fixes the
state. The transformed free-word representation differs from a tensor-convention
physical strategy only by that fixed unitary row permutation. No unjustified
same-party commutation is introduced by the party exchange.

The 145 free reflection words comprise I, single generators, A_i B_j, ordered
A_i A_k and B_j B_l (unequal indices), and both A_i B_j B_l and A_i A_k B_j.
The universal algebra uses only A_i^2=B_j^2=I and [A_i,B_j]=0. None of the
attaining-strategy rank, dimension or special measurement relations is imposed
on this algebra. Real symmetric Grams are expanded into 3385 adjoint-paired
normal words; self-adjointness makes this an identity of all 6481 oriented
words, without using cyclic trace equivalence.

Stack the two nine-component physical action matrices into W(x), with 18 rows.
The actual 18 frozen pivot columns are proved invertible throughout the root
box. Its kernel basis N(x), with identity at the other 127 indices, is a rational
145 by 127 matrix and satisfies W(x)N(x)=0. Let A(x) be the 3385 by 8128 map
from the independent entries of a real symmetric 127 by 127 Gram to the paired
coefficients of (N^T w)^* G (N^T w).

For each strategy s, let L_s be its separately normalized physical moments.
Use all 38 columns J=[L_1,d_1 L_1,...,d_18 L_1,L_2,d_1 L_2,...,d_18 L_2].
For fixed x keep N(x) fixed and vary an independent physical argument y in each
strategy. At y=x every residual annihilates its state, so every polarized square
has zero value and first derivative. Hence A(x)^T J(x)=0 identically on this
chart. Exact generic tests supplement, rather than replace, this argument.
For b=f1(x)e_I-c_Bell, J_s^T b=(0,-grad f_s); both blocks vanish at x* because
f2=f1 and all eighteen derivatives vanish there.

Exact interval arithmetic proves rank J=38, while the guarded directed Neumann
test proves K=A A^T+J J^T invertible. Consequently range A=ker J^T. With the
frozen rational reference Gram G0 set e=b-A vec(G0), delta=A^T K^(-1)e, and
G=G0+unvec(delta). Then A delta=e exactly. Integer Bareiss arithmetic proves
G0-eta I positive definite for the frozen positive eta. The exact rational bound
127 ||A^T||inf ||R||inf ||e||inf / (1-||I-RK||inf) < eta
proves G positive definite. Therefore the exact operator identity
       q I-Bell = (N^T w)^* G (N^T w)
holds in every commuting reflection representation, without any dimension
restriction. Private binary-reflection dilations cover binary POVMs as well.
The first explicit real qutrit strategy attains q, so Q_fin=Q_sp=Q_com=q.
No minimum-dimension, radical-expression, rigidity, maximal-rank, or worldwide
priority claim is required. The conclusion is released only after all nine
arithmetic gates, all original-literal checks and input-hash bindings pass.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `selected_root_certificate.json`. The physical parametrization and contraction are implemented in `family.py`, `family_r3.py`, `independent_root.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 113 --extract Y113-proof`.
