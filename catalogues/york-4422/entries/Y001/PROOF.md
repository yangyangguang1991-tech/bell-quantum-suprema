# Positivity of a joint outcome

## Source coordinates

The formulas below use the equivalent source representative in `entries/00-positivity/definition.json` inside `certificate.zip`. The symbols $A_i,B_j$ refer to that source representative, not directly to the York ordering in this entry's outer `definition.json`. Its local bound is zero. The explicit transformation at the end identifies the complete source and York polynomials, with scale one and zero additive shift.

## Upper bound and attaining strategy

The representative is $F=-p_{11}$. Products of commuting positive projections are positive, so $F\le0$. Alice's first positive-outcome effect is zero; the score is exactly zero on the displayed state. This is the defining probability constraint, the trivial facet in the completeness count.

For each reflection $R$, the reported outcome projection is $(I+R)/2$. Any binary effect can be dilated to a projection by the two-sector construction in the manual. Only cross-party commutation is used. The state and the source reflections are in `entries/00-positivity/strategy.json` inside the archive. That file stores six Alice and three Bob settings as a padded source realization; only the active settings used above enter its source polynomial. The four York reflections of each party are obtained by the transformation below. The verifier forms the positive-outcome projections and computes the Bell score on the two-qubit vector directly, including both sets of marginals.

## Transfer to the literal York table

Let $A_i^Y,B_j^Y$ denote the York reflections, with projections $(I+A_i^Y)/2$ and $(I+B_j^Y)/2$. Set

$$
(A^Y_1,A^Y_2,A^Y_3,A^Y_4)=(A_1,I,I,I),\qquad
(B^Y_1,B^Y_2,B^Y_3,B^Y_4)=(B_1,I,I,I).
$$

The state is unchanged. A minus sign complements the corresponding positive-outcome projection. Identity settings fill only the unused York coordinates. This transformation is reversible on the active settings and preserves cross-party commutation; it therefore transports both the universal upper bound and the attaining strategy. The archive's `transfer.json` records these permutations and signs. Its `verify.py` checks the full coefficient identity, including the constant and all marginals, against the 25 integers in `row.json`, and runs the enclosed source certificate.
