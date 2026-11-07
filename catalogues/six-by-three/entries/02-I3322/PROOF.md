# The Collins--Gisin inequality $I_{3322}$

## Definition and exact quantum supremum

The active probability table is

$$C=\begin{pmatrix}0&-1&-2&0\\0&1&1&-1\\-1&1&1&1\\0&-1&1&0\end{pmatrix}.$$

Let $P_i=(I+A_i)/2$ and $Q_j=(I+B_j)/2$ be the positive-outcome projections. The self-adjoint reflections satisfy $A_i^2=B_j^2=I$ and $[A_i,B_j]=0$; no same-party commutation is assumed. The displayed table means

$$F=C_{00}I+\sum_i C_{i0}P_i+\sum_j C_{0j}Q_j+\sum_{ij}C_{ij}P_iQ_j.$$

Append zero rows or columns to obtain six Alice and three Bob settings. Such padding leaves every quantum supremum unchanged: restriction removes unused settings, and assigning identities supplies the converse extension. The local bound is zero, checked on every deterministic assignment.

Define $q_*$ by the Jacobi path problem below. This entry proves

$$Q_{\mathrm{fin}}(F)=Q_{\mathrm{sp}}(F)=Q_{\mathrm{com}}(F)=q_*.$$

These are respectively the suprema over all finite local dimensions, spatial tensor-product strategies and commuting-operator strategies. The value is specified exactly by a scalar variational characterization, not asserted to be algebraic or expressible by radicals. Both the dimension-independent upper proof and a constructive finite-dimensional approaching sequence are included here. They suffice to prove the equality of suprema without any external certificate.

Finite-dimensional nonattainment and normal infinite-dimensional spatial attainment are additional theorems of Coladangelo, identified precisely in [REFERENCES.md](REFERENCES.md). Their proofs are not reproduced by a finite example calculation or by the enumerating program below. This distinction does not affect the self-contained upper-bound and approximation proof.

The probability convention is equation (27) of Coladangelo's version 2; no relabeling, rescaling or additive shift is needed for the supplied path program.

## An explicit Jacobi variational definition

Put

$$
d(u,v)=uv+\frac{u-v}{2}-1,\qquad
a(v)=\frac{\sqrt{1-v^2}}2.
$$

For an integer $m\ge1$, choose real labels $c_0,\ldots,c_m\in[-1,1]$ with $c_0,c_m\in\{-1,1\}$. Let $J_m(c)$ be the real symmetric tridiagonal matrix with

$$
(J_m)_{jj}=d(c_{j-1},c_j),\qquad
(J_m)_{j,j+1}=(J_m)_{j+1,j}=a(c_j).
$$

Define

$$
q_*:=\sup_{m,c}\lambda_{\max}(J_m(c)).
$$

This is an exact variational definition, not a claim that the constant is algebraic or expressible by radicals. It is finite: $d(u,v)\le0$ on the square and $0\le a(v)\le1/2$, so the row-sum estimate gives $q_*\le1$; a one-site path with labels $(1,1)$ gives $q_*\ge0$.

## The unrestricted upper bound

In the literal coordinates of this entry define

$$
\begin{aligned}
Z_A&=P_1+P_2-I,&X_A&=P_2-P_1,&W_A&=2P_3-I,\\
Z_B&=Q_1+Q_2-I,&X_B&=Q_2-Q_1,&W_B&=2Q_3-I.
\end{aligned}
$$

On each side,

$$
XZ=-ZX,\qquad X^2=I-Z^2,\qquad W^2=I.
$$

Both $Z_A,Z_B$ are self-adjoint contractions and commute with each other. Direct expansion in the literal probability polynomial gives

$$
F=Z_AZ_B+\frac{Z_A-Z_B}{2}-I
+\frac12X_AW_B+\frac12W_AX_B
=d(Z_A,Z_B)+\frac12X_AW_B+\frac12W_AX_B.
$$

Fix $q>q_*$ and set $\delta=q-q_*>0$. We construct a bounded positive Borel function $H$ with

$$
H(u)+H(-v)\le q-d(u,v),\qquad
H(u)H(-u)\ge a(u)^2.
$$

Consider any nonempty finite prefix of labels beginning at $+1$ and ending at $v\in[-1,1]$. Its Jacobi matrix becomes a principal submatrix of an admissible path matrix after appending a terminal label $+1$ or $-1$. Hence its matrix $qI-J$ is at least $\delta I$. Eliminate all coordinates but the last. Its last Schur pivot $p$ is at least $\delta$: equivalently, it is the minimum of the quadratic form of $qI-J$ with the last coordinate fixed at $1$.

Let $p(v)$ be the infimum of these last pivots over all such prefixes. The one-edge prefix gives

$$
\delta\le p(v)\le q-d(1,v).
$$

For each fixed earlier prefix the last pivot is continuous as a function of $v$; therefore the infimum is upper semicontinuous and Borel. Define $u_0(v)=a(v)^2/p(v)$. If a prefix ends at $u$ with last pivot $p$, appending $v$ gives the pivot

$$
q-d(u,v)-\frac{a(u)^2}{p}.
$$

Taking prefixes whose pivots tend to $p(u)$ proves

$$
u_0(u)+p(v)\le q-d(u,v).
$$

Apply the same inequality to $(-v,-u)$, using $d(-v,-u)=d(u,v)$, and average. For

$$
H(u)=\frac{u_0(u)+p(-u)}2
$$

this proves $H(u)+H(-v)\le q-d(u,v)$. Also,

$$
\begin{aligned}
H(u)H(-u)
&\ge\frac14\left(\sqrt{u_0(u)p(u)}
+\sqrt{u_0(-u)p(-u)}\right)^2\\
&=a(u)^2.
\end{aligned}
$$

The bounds on $p$ imply that $H$ is bounded and $H\ge\delta/2$, so its reciprocal is bounded as well.

Let $S=X_AW_B$. Cross-party commutation implies that $S$ is self-adjoint, $SZ_A=-Z_AS$, and $S^2=I-Z_A^2$. The anticommutation identity implies

$$
Sf(Z_A)=f(-Z_A)S
$$

for every bounded Borel function $f$, by spectral calculus. Thus the self-adjoint operator

$$
T=\frac12H(Z_A)^{-1/2}S H(Z_A)^{-1/2}
$$

satisfies

$$
T^2=\frac{I-Z_A^2}{4H(Z_A)H(-Z_A)}\preceq I.
$$

It follows that $S/2\preceq H(Z_A)$. Applying the same argument to $W_AX_B$ and the function $u\mapsto H(-u)$ gives $W_AX_B/2\preceq H(-Z_B)$. Joint spectral calculus for the commuting self-adjoint operators $Z_A,Z_B$ now yields

$$
F\preceq d(Z_A,Z_B)+H(Z_A)+H(-Z_B)\preceq qI.
$$

This holds for every $q>q_*$, so $F\preceq q_*I$ in every commuting-operator representation, with no dimension restriction.

The projection assumption loses no binary-effect strategies. For an effect $0\preceq E\preceq I$, the operator

$$
\Pi(E)=\begin{pmatrix}
E&\sqrt{E(I-E)}\\
\sqrt{E(I-E)}&I-E
\end{pmatrix}
$$

is a projection whose compression to the first ancillary coordinate is $E$. Use a separate two-dimensional ancilla for each measurement, and disjoint sets of ancillas for Alice and Bob. Cross-party commutation is preserved because it holds for the original effects and all their bounded functional calculi. Compression to the common first ancillary coordinates preserves every one-party expectation and every cross-party product expectation. The same upper bound therefore holds for all binary POVMs.

## Explicit finite-dimensional strategies

For a path of length $m$, use the basis $|j\rangle$, $1\le j\le m$, on each local space. Define diagonal matrices by

$$
(Z_A(j),Z_B(j))=
\begin{cases}
(c_{j-1},c_j),&j\text{ odd},\\
(-c_j,-c_{j-1}),&j\text{ even}.
\end{cases}
$$

For every edge $(j,j+1)$ put the symmetric off-diagonal coefficient $\sqrt{1-c_j^2}$ in $X_A$ when $j$ is even, and in $X_B$ when $j$ is odd. All other entries of $X_A,X_B$ are zero. Let $W_A$ exchange the endpoints of every odd edge, and $W_B$ those of every even edge; put the identity on the unpaired basis sites. Edges of a fixed parity are disjoint, so these definitions are unambiguous. They satisfy $XZ=-ZX$, $X^2=I-Z^2$, and $W^2=I$.

The projections are explicitly

$$
\begin{aligned}
(P_1,P_2,P_3)
&=\left(\frac{I+Z_A-X_A}{2},\frac{I+Z_A+X_A}{2},\frac{I+W_A}{2}\right),\\
(Q_1,Q_2,Q_3)
&=\left(\frac{I+Z_B-X_B}{2},\frac{I+Z_B+X_B}{2},\frac{I+W_B}{2}\right).
\end{aligned}
$$

Set $P_4=P_5=P_6=I$ to obtain all six Alice settings.

Each displayed operator is a projection. For any nonzero real vector $v=(v_1,\ldots,v_m)$ use the normalized state

$$
|\psi_v\rangle=\frac{\sum_{j=1}^m v_j|j,j\rangle}
{\sqrt{\sum_{j=1}^m v_j^2}}.
$$

Substitution into the full probability polynomial, including every marginal, gives

$$
\langle\psi_v|F|\psi_v\rangle
=\frac{\sum_j v_j^2d(c_{j-1},c_j)
+2\sum_{j=1}^{m-1}v_jv_{j+1}a(c_j)}{\sum_jv_j^2}
=\frac{v^{\mathsf T}J_m(c)v}{v^{\mathsf T}v}.
$$

The reflection identity for $d$ supplies the same diagonal entry on the even sites; the alternating exchanges supply exactly the indicated off-diagonal terms. Choosing a top eigenvector gives the reverse inequality $Q_{\mathrm{fin}}\ge q_*$. Together with the upper bound and inclusion of models, this proves the asserted equality of all three suprema.


## Exact rational approximation and reproduction

Use rational half-angle parameters

$$c=\frac{1-z^2}{1+z^2},\qquad s=\frac{2z}{1+z^2},\qquad z\in\mathbb Q_{\ge0},$$

also allowing $(c,s)=(-1,0)$. At stage $n$, `sequence.py` enumerates path lengths at most $n$, half-angle numerators and positive denominators at most $n$, all endpoint signs, and nonzero nonnegative integer trial vectors whose maximum coordinate is at most $n$. It selects the largest exact rational score. The sets are nested, so their maxima are nondecreasing. Their union is dense in each fixed-length problem: rational half-angle data are dense on the admissible semicircle, and integer rays exhaust rational rays. Since all Jacobi off-diagonal entries are nonnegative, replacing a real trial vector by its componentwise absolute value cannot decrease its score. Continuity and the Rayleigh principle therefore prove convergence of this deterministic sequence to $q_*$.

Run the complete entry from the repository root:

```console
python -B verify.py 2
```

This checks the exact noncommutative reduction, the stored `example.json`, and 32 rational paths, including their projection identities and literal Bell scores. To construct and export a different exact path:

```console
python -B entries/02-I3322/verify.py --labels 0,1/3,1/2,inf --vector 1,2,1 --export path.json
python -B entries/02-I3322/sequence.py 2
```

`inf` denotes the endpoint $(-1,0)$. `state_diagonal` gives the unnormalized Schmidt coefficients; divide them by the square root of `state_normalization_squared` to obtain the normalized state. The exported three projectors per party are exactly those in this proof; add three identity Alice projectors. All exported entries and scores are rational. Enumeration grows rapidly with the stage. Its finite outputs verify individual constructions; the argument above proves the unrestricted upper bound and convergence.

[Detailed exact-value, dimension and attainment references](REFERENCES.md).
