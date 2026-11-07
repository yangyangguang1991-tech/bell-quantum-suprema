# Global upper bound and attainment for Y122

Let w be the reduced reflection words in the supplied certificate. The checker expands every coefficient of qI−F in the group ring of the free reflections of each party, imposing only cross-party commutation and involutivity. For the factor matrix N and positive algebraic matrix G in the certificate, the identity is qI−F=(Nᵀw)† G (Nᵀw), with the listed field scalings included in N. All directed coefficients are compared exactly. A strict LDL factorization, by quadratic-field arithmetic or outward rational pivots, proves positivity of G in the specified real embedding. This identity bounds every vector state in every commuting representation. Simultaneous local dilations cover binary effects.

In strategy.json the rows give the coefficients of I,X,Y,Z. Use the normalized state (|00>+|11>)/sqrt(2), transpose each displayed Alice matrix, and take the Bob matrices directly. For the projections P=(I+A)/2 and Q=(I+B)/2 the joint probability is Tr(PᵀQ)/2. The exact checker verifies all eight reflection equations, marginal terms and joint probabilities and compares their weighted sum with q.

## Physical realization and literal score

The input `strategy.json` gives all eight Pauli coefficient vectors. The state is (|00⟩+|11⟩)/√2. Transpose the four Alice responses only. The included verifier checks hermiticity, eight reflection identities and the original probability score by exact symbolic contraction. For a normalized state vector ψ and the resulting effects, put P₀=Q₀=I. The independently reproducible score is Σᵢⱼ Cᵢⱼ ψ†(Pᵢ⊗Qⱼ)ψ, with i,j from zero to four and C from definition.json. This includes both marginals and the constant. Extract the core with `python verify.py 122 --extract Y122-proof`.
