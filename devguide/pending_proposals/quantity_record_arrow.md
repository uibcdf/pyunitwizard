---
summary: Evaluate an optional Arrow and Parquet binding for QuantityRecord.
issue: uibcdf/pyunitwizard#103
status: active
opened: 2026-10-04
closed:
verification: measured
area: [serialization, interoperability]
guard: tests/storage/test_arrow.py
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

## Maintainer-selected implementation — 2026-10-23

The maintainer selected #104, #102, #105 and #103 in that order and chose
both molecular arrays and heterogeneous observations from existing repositories.
The bounded contract is `docs/content/user/record-extensions.md`; no existing
consumer file/schema is migrated. Retained H5MSM coordinates and Sabueso's
343 ChEMBL observations supply actual input provenance. Repeated coordinate
frames in stress measurements are synthetic, not additional MD data.

The reusable owner operations are on QuantityRecord and the optional storage
modules; core forms and backend probe order are unchanged. Generic typed-array
restoration/metadata validation and metadata digests live in the codec, rather
than duplicated codecs in bindings. Zarr and Arrow use lazy DepDigest guards.
Domain failures retain RecordError/SMonitor diagnostics and original causes.
No new scientific method or attribution-session semantics are introduced; no
provider is imported or credited at startup. Optional profile versions are
Zarr 3.1.6 and PyArrow 25.0.0, published on PyPI/conda-forge. The development
profile declares them; baseline runtime/test requirements stay unchanged.

Tests were added before implementation. Source tests, real-boundary guards and
`devtools/benchmark_record_extensions.py` retain parity and raw timing samples.
Required full-suite, documentation and native optional installed matrix evidence
will be recorded at closeout. The public artifact and release remain separately
qualified; no new version is announced from source-only evidence.

## Local validation and retained measurements

Complete local Python 3.14.7 suite: **972 passed, one expected strict-JSON/NaN
skip and the existing main-module deprecation warning**, 51.46 seconds. Zarr
3.1.6/PyArrow 25.0.0 are real providers. Zarr and its transitive packages plus
physipy/quantities are task-local overlays; the shared environment is unchanged.
The sandbox blocks even a provider-only asynchronous Zarr group creation; the
owned probes were terminated and the same operations pass outside that sandbox.
This is an execution-environment restriction, not a hidden backend fallback.

Ruff lint/format passes (225 files). An owned-copy Sphinx build with
`-W --keep-going` completes without warnings. The updated storage workflow
retains the full optional source suite and copied installed tests outside
checkout on Linux/macOS arm64 and Python 3.11–3.14; its exact bytes are reviewed
in `devtools/dependency_routes.toml`. Native receipts will identify the tested
source/attempt rather than imply public-artifact qualification.

Raw operation samples, byte counts, versions, input provenance and source hashes:
`devguide/evidence/record_extensions_2026-10-23.json`. The reused measurement
tool has an executed parity/input-preservation guard. Three serial samples per
read/codec operation are retained; one complete initial write is reported,
including its initialization cost. Tiled coordinates are explicitly synthetic.
Tagged construction is compared with record/bundle construction without
including wire encoding in only one timed path. Wire sizes are separate.

Pre-rollout notice: https://github.com/uibcdf/molsyssuite/issues/46#issuecomment-6370463613 .
Actual consumer adoption and stable-format promotion remain centrally/locally
owned separately. After the next package and GitHub Release are published and
verified, the maintainer requests a separate MolSysSuite version-availability
issue; the pre-rollout notice does not satisfy that future handoff.

## #103 interpretation

Actual PyArrow/Parquet round trips cover the coordinate and heterogeneous
activity inputs. The activity Parquet file is 3829 bytes; its complete
verified read median is 2.551 ms. The tiled coordinate file is
4985 bytes, versus 1467736 bytes of JSON; compression benefits
from repeated synthetic data and cannot predict a real trajectory's ratio.
Initial write costs are retained separately, including provider initialization.
Value dtype/shape, signed zero, codes and sealed schema metadata are checked;
nulls are refused rather than converted to NaN. The contract explicitly requires
complete tables/files and per-descriptor expectations for tagged data.
This is not a domain table schema, column-projection verifier or cloud writer.
