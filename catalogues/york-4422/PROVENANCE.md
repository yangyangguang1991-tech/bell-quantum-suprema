# Mathematical provenance

## Original catalogue and coefficient crosswalk

The 175 classical representatives and their ordering are credited to
Thomas Cope and Roger Colbeck, *Bell Inequalities From No-Signalling
Distributions*, arXiv:1812.10017v3 / Physical Review A 100, 022114 (2019).
Traditional names are supplied through the coefficient supplement and
Appendix A of Oudot, Bancal, Sekatski and Sangouard, *Bipartite nonlocality
with a many-body system*, arXiv:1810.05636v2.

The retained import record identifies the original
[York author supplementary file](https://www-users.york.ac.uk/~rc973/Bell_Sup_Info/Complete_Bell_Lists/4422_Lists/Inequalities_Only_4422_Affine).
It converts the author's affine probability matrices to the full 25-term
CH convention. The retained normalized 175-row JSON has SHA256
`cf3955bf794001a771acf494795c6adf98449ec93398d5a1c3bd2f49d618f604`.
The original downloaded byte stream was not retained; no hash of that
unavailable stream is asserted. All 175 public tables were compared to
the retained normalized data. The separate supplied coefficient-crosswalk
archive, its mapping JSON and its export program are content-addressed in
[PROVENANCE.json](PROVENANCE.json). Their transformations concern the full
polynomial, including constants and marginals.

The catalogue and traditional-name sources are not claimed as this
repository's discoveries. Cope and Colbeck's arXiv manuscript uses the
[non-exclusive arXiv distribution notice](https://arxiv.org/licenses/nonexclusive-distrib/1.0/),
which does not constitute an MIT grant for the paper or the author's data
distribution. This repository does not purport to relicense those works.
It stores normalized mathematical coefficient data with attribution, not
the article's text, figures or source archive.

## Proof corpus and prior exact theorems

The numbered exact certificates are extracted from the user-organized
predecessor proof collection. The source-processing records show separate
extraction of the main algebraic proof cores, earlier fixed-input Gram
cores, elementary/spectral cases, and the full algebraic-value proof for
Y139. The proof notes are project expositions adapted to the common entry
structure. The source map distinguishes retained predecessor files from the current
project implementations and certificate packaging. Literal coefficient
bindings and prior mathematical attribution are recorded separately from
changes to verification software.

Y1--Y6 contain self-contained copies of the corresponding six-by-three
proofs, together with exact transformations to the York coordinates;
their duplication does not create additional original theorems. CHSH is
credited to Cirel'son. Y3 acknowledges the published I3322 path/Bellman
and spectral-comparison arguments in its
[detailed bibliography](entries/Y003/REFERENCES.md). Y25 and Y74 credit
Ben Li's exact correlation bounds and state their normalization maps.
The wider [history](HISTORY.md) distinguishes classical classification,
restricted-dimensional numerical studies and prior strict-value results.

For every closed entry, the provenance record pins the concatenated
certificate archive and each distributed file. Y59, Y124 and Y168 also
contain third-party Python-FLINT/native runtime material inside their
certificate archives. Those members retain upstream notices and are
excluded from the project-authored-code attribution; the runtime license
and source inventory governs them. An embedded runtime is not evidence
that its maintainers authored the Bell proof or certificate.

Y83, Y92, Y125 and Y128 contain definitions and the statement that the exact
unrestricted quantum supremum is unknown. No proof corpus, exact-value
claim, bound interval or per-entry research citation is added to them.

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

## Native directed interval verification

The entries that use a normal-map contraction certificate contain the project C99 implementation and its Python binding in `native_interval/`. The source, executable, fixed dimensions and binding program are identified in each entry's source map and acceptance manifest. The C program preserves the ordered scalar interval operations and guards IEEE binary64 behavior. Its calculation is one component of the complete upper-bound proof; root isolation, compatibility, range, Gram and literal Bell-functional checks remain part of that proof.

`native_interval/BUILD.md` identifies the exact toolchain and floating-point build options. The project implementation has the included MIT license. LLVM compiler-support and MinGW-w64 startup/runtime code retain their complete notices in the accompanying `licenses/` directory. The project authorship statement does not claim ownership of these third-party components.
