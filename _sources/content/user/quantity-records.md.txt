# Quantity Records

A number without its unit is the most dangerous value in a scientific pipeline. One tool
stores *3 nanomolar*; the next reads *3 picomolar*; nothing fails and the result is simply
wrong. A dimension check cannot catch it, because both are concentrations. Only a unit
that never leaves its values, and a reader that never assumes one, prevent it.

`QuantityRecord` is PyUnitWizard's form for storing and exchanging quantities. It is
**inert**, like the `"string"` form: it converts to and from every other form, but it does
not compute. To compute, convert it to pint, openmm.unit, astropy.units or unyt.

How this compares with CF/UDUNITS, ASDF, OpenFF, UCUM, QUDT and container checksums, and
why it exists, is explained in [Why QuantityRecord](quantity-records-why.md).

```{note}
Available from PyUnitWizard 0.27.0. Provisional API. `QuantityRecord` and the `qrec/0.3` format may still change before the
1.0 checklist promotes them. The design, the alternatives evaluated and the measurements
are recorded in [uibcdf/pyunitwizard#83](https://github.com/uibcdf/pyunitwizard/issues/83).
The implemented MVP is complete; its API and stored format remain provisional.
HDF5/CF, tagged layouts, Arrow/Parquet, Zarr, verified appends and hub translation
have separate proposals (#101–#106). Their tracking does not add those features
to the current format.
```

## Stated scalar uncertainty

The provisional `MeasurementRecord` envelope binds a finite scalar value to a
source-stated uncertainty. It stores the association, meaning, optional confidence
fraction and replicate count with the existing sealed quantity bundle. Its
separate format is `qrec-measurement/0.1`; existing qrec/0.3 bytes are unchanged.

```python
import pyunitwizard as puw
from pyunitwizard.measurement import MeasurementRecord

statement = MeasurementRecord.from_quantity(
    puw.quantity(12.0, "nM", form="pint"),
    kind="sd",
    half_width=puw.quantity(3.0, "nM", form="pint"),
    n=3,
    field="ic50",
)
stored = statement.to_dict()
back = MeasurementRecord.from_dict(stored)
quantities = back.to_quantities(field="ic50", kind="sd", unit="uM", form="pint")
# value: 0.012 uM; half_width: 0.003 uM; meaning remains SD, n=3

interval = MeasurementRecord.from_quantity(
    puw.quantity(10.0, "uM", form="pint"),
    kind="ci",
    lower=puw.quantity(8.0, "uM", form="pint"),
    upper=puw.quantity(12.0, "uM", form="pint"),
    level=0.95,
)
```

Kinds are `sd`, `sem`, `unspecified` (a bare “±”) and `ci`. Omitted `level` or
`n` stays unknown. The envelope refuses negative half-widths, unordered bounds,
wrong dimensions, nonfinite values and arrays; it does not broadcast a scalar
spread over an array. It checks the reader's field, kind and dimensionality.
Changing the quantities or association metadata outside the codec fails on read.
An estimator need not lie inside a separately stated confidence interval.

For temperature spreads, supply `delta_degC`, `delta_degF` or kelvin, rather
than an absolute Celsius/Fahrenheit quantity. A 20 °C value with a 3 Δ°C SD
becomes 293.15 K with a 3 K SD, or 68 °F with a 5.4 Δ°F SD. Interval bounds
are absolute quantities, so their conversion includes the offset. Backend
spellings remain subject to existing adapters: to export concentrations to
unyt or Astropy, negotiate `unit="mole/liter"` rather than the Pint-only
`nanomolar` spelling. Unsupported conversions raise `RecordError`.

This records a statement; it does not propagate errors, infer a distribution,
derive SEM from SD and `n`, or estimate confidence intervals. Source text,
stated precision, classification and migration of existing consumer schemas
remain consumer-owned. See [#90](https://github.com/uibcdf/pyunitwizard/issues/90).

## Writing and reading

```python
import json
import pyunitwizard as puw
from pyunitwizard import QuantityRecord

ic50 = puw.quantity([3.0, 12.5, 0.4], "nM")

record = QuantityRecord.from_quantity(ic50, field="bioactivity.ic50")
text = json.dumps(record.to_dict())          # store or send it

record = QuantityRecord.from_dict(json.loads(text))   # verified, or refused
q = record.to_quantity(field="bioactivity.ic50", unit="uM")
```

`record` is also a form, so the generic API works on it:

```python
record = puw.convert(ic50, to_form="record")
puw.get_form(record)                       # 'record'
puw.get_unit(record)                       # 'nanomolar'
puw.convert(record, to_form="openmm.unit", to_unit="uM")
```

## What a record guarantees

| Guarantee | How |
|---|---|
| The unit travels with the values | Every record holds its unit's canonical name *and* its description in SI base units (factor, offset, exponents). Readers check that both agree. |
| No change goes unnoticed | A blake2b digest covers the unit description and the values' bytes. Only `QuantityRecord` produces it, so a hand edit, a raw append, reordered or truncated values, or a renamed unit all fail on read. |
| The reader says what it expects | `to_quantity(field=..., unit=..., dimensionality=..., kind=...)` refuses a record bound to another field, of another dimension, or of another kind. |
| No defaults | A record without its manifest is refused. There is no fallback unit, ever. |
| Independent of the session | A record states its own unit; the session's standard units never change what it means. |
| Readable without PyUnitWizard | A reader needs a hash function, JSON and IEEE-754 floats. `pyunitwizard/_private/record_reference_reader.py` does it with the Python standard library alone, and `tests/quantity_record_vectors/` holds test vectors for readers in other languages. |

What no format can detect is a writer that is wrong *and* consistent: it meant nM, built pM,
and wrote pM. Contracts at your API boundaries and tests that compare values across tools
cover that case.

The public `record.values` array is an immutable snapshot. Direct assignment and
reactivating its NumPy write flag are refused. To change a recorded quantity,
construct a new record from the changed quantity so its seal describes the new values.

## Kinds

Some different quantities share SI dimensions: hertz and becquerel, joule and newton-metre.
Record the kind when it matters, and ask for it when reading:

```python
rate = QuantityRecord.from_quantity(puw.quantity(1.0, "1/s"), field="rate",
                                    kind="http://qudt.org/vocab/quantitykind/Frequency")
rate.to_quantity(kind="http://qudt.org/vocab/quantitykind/Frequency")
```

## Many small values: bundles

A document such as a data card holds many scalars. A `QuantityRecordBundle` seals them
together, at about half the size of one record each:

```python
from pyunitwizard import QuantityRecordBundle

card = QuantityRecordBundle.from_quantities({
    "molecular_weight": puw.quantity(180.16, "dalton"),
    "tpsa": puw.quantity(63.6, "angstrom**2"),
})
data = card.to_dict()
values = QuantityRecordBundle.from_dict(data).to_quantities(
    expected={"molecular_weight": {"[M]": 1}, "tpsa": {"[L]": 2}}
)
```

## Encodings

- `to_dict(encoding="json")` writes readable lists. It refuses NaN and infinity, which JSON
  cannot hold, so that every JSON reader, not only Python's, can load the file.
- `to_dict(encoding="base64")` writes the values' little-endian bytes (about 1.33 times
  their raw size), holds any value exactly, and is faster for large arrays.

Both encodings preserve empty multidimensional arrays with their dtype and shape.

The optional provisional [HDF5 binding and CF unit tools](hdf5-cf.md) store
numeric values with verified metadata and an explicitly negotiated CF label.
Arrow (#103), Zarr (#104), tagged layouts (#102) and verified appends (#105)
remain independent proposals.

## Not a passport

PyUnitWizard's integration guide lists "passports" as an anti-pattern: registries or caches
that remember a quantity was once canonical, so that a check can be skipped. A quantity
record is the opposite. It remembers nothing about live objects, and it is verified, never
trusted, every time it is read.
