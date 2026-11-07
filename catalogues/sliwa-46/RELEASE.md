# Exact quantum maxima of the Śliwa Bell inequalities

This is a constituent catalogue overview for version 1.0.0 of **Exact Quantum Suprema and Certificates for Selected Bell Scenarios**. Use the combined [release description](../../RELEASE.md), [publication instructions](../../UPLOAD.md) and [citation metadata](../../CITATION.cff) when publishing or citing this edition. The local `CITATION.cff` records constituent provenance.

## Constituent catalogue edition (v1.0.0)

**Yang-Guang Yang** · ORCID 0000-0001-9236-7544 · yangyangguang1991@gmail.com

This edition gives the exact quantum maximum of each of the 46 inequivalent Śliwa facets for three parties with two settings and two outcomes per party. The upper certificates cover commuting operators on arbitrary Hilbert spaces. A normalized three-qubit vector and six local two-dimensional observables attain each upper bound. Each numbered directory specifies its Bell functional in the normalization of López-Rosa, Xu and Cabello, the exact value, the positivity proof, and its attainment data.

Twenty-eight values are rational or radical expressions, eight are isolated real roots of univariate polynomials and ten are coordinates of isolated real polynomial systems. The proof reduces pairs of local reflections to qubit blocks. It then certifies positivity on the entire three-parameter cube. At an attaining parameter triple, a nonzero column of a polynomial in the Bell matrix gives the state. The files describe the radical branches, root isolation, normalization and tensor basis.

The 2003 Śliwa table identifies the facets. The 2016 work of López-Rosa, Xu and Cabello reported 27 analytical expressions and 19 decimal values. Vallins, Sainz and Liang supplied an independent later numerical comparison. Ioannou and Rosset exhibited explicit exact SOS certificates for classes 3, 10, 11 and 14. Earlier elementary cases, the Mermin and CHSH reductions, and further historical identifications are credited at the relevant entries. These distinctions describe the sources reviewed for this edition; they do not establish worldwide priority. See [References](REFERENCES.md) and [Historical comparison](docs/PRIOR_WORK_AND_CONTRIBUTIONS.md).

Panwar, Pandya and Wieśniak (2023) give an exact global calculation for class 7 and also treat the Mermin and extended CHSH full-correlation forms (classes 2 and 3). [Article](https://doi.org/10.1038/s41534-023-00735-3).

Extract the repository and run `python -B -S run.py verify --id 21` for an individual example or `python -B -S run.py verify --all` for all 46 upper proofs and explicit attaining strategies. The repository includes the required Python libraries and their licenses. Readers need a standard Python installation with venv; verification requires no package download, solver or remote data. The [entry index](INDEX.md), [proof guide](docs/PROOF_GUIDE.md) and [verification manual](docs/USAGE.md) give the full procedure.
