# $I_{4322}^{(1)}$

## Definition and exact value

$$C=\begin{pmatrix}
-4&0&0&3\\
0&1&1&-1\\
1&-1&1&-1\\
1&1&-1&-1\\
2&-1&-1&-1
\end{pmatrix},\qquad q=\sqrt2-1.$$

Let $P_i=(I+A_i)/2$ and $Q_j=(I+B_j)/2$ be the positive-outcome projections. The self-adjoint reflections satisfy $A_i^2=B_j^2=I$ and $[A_i,B_j]=0$; no same-party commutation is assumed. The displayed table means

$$F=C_{00}I+\sum_i C_{i0}P_i+\sum_j C_{0j}Q_j+\sum_{ij}C_{ij}P_iQ_j.$$

Append zero rows or columns to obtain six Alice and three Bob settings. Such padding leaves every quantum supremum unchanged: restriction removes unused settings, and assigning identities supplies the converse extension. The local bound is zero, checked on every deterministic assignment.

## Unrestricted upper bound

The local file `gram.json` supplies 20 reflection words $w$, a $20\times16$ matrix $N$ and a symmetric $16\times16$ matrix $Y$ in $\mathbb Q(\sqrt2)$. A scalar pair $[a,b]$ means $a+b\sqrt2$. Word $([i_1,\ldots,i_r],[j_1,\ldots,j_s])$ means $A_{i_1+1}\cdots A_{i_r+1}B_{j_1+1}\cdots B_{j_s+1}$; empty lists are identities. The exact certificate is

$$ (\sqrt2-1)I-F=w^*NYN^{\mathsf T}w. $$

The verifier expands the right-hand side using only the reflection squares and cross-party commutation. Within each party it cancels adjacent equal letters, preserving their remaining order. It does not identify a word with its reverse. Every resulting coefficient, including the constant, equals the corresponding coefficient on the left in $\mathbb Q(\sqrt2)$.

The matrix $Y$ is strictly positive. The integer interval LDL algorithm in `common/positive.py` encloses all 16 successive Schur pivots at 384 binary digits and proves every lower endpoint strictly positive. Each elementary operation rounds outwards using integer floor or ceiling division; the enclosure of $\sqrt2$ follows from integer square roots. Thus this is a rational inequality proof rather than a tolerance on floating-point eigenvalues. The [manual](../../MANUAL.md) gives the recurrence. Since $Y\succ0$, the displayed identity is positive in every representation.

## Attainment

Write $X=\begin{pmatrix}0&1\\1&0\end{pmatrix}$, $Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix}$, $Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}$, $\sigma=(X,Y,Z)$ and $|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2$.


On $|\Phi^+\rangle$, use Bob reflections $(Z,X,I)$ and Alice reflections

$$\frac{Z+X}{\sqrt2},\quad\frac{-Z+X}{\sqrt2},\quad\frac{Z-X}{\sqrt2},\quad\frac{-Z-X}{\sqrt2}.$$

Each squares to the identity. Substitution into the complete probability table gives $\sqrt2-1$. The supplied exact matrices include the two remaining identity Alice settings.

## Binary effects and model scope

For any effect $0\preceq E\preceq I$, the block operator

$$\Pi(E)=\begin{pmatrix}E&\sqrt{E(I-E)}\\\sqrt{E(I-E)}&I-E\end{pmatrix}$$

is a projection whose compression to the first ancillary coordinate is $E$. Use a separate two-dimensional ancillary factor for each measurement and disjoint ancillary factors for the two parties. Original cross-party commutation is preserved under bounded functional calculus. Compression to the common first ancillary coordinates preserves every marginal and cross-party product expectation. The upper proof therefore covers all binary POVMs in every commuting-operator representation. In particular it covers unrestricted spatial strategies. The finite-dimensional attaining construction proves equality of the finite-dimensional, spatial and commuting suprema.

## Reproduction

`strategy.json` contains the normalized state in basis order $00,01,10,11$ and all six Alice and three Bob reflections. Scalars are exact sums of $c\sqrt d\,i^j$, encoded by rational $c$, squarefree positive integer $d$, and $j\in\{0,1\}$. The verifier checks Hermiticity, involution, normalization, and the literal Bell score including all marginals. Unused settings are identities. No optimizer or external data is required.

Run `python -B verify.py 3` from the repository root, or run the local `verify.py` directly.
