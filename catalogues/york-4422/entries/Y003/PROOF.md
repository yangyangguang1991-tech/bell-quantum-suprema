# Y3: the Collins–Gisin inequality $I_{3322}$

## The York functional and its exact value

Let $P_1,\ldots,P_4$ and $Q_1,\ldots,Q_4$ be the positive-outcome projections of Alice and Bob. Only cross-party commutation, $[P_i,Q_j]=0$, is assumed. The literal probability table in `definition.json` is

$$
C_Y=\begin{pmatrix}
0&-1&-2&0&0\\
-1&1&1&1&0\\
0&-1&1&0&0\\
0&1&1&-1&0\\
0&0&0&0&0
\end{pmatrix}.
$$

Thus the Bell operator, with local bound zero, is

$$
F_Y=-P_1-Q_1-2Q_2
+P_1Q_1+P_1Q_2+P_1Q_3
-P_2Q_1+P_2Q_2
+P_3Q_1+P_3Q_2-P_3Q_3.
$$

The fourth setting of **each** party is absent from this polynomial; both may be set to the identity. There are four settings per party in this entry.

The exact value is the Jacobi path constant $q_*$ defined below. The proof establishes

$$
Q_{\mathrm{fin}}(F_Y)=Q_{\mathrm{sp}}(F_Y)
=Q_{\mathrm{com}}(F_Y)=q_*.
$$

Here $Q_{\mathrm{fin}}$ is the supremum over all finite local dimensions, $Q_{\mathrm{sp}}$ the supremum over spatial tensor-product strategies, and $Q_{\mathrm{com}}$ the supremum over commuting-observer strategies. The approaching finite-dimensional family and the unrestricted commuting upper bound are proved in this entry. The further assertions that no finite-dimensional strategy attains $q_*$ and that a normal infinite-dimensional spatial strategy does attain it are theorems of Coladangelo, cited in [REFERENCES.md](REFERENCES.md). They are not consequences of any finite collection of numerical examples.

## Coordinates used by the enclosed path program

The enclosed source program uses the equivalent three-setting functional

$$
C_S=\begin{pmatrix}
0&-1&-2&0\\
0&1&1&-1\\
-1&1&1&1\\
0&-1&1&0
\end{pmatrix},
$$

in the projection convention of equation (27) of Coladangelo's version 2. Write its projections as $R_1,R_2,R_3$ and $T_1,T_2,T_3$. The exact change of coordinates is

$$
(P_1,P_2,P_3,P_4)=(R_1,R_3,R_2,I),\qquad
(Q_1,Q_2,Q_3,Q_4)=(T_1,T_2,I-T_3,I).
$$

Direct substitution gives $F_Y(P,Q)=F_S(R,T)$, with no rescaling or constant shift. Conversely, any York strategy gives the source strategy

$$
(R_1,R_2,R_3)=(P_1,P_3,P_2),\qquad
(T_1,T_2,T_3)=(Q_1,Q_2,I-Q_3).
$$

The state is unchanged; there is no party exchange. The archive's `transfer.json` and outer archive verifier check this identity including every marginal and constant coefficient. This source convention is distinct from the literal York table displayed above.

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

In the **York** coordinates define

$$
\begin{aligned}
Z_A&=P_1+P_3-I,&X_A&=P_3-P_1,&W_A&=2P_2-I,\\
Z_B&=Q_1+Q_2-I,&X_B&=Q_2-Q_1,&W_B&=I-2Q_3.
\end{aligned}
$$

On each side,

$$
XZ=-ZX,\qquad X^2=I-Z^2,\qquad W^2=I.
$$

Both $Z_A,Z_B$ are self-adjoint contractions and commute with each other. Direct expansion in the literal York polynomial gives

$$
F_Y=Z_AZ_B+\frac{Z_A-Z_B}{2}-I
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
F_Y\preceq d(Z_A,Z_B)+H(Z_A)+H(-Z_B)\preceq qI.
$$

This holds for every $q>q_*$, so $F_Y\preceq q_*I$ in every commuting-observer representation, with no dimension restriction.

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

The **York** projections are explicitly

$$
\begin{aligned}
(P_1,P_2,P_3,P_4)
&=\left(\frac{I+Z_A-X_A}{2},\frac{I+W_A}{2},
\frac{I+Z_A+X_A}{2},I\right),\\
(Q_1,Q_2,Q_3,Q_4)
&=\left(\frac{I+Z_B-X_B}{2},\frac{I+Z_B+X_B}{2},
\frac{I-W_B}{2},I\right).
\end{aligned}
$$

Each displayed operator is a projection. For any nonzero real vector $v=(v_1,\ldots,v_m)$ use the normalized state

$$
|\psi_v\rangle=\frac{\sum_{j=1}^m v_j|j,j\rangle}
{\sqrt{\sum_{j=1}^m v_j^2}}.
$$

Substitution into the full York polynomial, including every marginal, gives

$$
\langle\psi_v|F_Y|\psi_v\rangle
=\frac{\sum_j v_j^2d(c_{j-1},c_j)
+2\sum_{j=1}^{m-1}v_jv_{j+1}a(c_j)}{\sum_jv_j^2}
=\frac{v^{\mathsf T}J_m(c)v}{v^{\mathsf T}v}.
$$

The reflection identity for $d$ supplies the same diagonal entry on the even sites; the alternating exchanges supply exactly the indicated off-diagonal terms. Choosing a top eigenvector gives the reverse inequality $Q_{\mathrm{fin}}\ge q_*$. Together with the upper bound and inclusion of models, this proves the asserted equality of all three suprema.

## Exact rational approximation and reproduction

An explicit approaching sequence uses rational half-angle parameters:

$$
c=\frac{1-z^2}{1+z^2},\qquad
s=\frac{2z}{1+z^2},\qquad z\in\mathbb Q_{\ge0},
$$

also allowing $(c,s)=(-1,0)$. End labels must have $s=0$. Enumerate lengths, rational parameters and nonzero rational trial vectors by increasing height and retain the largest score so far. These parameters are dense in the admissible circle arcs. At fixed length, continuity and the Rayleigh principle show that the record scores tend monotonically to $q_*$. Nonnegative integer trial vectors suffice because $J_m$ has nonnegative off-diagonal entries: replacing $v$ by its componentwise absolute value does not decrease its Rayleigh quotient, and integer rays include all nonnegative rational rays.

Run `python verify.py 3` from the root of this York catalogue. To inspect the source inputs, run `python verify.py 3 --extract proof-Y003`. Inside the extracted archive:

- `row.json` records the full York table;
- `transfer.json` records the signed permutation described above;
- `entries/02-I3322/verify.py` constructs exact rational projections and verifies their score in the explicitly identified source convention;
- `entries/02-I3322/sequence.py` enumerates the rational path family.

For example, from the catalogue root after extraction:

```console
python proof-Y003/entries/02-I3322/verify.py --labels 0,1/2,1,inf --vector 1,2,1 --export source-path.json
python proof-Y003/entries/02-I3322/sequence.py 2
```

The exported matrices are $(R_1,R_2,R_3)$ and $(T_1,T_2,T_3)$; apply the explicit coordinate map in this proof to obtain the four York measurements of each party. `state_diagonal` is the unnormalized Schmidt vector and `state_normalization_squared` its squared norm. Finite program runs verify concrete members of the family. The argument above, rather than those finite tests alone, proves the unrestricted bound and convergence.

[Exact-value and attainment references](REFERENCES.md).
