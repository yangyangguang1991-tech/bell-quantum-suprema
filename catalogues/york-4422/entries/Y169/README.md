# Y169 · A7;I4422^1

In the CH convention, the constant is at the top left, Bob marginals occupy the remainder of the first row, and Alice marginals occupy the remainder of the first column. The local bound is zero.

```text
  0  -1   0   0   0
 -3   1   1   1   1
 -2   1  -1   1   1
  0   1   0   0  -1
 -1   1   0  -1   1
```

**Exact quantum supremum.** f_169(b_star,u_star,v_star,t_star,h_star): unique isolated root of five rational gradient equations

The upper identity, Hilbert-space assumptions and construction of the attaining strategy are given in [the entry proof](PROOF.md). The data specified there are included in the local certificate.

Run `python verify.py 169` from the root of this York catalogue. To read the uncompressed mathematical inputs, run `python verify.py 169 --extract proof-Y169`.
