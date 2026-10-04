---
summary: Evaluate an optional Zarr binding for QuantityRecord.
issue: uibcdf/pyunitwizard#104
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

# Evaluate an optional Zarr binding for QuantityRecord

What — Track the deferred chunked storage binding from #82 independently.

How — Start from an identified consumer array. Design one authoritative in-object descriptor and verified chunks, using documented reusable operations. A units attribute must agree with the sealed descriptor; chunk checksums alone do not establish unit integrity.

Why — Chunked storage may serve large datasets, but consumer demand and actual costs remain unmeasured.

Acceptance — Record a real workload and supported optional installation; preserve dtype/shape/unit/kind across round trips; refuse missing or conflicting manifests, raw chunk writes, metadata changes and truncation; measure verification costs. Keep append API, format version changes and stable promotion separately owned.

Origin — #82/#83 scope reconciliation; qrec/0.3 and the existing public API remain provisional.
