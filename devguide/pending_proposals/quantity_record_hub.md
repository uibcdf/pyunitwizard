---
summary: Evaluate QuantityRecord as a backend translation hub.
issue: uibcdf/pyunitwizard#106
status: open
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
