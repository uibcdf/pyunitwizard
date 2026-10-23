# Chunked storage, tagged observations and verified append

These **provisional additions after 0.28.1** extend `QuantityRecord` without
changing existing `qrec/0.3` or bundle bytes. They do not migrate a consumer's
files or establish a stable 1.0 contract. First public availability belongs to
the corresponding release notes.

| Operation | Supported contract |
|---|---|
| Zarr | Homogeneous snapshots, complete or contiguous first-axis reads |
| Tagged layout | Equal-shaped source quantities with local unit/kind descriptors |
| Append | A new homogeneous in-memory snapshot, extending axis zero |
| Arrow/Parquet | Complete homogeneous or tagged records in one typed table/file |

## Optional installation and import

The qualified optional development profile selects Zarr 3.1.6 and PyArrow
25.0.0. Both are published on conda-forge; Zarr 3.1.6 retains Python 3.11
compatibility, whereas newer Zarr releases may have a narrower Python range.

```bash
conda install -c conda-forge zarr=3.1.6 pyarrow=25.0.0
```

Neither provider is a required PyUnitWizard runtime dependency. Importing
`pyunitwizard.storage.zarr` or `.arrow` imports neither provider. Operations
check the selected provider through DepDigest and give an installation diagnostic
for absence; transitive import failures remain distinct. Baseline forms, parsers
and automatic backend selection are unchanged.

## Verified Zarr snapshots and partial reads

```python
import numpy as np
import zarr
import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord
from pyunitwizard.storage import zarr as storage

record = QuantityRecord.from_quantity(
    puw.quantity(np.zeros((100, 22, 3), dtype=np.float32), 'nanometer', form='pint'),
    field='coordinates',
)
root = zarr.open_group('trajectory.zarr', mode='a')
storage.write(root, 'coordinates', record, chunk_rows=16)
saved = storage.read(root['coordinates'], selection=slice(20, 30),
                     field='coordinates', unit='nanometer')
coordinates = saved.to_quantity(unit='angstrom', form='pint')
```

`qrec-zarr/0.1` stores one numeric array with the original sealed qrec metadata,
an ordered table of independently sealed chunks and a binding digest covering
their association. The in-group `units` attribute must match the authoritative
manifest; array-level secondary metadata is refused. Values, dtype, shape,
physical chunk shape and available chunk inventory are checked. Zero chunks are
written explicitly so a missing object cannot silently become default fill.

A reader must declare an expected `unit` or `dimensionality`; `field` and `kind`
provide additional checks. The returned inert record retains its stored unit.
Conversion is a separate explicit operation. Scalars, empty arrays, NaN/Inf,
signed zero and the codec's numeric dtypes are supported.

Partial reads accept unit-stride `slice` selections on axis zero. They validate
the binding and inventory, then read and verify each complete intersecting chunk.
They return a newly sealed subset, **not a certificate of unread chunk contents**.
Metadata/inventory work still scales with chunk count. A full read verifies all
chunks and the original qrec seal. An empty selection still checks the unit
descriptor and reader expectations.

Writes require a new direct child and never overwrite existing data. The final
authoritative attribute is written only after the array is complete; a caught
failure removes that newly owned child. A reader refuses an incomplete child.
The caller owns the store, permissions, lifecycle and concurrency. This route
targets Zarr format 3 without shards and uses provider-default compression;
remote object-store behavior, concurrent writers, crash recovery, tagged arrays,
and in-place/streaming append are outside this qualification.

## One class, a tagged layout

```python
observations = QuantityRecord.from_tagged(
    [puw.quantity(15000.0, 'nM', form='pint'),
     puw.quantity(50.0, 'percent', form='pint')],
    field='activities', kinds=['Ki', 'Inhibition'],
)
payload = observations.to_dict(encoding='base64')
restored = QuantityRecord.from_dict(payload)
groups = restored.split()
potency = groups[0].to_quantity(field='activities', kind='Ki', unit='uM', form='pint')
```

`qrec-tagged/0.1` identifies this layout explicitly. Its manifest contains
`layout: tagged`, field, dtype, shape and a local table of canonical unit/SI
descriptions with optional application-owned kinds. Read-only uint16 `codes`
identify one descriptor per value. Each input scalar or equal-shaped array
contributes an outer-axis entry; codes broadcast across that input's values.
The writer deduplicates descriptors in first-occurrence order. At most 65,536
descriptors are supported. Original magnitudes stay unchanged. Mixed source
dtypes promote to one common supported dtype only if their values survive
round-trip casting exactly; unsafe integer-to-float promotion is refused.

The seal binds manifest, descriptor table, numeric bytes and code bytes. JSON
codes follow the value shape; base64 encodes numeric values as in homogeneous
records. Descriptors are detached copies, and values/codes have immutable backing.
Wire shapes contain explicit nonnegative integer sizes; inferred negative sizes
are refused even when an external writer recomputes the seal.
Existing homogeneous writers still emit exactly `qrec/0.3`. Older readers may
refuse the new identifier; they must not reinterpret it as the older format.

For computation, call `to_quantity(unit=...)` with an explicit common unit.
Every descriptor must have compatible dimensions and the same declared kind.
Otherwise use `split()`, which returns flattened homogeneous records keyed by
descriptor code; `codes == key` retains their original-position association.
Kinds are source declarations, not inferred ontology mappings. Source relation,
uncertainty, identifiers and domain validity remain consumer responsibilities.

For ordinary independent fields, a bundle remains useful. Tagged records serve
a heterogeneous collection; they are not a new live arithmetic backend. Direct
core unit introspection/implicit conversion of a heterogeneous record is refused;
use its explicit `to_quantity`/`split` route. Existing bundle, HDF5 and Zarr
bindings remain homogeneous rather than silently acquiring tagged semantics.

## Append without mutating a published snapshot

```python
first = QuantityRecord.from_quantity(
    puw.quantity(np.zeros((2, 22, 3), dtype=np.float32), 'nanometer', form='pint'),
    field='coordinates',
)
later = puw.quantity(np.ones((3, 22, 3), dtype=np.float32), 'angstrom', form='pint')
combined = first.append(later)
assert first.values.shape == (2, 22, 3)
assert combined.values.shape == (5, 22, 3)
```

The homogeneous `qrec/0.3` manifest already defines ordered blocks. `append`
converts incoming rows to the receiver's unit, checks exact source dtype and
trailing shape, and seals a new block and root. A record source must match field
and kind; a computing quantity is explicitly bound to the receiver's context.
Integer conversions that lose values/range and finite floating-point overflow
are refused. Affine conversion uses the actual unit provider. An empty append
is a validated no-op.

The old snapshot and block digests remain unchanged on success or failure.
Only new blocks need hashing, but immutable array concatenation still copies
O(total values) bytes; this is not constant-cost streaming. Scalars and tagged
records are refused. This codec operation does not add an append method to
HDF5/Zarr files or promise disk transactions.

## Arrow tables and Parquet files

```python
from pyunitwizard.storage import arrow

table = arrow.to_table(record)
saved = arrow.from_table(table, field='coordinates', unit='nanometer')
arrow.write('coordinates.parquet', record)
saved = arrow.read('coordinates.parquet', field='coordinates', unit='nanometer')

table = arrow.to_table(observations)
saved = arrow.from_table(table, field='activities',
                         units=['nM', 'percent'], kinds=['Ki', 'Inhibition'])
```

`qrec-arrow/0.1` stores flattened typed `values` and, for tagged records,
uint16 `codes` columns. Original shape, descriptors and codec seals travel in
one authoritative schema-metadata envelope with its own binding digest.
The code column is checked against the tagged seal; its data is not duplicated
inside the Arrow envelope. Extra/reordered columns and secondary field metadata
are refused. Removing metadata, projecting a column or editing values/codes
does not yield a verified record.

Homogeneous readers require `unit` or `dimensionality`. Tagged readers require
`units` in descriptor-code order and may declare `kinds` in that same order.
The returned record retains its original values/units; these arguments are a
handshake, not a hidden numerical normalization.

Nulls are refused because current qrec has no missing-value bitmap. Numeric
NaN/Inf remain numeric values and never become nulls. NumPy dtype, shape and
signed zero are preserved, including scalar and empty records. This route
requires complete tables/files; it does not claim verified projection,
row-group selection, partitioned datasets, dataframe schema inference or
zero-copy verification.

Parquet uses the actual PyArrow writer with stored Arrow schema metadata.
Local publication writes an owned same-directory temporary file, then creates
the final path exclusively without overwriting existing data; staging is removed
after success/failure. This relies on local hard-link semantics and does not
qualify remote/cloud filesystems or crash-durability guarantees.

## Evidence and scientific boundaries

Consumer-derived tests use retained H5MSM coordinates and 343 ChEMBL numerical
observations from Sabueso fixtures, with original file hashes and source commits.
They exercise non-default session policy. Source relation and assay context
stay in the fixture provenance; a record seal does not validate an assay or
turn a bound into an exact measurement. Provider tests do not migrate those clients.

`devtools/benchmark_record_extensions.py` records raw operation times, input
provenance, source hashes and bytes. Its tiled coordinate stress case repeats
one real frame and is explicitly synthetic. Compare the same operation/scope;
results are not a universal speed or compression claim. Optional installed
matrix evidence and public package qualification remain separate from local
development measurements. Digests detect inconsistency, not authenticity or a
source that is already scientifically wrong.
