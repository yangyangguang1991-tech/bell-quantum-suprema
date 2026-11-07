# Distribution of the (6,3,2,2) catalogue

This is the seven-class constituent catalogue of **Exact Quantum Suprema
and Certificates for Selected Bell Scenarios**, version 1.0.0. Its directory
in the combined repository is `catalogues/six-by-three/`.

Use the root [distribution instructions](../../DISTRIBUTION.md) and
[upload guide](../../UPLOAD.md). The root [CITATION.cff](../../CITATION.cff)
identifies the combined edition; this directory's [CITATION.cff](CITATION.cff)
records constituent provenance. The author is Yang-Guang Yang, ORCID
[0000-0001-9236-7544](https://orcid.org/0000-0001-9236-7544),
email yangyangguang1991@gmail.com.

## Complete local reproduction

Retain all seven numbered entry directories, `common/`, local documents,
verification programs and license. The complete local quantum proofs and
the exact facet-classification enumeration require no other catalogue or
external research file. Python 3.10 or later and its standard library are
sufficient. Run from `catalogues/six-by-three/`:

```console
python -B verify_files.py
python -B verify.py
```

The first command checks file hashes. The second runs all seven entries and
the complete classification. For one entry use, for example,
`python -B verify.py 4`. Keep assertions enabled. The mathematical manual
distinguishes the exact I3322 path constant and its approximating family
from finite-dimensional attainment.

This entire catalogue consists of small source files and is included in both
the lightweight Git source edition and the complete offline distribution.
The combined project's omitted large payloads belong to York. To reproduce
the entire combined collection, obtain and extract every complete-release
volume as described in the root instructions; its automatic Git source ZIP
alone is not the full proof distribution.

## Publication and references

Publish this directory as part of the combined repository using the root
release description and citation metadata. No separate repository or DOI is
required for this constituent. Add a real version DOI only after the actual
complete combined edition has been archived. Keep `SHA256SUMS.txt` and
`.gitattributes` consistent with the distributed bytes.

Historical papers retain their own authorship. Entry references identify
prior strict exact unrestricted results; the catalogue history also covers
facet construction, numerical work and related methods. See [LICENSE](LICENSE)
and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for reuse terms and provenance.
