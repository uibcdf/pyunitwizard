---
summary: Public record values can be made writable behind the integrity seal.
issue: uibcdf/pyunitwizard#100
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: high
verification: reproduced
area: [serialization, integrity]
guard: tests/test_quantity_record.py::test_record_values_cannot_be_made_writable
normative:
blocked_by: []
supersedes: []
---

# QuantityRecord values behind the seal

## What

`QuantityRecord.values` exposes a NumPy array with mutable owning storage. Its
initial write flag is false, but callers can set it true and alter a scientific
value without updating the integrity digest. An ordinary `to_quantity` read then
returns that altered value. Reproduction at published source `f34b111`: a 3 nM
record reads 3000 nM with its original digest after public write-flag reactivation.

## How

The regression-first run fails the reactivation guard and passes source isolation.
Store the existing dtype/shape snapshot over immutable bytes. NumPy refuses to
enable writes even through the returned array. This retains one independent
numeric snapshot, public signatures, qrec/0.3 manifests, encoding, seals and
reader handshakes. It does not add repeated hashing to every scientific read.

## Why

A read-only flag alone does not protect an owning NumPy allocation. The public
values property promises that callers cannot change values behind the seal;
immutable backing enforces that promise without relying on caller discipline.
Private attribute replacement and deliberate resealing remain outside the
mistake-protection contract.

## Validation and closure

The named guard tests that `setflags(write=True)` raises and the original
serialized values still read unchanged. A second guard mutates the input array
after construction and verifies that the record remains detached. Record
round trips and frozen vectors must continue passing before closure. The owning
QuantityRecord implementation/design issues are #82/#83; this defect does not
promote their provisional schema or API.

## Resolution — 2026-10-04

Fixed in `fc062598fb968988acb493cd2e6ef2f2537c3423`. The regression first failed
and now refuses write-flag reactivation; input-isolation and all frozen vectors
pass. Linux/macOS Python 3.11–3.14 full matrix and release gates pass at that
runtime source. An installed wheel outside checkout passes 63 record cases
(1 strict-JSON NaN skip). The receipt is
`devguide/evidence/quantity_record_mvp_2026-10-04.json`; subsequent consumer
canaries and archival guidance do not relabel its exact runtime source.
