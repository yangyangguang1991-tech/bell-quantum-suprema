# Global upper bound and attainment for Y73

All 25 coefficients belong to York entry Y73; original_york_4422_CG.json contains that single row. The
independent literal verifier checks all 256 local strategies and facet rank.
The exact value is q=f(x*) where x* is the unique root in the specified rational
box of all eighteen partial derivatives of the complete probability function f.
The attaining real qutrit family is vec(diag(1,s1,s2)) normalized by its positive
norm. Each of eight projectors is vv^T/(v^T v), or its complement, with one fixed
coordinate equal to 1 and two independent coordinates. Projection ranks, poles,
ordered variables and all rational expressions are given explicitly. All chart
denominators are positive. Exact interval Krawczyk inclusion and contraction
prove the selected root exists and is unique. The decimal enclosure locates an
exact algebraic number; its width is not an optimization gap.

The universal 145-word reflection basis comprises I, all single generators,
A_i B_j, ordered unequal A_i A_k and B_j B_l, and both A_i B_j B_l and A_i A_k B_j.
Only A_i^2=B_j^2=I and [A_i,B_j]=0 reduce free words. Dimension, projection rank
and relations of the attaining strategy are never added to this universal
algebra. The 3385 adjoint-paired classes cover all 6481 oriented words without
cyclic trace equivalence.

Let W(x) have the nine physical action coordinates of these 145 words. Exact
interval inversion proves the actual nine frozen pivot columns form an
invertible matrix throughout the selected root box. Thus N(x), with identity
in the other 136 positions, is a rational 145 by 136 kernel basis. Let A(x)
map the 9316 independent entries of a real symmetric 136 by 136 Gram to the
3385 paired coefficients of (N^T w)^* G (N^T w).

Let J=[L,d_1 L,...,d_18 L] be the nineteen normalized physical moment columns.
For fixed x, keep N(x) fixed and vary an independent physical argument y. Every
residual annihilates the state at y=x, hence every polarized square has zero
value and first derivative there. This proves A(x)^T J(x)=0 on the whole chart.
Generic exact tests check implementation conventions and do not replace this
analytic argument. For b=f(x)e_I-c_Bell, J^T b=(0,-grad f), which vanishes at x*.

Exact arithmetic proves rank J=19; a guarded directed Neumann bound proves
K=A A^T+J J^T invertible. Therefore range A=ker J^T. Set e=b-A vec(G0),
delta=A^T K^(-1)e, and G=G0+unvec(delta). Then A delta=e exactly. Integer Bareiss
arithmetic proves G0-eta I positive definite for frozen eta>0. The exact bound
136 ||A^T||inf ||R||inf ||e||inf/(1-||I-RK||inf)<eta proves G positive definite.
Consequently q I-Bell=(N^T w)^* G (N^T w) in the universal reflection algebra.
This proves the upper bound in every dimension and in the commuting model;
private binary-reflection dilations cover binary POVMs. The displayed real
qutrit strategy attains q. Thus Q_fin=Q_sp=Q_com=q. There is no additional
minimal-dimension, radical-expression, rigidity, maximal-Gram-rank or worldwide
priority claim. Release requires all nine actual arithmetic gates and bindings.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `selected_root_certificate.json`. The physical parametrization and contraction are implemented in `family.py`, `family_r3.py`, `independent_root.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 73 --extract Y073-proof`.
