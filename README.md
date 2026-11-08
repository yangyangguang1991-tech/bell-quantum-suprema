# Exact Quantum Suprema and Certificates for Selected Bell Scenarios

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24047078.svg)](https://doi.org/10.5281/zenodo.24047078)

**Archived edition:** https://doi.org/10.5281/zenodo.24047078
**First repository edition: v1.0.0**

**Repository author and maintainer:** Yang-Guang Yang  
**Email:** [yangyangguang1991@gmail.com](mailto:yangyangguang1991@gmail.com)  
**ORCID:** [0000-0001-9236-7544](https://orcid.org/0000-0001-9236-7544)

This collection supplies historical Bell functionals in their original
normalizations, exact quantum-supremum
definitions, dimension-independent upper proofs, and attaining strategies or
explicit approximating families for three catalogues. Their original numbering
and normalizations are retained.

- **[Sliwa S001-S046](catalogues/sliwa-46/INDEX.md):** the complete tripartite,
  two-settings, two-outcomes catalogue. All 46 entries have exact upper proofs
  and attaining three-qubit strategies.
- **[(6,3,2,2) facets](catalogues/six-by-three/README.md):** all seven bipartite
  facet classes, including the exact finite classification and its enumeration.
  Six have finite attaining strategies; I3322 has a precise variational value
  and an explicit convergent finite-dimensional strategy family.
- **[York Y1-Y175](catalogues/york-4422/INDEX.md):** the complete (4,4,2,2)
  catalogue. There are 170 finite-dimensional attaining cases, the exact I3322
  characterization, and four unresolved representatives.

Y83, Y92, Y125 and Y128 remain at their original positions with the statement
**Exact unrestricted quantum supremum: unknown.** No numerical bound intervals
for them are included in this edition.

There are 228 catalogue positions, of which 224 contain exact-value proof
materials. These counts include repeated bipartite representatives. The two
bipartite catalogues share six classes and together contain 176 classes under
the specified relabeling and unused-setting convention. Tripartite classes
are counted separately. See [the exact correspondence index](CROSSWALK.md).

## Authorship and mathematical contributions

Except for expressly credited earlier results and third-party contributions,
the proof and certificate constructions, physical constructions, exposition
and verification implementations supplied in this edition are the work of
Yang-Guang Yang. See the [release overview](RELEASE.md),
[contribution map](CONTRIBUTION_MAP.md) and [historical notes](HISTORY.md)
for the scope and source attribution of each entry.

## Mathematical scope

The closed entries specify identical finite-dimensional, spatial and
commuting-operator suprema through universal upper proofs and matching physical
constructions. A finite maximum is distinguished from a supremum approached
by a sequence. I3322 is defined by an explicit variational constant, without
an assertion that it is a radical or an algebraic number. Its detailed proof
and exact-result bibliography appear in both relevant catalogue positions.
No equality between the three models is asserted for unresolved entries.

The exact-value formats include rational numbers, radicals, isolated algebraic
roots, uniquely isolated polynomial-system solutions and the I3322 variational
constant. A decimal evaluation is never the definition of an exact result.

## Reproduce the materials

For the entire collection use **64-bit Windows on x86-64 with CPython 3.12**.
The complete offline distribution includes its arithmetic libraries and native
verification programs. Windows and CPython, including their platform runtime
components, are prerequisites. No PowerShell/.NET distribution or MSVC runtime
DLL is bundled. NumPy is a documented local LLVM-MinGW build; see the
[runtime source-supply statement](third_party/runtime/SOURCE_SUPPLY.md).
No optimizer, internet
connection, another research archive or downloaded certificate is needed.
The individual Sliwa and six-by-three catalogues support additional environments
described in their own manuals.

```console
python -B verify.py --files
python -B verify.py --definitions-only
python -B verify.py --catalogue sliwa --entry 7
python -B verify.py --catalogue six-by-three --entry 4
python -B verify.py --catalogue york --entry 139
python -B verify.py --all
```

The first two commands check file integrity and definitions only. The last
command executes every supplied upper-and-attainment proof, the six-by-three
classification, and the unknown statements. Large exact certificates can take
substantial time and memory. Run ordinary Python without `-O` or `-OO`.

**Download distinction:** the lightweight Git source edition retains the
readable material and programs but omits large certificate/runtime payloads.
GitHub's automatic source archive alone is therefore not the full proof
distribution. Download and extract every complete-release volume into the same
directory for offline reproduction. See [DISTRIBUTION.md](DISTRIBUTION.md).

## Organization and provenance

The three catalogue directories remain independently organized. Each entry
keeps its original definition and local proof data; the shared root only
provides navigation, exact correspondence checks and command dispatch. No
proof target is replaced by a different representative without a coefficient
identity. Repeated proof cores are retained in this first edition.

- [Complete reproduction manual](MANUAL.md).
- [Historical context and bibliography guide](HISTORY.md).
- [Release description](RELEASE.md).
- [Citation metadata](CITATION.cff), [license](LICENSE), and
  [third-party notices](THIRD_PARTY.md).

Each entry credits identified prior strict exact-value proofs. The historical
surveys additionally discuss numerical, dimension-restricted and computational
work, including relevant automated research. Absence of an identified earlier
proof is not used as a claim of worldwide priority. Verification here means
the supplied exact mathematical checks and written arguments, not a claim
that the entire collection has been formalized in a proof assistant.

## Contributions, sources and reuse

Historical results retain their original mathematical attribution. The
repository's compilation, exposition and implementation are described in
[CONTRIBUTIONS.md](CONTRIBUTIONS.md); file origins and source distinctions
are recorded in [PROVENANCE.md](PROVENANCE.md). The project license covers
the project's own materials, while third-party components retain their
licenses. See [RIGHTS.md](RIGHTS.md), [THIRD_PARTY.md](THIRD_PARTY.md), and
the [runtime source-supply documentation](third_party/runtime/SOURCE_SUPPLY.md).

## Authorship and scholarly credit

For contribution boundaries, reuse, AI-assistance disclosure, stable citations
and the preservation of this edition, see
[AUTHORSHIP_AND_CITATION.md](AUTHORSHIP_AND_CITATION.md).
Earlier theorems retain their original attribution; repository authorship
and successful reproduction do not establish first discovery.

## Entry-specific contribution map

The [complete contribution map](CONTRIBUTION_MAP.md) enumerates all 228
catalogue positions and distinguishes earlier strict results and their
consequences, earlier analytical expressions, the exact proof materials
supplied in this edition, elementary results and unresolved entries.
The [release description](RELEASE.md) provides a concise overview and links to these distinctions.
Catalogue totals and successful proof replays are not novelty counts.
