---
summary: QuantityRecord base64 export fails for empty multidimensional arrays.
issue: uibcdf/pyunitwizard#109
status: resolved
opened: 2026-10-05
closed: 2026-10-05
severity: medium
verification: reproduced
area: [serialization, record]
guard: tests/test_quantity_record_empty.py::test_empty_multidimensional_record_base64_round_trip
normative:
blocked_by: []
supersedes: []
---

# Empty multidimensional base64 export

What — Valid empty record arrays construct and seal, but exporting shape (0,3)
or (1,0,3) as base64 raises TypeError when memoryview.cast sees zero dimensions.
Reproduced independently by four failing parameter cases before the fix; flat
empty arrays already work.

How — Flatten the C-order little-endian array view before its byte cast. This
preserves existing bytes, dtype, shape, block and top digests. Do not invent
storage-specific empty-array encoding. Tests exercise float32/int32 and three
empty shapes, checking exact empty base64 payload and unchanged record seal.

Why — The new optional HDF5 binding (#101) must write empty arrays without
changing the original codec or silently dropping shape metadata.

## Resolution — 2026-10-05

The six dedicated shape/dtype cases pass after flattening the byte view. Existing
record tests and frozen wire vectors also pass; this changes no schema or stored
nonempty bytes. The guard reproduces the original failure for multidimensional
empty arrays and checks payload, dtype, shape and seal identity on reconstruction.
