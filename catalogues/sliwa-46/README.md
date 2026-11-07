# Exact quantum maxima of the Śliwa Bell inequalities

**Constituent catalogue edition · v1.0.0**

Global upper bounds and attaining strategies for the (3,2,2) Bell scenario.

A self-contained collection of exact proofs for all 46 representatives of the tripartite, two-settings, two-outcomes Śliwa catalogue. Every numbered entry contains its own global upper-bound inputs and verifiers, together with an explicitly specified attaining state and measurements.

Author and maintainer: **Yang-Guang Yang**  
ORCID: [0000-0001-9236-7544](https://orcid.org/0000-0001-9236-7544)  
Email: [yangyangguang1991@gmail.com](mailto:yangyangguang1991@gmail.com)  
GitHub: [yangyangguang1991-tech](https://github.com/yangyangguang1991-tech)

## Mathematical result and scientific contribution

For each of the 46 fixed representatives, the exact finite-dimensional, spatial and commuting quantum maxima coincide with the supplied attaining three-qubit value. Rational or radical expressions specify 28 entries; eight values are isolated univariate roots, and ten are coordinates of uniquely isolated real solutions of polynomial systems.

The contribution is a complete exact upper-and-attainment certificate corpus in a fixed literal normalization. The 19 decimal rows of the 2016 benchmark receive exact algebraic specifications and global certificates. Entry bibliographies credit prior strict global proofs. Earlier reported analytical expressions and numerical benchmarks are compared in the general historical survey.

Panwar, Pandya and Wieśniak (2023) give an exact global calculation for class 7 and also treat the Mermin and extended CHSH full-correlation forms (classes 2 and 3). [Article](https://doi.org/10.1038/s41534-023-00735-3).

- [Scientific overview and main theorem](docs/SCIENTIFIC_NOTE.md).
- [Historical comparison and contributions for all 46 entries](docs/PRIOR_WORK_AND_CONTRIBUTIONS.md).
- [Archiving, DOI registration and citation](docs/ARCHIVING_AND_CITATION.md).
- [Offline reference tables](manuscript/README.md).

## Contents

- [S001–S046 entry index](INDEX.md).
- [Mathematical proof guide](docs/PROOF_GUIDE.md): arbitrary-dimension reduction, exact positivity certificates and constructive attainment.
- [Usage and data formats](docs/USAGE.md).
- [References](REFERENCES.md) and [BibTeX bibliography](references.bib), [license](LICENSE) and [third-party notices](THIRD_PARTY_NOTICES.md).
- [Release description](RELEASE.md) and [distribution instructions](DISTRIBUTION.md).

Each entry fixes the literal Bell expression and its normalization. Its exact value is specified by radicals, an isolated univariate algebraic root, or a uniquely isolated solution of an explicit polynomial system. All three forms specify exact real numbers.

The upper bounds cover arbitrary Hilbert-space dimension, binary POVMs and the commuting-operator model. The supplied strategies attain them with three qubits. The dimension reduction and its endpoint cases are proved in the proof guide.

## Quick start

Use Python 3.11 or later. SymPy 1.14.0 and mpmath 1.3.0 sources and licenses are bundled. Verification requires no pip installation, internet connection, SDP solver or earlier project archive.

```text
python -S run.py manifest
python -S run.py verify --id 21
python -S run.py verify --all
```

The final command checks every exact upper bound and regenerates every attaining strategy. It can take tens of minutes. Keep assertions enabled: do not add `-O` or `-OO` to a full proof run.

The full replay follows a fixed schedule of 52 upper-verifier invocations across the 46 entries. The entry configuration must match that schedule. Each invocation checks the target bindings and the unchanged contents of its source and execution inputs; designated reports are separate outputs. The positivity verifiers check both the complete list of required proof obligations and coverage within each subdivision tree.

For a fast check of the delivered files and numerical strategies:

```text
python -S tools/verify_package.py
```

This fast check does not replay the global upper-bound proofs.

## States, measurements and independent scores

Every `entries/Sxxx/attainment/strategy_numeric.json` contains eight real state amplitudes and all six real 2-by-2 observables, displayed to 80 decimal digits. The corresponding `strategy_exact.json` gives the exact parameters and a finite arithmetic formula for each normalized amplitude.

Measurement square roots use the nonnegative branch, including zero at endpoint overlaps. The state normalization uses a strictly positive square root. The eigen-equation residual in each numerical file is evaluated from that file's published rounded amplitudes, observables and value; `residual_evaluation` states its inputs and working precision.

```text
python -S tools/check_strategy.py entries/S021/attainment/strategy_numeric.json
python -S run.py export --id 21 --digits 80
```

The independent score checker uses only standard-library Decimal arithmetic. Export writes JSON, CSV and independent audit reports to `exports/S021/`. Exact equality follows from the algebraic construction and the separate global upper proof; decimal calculations provide a reproducibility check.

## Organization

```text
entries/S001/ ... entries/S046/
  README.md
  functional.json
  strategy_spec.json
  upper_bound/       this entry's certificate inputs and verification programs
  attainment/        this entry's exact and numerical attaining strategy
  verify.py
bellverify/          exact algebra, state construction and input binding
prooflib/            shared generic upper-verification algorithms
tools/               independent checks and integrity tools
third_party/         bundled runtime sources and licenses
```

No entry includes another entry's certificate data. Common algorithms and runtime libraries are shared at repository level. Unpack or clone the complete repository before running an entry.

The [bibliography](REFERENCES.md) identifies the original catalogue, earlier global proofs and subsequent computational work.

## How to read the certificates

The numbered directories supply the literal Bell expression, the algebraic value and its selector, the global positivity inputs, and a state with six observables. To follow a single proof, run the command shown in that entry. To recompute its score from the displayed vector and matrices alone, use the independent numerical checker; the exact attainment audit also verifies the algebraic vector. The full assignment of historical formulas, numerical benchmarks and earlier strict proofs is documented in each entry and in the [historical survey](docs/PRIOR_WORK_AND_CONTRIBUTIONS.md). The included [independent auditors](tools/independent/README.txt) use Python's standard library. The two-settings, two-outcomes reduction is proved within the [proof guide](docs/PROOF_GUIDE.md).

This catalogue belongs to the first combined repository edition. A prepared archive does not imply a GitHub publication date or DOI registration. Consult the combined [release description](../../RELEASE.md), [upload instructions](../../UPLOAD.md) and [citation metadata](../../CITATION.cff). The local [catalogue overview](RELEASE.md) and `CITATION.cff` retain constituent information.
