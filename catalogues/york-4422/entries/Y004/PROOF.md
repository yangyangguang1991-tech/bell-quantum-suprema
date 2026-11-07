# $I_{4322}^{(3)}$

## Source coordinates

The formulas below use the equivalent source representative in `entries/05-I4322-3/definition.json` inside `certificate.zip`. The symbols $A_i,B_j$ refer to that source representative, not directly to the York ordering in this entry's outer `definition.json`. Its local bound is zero. The explicit transformation at the end identifies the complete source and York polynomials, with scale one and zero additive shift.

## Upper bound and attaining strategy

Put $U=B_1+B_2-B_3$, $V=B_1+B_2+2B_3$, $T=B_1-B_2$. Conversion of the source probability table gives $4F=-6I+A_1T+A_2(U+I)+A_3(-U+I)-A_4V$. Direct expansion gives $U^2+V^2/2+3T^2/2=9I$. For self-adjoint $T_i$ and positive weights $w_i$, vector Cauchy–Schwarz gives $(\sum_i |T_i|)^2\preceq(\sum_i 1/w_i)\sum_i w_iT_i^2$. Taking the operator-monotone square root bounds the sum of absolute values. If $A$ is a commuting reflection, $AT\preceq |T|$, by joint spectral calculus. Neither step requires the $T_i$ to commute with each other.

Thus $4F+6I\preceq 2\max(I,|U|)+\sqrt{8/3}\sqrt{9I-U^2}$. For $0\le u\le1$ this is at most $2+2\sqrt6<2\sqrt{15}$. For $1\le u\le3$, ordinary Cauchy–Schwarz on $(u,\sqrt{9-u^2})$ bounds it by $2\sqrt{15}$, attained at $u^2=27/5$.

Choose Bob Pauli vectors with off-diagonal Gram entries $(7/10,-1/4,-1/4)$ in pair order $(12,13,23)$. The three squared norms of $U,V,T$ are $27/5,27/5,3/5$. Alice uses the transposes of the normalized $T,U,-U,-V$ on the maximally entangled pair. The resulting value is $(\sqrt{15}-3)/2$. 

For each reflection $R$, the reported outcome projection is $(I+R)/2$. Any binary effect can be dilated to a projection by the two-sector construction in the manual. Only cross-party commutation is used. The state and the source reflections are in `entries/05-I4322-3/strategy.json` inside the archive. That file stores six Alice and three Bob settings as a padded source realization; only the active settings used above enter its source polynomial. The four York reflections of each party are obtained by the transformation below. The verifier forms the positive-outcome projections and computes the Bell score on the two-qubit vector directly, including both sets of marginals.

## Transfer to the literal York table

Let $A_i^Y,B_j^Y$ denote the York reflections, with projections $(I+A_i^Y)/2$ and $(I+B_j^Y)/2$. Set

$$
(A^Y_1,A^Y_2,A^Y_3,A^Y_4)=(B_1,B_2,-B_3,I),\qquad
(B^Y_1,B^Y_2,B^Y_3,B^Y_4)=(A_2,A_1,-A_3,-A_4).
$$

Exchange the source tensor factors when transporting the state: a source vector $\sum_{k,l}\psi_{kl}|k\rangle_A|l\rangle_B$ becomes $\sum_{k,l}\psi_{kl}|l\rangle_A|k\rangle_B$. A minus sign complements the corresponding positive-outcome projection. Identity settings fill only the unused York coordinates. This transformation is reversible on the active settings and preserves cross-party commutation; it therefore transports both the universal upper bound and the attaining strategy. The archive's `transfer.json` records these permutations and signs. Its `verify.py` checks the full coefficient identity, including the constant and all marginals, against the 25 integers in `row.json`, and runs the enclosed source certificate.
