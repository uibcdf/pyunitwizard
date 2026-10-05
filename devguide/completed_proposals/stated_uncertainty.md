---
summary: Bind a scalar measurement to its stated uncertainty without statistical inference.
issue: uibcdf/pyunitwizard#90
status: resolved
opened: 2026-10-04
closed: 2026-10-04
verification: measured
area: [serialization, interoperability]
guard: tests/test_measurement_record.py::test_sabueso_statement_round_trip_under_another_policy
normative: devguide/api_freeze_pre_1.0_decision.md
blocked_by: []
supersedes: []
---

# Stated uncertainty

What — Sabueso #37 stores stated SD/SEM/bare ± half-widths or confidence interval
bounds as separate sealed columns. Their association and `kind`, `level`, `n`
remain consumer-owned metadata. A reusable provider record should bind them.

How — Add a bounded provisional `MeasurementRecord` in its own module, reusing
QuantityRecordBundle and the existing canonical seal operation. A new explicit
`qrec-measurement/0.1` envelope binds metadata to the bundle digest. Do not change
qrec/0.3 or bundle/0.3. Implement finite scalar statements, four kinds, optional
positive integral replicate count and CI-only fractional confidence level.
Require matching dimensions, nonnegative half-width, ordered CI bounds and no
shape broadcasting. CI bounds need not contain a separately stated estimator.
Temperature half-widths use differences (K/delta units), never absolute offsets.

Why — The actual source statement must survive storage and negotiated unit
conversion without a reader guessing what a spread represents. This is inert
transcription: no propagation, SD-to-SEM inference, interval estimation,
distributions, classification changes or rounding of source precision. Sabueso
keeps its verbatim data and adoption/migration decisions. Its published decision
is `devguide/DECISIONS.md`, “Ranges and stated uncertainty” (2026-09-25).

Acceptance — Regression-first consumer examples, seal and expectation refusal,
metadata/shape/dimension/nonfinite rejection, affine scale-only conversion,
backend round trips, lazy imports, existing frozen vectors, full suite, docs and
installed-file evidence. Admit this named experimental exception in the RC scope
and retain the 1.0 release decision as provisional. Arrays and general statistical
computation require separately justified future work.

## Resolution — 2026-10-04

Implemented at `cda2108aba41abdd6336a1837ba7b40fc89a7070`. The named guard
preserves all three ± meanings and converts the original Sabueso example
under a different session policy without changing the seal. All 47 statement
cases pass, including CI metadata, tampering, exact scalar dtype, affine
spread/bounds and existing backend exports with explicit units. Linux/macOS
Python 3.11–3.14 and release gates pass at the exact runtime source.
An installed wheel outside checkout passes the same 47 cases; all shipped
package files match. See `devguide/evidence/stated_uncertainty_2026-10-04.json`.

The initial CI job passed tests and failed Codecov TLS upload; same-head retry
fails at the same external upload step. Coverage upload remains unresolved;
full scientific matrix, release gates and policy pass. The API/format stay provisional through the named RC checklist
exception. Sabueso adoption, source text/precision and migration stay with
its owner; closing this provider issue does not claim consumer adoption.
