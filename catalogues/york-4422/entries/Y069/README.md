# Y69 · J4422^25

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
  0  -2  -1   0   0
 -3   1   1   1   2
  0   1  -1   0   0
 -1   1   1   1  -2
  0   1   1  -1   0
```

**Exact quantum supremum.** Unique root in (0.5147829042000097,0.5147829042000098) of 32q^8+384q^7+1776q^6+3888q^5+3794q^4+732q^3-990q^2-432q-59

The upper identity, Hilbert-space assumptions and construction of the attaining strategy are given in [the entry proof](PROOF.md). The data specified there are included in the local certificate.

Run `python verify.py 69` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 69 --extract proof-Y069`.
