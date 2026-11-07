# Distribution of the York (4,4,2,2) catalogue

This catalogue is the `catalogues/york-4422/` constituent of
**Exact Quantum Suprema and Certificates for Selected Bell Scenarios**,
version 1.0.0. All 175 original positions are retained, including the four
unknown entries. No additional catalogue is needed to supply a York proof
once its own complete inputs have been extracted.

## Obtain the complete offline inputs

Follow the combined [distribution instructions](../../DISTRIBUTION.md) and
[upload guide](../../UPLOAD.md). The lightweight Git source edition contains
readable definitions and proof descriptions, but omits the large certificate
and runtime payloads listed in the root `PAYLOADS.json`. It cannot perform
complete York mathematical replay by itself.

Download all ordinary complete-release ZIP volumes of the combined edition
and extract every volume into the same empty directory. These archives have
disjoint paths and must not be concatenated. The complete combined master
ZIP is an alternative local distribution of the same file tree. Do not mix
payloads and checksums from different editions. No verifier downloads files.

Inside an entry, `certificate.zip.part001` and subsequent parts are different:
they are ordered binary pieces of a single certificate ZIP. Do not unzip
them separately. The local `verify.py` reads `proof.json`, assembles the
parts in the specified order and checks the digest before extraction.

## Local reproduction

Use Windows x86-64 with a separately installed 64-bit CPython 3.12. The
complete distribution includes the arithmetic libraries and the relevant
entries' C99 interval verifier sources and executables. The numerical
libraries include a local binary64 Windows build of NumPy and SciPy; see
the [runtime source and license inventory](../../third_party/runtime/SOURCE_SUPPLY.md).
No PowerShell/.NET distribution or MSVC runtime DLL is bundled. Verification
needs no compiler installation, network access, external research archive
or SDP solver. See [MANUAL.md](MANUAL.md) for platform prerequisites,
temporary disk space and exact certificate commands.

Run from `catalogues/york-4422/`:

```console
python -B verify_files.py
python -B verify_names.py
python -B verify.py 25
python -B verify.py 139
```

The first command checks the catalogue's hashes, and the second checks all
traditional-name coefficient identities. Each numbered command runs that
entry's complete proof schedule or states that its exact supremum is unknown.
To visit the entire York catalogue from the combined root, use
`python -B verify.py --catalogue york --all`. Keep assertions enabled.

## Publication, citation and licenses

Publish the combined root and its complete-release artifacts according to
[UPLOAD.md](../../UPLOAD.md); do not use a different standalone York ZIP
name or an earlier edition's volume list. Preserve the root and local
`.gitattributes` rules before staging files so that Git does not normalize
bytes covered by the manifests. The root upload procedure keeps large
payloads in release artifacts rather than ordinary Git history.

The root [CITATION.cff](../../CITATION.cff) identifies the combined edition.
The local [CITATION.cff](CITATION.cff) preserves the constituent catalogue's
title and provenance. Cite historical theorems separately as specified in
the entries. Retain this directory's license, third-party notices and
`SHA256SUMS.txt`. A version DOI must identify the actual archived complete
edition and must not be invented in advance.
