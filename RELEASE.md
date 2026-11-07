# v1.0.0 — Exact Quantum Suprema and Certificates for Selected Bell Scenarios

**Author and maintainer:** Yang-Guang Yang  
**Email:** yangyangguang1991@gmail.com  
**ORCID:** https://orcid.org/0000-0001-9236-7544

First repository edition, containing three Bell-inequality catalogues with
their original indices and normalizations:

- **Śliwa S001–S046:** all 46 entries have exact global upper proofs and
  attaining three-qubit strategies.
- **The (6,3,2,2) catalogue:** all seven facet classes, their exact-value
  proof materials, and reproduction of the complete facet classification.
- **York Y1–Y175:** 171 exact suprema with proof materials and four entries
  whose exact unrestricted quantum suprema remain unknown.

Six bipartite classes occur in both catalogues and retain complete local
proofs at both positions. These repeated positions are not additional
results. Closed entries supply a dimension-independent upper argument and
a matching attaining strategy or approximating family. The $I_{3322}$
entry uses an exact variational characterization and states attainment
separately. Unknown entries retain their numbering without numerical bound
intervals.

## Authorship and contributions

Except for the earlier results and third-party contributions expressly
credited in this repository, the mathematical proof and certificate
constructions, attainment or approximation materials, exposition and
verification implementations supplied in this edition are the work of
Yang-Guang Yang. Historical inequalities, classifications, analytical
expressions and theorems retain their original attribution. The
[entry-by-entry contribution map](CONTRIBUTION_MAP.md) and
[historical notes](HISTORY.md) give the detailed distinctions and references.

## Download and reproduce

Download all complete-release ZIP volumes and extract them into the same
directory, or use the complete master ZIP. GitHub's automatic source-code
archive omits the large certificate and runtime payloads.

The complete collection runs offline on Windows x64 with CPython 3.12;
the required arithmetic libraries and native verification programs are
included. Windows and the interpreter are separate prerequisites. From
the extracted repository root:

```console
python -B verify.py --files
python -B verify.py --all
```

The first command checks file integrity; the second executes the supplied
proof schedules. See [MANUAL.md](MANUAL.md) for individual entries and
[DISTRIBUTION.md](DISTRIBUTION.md) for the file layout and requirements.

## Citation and licensing

Use [CITATION.cff](CITATION.cff) to cite this repository edition and cite
the original mathematical sources relevant to the results used. Once the
complete edition is archived, use its registered version DOI for the
corresponding files.

The [MIT License](LICENSE) covers the project's eligible original material.
Third-party components retain their own licenses and notices; the complete
distribution is not exclusively MIT-licensed. See [RIGHTS.md](RIGHTS.md),
[third-party notices](THIRD_PARTY.md) and
[corresponding-source information](third_party/runtime/SOURCE_SUPPLY.md).
Authorship, citation and computational-assistance details appear in
[CONTRIBUTIONS.md](CONTRIBUTIONS.md).
