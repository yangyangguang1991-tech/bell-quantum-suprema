# Replacing and rebuilding the LGPL runtime libraries

The distributed archive hashes identify the published proof inputs. They are not a restriction on a recipient's right to modify the LGPL libraries. Use a separate writable directory for a modified runtime; do not overwrite the original certificate archive when recording a reproduction.

The following commands use the complete offline release and a compatible Windows x64 Python. The release verification environment is Python 3.12; python-flint's supplied wheel uses the CPython 3.10 stable ABI. Run commands from the repository root. The helper does not download or install anything.

```text
python third_party/runtime/tools/runtime_workspace.py extract ../modified-runtime
python third_party/runtime/tools/runtime_workspace.py probe ../modified-runtime
```

The default extracts only python-flint and its native libraries. Add `--all-components` when the proof script also requires SymPy, NumPy or SciPy. The destination must be new and outside the release directory. Original archive hashes are checked during extraction. Afterwards, the probe loads libraries from that writable directory without demanding the original DLL hashes.

## A reproducible replacement demonstration

```text
python third_party/runtime/tools/runtime_workspace.py demonstrate-replacement ../modified-runtime
```

On the original supplied FLINT DLL, this command changes only the exported version string from `3.6.0` to `3.6.R`, loads the modified DLL in a new process, and performs exact integer and rational matrix calculations and an Arb containment check. It records the before/after DLL hashes in the workspace. Arithmetic code is unchanged. This is a test of the replacement mechanism, **not** a claim that every modified library is ABI-compatible, that a complete source build was performed, or that the demonstration is a Bell proof. The helper refuses to modify the release directory or an unexpected DLL.

## Building a substantive replacement

The exact upstream python-flint source archive and all three LGPL library sources are in `sources/`; their hashes are recorded in `sources.sha256`. Inspect `build-recipes/python-flint/bin/build_variables.sh`, `bin/build_dependencies_unix.sh`, `bin/cibw_before_all_windows.sh`, `bin/patch-C23.diff`, `pyproject.toml`, and `.github/workflows/buildwheel.yml`. Those are the upstream Windows build instructions and interface definitions, including the required GMP C23 patch. The original workflow uses an MSYS2 UCRT64 GCC toolchain for the native libraries and an MSVC-compatible build for the Python extension. General-purpose compilers and build tools must be supplied by the person rebuilding.

Retain the shared-library ABI, architecture, exported symbols, and dependency compatibility when replacing only a native library. The original `delvewheel` repair step gives DLLs collision-resistant names. Either provide the replacement at the imported name together with its compatible dependencies, or rebuild and repair the Python wheel so its import tables use the new names. Do not merely rename a DLL with an incompatible ABI. No publisher signature or secret key is needed to load compatible replacements in the extracted Python environment.

The source archives plus build scripts describe how the supplied upstream libraries were built; they are not a promise of reproducible toolchain timestamps or identical compiler output. The source licenses, including the LGPL/GPL text, remain in the source archives and in `licenses/`.

## Running a proof with a modified runtime

Use the relevant catalogue's existing `--extract` option to place the certificate in a new writable directory. Its `proof.json` specifies the proof commands. Preserve the original coefficient binding and execute the documented proof commands with `PYTHONPATH` set to the extracted runtime. For example, in PowerShell:

```powershell
# Set this to the directory created above, using an absolute path.
$env:PYTHONPATH = (Resolve-Path ../modified-runtime).Path
$env:PYTHONNOUSERSITE = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
# Change to the extracted certificate directory and run its documented commands.
```

Use the entry's exact command and working-directory convention; some scripts launch other scripts. The standard top-level replay command deliberately re-extracts the published runtime, so use the extracted proof scripts when testing a replacement. York Y059, Y124, and Y168 additionally have embedded python-flint copies under their certificate directory. Replace those copies as well, or explicitly adjust that extracted script's module path to the modified runtime; record which files were changed. Never describe a run against changed mathematical definitions as a replay of the published theorem.

There is no requirement to obtain permission from this project to modify or debug LGPL components. A modified runtime may produce errors or different results. Keep its version, source changes, and hashes with the reproduction record and rerun all mathematical checks relevant to the proof. Do not carry a successful result from the original runtime over to an untested replacement.
