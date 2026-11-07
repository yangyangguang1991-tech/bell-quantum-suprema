# NumPy source build for the verification runtime

This is a locally built NumPy 2.3.5 variant, not the official PyPI Windows wheel. NumPy's authorship and licenses are retained. The supplied patch changes three source files to keep the Windows binary64 `longdouble` ABI while avoiding MinGW's precompiled binary80 mathematical entry points. Real functions, complex functions, real/imaginary extraction and decimal conversion are covered. The compiler receives `-mlong-double-64`; a file-prefix map removes local build-directory names from diagnostic strings.

The build uses CPython 3.12 x64, Cython 3.3.1, Ninja 1.13.2 and NumPy's bundled Meson. LLVM-MinGW release `20261104` contains Clang 23.1.5. Its [official x64 UCRT archive](https://github.com/mstorsjo/llvm-mingw/releases/download/20261104/llvm-mingw-20261104-ucrt-x86_64.zip) has SHA-256 `552191b5754c49a5a20723276a6fc56541ea1922c4c50b7b669022333fc1b40f`. These general-purpose development tools are required for rebuilding; they are not required for executing the supplied binaries.

Configuration: release build, `blas=none`, `lapack=none`, `cpu-dispatch=none`, `cpu-baseline=min`. NumPy uses its bundled `lapack_lite`; SciPy retains its separately licensed original OpenBLAS binary. NumPy therefore does not carry the official wheel's OpenBLAS or MSVCP DLL. Static LLVM/MinGW runtime notices are in `../../licenses/numpy/`.

From the repository root, after preparing the specified development tools:

```text
python third_party/runtime/build-recipes/numpy/build_numpy.py --toolchain C:\llvm-mingw --build-deps C:\numpy-build-deps --work C:\numpy-rebuild
```

The script verifies the supplied source archive, applies the exact patch, configures, compiles and installs to a new directory. It does not download tools. `__config__.py` retains compiler names and versions but replaces machine-specific executable paths by basenames. The release omits test suites, examples, headers, static development archives and bytecode caches from its runtime tree; the complete source archive retains them. No bit-for-bit reproducible compiler output is claimed.

The resulting dtype ABI has 8-byte `longdouble`, 16-byte `clongdouble`, a 52-bit long-double mantissa and NumPy ndarray C ABI `0x02000000`. Upstream NumPy's MinGW experimental-platform warning remains enabled; this is a verification-specific runtime, not an upstream-supported general-purpose NumPy distribution. Its mathematical role is unchanged: floating-point proposals must be accepted by the independent exact certificate checks.
