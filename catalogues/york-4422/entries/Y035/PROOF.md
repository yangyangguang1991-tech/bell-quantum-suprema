# Global upper bound and attainment for Y35

Accepted on 2026-10-14 after independent mathematical audit and independent
root, full reference-Gram, complete compatibility and guarded interval checks.
The unrestricted exact value is Q_fin(Y35)=Q_sp(Y35)=Q_com(Y35)=q, with
q=0.773667326298096346249072670119293988857177102081884026734291625... .
Its exact definition is the selected algebraic root construction below;
the decimal display alone is never used to certify the equality.

Let x=(t,a0,a1,a2,a3,b0,b1,b2). Use the real physical two-qubit state
psi(x)=(|00>+t|11>)/sqrt(1+t^2) and reflection matrices
R(u)=((1-u^2)Z+2uX)/(1+u^2).
Alice uses R(a0),...,R(a3), Bob uses R(b0),-I,R(b1),R(b2).
Here Y35 denotes the literal frozen York expression with parties exchanged
(factor 1, shift 0), so the original attaining strategy has Alice 2=-I.
The fixed acceptance verifies all 25 coefficients and 256 deterministic
assignments under this exact party swap. Upper tested operators remain all
eight free reflections: B2=-I is used only to construct the attaining family.
Let f(x) be the party-swapped frozen Y35 expectation. selected_root_certificate.json
gives its rational expression and eight gradient polynomial numerators; the
integer dyadic interval Krawczyk checker certifies a unique root x* in its box.
Thus q=f(x*) is an exact selected algebraic value, not a decimal guess.

Use the frozen 97-word reflection basis w. W(x) is the 4x97 matrix whose
columns are w_i psi(x), with the common state normalization omitted. The pivot
columns 4,33,11,51 are invertible throughout the root box (interval Gaussian
elimination in replay_interval_face_fixed.py proves no pivot interval contains 0).
For the other 93 columns define N(x) with one unit entry and four pivot entries
-W_pivot(x)^-1 W_column(x). This gives W(x)N(x)=0 exactly, as a rational identity.
Write r=N^T w. Define A(x): R^4371 -> R^1801 to be the exact coefficient map
G -> r^dagger G r, using real symmetric Gram variables (upper triangles).
Only Ai^2=Bj^2=I and cross-party commutation reduce words; adjoint word pairs
are grouped. A real symmetric Gram produces equal adjoint coefficients, so
zero paired coefficient is equivalent to zero oriented coefficient.

For each of the 1801 word classes let L(x) be its real expectation under the
physical strategy. Let J(x)=[L,partial_t L,...,partial_b2 L]. Then
A(x)^T J(x)=0 EXACTLY FOR EVERY x in the box: each column polynomial of A is
a square or a real symmetrized product of r_i. At y=x, r_i(x)psi(y)=0. Holding
the coefficients N(x) fixed while differentiating y, both its expectation
and its first derivatives vanish. This is the usual first-derivative identity
for a function with a zero squared vector norm; it applies to off-diagonal
symmetrized products by polarization. Derivatives of the normalized state
also vanish because the undifferentiated r_i psi is zero.

Let b(x) be the coefficient vector of f(x)I-Y35. Then L^T b=0 for every x,
and (partial_k L)^T b=-partial_k f(x), since L_I=1 and partial_k L_I=0.
Therefore J(x*)^T b(x*)=0 at the certified stationary root.

The interval family checker encloses every entry of A(x),J(x) throughout the
box using 1024-bit integer-only outward dyadic arithmetic. The independent
linear checker encloses I-RK(x), where K=A A^T+J J^T and R is merely a frozen
dyadic numerical preconditioner. After every scalar multiply/add/subtract,
its IEEE binary64 result is enlarged by one adjacent representable value in
each required outward direction. It proves ||I-RK(x)||_infinity<1/2 uniformly.
Thus K(x) is invertible. K is a sum of two real PSD matrices, hence positive.
Its two ranges are orthogonal because A^T J=0; their direct sum is all R^1801.
Every vector orthogonal to range J therefore belongs to range A.

Fix the rational dyadic symmetric 93x93 matrix G0 frozen in fixed_inputs.json.
Its construction used numerical projection during discovery; the accepted
proof uses only the explicit frozen rational matrix and its positivity check.
Exact Bareiss positivity proves G0-eta I>0 for eta=10^-5. The residual
e=b(x*)-A(x*)vec(G0) is orthogonal to range J, hence belongs to range A.
Since K preserves these orthogonal ranges, y=K^-1 e belongs to range A and
A A^T y=e. Thus delta_g=A^T K^-1 e EXACTLY solves A delta_g=e.
Define G=G0+unvec(delta_g). Then r^dagger G r=q I-Y35 as a full free-reflection
operator identity. It is not an approximate repaired decimal identity.

The exact certificate bounds give ||K^-1||_infinity <= ||R||_infinity/(1-d),
where d is the independently certified Neumann residual. They also bound the
actual transpose-map row sums and ||e||_infinity. Hence
||unvec(delta_g)||_op <= 93 ||delta_g||_infinity
 <=93 ||A^T||_infinity ||R||_infinity ||e||_infinity/(1-d) < eta.
All scalar inequalities are checked by Fraction integer arithmetic in
replay_final_bounds_fixed.py. Therefore G>0.

This exact SOS proves Y35<=q in every commuting-operator representation and
arbitrary dimension. The selected real two-qubit strategy has expectation
exactly q by definition. Therefore Q_fin(Y35)=Q_sp(Y35)=Q_com(Y35)=q.
This includes arbitrary binary POVMs: simultaneous local reflection
dilations on a private ancilla at each party preserve the Bell terms and
cross-party commutation, so the same upper bound applies. The finite
two-qubit witness already attains the bound.

The maximum PSD Gram rank in the specified 97-word basis is exactly 93.
Every optimal Gram H must have WH=0 by saturation on the attaining strategy,
so rank(H)<=97-rank(W)=93; N G N^T is a rank 93 attaining Gram.

The original Alice second setting is deterministic minus at every optimizer
on its state support. With gamma=9*10^-6 the reduced-Gram margin gives
qI-Y35 >= gamma/2*(B2+I)^2 in swapped party labels, hence
p_Alice2(+)<=epsilon/(2*gamma). Its probability exponent 1 is sharp, as
certified in deterministic_setting_corollary.txt. This is a state-supported
measurement relation, not a fixed-operator hypothesis in the upper proof.

Scope: this proof does not assert a short minimal polynomial, radicals,
uniqueness of all maximizing strategies, or worldwide priority. The analytic
cokernel/range argument is given above and in lemmas/gram_correction_argument.txt.
Selected root certification alone would NOT imply global optimality; the full
SOS compatibility and positivity proof supplies the additional argument.
The exact inputs and independent checkers are bound by
fixed_acceptance_manifest.json. Verification reads frozen rational inputs and
does not optimize a strategy or recompute a numerical Gram/preconditioner.

## Physical realization and literal score

The witness uses the isolated real algebraic parameters specified in `selected_root_certificate.json`. The physical parametrization and contraction are implemented in `independent_root.py`, `replay_selected_root_fixed.py`. Use the designated isolated root, rather than rounded coordinates, in the ranks and charts specified above. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 35 --extract Y035-proof`.
