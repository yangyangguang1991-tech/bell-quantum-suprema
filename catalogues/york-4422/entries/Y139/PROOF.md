# Global upper bound and attainment for Y139

The traditional label is $J_{4422}^{97}$. This proof uses the full probability table in [definition.json](definition.json), including both sets of marginals, with no change of scale or constant. The exact value is defined below by a polynomial system and a rational isolating box. It is attained on two qubits.

## 1. Bell functional and exact value

For outcome-one projections $P_i,Q_j$, put

$$
F=\sum_{i=1}^4 a_iP_i+\sum_{j=1}^4 b_jQ_j+
\sum_{i,j=1}^4 J_{ij}P_iQ_j,
$$

where

$$
a=(-3,-1,0,-3),\qquad b=(-7,-2,-1,0),\qquad
J=\begin{pmatrix}
3&3&1&2\\
4&-4&1&1\\
4&2&-4&-3\\
2&1&4&-3
\end{pmatrix}.
$$

Enumeration of all $256$ deterministic assignments gives classical maximum zero, with $24$ saturating assignments. Write

$$
P_i=\frac{I+A_i}{2},\qquad Q_j=\frac{I+B_j}{2}.
$$

Then the exact reflection expansion is

$$
H:=4F=-20I+(3,0,-1,-2)\cdot A+(-1,-2,0,-3)\cdot B
+\sum_{i,j=1}^4J_{ij}A_iB_j.
$$

The universal algebra imposes only self-adjointness, $A_i^2=B_j^2=I$, and $[A_i,B_j]=0$. No commutation within either party is imposed. Throughout the variation arguments below, $H$ denotes this operator $4F$; its maximizing energy is $4\mu$ when the maximizing value of $F$ is $\mu$.

Define the symmetric matrix and marginal vector

$$
C=\begin{pmatrix}
1&2&4&3\\
2&4&-4&3\\
4&-4&-1&1\\
3&3&1&-2
\end{pmatrix},\qquad
\alpha=(-2,-1,0,3)^{\mathsf T}.
$$

Use the ten real variables in the fixed order

$$
v=(x_1,x_2,x_3,x_4,z_1,z_2,z_3,z_4,s,t).
$$

They satisfy the ten polynomial equations

$$
\begin{aligned}
x_i^2+z_i^2-1&=0 &&(1\leq i\leq4),\\
s^2+t^2-1&=0,\\
g_i:=s z_i(Cx)_i-x_i(Cz)_i-\alpha_i t x_i&=0
&&(1\leq i\leq4),\\
g_S:=t x^{\mathsf T}Cx-2s\alpha^{\mathsf T}z&=0.
\end{aligned}
$$

Select the unique root in the closed coordinate box of radius $10^{-10}$ about the following exact rational center. Every terminating decimal in this center is interpreted as a rational number.

$$
\begin{aligned}
x^c={}&(-0.455690311956,\ 0.519279288589,\ 0.988103771907,\ -0.521182586082),\\
z^c={}&(0.890138382270,\ 0.854604598889,\ 0.153788607978,\ 0.853445201501),\\
s^c={}&-0.999891403268,\qquad t^c=-0.014737084894.
\end{aligned}
$$

The exact value is

$$
\boxed{q_*=\frac{-20+z^{\mathsf T}Cz+s x^{\mathsf T}Cx+2t\alpha^{\mathsf T}z}{4}.}
$$

Its decimal expansion begins

$$
q_*=1.158362553303224691752726414149406588918831908235235364785756\ldots.
$$

The polynomial system, isolating box, and expression for $q_*$ define the value exactly; the displayed decimal is not the definition. The result is

$$
\boxed{Q_{\mathrm{fin}}(F)=Q_{\mathrm{sp}}(F)=Q_{\mathrm{com}}(F)=q_*.}
$$

Here the first two quantities are suprema over all finite-dimensional and spatial tensor-product strategies. The third is the maximum over commuting-operator strategies. Equality of the corresponding correlation sets is not assumed.

## 2. Root isolation

Let $f$ be the ten-component polynomial system in Section 1. For a rational center $c$, radius $\rho>0$, and rational matrix $R$, define $T(v)=v-Rf(v)$. The following two strict rational interval inequalities imply that $T$ is a contraction and a self-map of the closed box $\mathcal B=[c-\rho,c+\rho]$:

$$
\eta:=\sup_{v\in\mathcal B}\|I-RDf(v)\|_\infty<1,
$$

$$
|(Rf(c))_i|+\rho\sup_{v\in\mathcal B}
\sum_j|(I-RDf(v))_{ij}|<\rho\qquad(1\leq i\leq10).
$$

The first inequality also makes $RDf(c)$, and hence $R$, invertible. Thus the unique fixed point of $T$ is exactly the unique zero of $f$ in the box.

The file `proof/algebraic_candidate_exact_certificate.json` in the certificate archive supplies an exact rational preconditioner $R$, a rational center, and a radius-$10^{-90}$ box. The checker reconstructs all ten equations and their derivatives and verifies strict contraction and self-mapping by rational arithmetic. For the short center and radius $10^{-10}$ displayed in Section 1, the same preconditioner gives the strict bounds

$$
\eta<10^{-6},\qquad
\min_i\left(\rho-|(Rf(c))_i|-\rho\sup_{v\in\mathcal B}
\sum_j|(I-RDf(v))_{ij}|\right)>99\cdot10^{-12}.
$$

The archived radius-$10^{-90}$ box lies strictly inside this short box. Both therefore select the same root. The included `check_short_box.py` executes this exact rational calculation as part of the entry replay.

The separate `independent_attainment.py` starts from the short printed coordinates and uses high-precision Newton iteration only to choose rational data. It then certifies a radius-$10^{-120}$ box by exact rational arithmetic, separately recertifies the archived box, and proves strict inclusion of the smaller box in the archived box. Numerical iteration is not a proof premise. The verifier also rejects three deliberately corrupted root certificates.

## 3. Attaining state, measurements, and literal score

Let

$$
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\qquad p_i=x_iX+z_iZ.
$$

In the ordered basis $|00\rangle,|01\rangle,|10\rangle,|11\rangle$, put

$$
\phi=(1+t,0,0,s)^{\mathsf T},\qquad
\psi=\frac{\phi}{\sqrt{2(1+t)}}.
$$

The local reflections in the original York labeling are

$$
\begin{aligned}
(A_1,A_2,A_3,A_4)&=(p_4,-p_3,p_2,p_1),\\
(B_1,B_2,B_3,B_4)&=(p_2,p_1,p_3,-p_4).
\end{aligned}
$$

Use $P_i=(I+A_i)/2$ on Alice and $Q_j=(I+B_j)/2$ on Bob. The circle equations give $p_i^2=I$ and $\|\phi\|^2=2(1+t)$, while $1+t>0$ throughout the isolating box. These are legitimate projective measurements and a normalized two-qubit state.

For direct probability evaluation, set $P_0=Q_0=I$ and let $D$ be the $5\times5$ probability table in [definition.json](definition.json). The literal score is

$$
\sum_{i,j=0}^4D_{ij}\langle\psi|P_i\otimes Q_j|\psi\rangle=q_*.
$$

This contraction includes the constant and both sets of marginals. Its exact eigenvector verification can be written particularly compactly. Substituting the above measurements into $H=4F$ gives

$$
H=-20I+\sum_i\alpha_i(p_i\otimes I+I\otimes p_i)
+\sum_{i,j}C_{ij}p_i\otimes p_j.
$$

Put $h=4q_*$, $N=s^2+t^2-1$, $a_0=1+t$, $G=\sum_i g_i$, $p=\alpha^{\mathsf T}x$, and $r=(H-hI)\phi$. Direct polynomial expansion, before imposing the root equations, gives

$$
\begin{aligned}
r_{00}&=-s g_S-2(\alpha^{\mathsf T}z)N,\\
r_{11}&=a_0g_S-(x^{\mathsf T}Cx)N,\\
(s-1)r_{01}&=(a_0-s)G+pN,\\
r_{10}&=r_{01}.
\end{aligned}
$$

Since $s-1\neq0$ in the box, these identities imply $H\phi=h\phi$. The independent attainment checker constructs the original probability operator from $4\times4$ Kronecker matrices, verifies the full identity $4F=H$ after the stated signed relabeling, and checks the polynomial identities above. Its exported numerical state and matrices are convenient displays; the isolated algebraic parameters define the exact strategy.

## 4. An unrestricted maximizing state and its symmetry

Let $\mathcal A$ be the universal unital $C^*$-algebra on the eight reflections with cross-party commutation. Its state space is weak-star compact, so $\omega\mapsto\omega(F)$ has a maximizing state with value $\mu$. Since $\mu I-F$ is positive in the universal algebra and has zero expectation at a maximizing state, its GNS vector satisfies

$$
F\Omega=\mu\Omega.
$$

The physical strategy gives $\mu\geq q_*$. The included chain of rational upper certificates, beginning with an unconditional branch certificate, gives

$$
\mu\leq U=
\frac{121989815082782225281427625972136541713010749149232723103495767447}
{105312291668557186697918027683670432318895095400549111254310977536}.
$$

This auxiliary endpoint is proved from the supplied coefficients and certificates; stored numerical approximations are not used as axioms.

The signed exchange

$$
\begin{aligned}
\tau(A_1)&=-B_4,&\tau(A_2)&=-B_3,&\tau(A_3)&=B_1,&\tau(A_4)&=B_2,\\
\tau(B_1)&=A_3,&\tau(B_2)&=A_4,&\tau(B_3)&=-A_2,&\tau(B_4)&=-A_1
\end{aligned}
$$

is an involutive $*$-automorphism preserving the complete Bell polynomial, including the marginals. Average a maximizing state with its pullback under $\tau$, and derive every necessary condition in this averaged state's own GNS representation.

Use real moments $y_w=\operatorname{Re}\omega(w)$. Adjoint identification and the signed exchange reduce $6157$ coordinates to $3105$: there are $53$ positive fixed orbits and $3052$ two-element orbits. This is an expectation reduction at a maximizing state, not a universal relation between words. It does not require the measurements or state to have real matrix entries. The real symmetric moment forms below are necessary for complex strategies as well.

## 5. Seventeen positive forms and the Ward equations

### Ordinary moments and local response

The ordinary moment block uses all $217$ reduced words of total degree at most three. It is positive at every state.

For the Alice field $D_i$ in $H=C_0+\sum_iA_iD_i$, the functional $\ell_i(a)=\omega(aD_i)$ on Alice's algebra is Hermitian. Maximality implies $\ell_i(A_i)=\|\ell_i\|$. Indeed, any self-adjoint contraction $a$ from that algebra can replace $A_i$ after the reflection dilation

$$
\begin{pmatrix}
a&\sqrt{I-a^2}\\
\sqrt{I-a^2}&-a
\end{pmatrix}.
$$

Duplicating the other operators preserves cross-party commutation. The value of the maximizing strategy therefore dominates every such replacement, which establishes the asserted norm equality.

The functional $a\mapsto\ell_i(A_i a)$ has norm equal to its nonnegative value at the identity, and consequently is positive. Hermiticity gives $\ell_i(A_i a)=\ell_i(aA_i)$. Thus

$$
\left[\omega\!\left(D_i(A_i u^*v+u^*vA_i)\right)\right]_{u,v}\succeq0.
$$

The analogous construction applies to Bob. The certificate uses eight such blocks of size $17$, taking their real symmetric forms in the folded coordinates. No finite-dimensional partial trace is used in this argument.

### Joint state and measurement variations

For anti-Hermitian generators $K_i$ from the relevant local algebra, consider the admissible paths

$$
A_i(\varepsilon)=e^{\varepsilon K_i}A_i e^{-\varepsilon K_i},\qquad
\Omega(\varepsilon)=
\frac{\Omega+\varepsilon u\Omega}{\|\Omega+\varepsilon u\Omega\|}.
$$

The state word $u$ may be a joint word and need not be Hermitian. At a global maximum the first derivatives vanish and the negative Hessian is positive. For directions $(u,K),(v,L)$, write $H'_K,H'_L,H''_{KL}$ for the Bell derivatives. Minus twice the mixed Hessian is represented, in expectation at $H\Omega=4\mu\Omega$, by

$$
\begin{aligned}
\mathcal H={}&H(u^*v+v^*u)+(u^*v+v^*u)H
-2(u^*Hv+v^*Hu)\\
&-2(u^*H'_L+H'_Lu+v^*H'_K+H'_Kv)-2H''_{KL}.
\end{aligned}
$$

Hermitian generators multiplied by $i$, together with tangents $iu$, give the imaginary block. Anti-Hermitian commutators give the real block. The selected block sizes are $75,47,83$, with the exact positive rescalings specified in the archive.

The independent checker uses arbitrary-precision Gaussian-integer coefficients to reconstruct the variations. It reconstructs the imaginary block, the full $96$-direction real Hessian, and the selected real blocks. Thirteen explicit gauge columns have identically zero quadratic polynomials before real-adjoint folding. Positivity then forces their mixed products with all other columns to vanish. Together with state and local first variations, these identities give all $366$ selected homogeneous Ward equations.

### Classical auxiliary flags

Adjoin a two-dimensional flag on Alice, duplicate Bob, and use local Alice words $T_i$ in

$$
\widehat A_i=\begin{pmatrix}A_i&0\\0&\sigma_i I\end{pmatrix},\qquad
K_i=\begin{pmatrix}0&T_i\\-T_i^*&0\end{pmatrix},\qquad
\widehat\Omega(\varepsilon)\propto(\Omega,\varepsilon u\Omega).
$$

For $H=C_0+\sum_iA_iD_i$, define

$$
H_\sigma=C_0+\sum_i\sigma_iD_i,\qquad
V=\sum_iD_iT_i^*(\sigma_i I-A_i),
$$

$$
W=\sum_iD_i\left(2\sigma_iT_iT_i^*-T_iT_i^*A_i-A_iT_iT_i^*\right).
$$

The necessary nonnegative second-variation form is

$$
4\langle u\Omega,(4\mu-H_\sigma)u\Omega\rangle
-8\operatorname{Re}\langle u\Omega,V\Omega\rangle
-2\langle\Omega,W\Omega\rangle.
$$

The sign patterns $(+,-,-,-)$ and $(+,+,-,-)$ each give a block of size $117$. The independent checker differentiates the enlarged operator matrices and matches all $27378$ entries of the two maps. The letter $W$ in this display is the flag second derivative; the Ward matrix in Section 6 is denoted $\mathsf W$ to distinguish it.

### Spectral endpoint forms

At $F\Omega=\mu\Omega$, for $T=u^*v$ the endpoint identities are

$$
\omega((F-q_*)T+T(F-q_*))=2(\mu-q_*)\omega(T),
$$

$$
\omega((U-F)T+T(U-F))=2(U-\mu)\omega(T),
$$

$$
\omega\!\left(\frac{q_*+U}{2}(FT+TF)-FTF-q_*UT\right)
=(\mu-q_*)(U-\mu)\omega(T).
$$

Because $q_*\leq\mu\leq U$, the corresponding matrices are positive. Their sizes are $49,49,9$, respectively. The placement of $F$ at the two exterior positions is essential. In particular, the third expression is not replaced by $u^*(F-q_*)(U-F)v$.

## 6. Candidate kernels and exact coefficient correction

In the archive's fixed order, the seventeen block sizes and candidate ranks are

$$
(n_i)=(217,75,\underbrace{17,\ldots,17}_{8},47,83,49,9,49,117,117),
$$

$$
(r_i)=(4,7,\underbrace{4,\ldots,4}_{8},3,9,0,0,4,8,8).
$$

Exact algebraic feature maps and nonvanishing fixed minors establish the kernels and ranks. No floating-point eigenvalue threshold defines a kernel. For the ordinary block the feature map is $w\mapsto w(A,B)\phi$, with pivot words $I,A_2,B_1,A_2B_1$. The joint blocks use exact state and local-unitary gauge decompositions. Each classical flag has eight real features and a strictly positive weighted-square decomposition. The supplied polynomial identities and rational interval calculations establish the kernel inclusions and denominator signs.

These candidate kernels restrict **dual multipliers only**. They are not imposed on arbitrary competing strategies. The candidate's folded moments and all its selected Ward equations are also checked exactly.

For each exact full-row-rank feature matrix $E_i$, whose nullspace is the candidate kernel, define

$$
\Pi_i=I-E_i^{\mathsf T}(E_iE_i^{\mathsf T})^{-1}E_i,\qquad
G_i^0=\Pi_i R_iR_i^{\mathsf T}\Pi_i.
$$

For either zero-rank candidate block, $\Pi_i=I$. The frozen matrices $R_i$ are exact dyadic rational data. The notation $\Pi_i$ avoids confusion with the physical outcome projections $P_i$. No scalar inequality multipliers are used in the final certificate.

Let $\mathcal M_i(y)$ be the symmetric block maps on the $3105$ folded real moments, with $y_0=1$, and let $\mathsf W y=0$ be the scaled homogeneous Ward equations. The adjoint maps use the trace pairing. Write

$$
\mathcal M_i(y)=y_0\mathcal M_i(e_0)+\mathcal L_i(y_{\ne0}),\qquad
\mathsf W y=y_0\mathsf W e_0+\mathsf W_0y_{\ne0}.
$$

Here $\mathcal L_i$ and $\mathsf W_0$ are the restrictions to the $3104$ nonconstant coordinates. This notation makes explicit which maps enter the normal operator.

If $f$ denotes the coefficient vector of $F$, the initial residual is

$$
r=f-q_*e_0+\sum_i\mathcal M_i^*(G_i^0)-\mathsf W^{\mathsf T}\lambda_0.
$$

Define the $3104$-dimensional normal operator and exact correction by

$$
\mathcal N=
\sum_i\mathcal L_i^*\bigl(\Pi_i\mathcal L_i(\,\cdot\,)\Pi_i\bigr)
+\mathsf W_0^{\mathsf T}\mathsf W_0,
\qquad u=\mathcal N^{-1}r_{\ne0},
$$

$$
G_i=G_i^0-\Pi_i\mathcal L_i(u)\Pi_i,\qquad
\lambda=\lambda_0+\mathsf W_0u.
$$

Every nonconstant residual coefficient is exactly zero by $\mathcal N u=r_{\ne0}$. Each corrected $G_i$ is still supported on the exact candidate kernel. Evaluate the remaining residual at the candidate: its Bell score is $q_*$, its Ward equations vanish, and every trace pairing with a kernel-supported multiplier vanishes. The constant residual is therefore exactly zero as well. This proves the exact coefficient identity

$$
q_* y_0-f^{\mathsf T}y
=\sum_i\operatorname{Tr}\!\left(G_i\mathcal M_i(y)\right)
-\lambda^{\mathsf T}\mathsf W y.
$$

The constant-coordinate argument is an exact equality argument, not an interval enclosure that merely contains zero.

To establish the existence and size of the correction, interpret the archived approximate inverse $B$ as an exact dyadic matrix and check by outward interval arithmetic

$$
\eta\geq\|I-B\mathcal N\|_\infty,\qquad \eta<1.
$$

For a dyadic vector $c$, the unique exact solution satisfies

$$
\|\mathcal N^{-1}r_{\ne0}-c\|_\infty
\leq\frac{\|B(r_{\ne0}-\mathcal N c)\|_\infty}{1-\eta}.
$$

For each block take the archived basis matrix $Q_i^{\mathrm{ker}}$ and put $V_i=\Pi_iQ_i^{\mathrm{ker}}$. The number of columns equals the candidate kernel dimension, and

$$
\|V_i^{\mathsf T}V_i-I\|_\infty<1
$$

proves that those columns form a basis of the kernel. A nonsingular dyadic triangular congruence $T_i$ then proves $V_i^{\mathsf T}G_iV_i\succ0$ by

$$
\|T_iV_i^{\mathsf T}G_iV_iT_i^{\mathsf T}-I\|_\infty<1.
$$

Since $G_i=\Pi_iG_i\Pi_i$, positivity on that kernel proves $G_i\succeq0$ on the whole block. These tests cover the complete certified algebraic root box, and reject nonfinite interval values.

## 7. Global upper bound and equality

Take the symmetric maximizing state from Section 4. Every block $\mathcal M_i(y)$ is positive there, and every Ward equation vanishes. The exact coefficient identity from Section 6 gives

$$
q_*-\mu=
\sum_i\operatorname{Tr}\!\left(G_i\mathcal M_i(y)\right)\geq0.
$$

This is an optimizer-conditioned moment argument. It is not an assertion that each variation form is positive at an arbitrary state, nor that the folded words satisfy additional universal operator relations. The maximizing state exists for the universal commuting problem, which is enough to prove $Q_{\mathrm{com}}(F)\leq q_*$.

The explicit two-qubit strategy gives $Q_{\mathrm{fin}}(F)\geq q_*$. Finite-dimensional strategies are spatial, and spatial strategies are commuting. Consequently

$$
q_*\leq Q_{\mathrm{fin}}(F)\leq Q_{\mathrm{sp}}(F)
\leq Q_{\mathrm{com}}(F)\leq q_*.
$$

The upper proof also covers binary POVMs. Self-adjoint contractions obtained from binary effects admit simultaneous local reflection dilations, with independent local ancillas. These preserve all Bell probabilities and cross-party commutation. Thus the equality is unrestricted in local Hilbert-space dimension and in the choice between binary projective measurements and binary POVMs.

## 8. Reproduction from the supplied files

From the root of this York catalogue, run

```console
python -B verify.py 139
```

The entry descriptor [proof.json](proof.json) identifies the archive pieces, their concatenated digest, and the replay commands. The root verifier reconstructs the archive, checks its literal $25$-coefficient table against [definition.json](definition.json), supplies the bundled mathematical libraries, and invokes the archive's `verify.py` and `check_short_box.py`. The former executes the complete global certificate and the separate attainment reconstruction; the latter checks the short root definition printed here. No other catalogue or online source is required. The environment requirements are specified in the catalogue's [manual](../../MANUAL.md).

To inspect the certificate inputs without running the complete computation, use a new destination directory:

```console
python -B verify.py 139 --extract Y139-proof
```

Within the extracted archive:

- `proof/algebraic_candidate_exact_certificate.json` defines the archived root box and rational preconditioner.
- `independent_attainment.py` reconstructs the polynomial system, the state, all eight reflections, and the literal probability score; it also exports numerical state and matrix displays.
- `check_short_box.py` verifies the printed radius-$10^{-10}$ box, its strict contraction and self-map margins, and its containment of the archived box.
- `proof/verify_y139_ancestor_upper_chain.py` supplies the independently checked auxiliary upper endpoint.
- The fold, variation, flag, and kernel checkers reconstruct the signed reduction, necessary positive forms, selected equations, and exact candidate kernels.
- `proof/replay_y139_exact_global_certificate.py` orchestrates the complete upper proof, including the affine correction and interval positivity tests.
- `affine_data/` and `prerequisites/` contain the fixed mathematical inputs for the affine correction and auxiliary upper-bound lemmas.
