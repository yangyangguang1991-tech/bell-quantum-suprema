Independent exact audits
========================

These programs independently reconstruct selected parts of the proof using
Python's standard library. They do not import bellverify, prooflib, SymPy or
mpmath. Their scopes are deliberately separate:

* independent_attainment_audit.py: all 46 exact parameter selections,
  characteristic multiplicities, physical Bell matrices, actual arithmetic
  graphs, nonzero columns and normalized attaining states. Arithmetic uses
  rational numbers, quotient algebras and outward rational intervals.
* independent_charpoly.py: all 46 literal characteristic identities. The
  finite integer grid is accompanied by a proved per-axis degree bound.
* recheck_boundaries_stdlib.py: all algebraic reductions, domain checks and
  positivity coefficients for S16 and S46; not the other 44 global bounds.
* audit_frozen_tables_and_obligations.py: the exact tables, required proof
  obligations and every covering tree; this structural audit does not itself
  determine positivity signs.
* audit_local_facets.py: local maxima, facet ranks and inequivalent orbits of
  the 46 supplied representatives; not an enumeration of all halfspaces.
* audit_primary_benchmarks.py: literal coefficients and historical reported
  values against the adjacent primary_source_values.json. It compares the
  supplied exact enclosures; their validity is checked by the other audits.
* check_independent_kernel_controls.py: targeted negative controls for the
  independent attainment implementation. Keep it beside that implementation.

From the package root, use an output path OUT outside this package:

python -S tools/independent/independent_attainment_audit.py . --output OUT
python -S tools/independent/independent_charpoly.py . --output OUT
python -S tools/independent/recheck_boundaries_stdlib.py . --output OUT
python -S tools/independent/audit_frozen_tables_and_obligations.py . --output OUT
python -S tools/independent/audit_local_facets.py . --output OUT
python -S tools/independent/audit_primary_benchmarks.py . --output OUT
python -S tools/independent/check_independent_kernel_controls.py . OUT

Choose a distinct output file for each command. Some audit programs snapshot
their inputs, so run them while the package is otherwise unchanged. These
audits supplement the complete released verification chain:

python -S run.py verify --all

Finite decimal score checks and exact global proof checks retain their
different meanings. A passing numerical residual alone is not an equality
certificate.

Fresh release replay (OUT must not exist):
  python -S tools/independent/replay_release.py RELEASE.zip OUT --workers 4
This launches the package public verifier for all 46 entries; it is a replay
driver, not a separate mathematical implementation of the 44 non-boundary
upper proofs.
