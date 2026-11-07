# Exact Quantum Suprema and Certificates for the York (4,4,2,2) Bell Catalogue

**Yang-Guang Yang** · [Email](mailto:yangyangguang1991@gmail.com) · [ORCID](https://orcid.org/0000-0001-9236-7544)

This first edition treats every facet class of the bipartite scenario with four binary measurements per observer. The original York probability table and a traditional name identify each entry. The local bound throughout is zero. The normalization includes the constant term, both sets of marginals and all sixteen joint probabilities.

[Catalogue in numerical order](INDEX.md) · [Reproduction manual](MANUAL.md) · [Historical notes and references](HISTORY.md) · [Catalogue overview](RELEASE.md) · [Combined release](../../RELEASE.md) · [Combined citation](../../CITATION.cff)

The catalogue gives finite-dimensional attaining strategies and global upper proofs for 170 representatives. The entry for the lifted `I3322` gives an exact analytic characterization, a finite strategy sequence and the external infinite-dimensional attainment theorem. Four representatives have an unknown exact unrestricted quantum supremum. They appear at their original indices, Y83, Y92, Y125 and Y128.

```console
python verify_files.py
python verify_names.py
python verify.py 25
python verify.py 139 --extract Y139-proof
```

The supported reproduction environment is Windows x86-64 with a separately installed 64-bit CPython 3.12. The complete distribution includes the arithmetic libraries and, in each relevant certificate, the C99 interval verifier's source and executable. It includes a local binary64 Windows build of NumPy and SciPy for the checkers that need them. No PowerShell/.NET distribution or MSVC runtime DLL is bundled, and verification needs no compiler or software download. See [third-party notices](THIRD_PARTY.md) for the exact library sources, build variant and licenses.

Each proof uses the original coefficients and allows arbitrary Hilbert-space dimension. The universal upper certificates apply to the commuting-observer model. The matching physical construction specifies either projections and a state attaining the value, or an explicit family of legal strategies whose scores tend to the supremum. A root box specifies which algebraic solution defines an exact strategy; its endpoints are part of its definition.

The six overlaps with the (6,3,2,2) volume are Y1 through Y6. Seven representatives also occur in the Ito–Imai–Avis collection: Y1, Y2, Y3, Y6, Y9, Y51 and Y169. Their proof cores appear here in full and never require another volume. For open representatives, the finite-dimensional, spatial and commuting suprema are not identified with one another by this catalogue.

The file framework is uniform: every entry contains `README.md` and `definition.json`; each closed entry also contains `PROOF.md`, `proof.json` and its local certificate ZIP or ordered binary parts. The extended bibliography of Y003 is in `REFERENCES.md`. Y139 uses the same framework and requires no TeX file. Proof lengths and internal certificate formats reflect the mathematical method used for each entry.
