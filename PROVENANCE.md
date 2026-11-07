# Mathematical sources and implementation provenance

This edition preserves three separate mathematical catalogues: the 46
tripartite Sliwa representatives, seven representatives for the complete
(6,3,2,2) scenario, and the 175 York representatives for (4,4,2,2).
These are 228 indexed entries. The repeated bipartite representatives are
retained under each catalogue's own numbering; they are not counted as
additional inequivalent inequalities. The exact transformations are in
[CROSSWALK.md](CROSSWALK.md).

The component records identify the published coefficient definitions,
previously proved exact-value theorems, project certificate and code
lineage, and any embedded third-party runtime exceptions:

- [Sliwa catalogue sources](catalogues/sliwa-46/PROVENANCE.md).
- [Six-by-three catalogue sources](catalogues/six-by-three/PROVENANCE.md).
- [York catalogue sources](catalogues/york-4422/PROVENANCE.md).

[PROVENANCE.json](PROVENANCE.json) pins each component source map and
explanation by SHA256. The component maps in turn identify every numbered
entry file group and the shared mathematical implementations. They specify
the preceding constituent edition and the content identity of the
extraction or adaptation programs. Historical preparation artifacts are
identified for source traceability; they are not dependencies needed to
run the distributed proof verifiers.

The root `verify.py` dispatches to those local verifiers. The root
`verify_crosswalk.py` checks the complete coefficient transformations, and
`verify_files.py` checks distribution integrity. The latter is not itself
a proof of a quantum bound. These programs and the crosswalk data are
project integration materials for this combined edition; their exact
file identities are included in the source map.

Yang-Guang Yang confirmed that he organized the predecessor project
materials and can license the project's own new code, prose and
certificates, with no undisclosed rights holders or restrictions. This
records the contributor declaration. It does not adjudicate external
ownership or relicense cited papers, mathematical catalogues or bundled
upstream software. The applicable distinctions and runtime notices are
set out in [RIGHTS.md](RIGHTS.md) and [THIRD_PARTY.md](THIRD_PARTY.md).

Original definitions and prior theorems remain attributed to their
authors. Local implementation or proof reproduction does not imply
independent discovery. Classification and numerical studies are discussed
in the global histories; each entry's strict-value references identify
prior exact proofs where established. Unknown entries remain explicitly
unknown, with no numerical bound interval presented. A file hash binds an
artifact; it does not establish novelty or mathematical validity.
