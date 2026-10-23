---
summary: Verify explicit case-sensitive UCUM codes at biomedical exchange boundaries.
issue: uibcdf/pyunitwizard#125
status: active
opened: 2026-10-23
closed:
verification: inspected
area: [units, interoperability]
guard:
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

Contract and installed qualification are provisional until completed. This
slice alone neither closes #85 nor qualifies publication of 0.29.0.

## Actual provider findings

ucumvert 0.3.2 maps UCUM apostrophe (angle minute in the original essence
definition) to Pint's time minute. A reproducing guard failed before the bounded
atom admission rule was added. Do not expose unchecked beta-provider atoms;
qualify new atoms independently. Its default transformer also selects Pint's
application registry; this adapter supplies an isolated dedicated registry
explicitly and guards that global application definitions stay unchanged.
