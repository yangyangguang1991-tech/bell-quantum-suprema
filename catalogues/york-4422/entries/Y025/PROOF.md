# Global upper bound and attainment for Y25

For each unit vector ψ put S=B₁+B₃+B₄, D=B₁−B₄, V=B₁+B₄−2B₃ and z=‖Sψ‖². Direct expansion gives S²+3D²/2+V²/2=9I and 4F+6I=A₁(S+B₂)+A₂(S−B₂)+A₃D+A₄V. The parallelogram identity and Cauchy–Schwarz bound the sum of the first two expectations by 2√(z+1). Weighted Cauchy–Schwarz bounds the sum of the last two by √(8/3)√(9−z). Applying scalar Cauchy–Schwarz to these two terms gives 10√6/3, with equality possible at z=5. The supplied Pauli matrices, with Alice transposed on the maximally entangled state, give the claimed CH score.

## Relation to the historical correlation facet

Take the unnormalized integer matrix in B. Li, Eq. (9), type 4_1. Its rows are `[[2, 1, -1, 0], [1, -1, 1, 1], [-1, 1, -1, 1], [0, 1, 1, 0]]`. Transpose it first: False. In one-based notation permute the rows by `[2, 3, 4, 1]` and columns by `[2, 4, 1, 3]`. Multiply rows by `[-1, 1, 1, 1]` and columns by `[1, -1, -1, -1]`. This gives the joint block of the York CH table entry by entry. Its exact quantum correlation value therefore transfers under the affine factor given in the entry introduction.

## Physical realization and literal score

The input `strategy.json` gives all eight Pauli coefficient vectors. The state is (|00⟩+|11⟩)/√2. Transpose the four Alice responses only. The included verifier checks hermiticity, eight reflection identities and the original probability score by exact symbolic contraction. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 25 --extract Y025-proof`.
