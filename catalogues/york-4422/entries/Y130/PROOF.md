# Global upper bound and attainment for Y130

Original complete 25 coefficients: [0, -3, 0, -1, -1, -3, 2, 2, 1, 2, 0, 1, -2, 1, 1, -1, 1, 1, 1, -2, 0, 2, -1, -1, -1].

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

Let w be the 97 words in fixed_inputs, W their 4-component witness actions,

and N the 97-by-93 rational kernel basis with identity nonpivot block. Its

4-by-4 pivot block is interval-verified invertible throughout the root box.

The real symmetric Gram coefficient map A has 1801 rows and 4371 columns,

identified only by adjoint pairs. Let J=[L,d1L,...,d8L] be normalized moments.

Fix x and N(x), varying a separate witness parameter y. Each annihilator is

zero at y=x. Thus each polarized square has zero expectation and first

derivative there, proving A(x)^T J(x)=0 analytically on the chart. The generic

rational test checks conventions, and is not the proof of this identity.

With b=f(x)e_I-c_Bell, J^T b=(0,-grad f), hence J^T b=0 at x*.

Exact interval LDL gives rank J=9. Directed Neumann arithmetic gives

K=A A^T+J J^T invertible. Thus range A=ker J^T and rank A=1792.

For e=b-A vec(G0), delta=A^T K^(-1)e satisfies A delta=e exactly.

Exact integer Bareiss proves G0-(1/100000)I>0. The independently checked bound

93 ||A^T||inf ||R||inf ||e||inf / (1-||I-RK||inf) < 1/100000

therefore proves G=G0+unvec(delta)>0. Consequently

qI-Bell=(N^T w)^dagger G(N^T w)

in the universal bipartite reflection algebra. The upper bound holds in every

dimension and commuting representation. Private binary reflection dilations

also cover binary POVMs. Physical attainment gives Q_fin=Q_sp=Q_com=q.

The selected stationary root defines the same exact value as the radical
expression proved below. The printed decimal is not its definition. No
worldwide-priority claim is made.

## Radical value and binding to the selected root

Put

$$
s=\sqrt{17},\qquad u=\sqrt{9-2s},\qquad
v=\frac{u^2-1}{2u},\qquad w=-3v,
$$

where both square roots are positive. The polynomial relation
$u^4-18u^2+13=0$ follows immediately. In the ordered chart coordinates
$(s_1,s_2,s_3,a_0,a_2,a_3,b_0,b_1)$, take

$$
x=(u,u,-1,u,u,v,w,-w).
$$

The eight partial derivatives of the full rational score are formed before
this specialization. Their numerators vanish modulo
$u^4-18u^2+13$, and their denominators are nonzero. To see the reduced
relations explicitly, first set $s_1=s_2=a_0=a_2=u$, $s_3=-1$,
$a_3=v$, $b_0=w$, $b_1=-w$. With
$v=(u^2-1)/(2u)$, the five derivatives in
$s_1,s_2,s_3,a_0,a_2$ vanish. The remaining three vanish when

$$
3u^2+2uw-3=0,\qquad
4u^2w+3uw^2-3u+2w=0.
$$

Substituting $w=3(1-u^2)/(2u)$ makes the first identity immediate and
reduces the second left-hand side to
$3(u^4-18u^2+13)/(4u)=0$. Thus this is stationary in all eight
independent chart directions, not just along a restricted curve.

The literal 25-term CH score at this strategy is

$$
f(x)=-\frac{2w(2u^2w-3u+w)}{(1+u^2)(1+w^2)}
     =\frac{27-9u^2}{32}
     =\frac{9\sqrt{17}-27}{16}.
$$

The added checker `check_radical_binding.py` proves these identities over
$\mathbb Q[u]/(u^4-18u^2+13)$. It also encloses the positive radicals
using integer square roots with 768-bit outward dyadic bounds and places all
eight coordinates strictly inside the existing rational isolating box.
Uniqueness in that box, proved by the root certificate used for the universal
upper bound, identifies this explicit vector with the same $x_*$.
Consequently the radical is the upper certificate's exact value, not a fit
to its decimal enclosure.

For an explicit attaining realization, define

$$
R(t)=\frac{(1-t^2)Z+2tX}{1+t^2},\qquad
|\psi\rangle=\frac{(1,u,u,-1)^{\mathsf T}}{\sqrt{2+2u^2}},
$$

and use the following reflections in the original York order, now numbered
from one to four:

$$
(A_1,A_2,A_3,A_4)=(R(u),Z,R(u),R(v)),\qquad
(B_1,B_2,B_3,B_4)=(R(w),R(-w),Z,-I).
$$

All eight reflections square to the identity. The effects
$P_i=(I+A_i)/2$, $Q_j=(I+B_j)/2$, together with the displayed state,
give the original CH score exactly. In particular, $B_4=-I$ and
$A_1=A_3$ describe this attaining strategy only. They are not relations
in the universal upper-bound algebra.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `selected_root_certificate.json`. The physical parametrization and contraction are implemented in `family.py`, `independent_root.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 130 --extract Y130-proof`.
