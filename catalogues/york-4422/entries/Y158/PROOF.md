# Global upper bound and attainment for Y158

Original complete 25 coefficients: [0, -3, 0, 0, 0, -6, 3, 1, 2, 3, -1, 2, -1, 1, -1, -1, 3, -2, -3, 1, -3, 3, 3, -1, -2].

The local certificate supplies the fixed Gram correction, independent root checks and exact radical identification used below.

Witness chart: Full real state (1,s1,s2,s3); exact witness chart_spec.json, 7 physical parameters. Constants and anchors constrain only this witness. See chart_spec.json for its exact constant signs and anchors.

Let x* be the unique zero of the 7 rational gradient equations in the rational

box in selected_root_certificate.json. Set q=f(x*) using the original CH score.

The state (1,s1,s2,s3)/sqrt(1+s1^2+s2^2+s3^2), constant reflections +/-I,

anchor reflections Z and rational reflections R(u) are a legal two-qubit strategy.

The universal upper algebra has ALL original A0,...,A3,B0,...,B3 FREE, subject

only to involution and cross-party commutation. In particular, constants in the

attaining strategy are NEVER substituted in the formal operator coefficients.

Let w be the 97 words in fixed_inputs, W their 4-component witness actions,

and N the 97-by-93 rational kernel basis with identity nonpivot block. Its

4-by-4 pivot block is interval-verified invertible throughout the root box.

The real symmetric Gram coefficient map A has 1801 rows and 4371 columns,

identified only by adjoint pairs. Let J=[L,d1L,...,d7L] be normalized moments.

Fix x and N(x), varying a separate witness parameter y. Each annihilator is

zero at y=x. Thus each polarized square has zero expectation and first

derivative there, proving A(x)^T J(x)=0 analytically on the chart. The generic

rational test checks conventions, and is not the proof of this identity.

With b=f(x)e_I-c_Bell, J^T b=(0,-grad f), hence J^T b=0 at x*.

Exact interval LDL gives rank J=8. Directed Neumann arithmetic gives

K=A A^T+J J^T invertible. Thus range A=ker J^T and rank A=1793.

For e=b-A vec(G0), delta=A^T K^(-1)e satisfies A delta=e exactly.

Exact integer Bareiss proves G0-(1/100000)I>0. The independently checked bound

93 ||A^T||inf ||R||inf ||e||inf / (1-||I-RK||inf) < 1/100000

therefore proves G=G0+unvec(delta)>0. Consequently

qI-Bell=(N^T w)^dagger G(N^T w)

in the universal bipartite reflection algebra. The upper bound holds in every

dimension and commuting representation. Private binary reflection dilations

also cover binary POVMs. Physical attainment gives Q_fin=Q_sp=Q_com=q.

The isolated-root definition is identified exactly with the radical below. The identification uses all seven gradient equations and strict containment in the same isolating box; it is not inferred from decimal agreement. No priority claim is made.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `selected_root_certificate.json`. The physical parametrization and contraction are implemented in `check_explicit_phi_strategy.py`, `family.py`, `independent_root.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 158 --extract Y158-proof`.

## Exact radical identification and explicit attainment

Put $r=\sqrt{19}$, $h=\sqrt3$ and $p=h(r-4)/3$. In the ordered coordinates of `family.py`, the exact point is

$$x=(p,-p,1,h,-h,-h/3,h/3).$$

The script `check_radical_binding.py` substitutes this point into **all seven** gradient equations and the complete original score using exact arithmetic in $\mathbb Q(\sqrt3,\sqrt{19})$. Every gradient vanishes and

$$f(x)=\frac{3\sqrt{19}-10}{4}.$$

Integer square roots give outward rational enclosures for every coordinate, strictly inside `selected_root_certificate.json`. Uniqueness of the certified root therefore gives $x=x_*$, so the universal upper identity above has exactly this radical as its constant.

A separate attaining strategy uses $|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2$ and the Pauli matrices $X,Z$:

$$
(A_1,A_2,A_3,A_4)=\left(Z,I,\frac{-Z+hX}{2},\frac{-Z-hX}{2}\right),
$$
$$
(B_1,B_2,B_3,B_4)=\left(I,\frac{Z-5hX}{2r},\frac{4Z-hX}{r},\frac{7Z+3hX}{2r}\right).
$$

All eight matrices are self-adjoint reflections. With $P_i=(I+A_i)/2$ and $Q_j=(I+B_j)/2$, direct evaluation of every marginal and joint probability in the original table gives $(3\sqrt{19}-10)/4$. The identity reflections are legal degenerate measurements and constrain only the attaining strategy. `check_explicit_phi_strategy.py` carries out this independent $4\times4$ calculation without importing the chart or SOS algebra. The catalogue command runs the global upper proof, the same-root radical identification and this direct strategy calculation in that order.
