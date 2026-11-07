# Authorship, citation and preservation of contributions

## Scope of the attribution

Yang-Guang Yang is the author and maintainer of this repository edition.
This identifies responsibility for the supplied compilation, exposition,
verification implementation and release. It does not assign authorship of
all underlying inequalities, methods or exact-value theorems to the maintainer.
Earlier mathematical contributions retain the attribution given in the entries
and historical bibliography. Reproduction of a known result is described as
reproduction, not as its first discovery.

Version 1.0.0 makes no blanket claim of newly discovered quantum suprema.
Neither an absent earlier reference nor a successful exact computation establishes
priority. Any future novelty claim must identify the precise statement,
normalization and quantum model, distinguish earlier theorems from numerical
evidence, supply both proof directions, and explain the comparison with prior
literature. A new verifier, an alternative proof and a previously unknown value
are different contributions and must be described separately.

## Reuse and scholarly credit

Please cite this repository when using its supplied exposition, programs,
certificates or catalogue correspondences, and cite the original mathematical
sources for the results used. Give the catalogue and entry identifiers,
version, and the version-specific DOI once it exists. Until then, identify
the repository URL, release tag and commit. `CITATION.cff` supplies the
repository citation; it does not replace entry-level theorem references.

Recommended acknowledgement, adapted to the actual use:

> The verification materials for [catalogue and entry identifiers] were taken
> from Yang-Guang Yang, [repository title], version 1.0.0, [version DOI or
> release URL and commit]. The underlying mathematical results are attributed
> to the original sources listed for those entries. Our modifications are
> described separately.

These bracketed fields are an example for readers, not registered identifiers
or a claim that a DOI has already been obtained. Derived distributions should
identify their modifications and should not imply that the maintainer checked
or endorsed the changed results.

The existing MIT license applies to the project's eligible original materials;
third-party components retain their separate licenses and notices. MIT permits
reuse, modification and commercial distribution while requiring preservation
of its copyright and permission notice. The scholarly citation request here
is not an extra MIT license condition. No license change is introduced by
this document. See the [MIT license explanation](https://choosealicense.com/licenses/mit/),
`LICENSE`, `RIGHTS.md` and `THIRD_PARTY.md`.

Copyright and mathematical priority are distinct. Copyright concerns eligible
expression, not mathematical concepts or methods as such. A copyright notice
does not reserve exclusive use of a theorem, its numerical value or its idea.
This distinction is explained in the [WIPO copyright FAQ](https://www.wipo.int/en/web/copyright/faq-copyright).
Open publication supports attribution and reproducibility.

## Durable public records

The publication procedure in `UPLOAD.md` preserves a specific, inspectable
edition. Publish the complete proof payloads, checksums, citation information
and release description together. A checksum establishes file identity;
it is not, by itself, a timestamp, authorship certificate or proof of correctness.
Keep the dated working records and precise contribution history separately.

Enable GitHub release immutability before publishing the first release.
Prepare a draft, attach every volume and checksum, and review it before
publication. Immutable releases lock the tag and assets and provide release
attestations; the title and release notes remain editable. Preserve a copy
of the substantive release description inside the archived files too.
See [GitHub's immutable-release documentation](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases).

Deposit the complete edition in Zenodo rather than assuming the lightweight
Git tree contains its separate release assets. Use the version DOI for an
exact reproducible edition; the concept DOI refers to the version family.
Archive corrections as new versions. See [Zenodo's DOI versioning guidance](https://zenodo.org/help/versioning).
A DOI makes the deposited object identifiable and citable; it does not
certify novelty, correctness or ownership of every included theorem.

For a genuinely new theorem, a readable research note or preprint should state
the actual theorem, proof, earlier work and contribution boundaries explicitly,
and link the exact certificate edition. A repository timestamp alone is a
poor substitute for explaining what was established. No preprint, remote
release, immutable-release setting or DOI registration is performed merely
by distributing this local package. Use actual publication dates and
identifiers; do not backdate a record.

## AI-assisted work

The assistance disclosure in `CONTRIBUTIONS.md` remains part of this edition.
AI assistance does not replace earlier authors' credit, human responsibility
for the release, or the mathematical proof obligations. Repository authorship
does not imply that every line was written manually. Tool use should be
reported accurately; unavailable model versions or contribution histories
must not be invented.

Copyright eligibility of AI-assisted expression depends on applicable law and
the actual human contribution. For example, the U.S. Copyright Office's 2025
report distinguishes human-authored expression from output obtained through
prompts alone. It is not a blanket determination about this repository or
other jurisdictions. See [Copyright and Artificial Intelligence, Part 2](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf).
The project claims rights only to the extent they exist and are held by its
licensor; a notice cannot create otherwise absent rights.

## Corrections and future contributions

Report a mathematical or attribution issue with the entry identifier, affected
version, relevant statement or file, and the supporting source. Contact
yangyangguang1991@gmail.com or use the repository issue tracker after publication.
Preserve earlier editions and describe corrections in a new release. A verified
earlier source must receive credit even when the present implementation was
constructed separately.

Future contributions should identify their authors, third-party sources,
permission basis and substantive computational assistance. Maintainer review
must check both the contribution's mathematical content and its attribution.
This policy supports accurate credit and a durable record of contributions.
