# $I_{4322}^{(1)}$

## Source coordinates

The formulas below use the equivalent source representative in `entries/03-I4322-1/definition.json` inside `certificate.zip`. The symbols $A_i,B_j$ refer to that source representative, not directly to the York ordering in this entry's outer `definition.json`. Its local bound is zero. The explicit transformation at the end identifies the complete source and York polynomials, with scale one and zero additive shift.

## Upper bound and attaining strategy

The exact maximum in the source local-bound-zero representative is $\sqrt{2}-1$. With $w$ the 20 reflection words in `gram.json`, the certificate is $qI-F=w^*NYN^Tw$. Pairs in $N,Y$ encode $a+b\sqrt{2}$. The last check expands both sides in the free product of reflections on each party, without identifying a word with its reverse. An outward rational interval LDL decomposition establishes that every one of the 16 pivots of $Y$ is strictly positive. Thus the identity is positive in every representation.

Take Bob $(Z,X,I)$, and Alice $(Z+X,-Z+X,Z-X,-Z-X)/\sqrt2$, on the Bell pair. Substitution of all four Alice rows, all three Bob columns, and both sets of marginals in the source table gives $q$. 

For each reflection $R$, the reported outcome projection is $(I+R)/2$. Any binary effect can be dilated to a projection by the two-sector construction in the manual. Only cross-party commutation is used. The state and the source reflections are in `entries/03-I4322-1/strategy.json` inside the archive. That file stores six Alice and three Bob settings as a padded source realization; only the active settings used above enter its source polynomial. The four York reflections of each party are obtained by the transformation below. The verifier forms the positive-outcome projections and computes the Bell score on the two-qubit vector directly, including both sets of marginals.

## Transfer to the literal York table

Let $A_i^Y,B_j^Y$ denote the York reflections, with projections $(I+A_i^Y)/2$ and $(I+B_j^Y)/2$. Set

$$
(A^Y_1,A^Y_2,A^Y_3,A^Y_4)=(-B_3,B_1,B_2,I),\qquad
(B^Y_1,B^Y_2,B^Y_3,B^Y_4)=(A_1,-A_4,A_3,A_2).
$$

Exchange the source tensor factors when transporting the state: a source vector $\sum_{k,l}\psi_{kl}|k\rangle_A|l\rangle_B$ becomes $\sum_{k,l}\psi_{kl}|l\rangle_A|k\rangle_B$. A minus sign complements the corresponding positive-outcome projection. Identity settings fill only the unused York coordinates. This transformation is reversible on the active settings and preserves cross-party commutation; it therefore transports both the universal upper bound and the attaining strategy. The archive's `transfer.json` records these permutations and signs. Its `verify.py` checks the full coefficient identity, including the constant and all marginals, against the 25 integers in `row.json`, and runs the enclosed source certificate.
