# I3322

The literal coefficient table and probability convention are in [definition.json](definition.json). The complete upper-bound argument and the attaining construction or approaching sequence are in [PROOF.md](PROOF.md).

Run this entry from the repository root:

```console
python -B verify.py 2
```

The same check can be run directly with `python -B entries/02-I3322/verify.py`. Use Python 3.10 or later with assertions enabled. All required mathematical data and arithmetic code are included; only the Python standard library is required.

The exact value is the Jacobi path constant defined in the proof. This is a supremum; finite-dimensional attainment is not assumed. `sequence.py` constructs the approaching family, and `example.json` is checked directly against the complete probability table.
