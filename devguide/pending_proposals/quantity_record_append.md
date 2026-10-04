---
summary: Define verified append operations for block-based QuantityRecords.
issue: uibcdf/pyunitwizard#105
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

# Define verified append operations for block-based QuantityRecords

What — Track the deferred growing-record scope from #82 independently.

How — Define a reusable codec operation that converts incoming quantities to the negotiated unit, writes/seals new blocks and binds their order/shape to the top manifest. Retain immutable snapshots and reader expectations; storage binding behavior is separately owned.

Why — The format describes blocks but the current writer produces a complete snapshot. Growing trajectories must not permit raw appends to bypass the seal.

Acceptance — Obtain a measured growing-data consumer; specify snapshot/atomic-failure behavior, exact dtype/unit conversion and shape constraints; refuse reordered, removed, truncated or raw-appended blocks; measure total and incremental costs. Do not mutate already published qrec/0.3 bytes or promise an HDF5/Zarr API from this issue.

Origin — #82/#83 scope reconciliation; qrec/0.3 and the existing public API remain provisional.
