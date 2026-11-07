# Reproduction manual

## Read one theorem

Open the numbered folder in `entries/`. `definition.json` gives the 5-by-5 CH coefficient array and an exact map to the traditionally named correlator. In row zero, column zero is the constant and the other columns are Bob marginals. In each subsequent row the first entry is the Alice marginal and the remaining four entries multiply the joint probabilities. The displayed exact value refers to this CH table. The sign and scale written in the crosswalk are essential when comparing traditional tables.

For the mathematical derivation read `PROOF.md`. Each closed entry includes its own compressed proof core. `proof.json` lists its parts in order and records the digest of the concatenated ZIP. The script reconstructs these bytes before extracting. Identically named files in two different entries have separate roles and must stay with their own table. To inspect every word, coefficient, state parameter and measurement chart, use `python verify.py 7 --extract Y007-proof` with a destination that does not yet exist. The certificate can be read without building any other entry.

## Replay

Run commands from this catalogue's root, the directory containing this `MANUAL.md` and `verify.py`. In a combined repository, enter the York catalogue directory first. Use Windows x86-64 with a separately installed 64-bit CPython 3.12. All certificate data are included. Certificates that require a directed normal-map calculation contain `native_interval/normal_map.c`, its Windows executable, the Python binding, fixed dimension configuration, build instructions and licenses. The verifier runs that executable directly; it does not invoke PowerShell or a C# compiler. The shared `runtime/` folder supplies SymPy/mpmath, python-flint and the numerical libraries needed by the larger checkers. NumPy is the documented local binary64 Windows build; SciPy is also supplied. Complete source and license records are in the combined [runtime source inventory](../../third_party/runtime/SOURCE_SUPPLY.md).

No PowerShell/.NET distribution or MSVC runtime DLL is bundled. Windows and the installed Python interpreter, including its own platform runtime, are external prerequisites. Local security policies must permit running the supplied programs. No network request, compiler installation or SDP solver is part of acceptance. The supplied native programs target Windows x86-64; another platform requires a separate compatible arithmetic environment and is outside this bundled reproduction configuration. Use default Python assertion settings; do not pass `-O`. Keep the temporary directory path short. Allow several gigabytes of temporary disk space for the largest checkers.

```console
python verify_files.py
python verify_names.py
python verify.py 2
python verify.py 7
python verify.py 139
```

`python verify_files.py` checks the release file hashes; it does not check the mathematical proofs. `python verify_names.py` checks the coefficient relabellings. Run `python verify.py N` for the mathematical proof of any catalogue number. It reconstructs the local certificate, runs its stages and raises an error if any stage fails. Some checks require significant CPU time. Word coefficients, projection and score identities, root isolation, interval invertibility and strict positivity are distinct operations. A successful coefficient or fingerprint test alone cannot certify a quantum value. Open entries have no numerical endpoint or proof core.

## Interpreting the proofs

The reflection relation is intra-setting involutivity. Every Alice operator commutes with every Bob operator. Distinct choices by the same observer need not commute. A binary effect can be dilated to a projection with a private ancillary space while preserving the original Bell terms. The lower construction alone may choose a Schmidt form, a finite real parametrization or prescribed ranks. No such choices restrict the unrestricted upper argument; an entry may use a universal operator identity or necessary conditions at a global maximizing state, as specified in its proof.

Explicitly, for any effect E set S=(E(I−E))^(1/2) and form the two-by-two block matrix with diagonal E and I−E and both off-diagonal entries S. It is self-adjoint and its square equals itself because S commutes with E. Use the same two-dimensional auxiliary coordinate for every setting on Alice, and a second, private coordinate for all Bob settings. Entries from opposite observers commute by continuous functional calculus. On the original state tensored with the first basis vector of each coordinate, each marginal and each cross-party joint expectation compresses to its undilated value.

For implicit algebraic values the enclosed box and polynomial equations select the strategy. Their denominators are checked on the selected box. In a typical implicit Gram proof one forms the physical action matrix, uses its kernel to reduce the word basis, and considers the linear map from a Gram matrix to the coefficients of its square. The value and first derivatives of the attaining strategy supply the exact orthogonality conditions. Invertibility in the complementary space permits a correction at the very same root. A rigorously positive corrected Gram matrix yields the global operator inequality. Entries employing another method supply their own proof.

For a two-qubit Pauli certificate the normalized state is `(|00>+|11>)/sqrt(2)`. A transposed Alice response is essential for Pauli Y. For projection charts, construct the state and projections from the root rather than substituting rounded printed coordinates. For I3322 see the separate path construction, convention conversion and strict-value papers in Y003.

The largest files hold entry-specific preconditioners and Gram input, often stored in binary64. In these certificates their stored bit patterns define exact dyadic rationals. The directed residual check proves that the preconditioner is close enough to the true inverse; a floating-point inverse by itself would give no upper proof. The binary inputs are split for distribution without changing their bytes.

## Worked entry selection

* **Y2, CHSH.** Run `python verify.py 2`. The core gives the elementary reflection-square identity, the state and the four active reflections. Their signed permutation gives this York row.
* **Y3, I3322.** First read this catalogue's `entries/Y003/PROOF.md`, which states the literal York polynomial, its path constant, and the exact change from the enclosed source convention. Run `python verify.py 3 --extract Y003-proof` to inspect the local inputs. Inside that extracted core, `entries/02-I3322/PROOF.md` and `sequence.py` use the source three-setting coordinates. Apply the explicit map in the outer proof to obtain the four York measurements of each party; only the fourth setting of each party is unused in the York table. The outer proof gives the unrestricted upper bound and the convergence argument. The separate bibliography attributes finite-dimensional nonattainment and normal infinite-dimensional attainment to the stated external theorems.
* **Y25, correlation-only.** Run `python verify.py 25` for an exact Pauli contraction and read the scalar upper argument in the entry proof. Y74 gives the other four-setting correlation type and constructs four-dimensional Clifford matrices.
* **Y23, explicit Gram.** Run `python verify.py 23 --extract Y023-proof`. Read `strategy.json` for the two-qubit state convention and the eight matrices. The separate `gram.json` holds the coefficient field, basis and factor; `verify.py` in the extracted folder verifies both sides.
* **Y7, implicit Gram.** Run `python verify.py 7 --extract Y007-proof`. The root file selects the 18 coordinates; `family.py` and `family_r3.py` specify the state and eight independent projections. The proof uses the full-rank jet and interval Neumann calculation to construct the matching Gram.
* **Y165, higher-word correction.** Run `python verify.py 165`. The root input fixes the physical directions, the symbolic free lift addresses the high-word coefficients and the Gram correction is checked at that same root.
* **Y139, optimal-state proof.** Read `entries/Y139/PROOF.md` for the two-qubit state, the explicit ten-equation root and the legal positive forms. Run `python verify.py 139` for the kernel, Ward, affine correction and matrix positivity steps and the independent original-score reconstruction.
