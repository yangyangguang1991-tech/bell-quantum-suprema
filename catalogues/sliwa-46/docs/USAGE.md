# Verification and reproducibility

## Installation

Extract the archive and open a terminal in the directory containing `run.py`. On Windows, a short destination such as `C:\BellProofs` avoids legacy path-length limits in external extraction tools. Python 3.11 or later, including its standard `venv` module, is sufficient. On Windows, `py -3` can replace `python`; on Linux and macOS, use `python3` if appropriate.

The `-S` option skips system site packages. The entry point locates the bundled libraries. Upper-bound subprocesses run in a temporary empty environment, created without pip or inherited site packages. The environment and execution copies are removed after verification. The execution layer checks the unchanged contents of the inputs used by every required command.

## Commands

List the values:

```text
python -S run.py list
```

Check the integrity manifest:

```text
python -S run.py manifest
```

Verify a complete upper-and-attainment chain:

```text
python -S run.py verify --id 21
python -S entries/S021/verify.py
```

Verify the complete catalogue:

```text
python -S run.py verify --all
```

Run only the exact upper proofs, including the literal characteristic binding:

```text
python -S run.py upper --id 21
```

Regenerate states and measurements:

```text
python -S run.py export --id 21 --digits 80
python -S run.py export --all --digits 80
```

`export` does not replay the global upper proofs. An optional `--report exports/run-report.json` saves the selected command's execution record. The `exports/` directory is excluded from Git and the integrity manifest.

## Per-entry inputs

`functional.json` specifies the exact literal expression, local bound and observable convention. Uppercase and lowercase letters distinguish the two settings of a party: `A,a; B,b; C,c`. No constant shift or scale factor is implicit.

`strategy_spec.json` specifies the exact Bell value and three measurement overlaps. Univariate roots include a polynomial and rational isolating interval. Polynomial systems include the variable order, equations and rational root box.

`upper_bound/inputs.json` identifies the entry's characteristic polynomial and the exact programs to run. It must match the fixed per-entry schedule in `bellverify/replay_contract.py`, including entry identity, engine, characteristic file and ordered commands. The complete catalogue requires 52 upper-verifier invocations. Shared algorithms receive only this entry's inputs. The remaining files in `upper_bound/` are the certificate data and programs required by this upper proof. S16 and S46 include additional explanations of their boundary reductions.

Before and after each invocation, the execution layer checks the original entry and the temporary execution copy for unchanged input contents and consistent exact targets. Each command's permitted output files are specified by the verification code. For S28, the generated root-replay result becomes a fixed input for the subsequent global check. The S46 boundary verifier writes `verification_46_reduced.json` separately from the supplied certificate. The S40 upper-value interval must equal the contact root interval and the interval defined by its rational centre and radius.

## Attaining states

`attainment/strategy_numeric.json` contains:

- `basis_order`: `000,001,010,011,100,101,110,111`;
- `state_vector_real`: the eight normalized real amplitudes;
- `observables_real`: the six matrices named `A,a,B,b,C,c`;
- `q_display` and `overlaps_display`: numerical displays of the exact selected parameters.

The two outcome effects of an observable `O` are `(I+O)/2` and `(I-O)/2`. Decimal matrices are rounded displays; exact reflection identities follow from the algebraic definitions. Measurement factors `sqrt(1−x²)`, `sqrt(1−y²)` and `sqrt(1−z²)` use the nonnegative branch, including zero at endpoint overlaps.

`floating_point_eigen_residual_display` is evaluated by rebuilding the Bell matrix from the published `observables_real`, then applying it to the published `state_vector_real` and `q_display`. The `residual_evaluation` object records the input fields and arithmetic precision. This residual concerns the rounded export. The residual of the unrounded internal state is used only as a construction check.

`attainment/strategy_exact.json` contains the parameter definitions, symbolic observables, Bell matrix, eigenvalue multiplicity, complementary characteristic polynomial, fixed column index and finite arithmetic graph for all eight normalized amplitudes. References in the graph point only to earlier nodes or defined algebraic parameters. A strict positive rational interval for the unnormalized squared norm certifies that the chosen state is nonzero; its normalization uses the strictly positive square root. The manuscript table takes the multiplicity from the exact attainment binding and cross-checks it with the historical comparison data.

Regenerated exports additionally contain `state_vector.csv`, `measurements.csv`, `independent_score.json` and `independent_dag_audit.json`. CSV matrix row and column indices start at zero. No unresolved eigenvector choice is left to the user.

## Independent checks

```text
python -S tools/check_strategy.py entries/S021/attainment/strategy_numeric.json
python -S tools/check_exact_dag.py entries/S021/attainment/strategy_exact.json entries/S021/attainment/strategy_numeric.json
```

The score checker reconstructs every tensor-product correlator directly from the supplied matrices and amplitudes. It checks normalization, self-adjointness, reflection squares, the term-by-term score, an independently assembled Bell-matrix score and the eigen-equation residual. The graph checker independently evaluates the finite amplitude formulas. These decimal checks complement the exact algebraic proofs.

## Specified negative controls

The control programs exercise particular altered inputs:

```text
python -S tools/test_negative_controls.py
python -S tools/test_exact_controls.py
python -S tools/test_selector_controls.py
python -S tools/test_geometry_controls.py
python -S tools/test_target_binding_controls.py --output ../sliwa-target-controls-v1.0.0
python -S tools/test_obligation_controls.py --output-dir ../sliwa-obligation-controls-v1.0.0
python -S tools/test_public_regressions.py --output ../sliwa-public-controls-v1.0.0
```

The report directories must be new directories outside the repository. The first three programs cover supplied numerical strategies and amplitude graphs, exact literal/parameter binding and compact selectors. The geometry controls check the original S21, S27 and S33 input bindings and reject unequal first-two contact intervals in S21, and negative or reversed upper-value intervals in S27 and S33. These are the premises used by the symmetric slab construction and signed-power bounds, respectively. The target-binding controls cover changed proof schedules, inconsistent S46/S40 targets, changes during execution and intermediate-result freezing. The obligation controls cover missing or duplicate exterior slabs, coefficient indices, named obligations and leaf paths in the affected positivity verifiers. The public-entry regression controls rebuild and successfully check the mutated copy's manifest before requiring the actual public verify command to reject the historical S46, S2 and S40 defects. Consult each execution record for the exact tested mutations and results. A finite control suite does not establish rejection of every possible altered file.

## Integrity and maintenance

`MANIFEST.sha256` covers the distributed sources and inputs. Generated `exports/` and `verification_runs/` directories are excluded from this source manifest; the release contains the proof inputs and verification software. A mismatch indicates missing, extra or changed tracked files. Review intentional edits before updating the manifest with `python -S tools/write_manifest.py`.

Keep S001–S046 and their normalizations fixed. After a mathematical edit, regenerate the affected strategy, verify its full upper-and-attainment chain, run the independent checks, update the manifest and publish a new version. Preserve published version tags.

Certificate programs use assertions. Full verification rejects `-O/-OO`. The supplied standard-library fast checks can also run in optimized mode. An optimized-mode control run has only the scope recorded for that command; it does not replace assertion-enabled upper verification.
