# I4322^(3)

The literal coefficient table and probability convention are in [definition.json](definition.json). The complete upper-bound argument and the attaining construction are in [PROOF.md](PROOF.md).

Run this entry from the repository root:

```console
python -B verify.py 5
```

The same check can be run directly with `python -B entries/05-I4322-3/verify.py`. Use Python 3.10 or later with assertions enabled. All required mathematical data and arithmetic code are included; only the Python standard library is required.

`strategy.json` gives the normalized state and all six Alice and three Bob reflections. The verifier checks their legality and recomputes the literal Bell score, including marginals.
