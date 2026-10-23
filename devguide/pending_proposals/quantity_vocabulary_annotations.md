---
summary: Validate explicit QUDT and UO unit annotations without kind inference.
issue: uibcdf/pyunitwizard#127
status: active
opened: 2026-10-23
closed:
verification: measured
area: [units, interoperability]
guard:
normative: docs/content/user/unit-dialects.md
blocked_by: []
supersedes: []
---

# Bounded authoritative vocabulary annotations

What — Add `qrec-vocabulary/0.1` sidecars for explicit QUDT quantity kinds and
QUDT/UO units under #85. Reuse the existing record kind and seal without changing
qrec bytes or adding another unit model.

How — Package six IRIs representing three named meanings: hertz, becquerel and
radians/second, one QUDT and one UO identifier each. Extract QUDT 3.5.3 direct
`unitForQuantityKind`, SI multiplier/dimension and UCUM facts from original
files at `07acd3f9ee2c7189341f322c85154ca63c9198f2`. Check UO 2026-10-12 terms
and semantic ancestry at `311f3d222444fcf8adf032dfa58f3c1b55bd22af`.
`devtools/extract_quantity_vocabulary.py` requires exact upstream file SHA-256
identities before extraction; packaged data carries provenance and CC BY 4.0
attribution, independently of the MIT implementation.

Why — A Gaia proper-motion rate must not become a frequency or radioactive
activity merely because its SI exponents equal inverse time. The measured case
is the real six-source Gaia fixture shared with #126; synthetic Hz/Bq controls
isolate the same-dimension failure mechanism.

## Semantic contract

- Consumers select the kind before constructing the record, then explicitly
  supply both IRIs. The record's kind must already match the chosen QUDT kind.
- Named unit and authoritative SI meaning must both match. Other scales and
  unnamed SI expressions need explicit consumer conversion before annotation.
- UO identifies a unit/category, not a QUDT quantity kind. The three crosswalks
  are reviewed **local PyUnitWizard alignments**, not upstream `exactMatch`
  assertions. No alias guessing, ontology reasoning or automatic kind inference.
- The sidecar seals the record digest, catalogue digest and selected IRIs;
  readers require their own expected IRIs. It is integrity, not authentication
  or proof that the consumer's scientific interpretation is correct.
- Unknown vocabulary entries, mismatched kinds and tagged global annotations
  are refused. Extending this subset needs identified consumer evidence,
  authoritative inputs, tests and a new catalogue/version decision.

Source and installed resource qualification remains pending. The standalone
catalogue works offline without importing RDF, UCUM or astronomy providers.
