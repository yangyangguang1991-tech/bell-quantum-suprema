# Publishing and archiving this repository

This guide describes actions performed by the maintainer. The delivered files
do not create a remote repository, publish a release, or register a DOI.

## Choose the correct distribution

The `bell-quantum-suprema-v1.0.0-source.zip` archive is the lightweight Git upload edition.
It contains readable documentation, original definitions, programs and a
manifest of the large certificate and runtime files. It intentionally omits
those large binary files. GitHub's automatically generated source archive
therefore is not the complete offline proof distribution.

The `bell-quantum-suprema-v1.0.0-complete.zip` archive is the complete offline edition.
Alternatively, extract every supplied ordinary release volume into the same
empty parent directory. Each volume contains a disjoint part of the same
repository tree; no external research archive or software download is needed.
Do not concatenate these ordinary ZIP volumes. The binary certificate parts
inside individual entries are different: the verifier assembles them itself.

Python is a platform prerequisite. The complete supported reproduction
environment is 64-bit Windows on x86-64 with CPython 3.12. Consult MANUAL.md
for the mathematical scope and per-catalogue commands.

## Upload the lightweight Git edition

1. Extract the source archive into a short directory, such as `C:\BellRepos`.
   Open PowerShell in the resulting `bell-quantum-suprema` directory.
2. Check the included source files:

   ```powershell
   python -B verify_files.py --source-only
   ```

   This command checks file integrity only. It does not prove a quantum bound.
3. Prepare a local Git repository:

   ```powershell
   git init -b main
   git config user.name "Yang-Guang Yang"
   git config user.email "yangyangguang1991@gmail.com"
   git add .
   git status --short
   git commit -m "Initial release v1.0.0"
   ```

   Retain `.gitattributes` and `.gitignore`. They preserve certificate bytes
   and keep the large release payloads outside ordinary Git history.
4. In GitHub, create an empty repository named `bell-quantum-suprema` under
   `yangyangguang1991-tech`. Do not initialize another README or license there.
   Use GitHub's normal authentication flow; no access token belongs in these files.
5. Connect and push the local repository:

   ```powershell
   git remote add origin https://github.com/yangyangguang1991-tech/bell-quantum-suprema.git
   git push -u origin main
   git tag -a v1.0.0 -m "Version 1.0.0"
   git push origin v1.0.0
   ```

These commands assume a new repository and an unused tag. Existing public tags
identify immutable editions; use a new version for a later corrected edition.

## Create the complete GitHub Release

Create a release from `v1.0.0`. Use the text of RELEASE.md as its description.
Upload all `bell-quantum-suprema-v1.0.0-volume-*.zip` files and the accompanying
`RELEASE_SHA256SUMS.txt`. These volumes provide the complete offline tree,
including the small source files. Keep all volumes together in the same release.

GitHub currently limits a release asset to less than 2 GiB; the supplied
volumes are smaller than 1 GiB. The large complete master ZIP is convenient
for local delivery or archival deposit, but should not be uploaded as a single
GitHub asset if it exceeds that platform limit.

After downloading all assets into a fresh location, check their SHA256 digests,
extract them and run the complete file check and the full proof commands in
MANUAL.md. A file digest is a binding to proof inputs, not a mathematical proof.

## Create a citable archival record

For a DOI covering the complete proofs, create a manual Zenodo deposit of
the complete master ZIP and its checksum file, with RELEASE.md as a readable
description. Do not assume that an automatic archive of the lightweight Git
tree contains the separately attached proof payloads. Inspect the actual
archived files before publishing the record.

Use the repository title and version from CITATION.cff; author
Yang-Guang Yang; ORCID `0000-0001-9236-7544`; and the GitHub release as a related
identifier. Use the applicable software license and retain all bundled
third-party notices. The current standard Zenodo upload allowance is 50 GB
and 100 files, sufficient for this edition's complete master archive.

Zenodo can reserve a DOI while a deposit is still a draft. No DOI is invented
in this distribution. After registration, put the real version DOI on the
GitHub release page. Cite that version DOI when referring to these exact files.
If a DOI is subsequently embedded into archived README/CITATION files, those
file hashes change: rebuild and verify that new archive before publishing it.
Keep already published mathematical editions identifiable by their original
checksums. Each of the two repositories can have its own archival record.

## Official publishing documentation

- [GitHub repository limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits).
- [GitHub release assets](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).
- [Zenodo: create a new upload and reserve a DOI](https://help.zenodo.org/docs/deposit/create-new-upload/).
- [Zenodo: manage files](https://help.zenodo.org/docs/deposit/manage-files/).

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

## Preserve the published edition and its credit

Before the first public release, open the repository's **Settings**, find
**Releases**, and enable **release immutability**. Create the release as a
draft, upload every ordinary volume and its checksum, and verify the draft
contents before publishing it. Once immutable, the assets and associated
tag cannot be replaced. Corrections require a new version, not a reused tag.
The official instructions are
[Preventing changes to your releases](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/prevent-release-changes).

Retain the published commit, archive checksums, release description, original
research records and Zenodo deposition record. Archive the complete mathematical
distribution and use its real version DOI in citations. Keep the substantive
release description inside the archive because GitHub release notes can still
be edited. Describe any new theorem in a readable research note with precise
earlier-work comparisons; publication infrastructure alone does not establish
that a theorem is new. Do not invent or backdate identifiers or dates.

The credit, licensing and AI-assistance boundaries are explained in
[AUTHORSHIP_AND_CITATION.md](AUTHORSHIP_AND_CITATION.md). These are publication
instructions for the maintainer; this local delivery has not performed any
remote publication, account-setting change or DOI registration.

## Paste the release description into a web form

The relative links in RELEASE.md work when that file is viewed in the
repository. Before pasting it into a standalone GitHub Release description,
convert those links to the fixed version's file URLs. From this repository's
root, the following PowerShell commands copy that version to the clipboard
without modifying any archived file:

```powershell
$releaseText = Get-Content -LiteralPath 'RELEASE.md' -Encoding UTF8 -Raw
$tagRoot = 'https://github.com/yangyangguang1991-tech/bell-quantum-suprema/blob/v1.0.0/'
[regex]::Replace($releaseText, '\]\((?!https?://|mailto:|#)([^)]+)\)', { param($m) '](' + $tagRoot + $m.Groups[1].Value + ')' }) | Set-Clipboard
```

Paste the result into the release editor and inspect its preview. The
version links become available after the v1.0.0 tag has been pushed. The
release description provides a concise overview; entry-specific
contribution details remain in CONTRIBUTION_MAP.md and HISTORY.md.
