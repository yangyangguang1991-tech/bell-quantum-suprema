# Reproduction manual

## Distribution and environment

Use the complete offline distribution for mathematical reproduction. The
lightweight Git source edition is suitable for browsing and reviewing the
definitions and programs. It omits the payloads listed in `PAYLOADS.json`.
Obtain all complete-release volumes and extract them into the same empty
directory; the resulting root contains this manual and `verify.py`.

The common supported full-replay environment is 64-bit Windows, x86-64,
with CPython 3.12. Required arithmetic libraries and native verification
programs are included in the complete distribution. Windows and CPython,
including the interpreter's platform runtime components, are prerequisites;
Python itself is not included. No PowerShell/.NET distribution or MSVC runtime
DLL is bundled. The NumPy source variant, binary64 ABI patch, component notices
and rebuild instructions are documented under `third_party/runtime/`.
Use a short extraction path, for example `C:\BellProofs\bell-quantum-suprema`,
to avoid operating-system path-length limitations. No administrative access,
network access or change to system execution policies is part of verification.

Individual catalogue support is broader where stated: six-by-three uses only
the standard library of Python 3.10 or later, while Sliwa supplies SymPy and
mpmath sources for Python 3.11 or later. Those facts do not establish complete
York replay on every such platform. Do not replace the bundled arithmetic
runtime with unrelated installed versions as part of a claimed reproduction.

## Verification levels

These commands have different mathematical scopes:

```console
python -B verify_files.py --source-only
python -B verify.py --files
python -B verify.py --definitions-only
python -B verify.py --all
```

The first checks the source-edition files against `SOURCE_FILES.sha256`.
The second checks the complete distribution against `SHA256SUMS.txt`.
Neither checks a mathematical theorem. The third checks all numbered entry
definitions and the exact bipartite coefficient correspondences; it does
not run the global upper and attainment proofs. The fourth runs the complete
supplied proof schedules and the six-by-three classification. It also visits
the four unresolved York entries and prints their unknown statements.

For the full run, the program sequentially invokes all 46 Sliwa entries,
the seven-entry six-by-three command including facet classification, and
all 175 York positions. The Sliwa schedule contains 52 upper-verifier calls.
York contains 171 exact-value proofs and four unknown statements. Counts
refer to catalogue positions, so the six shared bipartite classes occur twice.

Every command reports failures through a nonzero process exit status. A missing
payload, invalid coefficient binding, failed exact positivity condition or
failed strategy check must be resolved before accepting that entry. A digest
or an earlier execution report is not a replacement for the full command.
Use ordinary Python with assertions enabled; the dispatcher rejects `-O`
and `-OO`. Proof runs can require substantial time, temporary disk space
and memory. The default dispatcher runs one catalogue process at a time.

## Individual entries and catalogues

```console
python -B verify.py --catalogue sliwa --entry 21
python -B verify.py --catalogue six-by-three --entry 4
python -B verify.py --catalogue york --entry 139
python -B verify.py --catalogue sliwa --all
python -B verify.py --catalogue six-by-three --all
python -B verify.py --catalogue york --all
```

Sliwa uses indices 1-46; six-by-three uses 0-6; York uses 1-175.
The unqualified `--all` command visits every catalogue. An individual unknown
York entry prints `Exact unrestricted quantum supremum: unknown.` and does
not claim to verify an upper or attaining proof.

The dispatcher locates the catalogues relative to its own script and uses
their original public entry points. It does not infer a proof from the
metadata. Each catalogue may also be run directly using its own manual.
Individual entry subdirectories are not standalone distributions: keep their
shared catalogue programs and runtime directories.

## Original definitions and exact values

Sliwa uses raw correlator functionals with its stated local bounds. The
bipartite tables contain the constant, both marginals and the joint
probabilities, with the local bound normalized to zero. Mixing these
normalizations can change a displayed value; always use the accompanying
literal expression and coefficient mapping.

Each exact root is selected by its own isolating interval or box. For a
polynomial system the specified solution, nonzero denominators and relevant
positivity conditions are part of the definition. Decimal approximations
are for reading and independent score checks, not substitutions for exact
parameters. The I3322 value uses an explicit Jacobi-path variational
definition and a convergent legal strategy family. The distinction between
finite attainment, an unrestricted supremum and infinite-dimensional
attainment is retained in its proof and references.

## Upper and attainment materials

The complete entry materials supply both directions of the claimed equality:
a bound covering arbitrary Hilbert-space dimension and a physical strategy
achieving it, or a rigorously specified sequence approaching it. They also
bind the certificate to the original functional. The generic root wrapper
does not replace any of those checks.

Sliwa entries expose exact states and measurement matrices, plus independent
decimal score computations. Its [proof guide](catalogues/sliwa-46/docs/PROOF_GUIDE.md)
explains the arbitrary-dimension reduction and exact positivity algorithms.
The [six-by-three manual](catalogues/six-by-three/MANUAL.md) explains its
quadratic fields, directed-word Gram certificates and spectral identities;
[FACETS.md](catalogues/six-by-three/FACETS.md) proves catalogue completeness.
The [York manual](catalogues/york-4422/MANUAL.md) specifies the different
certificate formats and their exact replay schedules.

## Outputs and immutable inputs

The root dispatcher does not edit distributed proof inputs. The Sliwa
entry point may create its documented `exports/` and `verification_runs/`
directories; its verification algorithm checks fresh temporary proof outputs
and compares the bound inputs. York reconstructs certificate archives in
temporary directories and checks them against each entry's proof descriptor.
Keep generated output outside versioned proof inputs and preserve the supplied
`.gitattributes` rule when committing the source edition.

## Historical citations and unknown entries

The entry-level bibliographies credit identified prior strict exact-value
results. Broader numerical, classification, algorithmic and computational
references remain in the catalogue histories linked from [HISTORY.md](HISTORY.md).
Unknown entries carry no numerical interval or entry-level theorem bibliography.
The absence of an exact value is not a claim that all methods have been exhausted.

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
