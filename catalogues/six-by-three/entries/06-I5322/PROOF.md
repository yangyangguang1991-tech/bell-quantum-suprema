# $I_{5322}$

## Definition and exact value

$$C=\begin{pmatrix}
0&-1&-1&0\\
-1&1&-1&1\\
-1&0&1&1\\
-1&1&1&0\\
0&1&0&-1\\
0&-1&1&-1
\end{pmatrix},\qquad q=(3\sqrt7-6)/4.$$

Let $P_i=(I+A_i)/2$ and $Q_j=(I+B_j)/2$ be the positive-outcome projections. The self-adjoint reflections satisfy $A_i^2=B_j^2=I$ and $[A_i,B_j]=0$; no same-party commutation is assumed. The displayed table means

$$F=C_{00}I+\sum_i C_{i0}P_i+\sum_j C_{0j}Q_j+\sum_{ij}C_{ij}P_iQ_j.$$

Append zero rows or columns to obtain six Alice and three Bob settings. Such padding leaves every quantum supremum unchanged: restriction removes unused settings, and assigning identities supplies the converse extension. The local bound is zero, checked on every deterministic assignment.

## Unrestricted upper bound

Set $P=B_1-B_2+B_3$, $T_1=B_2+B_3$, $T_2=B_1+B_2$, $T_3=B_1-B_3$. The literal probability table gives

$$4F=-6I+A_1(P-I)+A_5(-P-I)+A_2T_1+A_3T_2+A_4T_3,$$

$$P^2+T_1^2+T_2^2+T_3^2=9I.$$

The comparison uses two elementary operator facts. If $A$ is a reflection commuting with self-adjoint $T$, joint functional calculus gives $AT\preceq|T|$. For self-adjoint $T_i$ and positive numbers $w_i$, Cauchy--Schwarz on vectors gives

$$\left\|\sum_i |T_i|\xi\right\|^2\le\left(\sum_iw_i^{-1}\right)\sum_iw_i\|T_i\xi\|^2.$$

Thus $(\sum_i|T_i|)^2\preceq(\sum_iw_i^{-1})\sum_iw_iT_i^2$, and operator monotonicity of the positive square root gives the corresponding bound for $\sum_i|T_i|$. This argument does not assume the $T_i$ commute. Also $|P+I|+|I-P|=2\max(I,|P|)$ by the spectral calculus of a single self-adjoint $P$.

The equal weights for the three $T_i$ yield

$$4F+6I\preceq2\max(I,|P|)+\sqrt3\sqrt{9I-P^2}.$$

For $0\le p\le1$ the scalar expression is at most $2+3\sqrt3<3\sqrt7$. For $1\le p\le3$, Cauchy--Schwarz gives

$$2p+\sqrt3\sqrt{9-p^2}\le3\sqrt{4+3}=3\sqrt7,$$

with equality at $p^2=36/7$. This proves $F\preceq(3\sqrt7-6)I/4$ in every dimension.

## Attainment

Write $X=\begin{pmatrix}0&1\\1&0\end{pmatrix}$, $Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix}$, $Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}$, $\sigma=(X,Y,Z)$ and $|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2$.


Use unit Bob vectors with Gram entries $(-5/14,5/14,-5/14)$ in pair order $(12,13,23)$. The leading principal minors are $1,171/196,243/343$, so the Gram matrix is positive definite. Put $B_j=b_j\cdot\sigma$. Then $P^2=36I/7$ and $T_i^2=9I/7$. Alice uses the transposes of the normalized $P,T_1,T_2,T_3,-P$ on $|\Phi^+\rangle$, with $A_6=I$. The first and last identity terms have zero expectation. Direct exact substitution gives $(3\sqrt7-6)/4$. The complete coordinates and matrices are in `strategy.json`.

## Binary effects and model scope

For any effect $0\preceq E\preceq I$, the block operator

$$\Pi(E)=\begin{pmatrix}E&\sqrt{E(I-E)}\\\sqrt{E(I-E)}&I-E\end{pmatrix}$$

is a projection whose compression to the first ancillary coordinate is $E$. Use a separate two-dimensional ancillary factor for each measurement and disjoint ancillary factors for the two parties. Original cross-party commutation is preserved under bounded functional calculus. Compression to the common first ancillary coordinates preserves every marginal and cross-party product expectation. The upper proof therefore covers all binary POVMs in every commuting-operator representation. In particular it covers unrestricted spatial strategies. The finite-dimensional attaining construction proves equality of the finite-dimensional, spatial and commuting suprema.

## Reproduction

`strategy.json` contains the normalized state in basis order $00,01,10,11$ and all six Alice and three Bob reflections. Scalars are exact sums of $c\sqrt d\,i^j$, encoded by rational $c$, squarefree positive integer $d$, and $j\in\{0,1\}$. The verifier checks Hermiticity, involution, normalization, and the literal Bell score including all marginals. Unused settings are identities. No optimizer or external data is required.

Run `python -B verify.py 6` from the repository root, or run the local `verify.py` directly.
