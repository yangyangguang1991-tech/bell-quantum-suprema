# The Clauser–Horne–Shimony–Holt inequality

## Source coordinates

The formulas below use the equivalent source representative in `entries/01-CHSH/definition.json` inside `certificate.zip`. The symbols $A_i,B_j$ refer to that source representative, not directly to the York ordering in this entry's outer `definition.json`. Its local bound is zero. The explicit transformation at the end identifies the complete source and York polynomials, with scale one and zero additive shift.

## Upper bound and attaining strategy

In the source normalization $4F=-2I+S$, with $S=A_1(B_1-B_2)-A_2(B_1+B_2)$. Multiplying out using cross-party commutation gives $S^2=4I-[A_1,A_2][B_1,B_2]$ (the coefficient of the commutator follows from $(B_1-B_2)(B_1+B_2)=[B_1,B_2]$). Each commutator has norm at most 2, so $S\preceq 2\sqrt{2}I$. Take Bob $(Z,X)$ and Alice $((Z-X)/\sqrt2,-(Z+X)/\sqrt2)$ on $(|00\rangle+|11\rangle)/\sqrt2$. The two correlator rows give $2\sqrt2$, hence the exact upper is $(\sqrt2-1)/2$. The sharp quantum bound is historically due to B. S. Cirel'son. [Cirel'son (1980)](https://doi.org/10.1007/BF00417500).

For each reflection $R$, the reported outcome projection is $(I+R)/2$. Any binary effect can be dilated to a projection by the two-sector construction in the manual. Only cross-party commutation is used. The state and the source reflections are in `entries/01-CHSH/strategy.json` inside the archive. That file stores six Alice and three Bob settings as a padded source realization; only the active settings used above enter its source polynomial. The four York reflections of each party are obtained by the transformation below. The verifier forms the positive-outcome projections and computes the Bell score on the two-qubit vector directly, including both sets of marginals.

## Transfer to the literal York table

Let $A_i^Y,B_j^Y$ denote the York reflections, with projections $(I+A_i^Y)/2$ and $(I+B_j^Y)/2$. Set

$$
(A^Y_1,A^Y_2,A^Y_3,A^Y_4)=(-A_1,-A_2,I,I),\qquad
(B^Y_1,B^Y_2,B^Y_3,B^Y_4)=(-B_1,B_2,I,I).
$$

The state is unchanged. A minus sign complements the corresponding positive-outcome projection. Identity settings fill only the unused York coordinates. This transformation is reversible on the active settings and preserves cross-party commutation; it therefore transports both the universal upper bound and the attaining strategy. The archive's `transfer.json` records these permutations and signs. Its `verify.py` checks the full coefficient identity, including the constant and all marginals, against the 25 integers in `row.json`, and runs the enclosed source certificate.
