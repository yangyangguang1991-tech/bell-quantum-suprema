# Global upper bound and attainment for Y18

Original 25 coefficients: [0, -4, -1, -2, 0, -2, 1, 2, 1, 1, -1, 3, -2, 2, 1, -1, 2, 1, -2, 0, 0, 1, 1, 1, -2]
Physical chart: psi=(|00>+t|11>)/sqrt(1+t^2); Ai=R(ai), Bj=R(bj), R(u)=((1-u^2)Z+2uX)/(1+u^2)
Exact value: q=f(x*) at the unique root in selected_root_certificate.json.
That file contains the rational f, every gradient-numerator polynomial, all
rational root-box endpoints, and the complete rational root preconditioner.
The selected root is real algebraic; all rational denominators are nonzero.
Its physical state and binary reflections attain f(x*) on two qubits.

Take the exact ordered 97-word vector w in fixed_inputs.json. The only
universal relations used in reducing words are Ai^2=Bj^2=I and [Ai,Bj]=0.
Different Alice measurements do not commute; different Bob measurements do
not commute. Fixed/equal/special measurements in the physical witness are
never imposed on the universal algebra. All 25 original coefficients remain.

The physical action matrix W(x) has four independent pivot columns [0, 87, 70, 39].
Set the nonpivot rows of N(x) to I_93, and its pivot rows to
 -W_pivot(x)^(-1) W_nonpivot(x).
The pivot inverse is defined throughout the certified root box, and WN=0.
Let A(x) map symmetric 93-by-93 Gram coordinates to the complete
adjoint-paired free-word coefficient vector. Real symmetric Grams make the
two oriented coefficients in each adjoint pair equal; checking their sum
is therefore equivalent to checking every oriented coefficient.
Let L(x) be the vector of normalized physical moments and
 J(x)=[L(x), partial_1 L(x), ..., partial_9 L(x)].

For each fixed x, HOLD N(x) FIXED while varying an independent physical y.
Every annihilator r_i=N(x)^T w annihilates the witness at y=x. Its squared
norm, and every real polarized product, have zero expectation and zero first
derivative there, including state-normalization derivatives. Consequently
 A(x)^T J(x)=0
is an analytic identity on this chart. This is not inferred from a single
generic test point, and N(x) is not differentiated in this argument.

For b(x)=f(x)e_I-c_Bell, normalization gives L^T b=0, and
 (partial_i L)^T b=-partial_i f.
All nine derivatives vanish at the selected root, so J(x*)^T b(x*)=0.
The exact interval check certifies K=AA^T+JJ^T invertible by a fixed dyadic
R with d=||I-RK||_infinity<1. Because A^T J=0, range(A)=ker(J^T).
Thus e=b-A vec(G0) lies in range(A), and the exact algebraic correction
 delta=A^T K^(-1)e,  G=G0+unvec(delta)
satisfies A delta=e. This yields the exact universal identity
 q I-Bell = (N^T w)^dagger G (N^T w).
G0 is defined by its frozen exact rational entries, independently of how
they were discovered. Full exact Bareiss principal minors prove G0-eta I>0.
The separate exact interval and outward IEEE checks prove
 93 ||A^T||_infinity ||R||_infinity ||e||_infinity/(1-d) < eta.
The left side bounds ||unvec(delta)||_operator, so G is strictly positive.

This is an algebraic sum of squares in the universal cross-commuting
reflection algebra, valid in arbitrary Hilbert-space dimension. Binary
POVMs are covered by private-ancilla reflection dilations preserving all
one-party and bipartite terms. Together with the explicit finite witness,
 Q_fin(Y18) = Q_sp(Y18) = Q_com(Y18) = q.
The width of the root's decimal enclosure is not an optimization gap.
No radical expression, minimal polynomial, cyclic-rigidity theorem, or
worldwide priority is asserted by this certificate.
The analytic compatibility argument above and the enclosed exact root,
Gram-positivity and directed inverse/error calculations are all parts of the proof.
The generic-point convention check does not replace the analytic argument.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `selected_root_certificate.json`. The physical parametrization and contraction are implemented in `independent_root.py`, `replay_selected_root_fixed.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 18 --extract Y018-proof`.
