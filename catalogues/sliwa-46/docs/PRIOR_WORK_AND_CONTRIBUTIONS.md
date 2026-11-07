# Prior work and contributions

## Historical scope

The catalogue consists of the 46 facet representatives in the appendix of Śliwa's 2003 arXiv paper [Sliwa2003]. The earlier facet enumeration of Pitowsky and Svozil [PitowskySvozil2001] is also part of its history. The journal version of Śliwa's article does not contain the 46-row appendix. The literal convention in this repository agrees with Table I of López-Rosa, Xu and Cabello [LopezRosa2016]. Values are raw correlator maxima, with no subtraction of the local bound.

López-Rosa et al., Section II A and Table IV, report analytical expressions for 27 entries and decimal values for 19 entries. Their stated test for reporting an analytical expression includes agreement with numerical optimization to at least nine digits, supplemented by numerical NPA bounds. This is a classification of what is reported in that paper; it does not establish that each row is accompanied there by a complete exact global positivity proof.

Vallins, Sainz and Liang [Vallins2017] give a separate quantum-value column `Q`. The comparison here uses Table I on the fifth physical PDF page of corrected arXiv version 5, dated 18 July 2018. Every present value agrees with that column at its displayed precision; almost-quantum and relaxation columns are not substituted for `Q`. Sixteen of the 19 decimal entries in the 2016 table are not rounding-equivalent to the present exact values: classes 16, 21, 22, 24, 25, 27, 31, 32, 33, 34, 35, 36, 39, 40, 41 and 42. The three compatible decimal entries are 19, 28 and 46. These differences between numerical displays do not contradict earlier certified rational bounds.

Werner and Wolf [WernerWolf2001] classified the full-correlation inequalities for two dichotomic observables per party. Their Appendix, Eq. (A2), gives a representative equivalent to S7, with a reported normalized violation of `5/3`. The S7 entry below spells out the output relabelling and factor of four. The Appendix describes its displayed violations as numerical results from the method of Section V; this earlier value report is not used as an exact upper certificate.

Ioannou and Rosset [IoannouRosset2021], Section IX, Eqs. (156), (158), (160) and (162), explicitly give exact SOS certificates for classes 3, 10, 11 and 14, respectively. Their projector notation and representatives should be distinguished from the literal operators stored here. These are credited as class-level prior upper proofs; the present programs independently bind the chosen literal expressions. Their symmetry data for the full catalogue do not constitute 46 explicit SOS certificates.

## Contributions of this archive

1. A uniform collection of exact global upper certificates for all 46 fixed representatives, covering arbitrary dimensions, binary POVMs and commuting representations through the two-observable reduction.
2. Exact specifications and global certificates for the 19 decimal rows of the 2016 benchmark: one radical value, eight univariate root definitions and ten definitions by coordinates of uniquely isolated real solutions of polynomial systems. This statement is relative to that benchmark and does not assign worldwide priority to the individual values.
3. An explicit normalized state formula for every entry, including repeated top eigenvalues, together with all six measurement matrices and independently evaluated Bell scores. The spectral-projector identity underlying the construction is standard linear algebra; the contribution is its complete executable realization for the catalogue.
4. Exact target binding across the fixed proof schedule, unchanged execution inputs, complete lists of positivity obligations, rational outward interval checks, complete covers, compact rational root selectors, and an offline verification distribution. Earlier catalogue classification, full-correlation results, qubit reduction, CHSH/Mermin bounds, SOS methods and interval analysis remain credited to their sources.

The historical comparisons below distinguish a previously reported value from a previously exhibited exact global proof. A missing class-specific proof citation means that the cited sources do not provide an earlier explicit certificate assigned to that row here; it does not establish the absence of other earlier proofs. The comparison is limited to these sources. Equivalence transformations, other normalizations and unpublished material may require further work to determine priority.

## Entry-by-entry comparison

For every entry, the current upper-verifier list and constructive attainment files are linked. The machine-readable record is [prior_work_and_contributions.json](../data/prior_work_and_contributions.json). Full bibliographic metadata appears in [REFERENCES.md](../REFERENCES.md) and [references.bib](../references.bib).

## Śliwa inequality 1

- **Earlier value:** `1`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `1` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Context:** Positivity; no quantum violation.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S001/strategy_spec.json); its display begins `1.0000000000000000…`.
- **Proof materials:** [global upper bound](../entries/S001/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S001/attainment/strategy_exact.json); [state vector and matrices](../entries/S001/attainment/strategy_numeric.json).

## Śliwa inequality 2

The tripartite Mermin specialization of Theorem 6 in Panwar, Pandya and Wieśniak (2023) gives the same maximum. [Article](https://doi.org/10.1038/s41534-023-00735-3).

- **Earlier value:** `4`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `4` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Context:** Mermin inequality; algebraic upper value 4 and GHZ attainment.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S002/strategy_spec.json); its display begins `4.0000000000000000…`.
- **Proof materials:** [global upper bound](../entries/S002/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S002/attainment/strategy_exact.json); [state vector and matrices](../entries/S002/attainment/strategy_numeric.json).

## Śliwa inequality 3

The extended CHSH expression adjoining Eq. (28) of Panwar, Pandya and Wieśniak (2023) is this literal divided by two. [Article](https://doi.org/10.1038/s41534-023-00735-3).

- **Earlier value:** `2*sqrt(2)`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `2.8284` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Earlier explicit global certificate:** [IoannouRosset2021], Section IX, Eq. (156), exact class-level SOS.
- **Context:** CHSH/Tsirelson reductions; this identifies a mathematical reduction, not an earliest class-specific publication.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S003/strategy_spec.json); its display begins `2.8284271247461900…`.
- **Proof materials:** [global upper bound](../entries/S003/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S003/attainment/strategy_exact.json); [state vector and matrices](../entries/S003/attainment/strategy_numeric.json).

## Śliwa inequality 4

The explicit party-lift identity and an earlier strict upper proof are recorded in the [entry note](../entries/S004/README.md#earlier-exact-proof).

For S004, the 2019 party-lifting result is preceded by Rosset, Bancal and Gisin (2014), Section II.4 and Appendix C.2, Proposition 4. The factorization S4=2I+(I−A)(H−2I), with H the CHSH operator, specializes their tight composition theorem to the value 4√2−2. This identifies an earlier general theorem that proves the present value; it does not assert that the 2014 paper lists Śliwa class 4 explicitly. [Article](https://doi.org/10.1088/1751-8113/47/42/424022).

- **Earlier value:** `4*sqrt(2)-2`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `4*sqrt(2)-2` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Context:** CHSH/Tsirelson reductions; this identifies a mathematical reduction, not an earliest class-specific publication.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S004/strategy_spec.json); its display begins `3.6568542494923801…`.
- **Proof materials:** [global upper bound](../entries/S004/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S004/attainment/strategy_exact.json); [state vector and matrices](../entries/S004/attainment/strategy_numeric.json).

## Śliwa inequality 5

- **Earlier value:** `8*sqrt(5)-13`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `4.8885` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S005/strategy_spec.json); its display begins `4.8885438199983175…`.
- **Proof materials:** [global upper bound](../entries/S005/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S005/attainment/strategy_exact.json); [state vector and matrices](../entries/S005/attainment/strategy_numeric.json).

## Śliwa inequality 6

- **Earlier value:** `4*sqrt(2)-1`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `4.6569` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S006/strategy_spec.json); its display begins `4.6568542494923801…`.
- **Proof materials:** [global upper bound](../entries/S006/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S006/attainment/strategy_exact.json); [state vector and matrices](../entries/S006/attainment/strategy_numeric.json).

## Śliwa inequality 7

Panwar, Pandya and Wieśniak (2023), Eq. (27) and accompanying discussion, give an explicit anti-diagonal reduction and the exact maximum $20/3$ of S007. This class-specific proof is distinct from the numerical evaluation in Werner and Wolf’s earlier table. [Article](https://doi.org/10.1038/s41534-023-00735-3).

- **Earlier value:** `20/3`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `20/3` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Earlier full-correlation context:** [WernerWolf2001], Appendix, Eq. (A2), gives $W=\tfrac14(a_1+a_2)(b_1+b_2)(c_1+c_2)-a_1b_1c_1$. Set $a_1=-A$, $a_2=a$, $b_1=-B$, $b_2=b$, $c_1=-C$, $c_2=c$. Then $4W=4ABC-(A-a)(B-b)(C-c)=\mathcal B_7$. Thus first-setting output flips at all three parties and a factor of four map their reported normalized `5/3` to `20/3`. Their numerical table is credited as an earlier value report, not as an exact upper certificate.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S007/strategy_spec.json); its display begins `6.6666666666666666…`.
- **Proof materials:** [global upper bound](../entries/S007/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S007/attainment/strategy_exact.json); [state vector and matrices](../entries/S007/attainment/strategy_numeric.json).

## Śliwa inequality 8

- **Earlier value:** `20/3`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `6.6667` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S008/strategy_spec.json); its display begins `6.6666666666666666…`.
- **Proof materials:** [global upper bound](../entries/S008/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S008/attainment/strategy_exact.json); [state vector and matrices](../entries/S008/attainment/strategy_numeric.json).

## Śliwa inequality 9

- **Earlier value:** `4*sqrt(2)`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `5.6569` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S009/strategy_spec.json); its display begins `5.6568542494923801…`.
- **Proof materials:** [global upper bound](../entries/S009/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S009/attainment/strategy_exact.json); [state vector and matrices](../entries/S009/attainment/strategy_numeric.json).

## Śliwa inequality 10

- **Earlier value:** `4`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `4` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Earlier explicit global certificate:** [IoannouRosset2021], Section IX, Eq. (158), exact class-level SOS.
- **Context:** Guess-your-neighbor-input family and earlier exact class SOS; no quantum advantage.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S010/strategy_spec.json); its display begins `4.0000000000000000…`.
- **Proof materials:** [global upper bound](../entries/S010/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S010/attainment/strategy_exact.json); [state vector and matrices](../entries/S010/attainment/strategy_numeric.json).

## Śliwa inequality 11

- **Earlier value:** `4*sqrt(2)`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `5.6569` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Earlier explicit global certificate:** [IoannouRosset2021], Section IX, Eq. (160), exact class-level SOS.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S011/strategy_spec.json); its display begins `5.6568542494923801…`.
- **Proof materials:** [global upper bound](../entries/S011/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S011/attainment/strategy_exact.json); [state vector and matrices](../entries/S011/attainment/strategy_numeric.json).

## Śliwa inequality 12

- **Earlier value:** `4*sqrt(2)`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `5.6569` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S012/strategy_spec.json); its display begins `5.6568542494923801…`.
- **Proof materials:** [global upper bound](../entries/S012/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S012/attainment/strategy_exact.json); [state vector and matrices](../entries/S012/attainment/strategy_numeric.json).

## Śliwa inequality 13

- **Earlier value:** `4*sqrt(2)`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `5.6569` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S013/strategy_spec.json); its display begins `5.6568542494923801…`.
- **Proof materials:** [global upper bound](../entries/S013/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S013/attainment/strategy_exact.json); [state vector and matrices](../entries/S013/attainment/strategy_numeric.json).

## Śliwa inequality 14

- **Earlier value:** `4*sqrt(2)`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `5.6569` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Earlier explicit global certificate:** [IoannouRosset2021], Section IX, Eq. (162), exact class-level SOS.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S014/strategy_spec.json); its display begins `5.6568542494923801…`.
- **Proof materials:** [global upper bound](../entries/S014/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S014/attainment/strategy_exact.json); [state vector and matrices](../entries/S014/attainment/strategy_numeric.json).

## Śliwa inequality 15

- **Earlier value:** `6`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `6.0000` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S015/strategy_spec.json); its display begins `6.0000000000000000…`.
- **Proof materials:** [global upper bound](../entries/S015/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S015/attainment/strategy_exact.json); [state vector and matrices](../entries/S015/attainment/strategy_numeric.json).

## Śliwa inequality 16

- **Earlier value:** `6.12883`; decimal display in [LopezRosa2016], Table IV. The present value lies outside the rounding cell of this printed decimal.
- **Later numerical comparison:** `6.1289` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S016/strategy_spec.json); its display begins `6.1288693702808872…`.
- **Proof materials:** [global upper bound](../entries/S016/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S016/attainment/strategy_exact.json); [state vector and matrices](../entries/S016/attainment/strategy_numeric.json).

## Śliwa inequality 17

- **Earlier value:** `4*sqrt(2)`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `5.6569` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S017/strategy_spec.json); its display begins `5.6568542494923801…`.
- **Proof materials:** [global upper bound](../entries/S017/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S017/attainment/strategy_exact.json); [state vector and matrices](../entries/S017/attainment/strategy_numeric.json).

## Śliwa inequality 18

- **Earlier value:** `2*(7-sqrt(17))`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `5.7538` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S018/strategy_spec.json); its display begins `5.7537887487646789…`.
- **Proof materials:** [global upper bound](../entries/S018/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S018/attainment/strategy_exact.json); [state vector and matrices](../entries/S018/attainment/strategy_numeric.json).

## Śliwa inequality 19

- **Earlier value:** `5.7829`; decimal display in [LopezRosa2016], Table IV. The present value agrees at the printed precision.
- **Later numerical comparison:** `5.7829` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S019/strategy_spec.json); its display begins `5.7829117532036863…`.
- **Proof materials:** [global upper bound](../entries/S019/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S019/attainment/strategy_exact.json); [state vector and matrices](../entries/S019/attainment/strategy_numeric.json).

## Śliwa inequality 20

- **Earlier value:** `6*sqrt(2)-2`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `6.4853` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S020/strategy_spec.json); its display begins `6.4852813742385702…`.
- **Proof materials:** [global upper bound](../entries/S020/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S020/attainment/strategy_exact.json); [state vector and matrices](../entries/S020/attainment/strategy_numeric.json).

## Śliwa inequality 21

- **Earlier value:** `5.95539`; decimal display in [LopezRosa2016], Table IV. The present value lies outside the rounding cell of this printed decimal.
- **Later numerical comparison:** `5.9555` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S021/strategy_spec.json); its display begins `5.9554569186959206…`.
- **Proof materials:** [global upper bound](../entries/S021/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S021/attainment/strategy_exact.json); [state vector and matrices](../entries/S021/attainment/strategy_numeric.json).

## Śliwa inequality 22

- **Earlier value:** `6.19794`; decimal display in [LopezRosa2016], Table IV. The present value lies outside the rounding cell of this printed decimal.
- **Later numerical comparison:** `6.1980` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S022/strategy_spec.json); its display begins `6.1979587791753010…`.
- **Proof materials:** [global upper bound](../entries/S022/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S022/attainment/strategy_exact.json); [state vector and matrices](../entries/S022/attainment/strategy_numeric.json).

## Śliwa inequality 23

- **Earlier value:** `3*(sqrt(17)-1)/2`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `4.6847` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S023/strategy_spec.json); its display begins `4.6846584384264908…`.
- **Proof materials:** [global upper bound](../entries/S023/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S023/attainment/strategy_exact.json); [state vector and matrices](../entries/S023/attainment/strategy_numeric.json).

## Śliwa inequality 24

- **Earlier value:** `7.94016`; decimal display in [LopezRosa2016], Table IV. The present value lies outside the rounding cell of this printed decimal.
- **Later numerical comparison:** `7.9401` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S024/strategy_spec.json); its display begins `7.9401098058580475…`.
- **Proof materials:** [global upper bound](../entries/S024/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S024/attainment/strategy_exact.json); [state vector and matrices](../entries/S024/attainment/strategy_numeric.json).

## Śliwa inequality 25

- **Earlier value:** `6.82421`; decimal display in [LopezRosa2016], Table IV. The present value lies outside the rounding cell of this printed decimal.
- **Later numerical comparison:** `6.8243` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S025/strategy_spec.json); its display begins `6.8242615835790617…`.
- **Proof materials:** [global upper bound](../entries/S025/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S025/attainment/strategy_exact.json); [state vector and matrices](../entries/S025/attainment/strategy_numeric.json).

## Śliwa inequality 26

- **Earlier value:** `1+4*sqrt(3)`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `7.9282` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S026/strategy_spec.json); its display begins `7.9282032302755091…`.
- **Proof materials:** [global upper bound](../entries/S026/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S026/attainment/strategy_exact.json); [state vector and matrices](../entries/S026/attainment/strategy_numeric.json).

## Śliwa inequality 27

- **Earlier value:** `6.95465`; decimal display in [LopezRosa2016], Table IV. The present value lies outside the rounding cell of this printed decimal.
- **Later numerical comparison:** `6.9547` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S027/strategy_spec.json); its display begins `6.9546558328928353…`.
- **Proof materials:** [global upper bound](../entries/S027/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S027/attainment/strategy_exact.json); [state vector and matrices](../entries/S027/attainment/strategy_numeric.json).

## Śliwa inequality 28

- **Earlier value:** `9.90976`; decimal display in [LopezRosa2016], Table IV. The present value agrees at the printed precision.
- **Later numerical comparison:** `9.9098` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S028/strategy_spec.json); its display begins `9.9097615783037003…`.
- **Proof materials:** [global upper bound](../entries/S028/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S028/attainment/strategy_exact.json); [state vector and matrices](../entries/S028/attainment/strategy_numeric.json).

## Śliwa inequality 29

- **Earlier value:** `8*sqrt(2)-2`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `9.3137` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S029/strategy_spec.json); its display begins `9.3137084989847603…`.
- **Proof materials:** [global upper bound](../entries/S029/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S029/attainment/strategy_exact.json); [state vector and matrices](../entries/S029/attainment/strategy_numeric.json).

## Śliwa inequality 30

- **Earlier value:** `8*sqrt(2)-2`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `9.3137` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S030/strategy_spec.json); its display begins `9.3137084989847603…`.
- **Proof materials:** [global upper bound](../entries/S030/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S030/attainment/strategy_exact.json); [state vector and matrices](../entries/S030/attainment/strategy_numeric.json).

## Śliwa inequality 31

- **Earlier value:** `7.80425`; decimal display in [LopezRosa2016], Table IV. The present value lies outside the rounding cell of this printed decimal.
- **Later numerical comparison:** `7.8043` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S031/strategy_spec.json); its display begins `7.8042658639319966…`.
- **Proof materials:** [global upper bound](../entries/S031/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S031/attainment/strategy_exact.json); [state vector and matrices](../entries/S031/attainment/strategy_numeric.json).

## Śliwa inequality 32

- **Earlier value:** `8.15161`; decimal display in [LopezRosa2016], Table IV. The present value lies outside the rounding cell of this printed decimal.
- **Later numerical comparison:** `8.1516` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S032/strategy_spec.json); its display begins `8.1515617620015306…`.
- **Proof materials:** [global upper bound](../entries/S032/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S032/attainment/strategy_exact.json); [state vector and matrices](../entries/S032/attainment/strategy_numeric.json).

## Śliwa inequality 33

- **Earlier value:** `9.78988`; decimal display in [LopezRosa2016], Table IV. The present value lies outside the rounding cell of this printed decimal.
- **Later numerical comparison:** `9.7899` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S033/strategy_spec.json); its display begins `9.7898533182726729…`.
- **Proof materials:** [global upper bound](../entries/S033/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S033/attainment/strategy_exact.json); [state vector and matrices](../entries/S033/attainment/strategy_numeric.json).

## Śliwa inequality 34

- **Earlier value:** `8.25142`; decimal display in [LopezRosa2016], Table IV. The present value lies outside the rounding cell of this printed decimal.
- **Later numerical comparison:** `8.2515` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S034/strategy_spec.json); its display begins `8.2514977740834443…`.
- **Proof materials:** [global upper bound](../entries/S034/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S034/attainment/strategy_exact.json); [state vector and matrices](../entries/S034/attainment/strategy_numeric.json).

## Śliwa inequality 35

- **Earlier value:** `7.85524`; decimal display in [LopezRosa2016], Table IV. The present value lies outside the rounding cell of this printed decimal.
- **Later numerical comparison:** `7.8553` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S035/strategy_spec.json); its display begins `7.8552777316212247…`.
- **Proof materials:** [global upper bound](../entries/S035/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S035/attainment/strategy_exact.json); [state vector and matrices](../entries/S035/attainment/strategy_numeric.json).

## Śliwa inequality 36

- **Earlier value:** `9.46139`; decimal display in [LopezRosa2016], Table IV. The present value lies outside the rounding cell of this printed decimal.
- **Later numerical comparison:** `9.4614` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S036/strategy_spec.json); its display begins `9.4614311524340106…`.
- **Proof materials:** [global upper bound](../entries/S036/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S036/attainment/strategy_exact.json); [state vector and matrices](../entries/S036/attainment/strategy_numeric.json).

## Śliwa inequality 37

- **Earlier value:** `8*sqrt(2)-2`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `9.3137` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S037/strategy_spec.json); its display begins `9.3137084989847603…`.
- **Proof materials:** [global upper bound](../entries/S037/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S037/attainment/strategy_exact.json); [state vector and matrices](../entries/S037/attainment/strategy_numeric.json).

## Śliwa inequality 38

- **Earlier value:** `8*sqrt(2)-2`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `9.3137` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S038/strategy_spec.json); its display begins `9.3137084989847603…`.
- **Proof materials:** [global upper bound](../entries/S038/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S038/attainment/strategy_exact.json); [state vector and matrices](../entries/S038/attainment/strategy_numeric.json).

## Śliwa inequality 39

- **Earlier value:** `9.32530`; decimal display in [LopezRosa2016], Table IV. The present value lies outside the rounding cell of this printed decimal.
- **Later numerical comparison:** `9.3253` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S039/strategy_spec.json); its display begins `9.3253401650139931…`.
- **Proof materials:** [global upper bound](../entries/S039/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S039/attainment/strategy_exact.json); [state vector and matrices](../entries/S039/attainment/strategy_numeric.json).

## Śliwa inequality 40

- **Earlier value:** `8.12983`; decimal display in [LopezRosa2016], Table IV. The present value lies outside the rounding cell of this printed decimal.
- **Later numerical comparison:** `8.1298` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S040/strategy_spec.json); its display begins `8.1297872420881080…`.
- **Proof materials:** [global upper bound](../entries/S040/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S040/attainment/strategy_exact.json); [state vector and matrices](../entries/S040/attainment/strategy_numeric.json).

## Śliwa inequality 41

- **Earlier value:** `10.3680`; decimal display in [LopezRosa2016], Table IV. The present value lies outside the rounding cell of this printed decimal.
- **Later numerical comparison:** `10.3677` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S041/strategy_spec.json); its display begins `10.367746725495842…`.
- **Proof materials:** [global upper bound](../entries/S041/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S041/attainment/strategy_exact.json); [state vector and matrices](../entries/S041/attainment/strategy_numeric.json).

## Śliwa inequality 42

- **Earlier value:** `13.0471`; decimal display in [LopezRosa2016], Table IV. The present value lies outside the rounding cell of this printed decimal.
- **Later numerical comparison:** `13.0470` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S042/strategy_spec.json); its display begins `13.047046076499511…`.
- **Proof materials:** [global upper bound](../entries/S042/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S042/attainment/strategy_exact.json); [state vector and matrices](../entries/S042/attainment/strategy_numeric.json).

## Śliwa inequality 43

- **Earlier value:** `8*sqrt(2)`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `11.3137` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S043/strategy_spec.json); its display begins `11.313708498984760…`.
- **Proof materials:** [global upper bound](../entries/S043/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S043/attainment/strategy_exact.json); [state vector and matrices](../entries/S043/attainment/strategy_numeric.json).

## Śliwa inequality 44

- **Earlier value:** `12*sqrt(2)-4`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `12.9706` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S044/strategy_spec.json); its display begins `12.970562748477140…`.
- **Proof materials:** [global upper bound](../entries/S044/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S044/attainment/strategy_exact.json); [state vector and matrices](../entries/S044/attainment/strategy_numeric.json).

## Śliwa inequality 45

- **Earlier value:** `12*sqrt(2)-4`; analytical expression in [LopezRosa2016], Table IV. The expression agrees symbolically with the present value.
- **Later numerical comparison:** `12.9706` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact global certificate and explicit arithmetic attaining strategy for a previously reported analytic value. The exact value is specified in [strategy_spec.json](../entries/S045/strategy_spec.json); its display begins `12.970562748477140…`.
- **Proof materials:** [global upper bound](../entries/S045/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S045/attainment/strategy_exact.json); [state vector and matrices](../entries/S045/attainment/strategy_numeric.json).

## Śliwa inequality 46

- **Earlier value:** `12.9852`; decimal display in [LopezRosa2016], Table IV. The present value agrees at the printed precision.
- **Later numerical comparison:** `12.9852` in corrected [Vallins2017], Table I; agreement at the displayed precision.
- **Present contribution:** Exact algebraic specification, global certificate and explicit arithmetic attaining strategy for a decimal entry of the 2016 benchmark. The exact value is specified in [strategy_spec.json](../entries/S046/strategy_spec.json); its display begins `12.985173496317373…`.
- **Proof materials:** [global upper bound](../entries/S046/upper_bound/inputs.json); [explicit algebraic attainment](../entries/S046/attainment/strategy_exact.json); [state vector and matrices](../entries/S046/attainment/strategy_numeric.json).

## Bibliographic keys

[Sliwa2003], [PitowskySvozil2001], [WernerWolf2001], [LopezRosa2016], [Vallins2017] and [IoannouRosset2021] and [RossetBancalGisin2014] refer to the corresponding entries in the repository bibliography.
