# $I_{4322}^{(2)}$

## Definition and exact value

$$C=\begin{pmatrix}
-3&0&1&2\\
0&0&1&-1\\
0&1&-1&0\\
0&1&0&-1\\
2&-1&-1&-1
\end{pmatrix},\qquad q=(3\sqrt3-4)/4.$$

Let $P_i=(I+A_i)/2$ and $Q_j=(I+B_j)/2$ be the positive-outcome projections. The self-adjoint reflections satisfy $A_i^2=B_j^2=I$ and $[A_i,B_j]=0$; no same-party commutation is assumed. The displayed table means

$$F=C_{00}I+\sum_i C_{i0}P_i+\sum_j C_{0j}Q_j+\sum_{ij}C_{ij}P_iQ_j.$$

Append zero rows or columns to obtain six Alice and three Bob settings. Such padding leaves every quantum supremum unchanged: restriction removes unused settings, and assigning identities supplies the converse extension. The local bound is zero, checked on every deterministic assignment.

## Unrestricted upper bound

`gram.json` contains 50 reflection words $w$, a rational $50\times46$ matrix $N$, a symmetric $46\times46$ matrix $Y\in\mathbb Q(\sqrt3)$, and exponents $s_i\in\{0,1\}$. Define $D_{ii}=(\sqrt3)^{s_i}$. With $q=(3\sqrt3-4)/4$, the certificate is

$$qI-F=w^*DNYN^{\mathsf T}Dw.$$

Word $([i_1,\ldots,i_r],[j_1,\ldots,j_s])$ means $A_{i_1+1}\cdots A_{i_r+1}B_{j_1+1}\cdots B_{j_s+1}$. Empty lists are identities. The verifier computes all oriented polynomial coefficients in $\mathbb Q(\sqrt3)$, using only reflection squares and cross-party commutation. Every coefficient agrees exactly with $qI-F$; words are never identified with their reverse.

Integer outward interval LDL proves all 46 pivots of $Y$ strictly positive at 384 binary digits. The square-root enclosure and every division are rational directed enclosures, described in the [manual](../../MANUAL.md). Consequently $Y\succ0$, and the displayed identity proves the unrestricted upper bound in every commuting-operator representation.

## Attainment

Write $X=\begin{pmatrix}0&1\\1&0\end{pmatrix}$, $Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix}$, $Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}$, $\sigma=(X,Y,Z)$ and $|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2$.


Let

$$B_1=Z,\qquad B_2=\frac{-Z+\sqrt3X}{2},\qquad B_3=\frac{-Z-\sqrt3X}{2}.$$

On $|\Phi^+\rangle$, choose Alice reflections

$$A_1=(B_2-B_3)^{\mathsf T}/\sqrt3,\quad A_2=(B_1-B_2)^{\mathsf T}/\sqrt3,\quad A_3=(B_1-B_3)^{\mathsf T}/\sqrt3,\quad A_4=I.$$

The vectors of any two Bob observables have inner product $-1/2$, so the three differences have squared norm three. These are legitimate reflections, and the complete score is $(3\sqrt3-4)/4$. Set $A_5=A_6=I$.

## Binary effects and model scope

For any effect $0\preceq E\preceq I$, the block operator

$$\Pi(E)=\begin{pmatrix}E&\sqrt{E(I-E)}\\\sqrt{E(I-E)}&I-E\end{pmatrix}$$

is a projection whose compression to the first ancillary coordinate is $E$. Use a separate two-dimensional ancillary factor for each measurement and disjoint ancillary factors for the two parties. Original cross-party commutation is preserved under bounded functional calculus. Compression to the common first ancillary coordinates preserves every marginal and cross-party product expectation. The upper proof therefore covers all binary POVMs in every commuting-operator representation. In particular it covers unrestricted spatial strategies. The finite-dimensional attaining construction proves equality of the finite-dimensional, spatial and commuting suprema.

## Reproduction

`strategy.json` contains the normalized state in basis order $00,01,10,11$ and all six Alice and three Bob reflections. Scalars are exact sums of $c\sqrt d\,i^j$, encoded by rational $c$, squarefree positive integer $d$, and $j\in\{0,1\}$. The verifier checks Hermiticity, involution, normalization, and the literal Bell score including all marginals. Unused settings are identities. No optimizer or external data is required.

Run `python -B verify.py 4` from the repository root, or run the local `verify.py` directly.
