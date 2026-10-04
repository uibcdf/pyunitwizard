---
summary: Evaluate an optional Arrow and Parquet binding for QuantityRecord.
issue: uibcdf/pyunitwizard#103
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

# Evaluate an optional Arrow and Parquet binding for QuantityRecord

What — Track the deferred columnar storage binding from #82 independently.

How — Begin with a measured consumer table. Design values and a verified unit manifest in one negotiated column/object, with owner-provided reader/writer operations and explicit handshakes. Reuse QuantityRecord seals rather than treating Parquet page checksums as unit integrity.

Why — A columnar binding could avoid per-row unit objects, but no implementation is justified solely by format popularity.

Acceptance — Document the consumer need, optional dependency/Python matrix and format mapping; preserve dtypes, shapes, null/NaN semantics and unit/kind metadata; refuse inconsistent or edited metadata/values; measure size/read/write costs. No mandatory dependency, new layout or format promotion without separate evidence.

Origin — #82/#83 scope reconciliation; qrec/0.3 and the existing public API remain provisional.
