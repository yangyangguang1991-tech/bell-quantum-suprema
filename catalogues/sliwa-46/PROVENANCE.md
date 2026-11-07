# Mathematical provenance

## Catalogue, normalization and previous theorems

The 46 representatives are credited to Cezary Sliwa's 2003 catalogue, using
the literal correlator normalization in Table I of Lopez-Rosa, Xu and
Cabello, arXiv:1611.01699v4. The project stores its own JSON serialization of
those mathematical expressions. `manuscript/` contains reference tables
generated from the project data; it is not a redistribution of an article's
LaTeX source or publisher layout.

The global [references](REFERENCES.md) and the
[historical comparison](docs/PRIOR_WORK_AND_CONTRIBUTIONS.md) distinguish
reported expressions and numerical benchmarks from earlier exact proofs.
In particular, the local certificates do not claim the previously known
Mermin, CHSH, no-quantum-advantage or symmetry-reduced SOS results as new
theorems. The earlier exact proofs for S2, S3, S4, S7, S10, S11 and S14 are
credited in their entries. Positivity in S1 is an elementary defining bound.
The absence of a prior-theorem citation for another entry is not a priority
claim. The two-setting reduction is explained locally and its relationship
to Masanes' work is credited in the references.

## Implementation and certificate lineage

Each entry's `upper_bound/` inputs, root selectors and attaining-state data
come from the user-organized predecessor proof corpus. The extraction
program first grouped the original exact proofs; a subsequent assembly
exported explicit state and measurement data; the single-entry adaptation
then separated shared algebraic and Bernstein verification routines from
each entry's data. `bellverify/`, `prooflib/` and the verification tools are
project implementations carried forward through those steps. The record
pins both the current files and the historical builder identities. It does
not describe those files as code copied from Ioannou and Rosset or from a
published software repository: no such code-copy source was established by
the inspected build chain.

All 46 entry file groups and shared mathematical files match the pinned
pre-consolidation constituent source. Third-party SymPy and mpmath runtime
code is excluded from the project-implementation attribution and retains
the notices described in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Scope of third-party publication rights

The original papers are cited, not relicensed under the repository's MIT
license. Sliwa's arXiv submission has the
[assumed non-exclusive arXiv distribution notice](https://arxiv.org/licenses/assumed-1991-2003/),
which is not an MIT grant to this repository. The included formulas and
locally generated tables are identified as mathematical source material;
article prose, figures, typesetting and source archives are not included.

## Interpretation of the provenance record

[PROVENANCE.json](PROVENANCE.json) identifies each numbered entry, the exact
SHA256 of its supplied files, the pre-consolidation constituent edition, and
the content identities of the extraction/adaptation programs. A tree digest
is defined there by an explicit canonical JSON encoding. The historical
builder identities document transfer history; those private build programs
are not required to verify any distributed proof.

Yang-Guang Yang has confirmed that he organized the predecessor project
materials and can license the project's own new code, prose and certificates,
with no undisclosed rights holders or restrictions. This is the contributor's
declaration, not an independent legal adjudication. Identified third-party
software, publications, mathematical catalogues and their original notices
remain separate. In older project artifacts, the generic label "Bell Exact
Bounds Project contributors" denoted that predecessor collection; it is not
used here as evidence for an unidentified external software project's license.

The records distinguish a published mathematical definition, a previously
proved theorem, and this distribution's implementation or certificate.
Reproducing a proof does not transfer priority for the theorem. Conversely,
a historical numerical value or a formula accepted by numerical agreement
is not relabelled as an earlier strict unrestricted proof. Prior strict-value
citations are identified within the relevant entry; the wider history includes
classification, numerical work and general methods.

The numbered entries contain the Bell coefficients, exact root selectors,
positivity inputs, physical strategies and verification programs. No claim
of worldwide priority or independent invention follows from a file hash.
