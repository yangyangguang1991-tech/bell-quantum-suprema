# Global quantum bounds and attaining strategies

## 1. Fixed problem and notation

There are three parties, two measurement settings per party and outcomes in `{-1,+1}`. Write the observables as `A,a; B,b; C,c`. For reflections, each observable is self-adjoint and squares to the identity. Operators from different parties commute; no commutation relation between the two settings of one party is imposed.

Each `functional.json` fixes a literal sum of one-, two- and three-party correlators. Its value is the expectation of that raw expression. The local bound is obtained from the 64 deterministic assignments. Neither subtraction of the local bound nor a further normalization is implicit.

## 2. The arbitrary-dimension reduction

### Binary POVMs

A binary POVM has a self-adjoint contraction `T=E_+−E_-`. Put `S=(I−T²)^(1/2)` and define, on `H⊕H`,

```text
R(T) = [[T,S],[S,−T]].
```

Functional calculus gives `TS=ST`, so `R(T)²=I`. The same embedding `Vψ=(ψ,0)` satisfies `V*R(T_i)V=T_i` for both settings. Give each party its own auxiliary two-dimensional factor. Cross-party commutation is preserved, and the original state with the auxiliary factors in `|000>` preserves every Bell correlator. It therefore suffices to prove the reflection bound.

### Central overlap decomposition

For one party's reflections `R,S`, the self-adjoint contraction `T=(RS+SR)/2` commutes with `R,S` and all other parties' observables. The three such overlap operators are central and admit a joint spectral decomposition. On a fibre they are scalars `x,y,z` in `[-1,1]`.

If `T=tI` and `|t|<1`, define `X=(S−tR)/sqrt(1−t²)`. Direct multiplication gives `X*=X`, `X²=I` and `RX+XR=0`. The operator `X` unitarily identifies the positive and negative eigenspaces of `R`. In that identification,

```text
R = Z ⊗ I_K,
X = [[0,1],[1,0]] ⊗ I_K,
S = [[t,sqrt(1−t²)],[sqrt(1−t²),−t]] ⊗ I_K.
```

An operator commuting with both `R` and `X` must be `I_2⊗D`: commutation with `R` eliminates off-diagonal blocks, and commutation with `X` equates the diagonal blocks. Thus the other parties act only on `K`, and the construction can be repeated.

At `t=±1`, `(S−tR)²=2I−2tT=0`, hence `S=tR`. Decomposing according to `R` gives deterministic one-dimensional branches. They are included by the endpoint matrices above and their corresponding basis vectors.

Every fibre is consequently an amplification of a matrix of size at most `2×2×2`. If every such matrix satisfies `M≤qI`, its direct integral does too. An infinite-dimensional representation need not be a discrete direct sum; the direct-integral argument handles that distinction.

For a vector in a nonseparable space, first restrict to its cyclic subspace under the six reflections. Rational complex linear combinations of finitely many words give a countable dense set, so this reducing subspace is separable. General states can be treated through vector states in a GNS representation. The argument therefore covers the commuting-operator model, including arbitrary dimensions, and in particular spatial and finite-dimensional tensor-product models.

## 3. The canonical Bell matrix

Use `A=B=C=Z=diag(1,−1)` and `a=R(x), b=R(y), c=R(z)`, where

```text
R(t) = [[t,sqrt(1−t²)],[sqrt(1−t²),−t]].
```

Every `sqrt(1−t²)` denotes the nonnegative real square root, which is zero at `t=±1`. This gives a real symmetric eight-dimensional Bell matrix and includes the endpoint deterministic branches. A largest-eigenvalue eigenvector can be chosen real.

For polynomial calculations replace `R(t)` by `[[t,1],[1−t²,−t]]`. In the interior it is similar to the symmetric reflection. The characteristic identities extend to the endpoints as polynomial identities. The exact binding program reconstructs this matrix from the literal expression and computes its complete characteristic polynomial over `Q[x,y,z]`, comparing every coefficient with the entry's distributed polynomial.

Some upper verifiers independently reconstruct the matrix on a complete five-point-per-coordinate grid. Every characteristic coefficient has degree at most four in each overlap. One way to see this is to reduce reflection words in the trace powers, use the Chebyshev trace formula for alternating even words, and apply the Newton identities. Consequently the 125-point interpolation test is an exact polynomial identity test.

## 4. From characteristic coefficients to positivity

Let `M` be real symmetric and write

```text
det(tI+(qI−M)) = t⁸ + e₁t⁷ + ... + e₈.
```

If every `e_k≥0`, the polynomial is strictly positive for every `t>0`. A negative eigenvalue `λ` of `qI−M` would give a positive root `t=−λ`, which is impossible. Thus `qI−M` is positive semidefinite.

The upper certificates establish these inequalities throughout the entire overlap cube. Certain entries use a simpler operator identity or an exact factorization. S16 and S46 require the additional boundary arguments documented in their own `upper_bound/PROOF.md` files.

### Bernstein certificates

After an affine map from a rational box to `[0,1]^n`, the product Bernstein basis is nonnegative and sums to one. Nonnegative exact Bernstein coefficients therefore prove polynomial nonnegativity throughout the box. For algebraic coefficients, outward rational enclosures with nonnegative lower endpoints suffice.

The verifiers check that the complete required family of coefficient indices, named positivity tasks and exterior boxes is present. Some certificate formats additionally require a fixed order and unique records; repeated records in other formats merely repeat the same obligation. The verifiers recompute the coefficient transformations and check that every subdivision tree covers its whole root box. Child boxes may share a boundary. The coverage checks reject gaps, missing leaves and inconsistent splits; formats with explicit leaf paths also check their uniqueness. A coefficient that cannot yet be certified is a reason to subdivide, not a proof that the polynomial is negative.

In the exterior-contact proofs for S19, S22, S39 and S40, the exterior list consists of exactly the six prescribed slabs, and shifted coefficient indices `1,...,7` each occur once. S23 requires the four named tasks `z0_constant`, `e1`, `e2` and `e3` exactly once. These checks concern the complete family of obligations; coverage of an individual tree alone would not establish that every required polynomial or region had been checked.

### Contact boxes

Suppose `p(a)=0`, `grad p(a)=0` exactly, and the Hessian is positive semidefinite on a convex box around `a`. The integral Taylor identity gives

```text
p(a+h) = integral_0^1 (1−s) h^T H_p(a+sh) h ds ≥ 0.
```

Interval Hessian bounds often establish strict diagonal dominance with positive diagonal entries; the symmetric Gershgorin estimate then proves positive definiteness. Complete exterior Bernstein covers handle the remaining domain.

## 5. Exact selected parameters

The parameter files use radicals, uniquely isolated real polynomial roots, or uniquely isolated roots of polynomial systems. A polynomial without a root selector is insufficient.

Univariate selectors are checked by exact root counting and rational intervals. For systems, the certificates supply rational boxes and exact inclusion/contraction checks. For a system `F`, a box `X`, a centre `a` and an invertible rational matrix `C`, let `T(v)=v−CF(v)`. Interval Jacobian bounds give

```text
T(X) ⊂ a−CF(a)+(I−C J_F(X))(X−a).
```

Strict inclusion in `X`, together with a bound below one on the induced norm of `I−C J_F(X)`, makes `T` a contraction of the closed box into itself. Banach's theorem gives the unique root. All acceptance inequalities use rational interval arithmetic. Numerical root refinement is used only for decimal exports.

The input-binding layer compares the exported parameter definitions with the upper certificate's defining polynomial or system, root selectors and overlap formulas. For S40, exact rational comparison binds the upper-value interval to the contact root interval and to the stated centre plus or minus the radius; all contact coordinates, the variable order and the preconditioner dimensions are checked. For S46, the reduced verifier checks the supplied defining polynomial, selected interval and overlap formula without rewriting the certificate. The execution checks in Section 7 preserve these correspondences for the files actually used by the proof programs.

## 6. An explicit exact attaining vector

Let `P(t)=det(tI−M)`, let `q` be the selected exact root, and let its algebraic multiplicity be `m`. Exact algebra verifies the vanishing derivatives below order `m` and a nonzero derivative at order `m`. Divide to obtain

```text
P(t)=(t−q)^m R(t),  R(q)≠0.
```

The spectral theorem gives `R(M)=R(q)Π_q`, because `R` vanishes at every other eigenvalue. Fix the supplied column index `j` and put `v=R(M)e_j`. A strict positive rational interval for `sum(v_i²)` proves `v≠0`. Therefore

```text
psi = v/sqrt(sum(v_i²)),
M psi = q psi.
```

The normalization square root is strictly positive, as certified by the lower bound for `sum(v_i²)`. Every scalar operation in all eight normalized coordinates is listed in `strategy_exact.json` as a finite directed acyclic arithmetic graph. The state is specified constructively; there is no instruction to choose an unspecified kernel vector.

The matrices are legal reflections and this vector is normalized. Its score is exactly `q`. Together with the global upper proof, it establishes

```text
Q_fin = Q_sp = Q_com = q.
```

## 7. Verification layers

The full command checks the literal characteristic identity, exact selected parameters, nonzero normalized state construction, the entry's complete upper proof, an independently rebuilt decimal Bell score, and an independent evaluation of the amplitude graph.

A fixed schedule specifies the required commands for all 46 entries, with 52 upper-verifier invocations in total. The entry configuration must match this schedule, including command order. Before and after each invocation, the execution layer checks the source inputs and the inputs in the temporary execution copy for unchanged contents and the required target bindings. Permitted output files are specified by the verification code for that invocation. If a later proof step consumes a generated intermediate result, that result is then checked as an unchanged input. S46 writes its boundary-verification report separately from its certificate inputs.

Finite decimal displays check exported signs, ordering and values against a separate implementation. The eigen-equation residual in `strategy_numeric.json` is computed from its published rounded amplitudes, observables and `q_display`; `residual_evaluation` identifies these inputs and the working precision. Internal refinement residuals only check the numerical construction. Exact equality is established by the upper certificate and algebraic attainment.

The negative-control programs exercise specified mutations of literals, state graphs, root selectors, proof schedules, target intervals, execution inputs and coverage obligations. Their execution records list the mutations and results. Such controls check particular failure modes; the mathematical proof rests on the stated identities, complete obligations and exact acceptance inequalities.

The trusted computational base is Python's integer/rational arithmetic, the bundled SymPy and mpmath code, and the explicit linear-algebra and interval arguments above. This is a computational proof repository, not a formal proof-kernel development. Full upper runs require assertions to remain enabled.
