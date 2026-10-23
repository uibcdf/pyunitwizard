---
summary: Evaluate QuantityRecord as a backend translation hub.
issue: uibcdf/pyunitwizard#106
status: active
opened: 2026-10-04
closed:
verification: inspected
area: [serialization, interoperability]
guard:
normative:
blocked_by: []
supersedes: []
---

# Evaluate QuantityRecord as a backend translation hub

What — Separate the deferred translation-hub evaluation from the design record #83 and MVP #82.

How — Measure selected real backend-to-backend pipelines against current translators. Evaluate whether SI descriptors can support independently useful translators without duplicating unit semantics or silently changing registry definitions; retain explicit dimensional/kind and affine checks.

Why — The design discusses reducing pairwise translators to one hub, but current record construction/read-to-quantity still uses Pint. The implemented inert storage form does not establish a Pint-independent translation hub.

Acceptance — Provide numerical/parity/definition-conflict tests and performance/maintenance evidence for a real workflow; identify precisely which dependencies and conversions disappear. Preserve existing signatures and scientific behavior. Implementation or deferral must follow evidence; no automatic replacement of current dispatch.

Origin — #82/#83 scope reconciliation; qrec/0.3 and the existing public API remain provisional.

## Evaluation plan — 2026-10-22

Use the published TopoMT coordinate fixture already retained in this repository
as a concrete molecular-data boundary. Compare public direct conversion,
live quantity to freshly sealed record to target, and an already-stored record
read to target. Do not compare the last case as if it paid the writer's cost.
Measure warmed repeats with telemetry explicitly enabled and disabled; retain
raw samples, source/input hashes and actual runtime/provider versions. Add parity,
affine, field/kind, tamper and conflicting-registry checks before timing.

An initial OpenMM-to-unyt angstrom probe fails because the existing translator
passes symbol `A` to unyt as amperes. Track and fix that separately before using
the route as performance evidence; a translator bug is not justification for a
new hub. No new record format, dispatch replacement or Pint-removal claim is
authorized by the evaluation alone.

The sequential pre-correction measurements also find an unyt→Astropy outlier:
its adapter calls `to_pint()` without the shared registry, causing construction
on every conversion (separately owned by #122). Add a live via-Pint control and
remeasure after that fix. The record path must not receive architectural credit
for avoiding a removable translator allocation. Before/after measurements retain
their own tool/source hashes and cost scopes.
