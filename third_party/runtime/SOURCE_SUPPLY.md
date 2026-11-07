# Bundled runtime: licenses and source supply

The mathematical collection and its third-party libraries are distinct works. The repository MIT license applies only to project-owned material. Original licenses and notices govern each dependency. This edition bundles no PowerShell/.NET distribution and no MSVC runtime DLLs. Windows x64 and CPython 3.12, including the interpreter's own platform runtime, remain external execution prerequisites; their installation is not supplied here.

`inventory.json` records source URLs, hashes, runtime archive members and native dependencies. `sources.sha256` identifies the source archives included in the complete offline release. The lightweight Git edition omits those archives; obtain the complete release described in [DISTRIBUTION.md](../../DISTRIBUTION.md). No verifier downloads material. Do not redistribute binary subsets without the source or notices required by their licenses.

## GNU LGPL libraries and corresponding source

The Windows python-flint 0.9.0 wheel includes FLINT 3.6.0, GMP 6.3.0, and MPFR 4.2.2. These native libraries are not covered by python-flint's MIT wrapper license. The distribution retains the LGPL and GPL text supplied by the wheel, including GMP's alternative licensing provisions. This source supply uses the LGPL-3.0-or-later option where available.

The complete release supplies:

- The unmodified FLINT 3.6.0, GMP 6.3.0, and MPFR 4.2.2 source archives.
- The python-flint 0.9.0 source distribution and its exact upstream Git source at commit `572c8a213a88c0f92feb1bdb938ce4622f4517fa`.
- Its Windows build workflow, dependency-version file, shell build scripts, Meson configuration, and `bin/patch-C23.diff`. That patch is applied to GMP by the upstream x64 Windows build. The source archive contains the complete files; selected recipes are also readable under `build-recipes/python-flint/`.
- GCC 16.1.0 source and the MSYS2 recipe/patch snapshot at `5d898bcf429d0a5e0d07407e0712ad106f229951`. The recipe specifies GCC 16.1.0 revision 5, matching the compiler string in the native libraries. The snapshot also records the winpthreads recipe; the associated MinGW-w64 source at `6b5798fd4deb4323cf3618f62c213958f6758457` is supplied. Selection of this snapshot does not establish the precise build revision of the wheel's winpthreads DLL.

Every retained python-flint package file in the runtime and in the embedded York copies is byte-identical to the corresponding file in the official PyPI wheel `python_flint-0.9.0-cp310-abi3-win_amd64.whl`, whose SHA-256 is `8f1059536b7393e48b1444894c3b54ce1b961e4aa4a356e19217b26690f20db0`. Installation bookkeeping files and bytecode caches are outside that comparison. York entries Y059, Y124, and Y168 contain additional copies covered by the same source supply and notices.

This establishes the upstream binary identity and the versioned source/build recipe supply. It does **not** claim a bit-for-bit local compiler rebuild. General-purpose build tools, operating-system headers, and a Windows compiler toolchain are separate prerequisites for rebuilding, not for running the supplied verification edition. The original upstream workflow identifies them.

## Other runtime components

- **NumPy 2.3.5:** a local LLVM-MinGW source build with an explicit binary64 ABI patch. The upstream BSD license, bundled LAPACK/FFT/random/math notices, LLVM license with exceptions and MinGW runtime notices are retained. The exact source, patch, configuration and rebuild script are in [build-recipes/numpy/README.md](build-recipes/numpy/README.md). This is not the official PyPI wheel. It uses bundled `lapack_lite`, with no bundled NumPy OpenBLAS or MSVCP DLL.
- **SciPy 1.18.1:** retained original files under its BSD and bundled-component licenses. Its OpenBLAS reports `0.3.31.dev`. Original notices cover OpenBLAS/LAPACK and statically linked GNU Fortran/compiler runtime under GPL with GCC Runtime Library Exception 3.1. No separate libquadmath DLL is distributed. The GCC-libs aggregate license must not be used to mislabel individual supplied DLLs. The SciPy source tarball is supplied without claiming that it reproduces the OpenBLAS DLL byte for byte.
- **SymPy 1.14.0 and mpmath 1.3.0:** retained BSD licenses and source distributions.
- **threadpoolctl 3.7.0:** BSD-3-Clause; present in the Ito-Imai-Avis runtime.
- **winpthreads:** MIT and BSD-3-Clause-Clear notices. Its precise upstream build revision is not inferred solely from a recipe snapshot.

Native libraries may import Windows system UCRT interfaces and the CPython installation's `VCRUNTIME140` libraries. Those are platform dependencies, not redistributed files. No personal Visual Studio installation is requested by this repository. No requirement here restricts modification of LGPL libraries or reverse engineering to debug such modifications; see [REPLACEMENT.md](REPLACEMENT.md).

## Source verification

```text
python third_party/runtime/tools/runtime_workspace.py verify-sources
```

This is a source-file digest check, not a Bell proof. Source supply and notices do not claim mathematical authorship, novelty or an upper bound.
