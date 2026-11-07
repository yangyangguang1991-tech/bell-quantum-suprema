# Global upper bound and attainment for Y107

Original 25 coefficients: [0, -3, -1, 0, 0, -2, 1, 1, 1, 1, -1, 2, -2, 0, 1, 0, 2, 1, 0, -2, -1, 1, 1, -1, 1]

All quantities are conditional on full fixed-input and independent acceptance.

Let x* be the unique root of all nine original probability-gradient equations in

selected_root_certificate.json. The standard real two-qubit strategy attains

q=f(x*). A second strategy applies the exact full-Bell automorphism in fixed_inputs:

{'party_swap': False, 'alice_permutation': [0, 2, 1, 3], 'alice_signs': [-1, -1, -1, -1], 'bob_permutation': [0, 3, 2, 1], 'bob_signs': [-1, -1, -1, -1]}

The integer coefficient checks prove f_2(x)=f_1(x) for every x, including marginals.

Stack both four-component word-action matrices to W(x) with eight rows.

Actual pivot indices: [0, 1, 38, 50, 66, 24, 62, 41]. Let N be its kernel basis with identity

nonpivot block, of size 97 by 89. The pivot block is verified on the root box.

Each strategy has its OWN normalized moments L_s and nine derivatives. Set

J=[L_1,d_1 L_1,...,d_9 L_1,L_2,d_1 L_2,...,d_9 L_2], with 20 columns.

For fixed x hold N(x) fixed and vary a separate physical parameter y in each

strategy. All annihilators vanish at y=x, so each polarized square has zero value

and first derivative. Hence A(x)^T J(x)=0 as an analytic identity on the chart.

For b=f_1(x)e_I-c_Bell, each block J_s^T b=(0,-grad f_s), which vanishes at x*

since f_2=f_1. This is not inferred from a generic-point check or an averaged state.

The 1801 by 4005 coefficient map A uses only Ai^2=Bj^2=I and cross-party commutation.

Real symmetric Gram entries give adjoint-paired coefficients; no same-party

commutation or special witness relation is imposed in the universal algebra.

Exact interval arithmetic proves rank J=20. A directed Neumann test proves

K=A A^T+J J^T invertible; thus range A=ker J^T and rank A=1781.

For e=b-A vec(G0), delta=A^T K^(-1)e solves A delta=e exactly.

The frozen rational reference matrix satisfies G0-(1/10000000) I>0 by exact

Bareiss arithmetic. The exact perturbation estimate

89||A^T||inf ||R||inf ||e||inf/(1-||I-RK||inf)<1/10000000

therefore proves G=G0+unvec(delta)>0 and

q I-Bell=(N^T w)^dagger G(N^T w).

This identity holds in every cross-party commuting representation, arbitrary

dimension; private reflection dilations cover binary POVMs. The original finite

attaining strategy gives Q_fin=Q_sp=Q_com=q. The selected eight-dimensional action

row space bounds the rank of any feasible 97-word PSD Gram by 89, attained here;

the real symmetric fixed-face affine Gram kernel has dimension 4005-1781=2224.

No cyclic rigidity, radical expression, minimal polynomial or priority is claimed.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `selected_root_certificate.json`. The physical parametrization and contraction are implemented in `independent_root.py`, `replay_selected_root_fixed.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 107 --extract Y107-proof`.
