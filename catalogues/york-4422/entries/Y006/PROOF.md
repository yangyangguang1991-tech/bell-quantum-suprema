# $I_{4322}^{(2)}$

## Source coordinates

The formulas below use the equivalent source representative in `entries/04-I4322-2/definition.json` inside `certificate.zip`. The symbols $A_i,B_j$ refer to that source representative, not directly to the York ordering in this entry's outer `definition.json`. Its local bound is zero. The explicit transformation at the end identifies the complete source and York polynomials, with scale one and zero additive shift.

## Upper bound and attaining strategy

Here $q=(3\sqrt3-4)/4$. The recorded 50 words $w$ give $qI-F=w^*DNYN^TDw$. The diagonal $D$ has $D_{ii}=(\sqrt3)^{s_i}$ with $s_i$ in `scaling_sqrt_d_powers`. The columns of $N$ and the 46-dimensional quadratic field matrix $Y$ are supplied in full. Rational outward rounding proves positive lower endpoints for every pivot of $Y$. The verifier expands the full oriented identity using only the reflection and cross-party relations.

Take Bob $B_1=Z$, $B_2=(-Z+\sqrt3 X)/2$, $B_3=(-Z-\sqrt3 X)/2$. Alice takes $(B_2-B_3,B_1-B_2,B_1-B_3)/\sqrt3$ and $I$ as her fourth setting, all transposed. On the maximally entangled qubit pair these reflections give the asserted score. 

For each reflection $R$, the reported outcome projection is $(I+R)/2$. Any binary effect can be dilated to a projection by the two-sector construction in the manual. Only cross-party commutation is used. The state and the source reflections are in `entries/04-I4322-2/strategy.json` inside the archive. That file stores six Alice and three Bob settings as a padded source realization; only the active settings used above enter its source polynomial. The four York reflections of each party are obtained by the transformation below. The verifier forms the positive-outcome projections and computes the Bell score on the two-qubit vector directly, including both sets of marginals.

## Transfer to the literal York table

Let $A_i^Y,B_j^Y$ denote the York reflections, with projections $(I+A_i^Y)/2$ and $(I+B_j^Y)/2$. Set

$$
(A^Y_1,A^Y_2,A^Y_3,A^Y_4)=(-B_1,B_2,-B_3,I),\qquad
(B^Y_1,B^Y_2,B^Y_3,B^Y_4)=(-A_2,A_4,A_1,-A_3).
$$

Exchange the source tensor factors when transporting the state: a source vector $\sum_{k,l}\psi_{kl}|k\rangle_A|l\rangle_B$ becomes $\sum_{k,l}\psi_{kl}|l\rangle_A|k\rangle_B$. A minus sign complements the corresponding positive-outcome projection. Identity settings fill only the unused York coordinates. This transformation is reversible on the active settings and preserves cross-party commutation; it therefore transports both the universal upper bound and the attaining strategy. The archive's `transfer.json` records these permutations and signs. Its `verify.py` checks the full coefficient identity, including the constant and all marginals, against the 25 integers in `row.json`, and runs the enclosed source certificate.
