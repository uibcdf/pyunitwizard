# Verified HDF5 snapshots and CF units

`pyunitwizard.storage.hdf5` is an optional **provisional** snapshot binding,
`qrec-hdf5/0.1`, over the existing `qrec/0.3` record. It preserves the record's
values, dtype, shape, field, kind and seal. No existing qrec bytes are redefined.

Install the optional providers:

```bash
conda install -c conda-forge cf-units=3.3.1 h5py=3.16.0
```

Importing these modules does not import either provider. The baseline package
requirements, computing forms and session parser selection stay the same.

## Write and read one quantity

```python
import h5py
import numpy as np
import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord
from pyunitwizard.storage import hdf5

record = QuantityRecord.from_quantity(
    puw.quantity(np.zeros((1, 22, 3), dtype=np.float32), 'nanometer', form='pint'),
    field='coordinates',
)
with h5py.File('quantities.h5', 'w') as file:
    hdf5.write(file, 'coordinates', record, cf_unit='nm')

with h5py.File('quantities.h5', 'r') as file:
    saved = hdf5.read(file['coordinates'], field='coordinates', unit='nanometer')
    coordinates = saved.to_quantity(unit='angstrom', form='pint')
```

The group owns one numeric `values` dataset. Its `pyunitwizard` attribute holds
the original record metadata and a separate binding seal; its CF `units` and
optional `units_metadata` attributes must agree with that seal. The reader
checks the complete array on every read. It refuses missing metadata, edited
values/units/dtype/shape, raw appends, extra datasets and secondary dataset-unit
attributes. It never reads a fallback unit from the file root or parent.

`read(..., unit=...)` checks compatible units and returns the original record
with its unchanged seal. Convert through `to_quantity` when needed. Use
`field`, `dimensionality` and `kind` to declare what the reader expects.

Writing requires a new direct child name and never overwrites existing data.
Validation happens before a temporary group is created. A caught write failure
removes that temporary group; publication uses an HDF5 link move. This does
not promise crash recovery, concurrent-writer transactions or append support.
The caller owns file handles, flushing, compression and storage policy. This
initial binding writes an uncompressed snapshot and materializes its full
values/envelope in memory; partial reads and incremental verification are outside
its scope. NaN, infinity, scalars and empty multidimensional arrays are supported.

This provider tool does not migrate MolSysMT's H5MSM format or establish a new
H5MSM schema. Consumers own their format integration and legacy-file handling.

## Explicit CF dialect tools

CF spellings are interpreted by actual `cf-units`/UDUNITS, with independently
verified computing units. The writer requires an explicit negotiated spelling;
it does not generate one from a guessed alias table.

```python
from pyunitwizard.dialects import cf

cf.validate_unit('nanometer / picosecond', 'nm ps-1')
q = cf.parse_quantity([10, 20], 'nm', unit='angstrom', form='pint')
assert list(q.magnitude) == [100, 200]
```

`validate_unit` requires equal dimensions, scale and offset at relative tolerance
1e-12, so the label describes unchanged numbers. For example, labelling nanometer
values as `m` fails. Real definition drift, such as UDUNITS `u` versus Pint
`dalton`, also fails rather than silently relabelling values. `parse_quantity`
uses UDUNITS' actual conversion to an explicitly requested computing unit and
may promote numeric dtypes. Neither operation changes session unit defaults.

The bounded dialect supports named physical units, products and integer powers.
Reference-time/calendar coordinates, logarithmic units, unknown/no-unit sentinels
and arbitrary numeric scale/offset expressions are refused. A dimensionless
quantity requires the explicit spelling `1`. This is unit interoperability,
not validation of a complete CF dataset or its standard-name/kind semantics.

## Temperature needs its meaning

A CF temperature label alone does not distinguish an on-scale temperature from
a temperature difference. Declare the meaning explicitly, including for Kelvin:

```python
cf.validate_unit('degree_Celsius', 'degC',
                 units_metadata='temperature: on_scale')
cf.validate_unit('delta_degree_Celsius', 'degC',
                 units_metadata='temperature: difference')

absolute = cf.parse_quantity(25, 'degC', unit='kelvin',
                             units_metadata='temperature: on_scale', form='pint')
difference = cf.parse_quantity(25, 'degC', unit='kelvin',
                               units_metadata='temperature: difference', form='pint')
# absolute is 298.15 K; difference is 25 K.
```

Pass the same `units_metadata` to `hdf5.write` for temperature records. Its value
is covered by the binding seal. Unknown temperature semantics are refused;
compound temperatures require difference semantics because on-scale compound
conversion cannot be determined from units alone.

The physical-unit rules and these temperature distinctions come from the
[CF conventions](https://cfconventions.org/cf-conventions/cf-conventions.html#units).
The provider's [public Unit operations](https://cf-units.readthedocs.io/en/stable/unit.html)
own UDUNITS parsing and conversions.
