# Distribution, citation and archiving

The repository is named `bell-quantum-suprema`. Its first edition is `v1.0.0`.
The repository includes three named catalogue directories; their established
entry numbering is preserved. Catalogue-level metadata documents the
constituent volumes, while root `CITATION.cff` identifies this combined edition.

## Two distribution forms

1. **Lightweight Git source edition.** It contains the readable definitions,
   proof descriptions, programs, bibliography and certificate descriptors.
   The large binary certificate and runtime payloads listed in `PAYLOADS.json`
   are omitted. It is suitable for a normal Git upload.
2. **Complete offline edition.** It contains the same source files and every
   listed payload. The complete master ZIP and its ordinary ZIP volumes are
   release artifacts. All volumes of the complete edition must be extracted
   into one directory for full offline reproduction. No file must be obtained
   from another research repository.

These are two distribution forms of one mathematical edition, not different
sets of claimed results. The manifest records relative paths, file sizes and
cryptographic digests. `SOURCE_FILES.sha256` covers the lightweight source
inputs; `SHA256SUMS.txt` covers the complete extracted tree. The root checksum
file excludes itself. The source checksum file excludes both checksum files,
avoiding circular hash definitions. Neither file-integrity procedure replaces
mathematical verification.

GitHub's automatically generated **Source code.zip** contains the Git tree
only. It is not the complete proof package when the large payloads are stored
as release attachments. The release description must retain this distinction.
The supplied verification programs do not download missing files. Complete
replay uses Windows x64 with CPython 3.12 and their separately installed
platform runtime components. Arithmetic libraries and native verification
programs are included; PowerShell/.NET and MSVC runtime DLLs are not bundled.
The local NumPy build is documented in the runtime source-supply statement.

## Upload and reproduce

Follow [UPLOAD.md](UPLOAD.md) for the source upload and complete-release
attachment procedure. Preserve all catalogue licenses, references and
third-party notices. Do not upload private working directories, old research
archives or execution logs. Do not place the complete large ZIP in Git.

The ordinary release volumes are independent ZIP archives, each containing
a disjoint subset of the complete tree. Extract every volume into the same
empty directory. They are different from the binary certificate fragments
inside a York entry; keep those fragments in their distributed order and
location. The complete master ZIP is an alternative local distribution of
the same file tree, not an additional required input.

After extraction:

```console
python -B verify.py --files
python -B verify.py --definitions-only
python -B verify.py --all
```

The source edition can be checked with `python -B verify_files.py --source-only`.
Its successful file check does not imply that absent proof payloads are present.

## Citation and DOI

Use the author, title and release version in `CITATION.cff`. The maintainer's
ORCID identifies the person and is not a mathematical dependency. A version
DOI should be added only after the actual edition is archived and a real DOI
has been issued. Cite the original theorem separately when using an entry
whose proof relies on it. There is no preassigned DOI in this distribution.

For a durable archive, include the **complete offline artifacts**, their
checksums and the release description, not only the lightweight Git tree.
Confirm what an archiving service actually ingests; automatic source capture
alone need not include release attachments. A version DOI identifies one
fixed edition; a concept DOI can additionally identify its sequence of versions.

If a tagged edition has already been publicly released, preserve that tag
and archive. Publish changed mathematical or distribution inputs under an
appropriate new version rather than replacing a publicly cited artifact.

## Runtime corresponding sources

The complete release also contains the corresponding-source archives and
build materials identified in [the runtime source-supply documentation](third_party/runtime/SOURCE_SUPPLY.md).
These are supplementary source materials for the bundled software; they are
not new mathematical certificates and are not needed to execute a proof.
The lightweight Git edition omits these archives alongside the large proof
and runtime payloads. Their versions, licenses, origins and checksums remain
documented in the Git edition, and every source archive is included in the
complete release volumes and master archive. Keep these materials with the
binary distribution when archiving or redistributing the complete edition.

The project's MIT license does not replace third-party licenses. See
[RIGHTS.md](RIGHTS.md), [CONTRIBUTIONS.md](CONTRIBUTIONS.md) and
[PROVENANCE.md](PROVENANCE.md) for the respective licensing and attribution scope.

When describing an archival deposit, state explicitly that this is a mixed-license
distribution: MIT covers the project's own contributions, and the bundled
third-party components retain the licenses identified in the source-supply
statement. Do not describe the complete archive as exclusively MIT-licensed.
