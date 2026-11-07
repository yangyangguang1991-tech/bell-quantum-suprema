# Exact Quantum Suprema of the (6,3,2,2) Bell Facets

**Author:** Yang-Guang Yang  
**Email:** yangyangguang1991@gmail.com  
**ORCID:** [0000-0001-9236-7544](https://orcid.org/0000-0001-9236-7544)  
**Version:** 1.0.0

This repository contains all seven facet classes of the bipartite scenario with six binary measurements for Alice and three for Bob. Every entry supplies its full active probability table, an unrestricted quantum upper-bound proof, and an attaining strategy or an explicit convergent family. All stated values use the supplied representative with local bound zero. Unused settings are padded with zero coefficients.

| Entry | Traditional name | Exact quantum supremum | Supplied reverse inequality |
|---:|---|---|---|
| [00](entries/00-positivity/README.md) | Joint probability positivity | $0$ | Explicit finite strategy |
| [01](entries/01-CHSH/README.md) | CHSH | $(\sqrt2-1)/2$ | Explicit two-qubit strategy |
| [02](entries/02-I3322/README.md) | $I_{3322}$ | Jacobi path constant $q_*$ | Explicit convergent finite-dimensional family |
| [03](entries/03-I4322-1/README.md) | $I_{4322}^{(1)}$ | $\sqrt2-1$ | Explicit two-qubit strategy |
| [04](entries/04-I4322-2/README.md) | $I_{4322}^{(2)}$ | $(3\sqrt3-4)/4$ | Explicit two-qubit strategy |
| [05](entries/05-I4322-3/README.md) | $I_{4322}^{(3)}$ | $(\sqrt{15}-3)/2$ | Explicit two-qubit strategy |
| [06](entries/06-I5322/README.md) | $I_{5322}$ | $(3\sqrt7-6)/4$ | Explicit two-qubit strategy |

The proofs identify the same supremum in the finite-dimensional tensor-product, unrestricted spatial and commuting-operator models. For $I_{3322}$ the exact specification is variational; no algebraic or radical expression is asserted. Its proof distinguishes equality of suprema from attainment in a specified model. Detailed exact-value and attainment references are included in that entry.

## Reproduce the catalogue

Use Python 3.10 or later. Only its standard library is required, on Windows, macOS or Linux. No package installation, network connection, optimizer or external certificate is needed.

```console
python -B verify.py
```

The default command runs every entry and the exact finite enumeration proving catalogue completeness. To run just one entry, for example:

```console
python -B verify.py 4
```

Do not use `-O` or `-OO`: every verification module rejects disabled assertions. The [manual](MANUAL.md) explains conventions, data formats and the scope of the finite checks. [FACETS.md](FACETS.md) proves completeness. [HISTORY.md](HISTORY.md) and [I3322_HISTORY.md](I3322_HISTORY.md) distinguish prior exact theorems from numerical and restricted-dimensional studies. Use the combined [release description](../../RELEASE.md), [upload instructions](../../UPLOAD.md) and [citation metadata](../../CITATION.cff) for publication and citation. The local [catalogue overview](RELEASE.md) and [CITATION.cff](CITATION.cff) record constituent information. [DISTRIBUTION.md](DISTRIBUTION.md) explains the repository contents and version citation.
