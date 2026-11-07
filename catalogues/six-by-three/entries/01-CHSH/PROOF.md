# CHSH

## Definition and exact value

$$C=\begin{pmatrix}
-1&0&1\\
0&1&-1\\
1&-1&-1
\end{pmatrix},\qquad q=(\sqrt2-1)/2.$$

Let $P_i=(I+A_i)/2$ and $Q_j=(I+B_j)/2$ be the positive-outcome projections. The self-adjoint reflections satisfy $A_i^2=B_j^2=I$ and $[A_i,B_j]=0$; no same-party commutation is assumed. The displayed table means

$$F=C_{00}I+\sum_i C_{i0}P_i+\sum_j C_{0j}Q_j+\sum_{ij}C_{ij}P_iQ_j.$$

Append zero rows or columns to obtain six Alice and three Bob settings. Such padding leaves every quantum supremum unchanged: restriction removes unused settings, and assigning identities supplies the converse extension. The local bound is zero, checked on every deterministic assignment.

## Unrestricted upper bound

The complete probability-to-reflection expansion is

$$4F=-2I+S,\qquad S=A_1(B_1-B_2)-A_2(B_1+B_2).$$

Direct multiplication, retaining both orientations of every word, gives

$$S^2=4I-[A_1,A_2][B_1,B_2].$$

The norm of each commutator is at most two. Thus $S^2\preceq8I$ and $S\preceq2\sqrt2 I$ by spectral calculus. This proves $F\preceq(\sqrt2-1)I/2$ without restricting local dimension.

## Attainment

Use $|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2$, Bob reflections $(Z,X)$ and Alice reflections $((Z-X)/\sqrt2,-(Z+X)/\sqrt2)$. Here $X,Y,Z$ denote the Pauli matrices. Since the displayed reflections are real, $\langle\Phi^+|M\otimes N|\Phi^+\rangle=\operatorname{Tr}(M^{\mathsf T}N)/2$ gives $\langle S\rangle=2\sqrt2$. This is the sharp unrestricted bound of Cirel'son; see [the exact-value reference](REFERENCES.md).

## Binary effects and model scope

For any effect $0\preceq E\preceq I$, the block operator

$$\Pi(E)=\begin{pmatrix}E&\sqrt{E(I-E)}\\\sqrt{E(I-E)}&I-E\end{pmatrix}$$

is a projection whose compression to the first ancillary coordinate is $E$. Use a separate two-dimensional ancillary factor for each measurement and disjoint ancillary factors for the two parties. Original cross-party commutation is preserved under bounded functional calculus. Compression to the common first ancillary coordinates preserves every marginal and cross-party product expectation. The upper proof therefore covers all binary POVMs in every commuting-operator representation. In particular it covers unrestricted spatial strategies. The finite-dimensional attaining construction proves equality of the finite-dimensional, spatial and commuting suprema.

## Reproduction

`strategy.json` contains the normalized state in basis order $00,01,10,11$ and all six Alice and three Bob reflections. Scalars are exact sums of $c\sqrt d\,i^j$, encoded by rational $c$, squarefree positive integer $d$, and $j\in\{0,1\}$. The verifier checks Hermiticity, involution, normalization, and the literal Bell score including all marginals. Unused settings are identities. No optimizer or external data is required.

Run `python -B verify.py 1` from the repository root, or run the local `verify.py` directly.
