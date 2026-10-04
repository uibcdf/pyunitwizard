---
summary: Specify and evaluate a tagged layout within QuantityRecord.
issue: uibcdf/pyunitwizard#102
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

# Specify and evaluate a tagged layout within QuantityRecord

What — Track the deferred heterogeneous layout from #82/#83 as its own proposal.

How — Retain one QuantityRecord class with a local unit-descriptor table and explicit per-value or broadcast codes. Define the serialized layout before implementation; compatibility requires an explicit version decision, not reinterpretation of existing qrec/0.3 records.

Why — The maintainer decided that homogeneous and tagged representations are layouts of one inert form. Normalized Sabueso columns are homogeneous, so mixed-unit implementation requires a measured consumer case.

Acceptance — Identify an actual heterogeneous workload and measure alternatives; seal descriptors, codes, dtype/shape and values together; require an explicit target unit or split when reading to a computing backend; reject dimension/kind conflicts and altered codes. No implicit mixed-unit coercion or live arithmetic.

Origin — #82/#83 scope reconciliation; qrec/0.3 and the existing public API remain provisional.
