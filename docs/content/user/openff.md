# OpenFF quantities

The optional `openff.units` form uses OpenFF's own unit registry. Install its
official Conda distribution in Python 3.12–3.14:

```bash
conda install -c conda-forge openff-units=0.4.0
```

OpenFF 0.4.0 requires Pint >=0.24,<0.26. PyUnitWizard's base installation keeps
its existing Python 3.11–3.14 and Pint requirements; OpenFF's constraints apply
when that optional backend is installed. The current PyPI upload is yanked, so
there is no advertised `pyunitwizard[openff]` pip extra. The complete optional
test environment is `devtools/conda-envs/openff_env.yaml`.

```python
import numpy as np
import pyunitwizard as puw
from openff.units import Quantity

source = Quantity(np.arange(6, dtype=np.float32).reshape(2, 3), "angstrom")
puw.get_form(source)                         # 'openff.units'
shared = puw.convert(source, to_form="pint")
back = puw.convert(shared, to_form="openff.units")
positions = puw.convert(source, to_form="openmm.unit")
```

The bridge preserves scalars, array shapes and dtype when units are unchanged.
Conversion that rescales a value follows backend numeric rules. Before crossing
registries it checks named base units, dimensionality, scale and affine offset
with the same 1e-12 tolerance as foreign Pint quantities. Changed or missing
definitions raise `ValueError`; equal-looking strings alone do not establish
agreement. Definition differences such as CODATA revisions beyond that tolerance
are refused, rather than silently accepted. Native OpenMM conversions use the
official OpenFF tools; `Vec3` lists return NumPy arrays with their original shape.

Construction, unit extraction, dimensional checks, scalar/array strings and
reader session policies use the existing PyUnitWizard API. OpenFF is detected
from its owning registry, since its generated classes may be named
`pint.Quantity`. Importing PyUnitWizard does not import OpenFF or change its
application registry. On Python 3.11 or when OpenFF is absent, an explicit
request gives an installation/version diagnostic. Existing adapters still
determine which unit spellings they can translate to unyt or Astropy.

## Unsealed val/unit data

OpenFF-style `{val, unit}` JSON has no integrity seal or application field.
Use explicit boundary tools rather than treating any dictionary as a quantity:

```python
from pyunitwizard.forms.api_openff_units import from_dict, to_dict
from pyunitwizard.record import QuantityRecord

raw = {"val": [[1.0, 2.0], [3.0, 4.0]], "unit": "angstrom"}
quantity = from_dict(raw, unit="nanometer", dimensionality={"[L]": 1})
record = QuantityRecord.from_quantity(quantity, field="coordinates")
stored = record.to_dict()
read = QuantityRecord.from_dict(stored).to_quantity(
    field="coordinates", unit="angstrom", dimensionality={"[L]": 1}, form="openff.units"
)
exported = to_dict(read)  # Only val and unit: leaves the verified domain.
```

The raw importer requires exactly two keys, an explicit unit and finite numeric
values. It checks definitions and any supplied dimensional/unit expectations;
the caller binds the trusted application field when sealing. Raw JSON cannot
prove what field it belongs to. Export discards seals and field association;
subsequent edits have no integrity guarantee. Existing qrec/0.3 stored bytes and
reader handshakes remain unchanged. JSON carries no exact dtype metadata; use
QuantityRecord when that matters.

See [OpenFF's API](https://docs.openforcefield.org/projects/units/en/stable/api/generated/openff.units.html),
[0.4.0 dependencies](https://github.com/openforcefield/openff-units/blob/0.4.0/pyproject.toml)
and [#86](https://github.com/uibcdf/pyunitwizard/issues/86).
