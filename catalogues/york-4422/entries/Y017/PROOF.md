# Global upper bound and attainment for Y17
Original complete 25 coefficients: [0, -3, -1, -1, -1, -3, 1, 3, 1, 2, -1, 2, -2, 2, 1, 0, 2, 1, -1, -2, -1, 1, -1, -2, 2].
The upper proof combines the analytic compatibility argument below with the
enclosed exact root, Gram-positivity and directed inverse/error calculations.
Witness chart: Full real state (1,s1,s2,s3); exact witness chart_spec.json, 8 physical parameters. Constants and anchors constrain only this witness. See chart_spec.json for its exact constant signs and anchors.
Let x* be the unique zero of the 8 rational gradient equations in the rational
box in selected_root_certificate.json. Set q=f(x*) using the original CH score.
The state (1,s1,s2,s3)/sqrt(1+s1^2+s2^2+s3^2), constant reflections +/-I,
anchor reflections Z and rational reflections R(u) are a legal two-qubit strategy.
The universal upper algebra has ALL original A0,...,A3,B0,...,B3 FREE, subject
only to involution and cross-party commutation. In particular, constants in the
attaining strategy are never substituted in the formal operator coefficients.
Let w be the 97 words in fixed_inputs, W the eight stacked components of two symmetry-related witness actions,
and N the 97-by-89 rational kernel basis with identity nonpivot block. Its
8-by-8 pivot block is interval-verified invertible throughout the root box.
The real symmetric Gram coefficient map A has 1801 rows and 4005 columns,
identified only by adjoint pairs. Let J=[L1,d1L1,...,d8L1,L2,d1L2,...,d8L2] be normalized moments.
Fix x and N(x), varying a separate witness parameter y. Each annihilator is
zero at y=x. Thus each polarized square has zero expectation and first
derivative there, proving A(x)^T J(x)=0 analytically on the chart. The generic
rational test checks conventions, and is not the proof of this identity.
With b=f(x)e_I-c_Bell, each block Js satisfies Js^T b=(0,-grad f),
hence the concatenated J satisfies J^T b=0 at x*.
Exact interval LDL gives rank J=18. Directed Neumann arithmetic gives
K=A A^T+J J^T invertible. Thus range A=ker J^T and rank A=1783.
For e=b-A vec(G0), delta=A^T K^(-1)e satisfies A delta=e exactly.
Exact integer Bareiss proves G0-(1/1000000)I>0. The independently checked bound
89 ||A^T||inf ||R||inf ||e||inf / (1-||I-RK||inf) < 1/1000000
therefore proves G=G0+unvec(delta)>0. Consequently
qI-Bell=(N^T w)^dagger G(N^T w)
in the universal bipartite reflection algebra. The upper bound holds in every
dimension and commuting representation. Private binary reflection dilations
also cover binary POVMs. Physical attainment gives Q_fin=Q_sp=Q_com=q.
The exact value is specified by a unique algebraic root and rational function,
not by its displayed decimal. No radical expression or priority is claimed.

The second physical strategy uses the exact full-Bell automorphism embedded in
fixed_inputs.json. Party exchange also swaps the physical state tensor factors.
For its action matrix the implementation omits a fixed SWAP on output vectors;
that orthogonal basis change preserves its kernel and all normalized moments.
The integer coefficient transform proves f2(x)=f1(x) for every chart point,
including all original marginals. Each strategy is normalized separately and
contributes its own full derivative block; no average or averaged jet is used.
For each block, holding N(x) fixed while varying that physical chart proves
A^T Js=0, and Js^T b=(0,-grad fs)=0 at the SAME selected root. The entire range
argument therefore uses all columns of J as written, with separate blocks.
No chart constant is ever substituted in the universal upper-bound word algebra.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `selected_root_certificate.json`. The physical parametrization and contraction are implemented in `family.py`, `independent_root.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 17 --extract Y017-proof`.
