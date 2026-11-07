# I4322^(2)

The literal coefficient table and probability convention are in [definition.json](definition.json). The complete upper-bound argument and the attaining construction are in [PROOF.md](PROOF.md).

Run this entry from the repository root:

```console
python -B verify.py 4
```

The same check can be run directly with `python -B entries/04-I4322-2/verify.py`. Use Python 3.10 or later with assertions enabled. All required mathematical data and arithmetic code are included; only the Python standard library is required.

`strategy.json` gives the normalized state and all six Alice and three Bob reflections. The verifier checks their legality and recomputes the literal Bell score, including marginals.

The exact Gram data are in `gram.json`; the complete oriented polynomial identity and strict pivot bounds are verified.
