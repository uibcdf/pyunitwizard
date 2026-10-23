---
summary: Verify explicit case-sensitive UCUM codes at biomedical exchange boundaries.
issue: uibcdf/pyunitwizard#125
status: resolved
opened: 2026-10-23
closed: 2026-10-23
verification: inspected
area: [units, interoperability]
guard: tests/dialects/test_ucum.py::test_every_admitted_multiplicative_atom_has_named_semantic_conformance
normative: docs/content/user/unit-dialects.md
blocked_by: []
supersedes: []
---

# Bounded UCUM physical-unit exchange

What — Add explicit UCUM parsing and verified emission under #85. The measured
consumer is the committed 343-row Sabueso/ChEMBL activity fixture: 48 nanomolar
concentrations and 295 percentages. Assay types and comparison relations remain
consumer provenance, rather than meanings inferred from a unit code.

How — Use actual ucumvert 0.3.2, its case-sensitive grammar and its unmodified
vendored UCUM 2.2 essence definitions. Validate a caller-negotiated code against
the computing unit's SI dimensions, scale and offset before emitting that code
for unchanged numbers. Import explicitly converts to a required computing unit.
Keep optional loading lazy and the existing record bytes and form order intact.

Why — Pint's `nM` alias is not UCUM. A biomedical interchange label cannot be
validated by parsing it with an unrelated computing registry.

## Acceptance boundary

- Explicitly qualified SI physical atoms plus litre/percent/time atoms,
  legal prefixes, products, quotients and integer powers;
  dimensionless `1` and percentages; explicit on-scale/difference temperatures.
- Reject annotations (the provider otherwise discards them), arbitrary units,
  nonlinear units and arbitrary numeric scale expressions. Do not infer kinds.
- Emission returns the checked, explicitly supplied code; this is not a reverse
  canonicalizer (UCUM has no unique canonical spelling and ucumvert has no
  general Pint-to-UCUM emitter).
- Actual-provider positive/negative conformance, observed biomedical values,
  unchanged input/session policy, optional-import isolation and source/installed
  Python 3.11–3.14 Linux/macOS evidence before closing.

The contract remains provisional after qualification. This slice alone does
not qualify publication of 0.29.0; release outcomes belong to #128.

## Actual provider findings

ucumvert 0.3.2 maps UCUM apostrophe (angle minute in the original essence
definition) to Pint's time minute. A reproducing guard failed before the bounded
atom admission rule was added. Do not expose unchecked beta-provider atoms;
qualify new atoms independently. Its default transformer also selects Pint's
application registry; this adapter supplies an isolated dedicated registry
explicitly and guards that global application definitions stay unchanged.

Initial optional matrix run 40009082556 found the provider's complete definition
file incompatible with Pint 0.26.2: the unrelated arbitrary-unit alias `i.U.` is
rejected by the newer Pint parser. The adapter now admits only the provider's
authored aliases for qualified atoms (Cel and Ohm), rather than loading its
unqualified full unit vocabulary. Existing actual-provider conformance guards
cover this route on Pint 0.25.3 and the current 0.26 line; new exact-head matrix
evidence is required. No provider file or shared application registry is patched.

The provider's bracketed Fahrenheit/Reaumur atoms also fail with the stricter
Pint 0.26 parser. They are consistently excluded from this first contract on all
versions; consumers convert explicitly to Celsius/Kelvin first. Admitted affine
UCUM input is `Cel`, with explicit temperature semantics. This narrows an
unpublished proposal; no previously published PyUnitWizard API is removed.


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

The selected guard checks every admitted multiplicative atom against its independently named computing meaning; separate affine, refusal and consumer cases cover the rest of this bounded UCUM contract.
