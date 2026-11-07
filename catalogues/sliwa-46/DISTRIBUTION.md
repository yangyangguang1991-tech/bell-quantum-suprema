# Distribution of the Sliwa catalogue

This catalogue is a constituent of **Exact Quantum Suprema and Certificates
for Selected Bell Scenarios**, version 1.0.0, by Yang-Guang Yang
(yangyangguang1991@gmail.com). Its location in the combined repository is
`catalogues/sliwa-46/`.

Use the combined [distribution instructions](../../DISTRIBUTION.md) and
[upload guide](../../UPLOAD.md). The root [CITATION.cff](../../CITATION.cff)
identifies the combined edition. This directory's [CITATION.cff](CITATION.cff)
records the constituent catalogue's title and provenance. The
[archiving and citation notes](docs/ARCHIVING_AND_CITATION.md) describe the
same combined publication and its root metadata and release artifacts.
There is no assigned DOI until the actual complete edition is archived.

## Complete inputs and directory layout

For the full combined collection, extract all ordinary complete-release
volumes into the same empty directory, as specified at the root. The complete
master archive is an alternative distribution of the same tree. The lightweight
Git source edition omits large York payloads, so GitHub's automatic source
archive alone is not the full combined proof distribution.

The complete Sliwa catalogue files, including `third_party/`, are retained
in both editions. Every Sliwa entry has its own coefficient, positivity and
attainment data. Its algorithms and libraries are shared within this catalogue;
no certificate from six-by-three, York or another research archive is needed
to run a Sliwa entry. Individual entry subdirectories are not standalone
distributions. Keep this entire catalogue directory together.

## Local verification

From `catalogues/sliwa-46/`, use a standard Python 3.11 or later installation
with `venv`. All mathematical libraries are supplied; no network installation,
optimizer or external proof data is required. The common full-collection
environment is specified in the root manual. Keep extraction paths short
on Windows, for example under `C:\BellProofs`.

```text
python -B -S run.py manifest
python -B -S run.py verify --all
```

The first command checks the catalogue inventory only. The second reconstructs
all exact upper proofs and attaining strategies. Keep assertions enabled.
Numerical score checks alone do not establish an exact upper proof.

All 46 entries retain the same outer framework: `README.md`, `functional.json`,
`strategy_spec.json`, `verify.py`, `upper_bound/` and `attainment/`. Necessary
boundary lemmas and polynomial-system inputs remain even when internal formats
differ. Optional sources in `manuscript/` do not require compilation for
mathematical verification.

## Publication and citation

Upload and tag the combined repository from its root, following
[UPLOAD.md](../../UPLOAD.md). Preserve `.gitattributes` and the original input
bytes. Retain this catalogue's `MANIFEST.sha256`, license and third-party
notices. Cite the combined release and the original mathematical results
credited in the relevant entry. Do not substitute an unissued DOI or replace
a publicly cited version's files in place.
