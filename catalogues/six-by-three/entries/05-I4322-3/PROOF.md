# $I_{4322}^{(3)}$

## Definition and exact value

$$C=\begin{pmatrix}
-3&0&1&1\\
0&1&-1&0\\
0&1&1&-1\\
1&-1&-1&1\\
2&-1&-1&-2
\end{pmatrix},\qquad q=(\sqrt{15}-3)/2.$$

Let $P_i=(I+A_i)/2$ and $Q_j=(I+B_j)/2$ be the positive-outcome projections. The self-adjoint reflections satisfy $A_i^2=B_j^2=I$ and $[A_i,B_j]=0$; no same-party commutation is assumed. The displayed table means

$$F=C_{00}I+\sum_i C_{i0}P_i+\sum_j C_{0j}Q_j+\sum_{ij}C_{ij}P_iQ_j.$$

Append zero rows or columns to obtain six Alice and three Bob settings. Such padding leaves every quantum supremum unchanged: restriction removes unused settings, and assigning identities supplies the converse extension. The local bound is zero, checked on every deterministic assignment.

## Unrestricted upper bound

Set $U=B_1+B_2-B_3$, $V=B_1+B_2+2B_3$ and $T=B_1-B_2$. Exact expansion gives

$$4F=-6I+A_1T+A_2(U+I)+A_3(-U+I)-A_4V,$$

$$U^2+\tfrac12V^2+\tfrac32T^2=9I.$$

The comparison uses two elementary operator facts. If $A$ is a reflection commuting with self-adjoint $T$, joint functional calculus gives $AT\preceq|T|$. For self-adjoint $T_i$ and positive numbers $w_i$, Cauchy--Schwarz on vectors gives

$$\left\|\sum_i |T_i|\xi\right\|^2\le\left(\sum_iw_i^{-1}\right)\sum_iw_i\|T_i\xi\|^2.$$

Thus $(\sum_i|T_i|)^2\preceq(\sum_iw_i^{-1})\sum_iw_iT_i^2$, and operator monotonicity of the positive square root gives the corresponding bound for $\sum_i|T_i|$. This argument does not assume the $T_i$ commute. Also $|U+I|+|I-U|=2\max(I,|U|)$ by the spectral calculus of a single self-adjoint $U$.

Using the weights $1/2,3/2$ for $V,T$ yields

$$4F+6I\preceq2\max(I,|U|)+\sqrt{8/3}\sqrt{9I-U^2}.$$

The right side is a function of $|U|$, whose spectrum lies in $[0,3]$. For $0\le u\le1$ it is at most $2+2\sqrt6<2\sqrt{15}$. For $1\le u\le3$, Cauchy--Schwarz on $(u,\sqrt{9-u^2})$ gives

$$2u+\sqrt{8/3}\sqrt{9-u^2}\le3\sqrt{4+8/3}=2\sqrt{15}.$$

Equality in this scalar inequality occurs at $u^2=27/5$. Therefore $F\preceq(\sqrt{15}-3)I/2$.

## Attainment

Write $X=\begin{pmatrix}0&1\\1&0\end{pmatrix}$, $Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix}$, $Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}$, $\sigma=(X,Y,Z)$ and $|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2$.


Choose unit real three-dimensional Bob vectors with Gram entries $(7/10,-1/4,-1/4)$ in pair order $(12,13,23)$, and put $B_j=b_j\cdot\sigma$. This Gram matrix is positive definite: its leading principal minors are $1,51/100,189/400$. It is therefore realized by three vectors. Exact coordinates and all matrices are explicitly included in `strategy.json`.

Their vector sums defining $U,V,T$ have squared lengths $27/5,27/5,3/5$. On $|\Phi^+\rangle$, Alice uses the transposes of the normalized $T,U,-U,-V$. The marginal expectations in the two identity terms vanish. The exact score is $(\sqrt{15}-3)/2$, as independently recomputed from the literal table.

## Binary effects and model scope

For any effect $0\preceq E\preceq I$, the block operator

$$\Pi(E)=\begin{pmatrix}E&\sqrt{E(I-E)}\\\sqrt{E(I-E)}&I-E\end{pmatrix}$$

is a projection whose compression to the first ancillary coordinate is $E$. Use a separate two-dimensional ancillary factor for each measurement and disjoint ancillary factors for the two parties. Original cross-party commutation is preserved under bounded functional calculus. Compression to the common first ancillary coordinates preserves every marginal and cross-party product expectation. The upper proof therefore covers all binary POVMs in every commuting-operator representation. In particular it covers unrestricted spatial strategies. The finite-dimensional attaining construction proves equality of the finite-dimensional, spatial and commuting suprema.

## Reproduction

`strategy.json` contains the normalized state in basis order $00,01,10,11$ and all six Alice and three Bob reflections. Scalars are exact sums of $c\sqrt d\,i^j$, encoded by rational $c$, squarefree positive integer $d$, and $j\in\{0,1\}$. The verifier checks Hermiticity, involution, normalization, and the literal Bell score including all marginals. Unused settings are identities. No optimizer or external data is required.

Run `python -B verify.py 5` from the repository root, or run the local `verify.py` directly.
