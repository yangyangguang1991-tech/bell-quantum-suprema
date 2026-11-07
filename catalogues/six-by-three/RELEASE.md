# Version 1.0.0: Exact Quantum Suprema of the (6,3,2,2) Bell Facets

This is a constituent catalogue overview for version 1.0.0 of **Exact Quantum Suprema and Certificates for Selected Bell Scenarios**. Use the combined [release description](../../RELEASE.md), [publication instructions](../../UPLOAD.md) and [citation metadata](../../CITATION.cff) when publishing or citing this edition. The local `CITATION.cff` records constituent provenance.

**Yang-Guang Yang** · yangyangguang1991@gmail.com · [ORCID 0000-0001-9236-7544](https://orcid.org/0000-0001-9236-7544)

This constituent catalogue presents all seven facet classes of the six-versus-three binary Bell scenario. Its seven independently organized entries contain the complete active probability coefficients, exact mathematical upper-bound arguments and reproducible reverse inequalities in the same normalization.

Six entries have explicit attaining two-qubit states and measurements. I3322 is specified by an exact Jacobi path variational constant and a constructive finite-dimensional family converging to it. The latter is a supremum characterization, with model-specific dimension and attainment theorems clearly attributed in the entry bibliography.

Two entries use exact oriented noncommutative Gram identities with rigorously enclosed positive pivots. The remaining upper arguments use projection positivity, the CHSH square, operator spectral comparisons or the I3322 scalar majorant. All literal finite scores, reflection identities and Gram expansions are reproducible with the included Python standard-library programs. The default command also performs a complete exact facet enumeration.

Start with [README.md](README.md), then follow [MANUAL.md](MANUAL.md). [FACETS.md](FACETS.md) gives the completeness argument. [HISTORY.md](HISTORY.md) and the detailed [I3322 history](I3322_HISTORY.md) distinguish historical exact results from numerical studies and describe relevant computer-assisted contributions. The release makes no unsupported claim of worldwide priority.

```console
python -B verify.py
```

Python 3.10 or later is sufficient. The complete package works offline and requires no additional library or mathematical data download.
