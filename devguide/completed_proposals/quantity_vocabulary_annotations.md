---
summary: Validate explicit QUDT and UO unit annotations without kind inference.
issue: uibcdf/pyunitwizard#127
status: resolved
opened: 2026-10-23
closed: 2026-10-23
verification: measured
area: [units, interoperability]
guard: tests/dialects/test_vocabulary.py::test_dimensions_and_numeric_convertibility_never_choose_semantics
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

Source and installed resource qualification are recorded in the dated outcome below. The standalone
catalogue works offline without importing RDF, UCUM or astronomy providers.


## Qualified outcome — 2026-10-23

Source `cfe067bcc4545c60aaca4c6950f6d84075ee6c36` passed all 29 mandatory
source jobs and routine CI, including actual Codecov coverage/test-result uploads.
The eight source storage/dialect wheel probes executed 247 cases each without
skips on Linux/macOS arm64, Python 3.11–3.14. Actual providers are ucumvert
0.3.2, asdf 6.0.0 and asdf-astropy 0.11.0; Pint 0.25.3 and 0.26.2 are covered.

Original producer 40014661788, attempt 1, built only
`pyunitwizard-0.29.0-py_0.tar.bz2` (94,325 bytes), SHA-256
`9169cd302dbda415ebc441ef6f5077dcde834d435626fcf80c179a9013657f34`.
All 30 exact-file installed cells and the producer verifier passed run
40018157605, attempt 1, at qualifier
`821231dbf188656b6872b5f6866b20e9114c87fb`. Its owner binding explicitly
retains the original source/file identity; #131 corrected only the qualifier's
Astropy dependency selection. The archive was not rebuilt.

Every required storage/dialect/record-extension module executed without skips
in all eight storage cells; every prepared-attribution module executed without
skips in all eight prepared cells. Whole-run counts retain the intentional
strict-JSON/NaN skip and unavailable prepared-API skips in fallback profiles.
The copied installed lane excludes its nested source-wheel builder because it
qualifies the original Conda file; source suites separately execute that builder.

Native receipts and actual source-wheel facts are retained in
`devguide/evidence/release_0.29.0_source.json` and
`devguide/evidence/unit_dialects_source_installed_2026-10-23.json`.
Archive bytes/resources, original-source binding, all 30 dependency closures and
individual case classifications are retained in `devguide/evidence/` as
`release_0.29.0_staged_bytes.json`, `release_0.29.0_installed.json` and
`release_0.29.0_installed_closures.json`. These qualify the implemented boundary;
publication/public-index observations remain separately owned by #128. All
provisional limits and consumer-owned scientific meanings above remain.

The selected guard refuses same-dimension unit/kind substitutions and unnamed or differently scaled units. Other catalogue/provenance and Gaia guards protect resource integrity and the measured consumer.
