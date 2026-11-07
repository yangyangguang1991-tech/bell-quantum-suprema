# Third-party notices

The MIT notice in LICENSE applies to the project material covered by that license. External mathematical work is credited in HISTORY.md and in the corresponding entry for an identified exact-value theorem. Rights in third-party software remain with its authors.

The reference environment includes **SymPy**, **mpmath**, **python-flint and FLINT**, **NumPy** and **SciPy**. Package and native-dependency notices are retained with the distributed material. The combined [runtime source inventory](../../third_party/runtime/SOURCE_SUPPLY.md), [file inventory](../../third_party/runtime/inventory.json), [license collection](../../third_party/runtime/licenses/) and [library replacement instructions](../../third_party/runtime/REPLACEMENT.md) identify the relevant sources, build recipes and obligations. SciPy's distribution licenses are also retained under `runtime/licenses/scipy/`; symbolic-library licenses and author lists accompany their packages.

NumPy 2.3.5 is a local LLVM-MinGW build with the documented binary64 Windows ABI adaptation, not the official PyPI wheel. Its exact source, patch and rebuild instructions are in the [NumPy build record](../../third_party/runtime/build-recipes/numpy/README.md). SciPy 1.18.1 and its separately licensed components are supplied as described in the runtime inventory. The project MIT license does not replace any upstream package or dependency license.

The directed interval normal-map verifier is project-authored C99 code with a Python binding. Each relevant certificate contains its source, executable, fixed configuration, `BUILD.md` and project MIT license in `native_interval/`. The executable's LLVM/compiler-support and MinGW-w64 startup/runtime notices are retained in that directory's `licenses/` subdirectory.

No PowerShell/.NET distribution or MSVC runtime DLL is bundled. Windows x86-64 and a separately installed 64-bit CPython 3.12, including the interpreter's own platform runtime, are execution prerequisites. The supplied native executables use operating-system APIs; Windows DLLs and a compiler toolchain are not included in the certificate directories. Verification requires no external mathematical data or software download.

[SymPy](https://github.com/sympy/sympy) · [mpmath](https://github.com/mpmath/mpmath) · [python-flint](https://github.com/flintlib/python-flint) · [FLINT](https://github.com/flintlib/flint) · [NumPy](https://github.com/numpy/numpy) · [SciPy](https://github.com/scipy/scipy)
