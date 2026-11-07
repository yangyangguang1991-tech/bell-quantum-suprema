# Global upper bound and attainment for Y74

The marginal terms cancel in reflection coordinates and 4F+10I is the correlator with joint matrix M from the displayed CH table. Direct multiplication gives (MMᵀ−10I)²=2I, so its operator norm is at most sqrt(10+sqrt(2)). For any state psi the two four-tuples (A_i psi) and (B_j psi) have norms 2. Their bilinear form with M is at most 4 sqrt(10+sqrt(2)), including in the commuting model. Let P=(MMᵀ−(10−sqrt(2))I)/(2 sqrt(2)), U=sqrt(2)P and V=MᵀU/sqrt(10+sqrt(2)). The verifier checks reflection norms for every row vector, using four anticommuting Pauli tensors in local dimension four. With the maximally entangled vector, the cross expectations are the row inner products. This attains the operator bound.

## Relation to the historical correlation facet

Take the unnormalized integer matrix in B. Li, Eq. (9), type 4_2. Its rows are `[[1, 1, 2, 2], [1, 2, 1, -2], [2, 1, -2, 1], [2, -2, 1, -1]]`. Transpose it first: False. In one-based notation permute the rows by `[1, 2, 4, 3]` and columns by `[3, 4, 2, 1]`. Multiply rows by `[-1, -1, -1, 1]` and columns by `[-1, -1, -1, -1]`. This gives the joint block of the York CH table entry by entry. Its exact quantum correlation value therefore transfers under the affine factor given in the entry introduction.

## Physical realization and literal score

The verifier constructs the four anticommuting matrices explicitly as tensor products of Pauli matrices. Take the normalized maximally entangled vector in local dimension four and form the reflections from the row vectors U and V above, transposing Alice’s matrices. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 74 --extract Y074-proof`.
