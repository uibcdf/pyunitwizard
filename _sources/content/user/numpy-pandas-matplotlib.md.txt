# NumPy, Pandas, and Matplotlib Interoperability

PyUnitWizard supports two complementary styles for frontend interoperability:

1. Explicit boundary helpers (`pyunitwizard.utils.*`) when you want full control.
2. Transparent mode (`setup_*` / context managers) when you want to keep
   standard `numpy`, `pandas`, and `matplotlib` calls.

## NumPy

Transparent mode:

```python
import numpy as np
import pyunitwizard as puw

puw.utils.numpy.setup_numpy(enable=True)
q = puw.quantity([1.0, 2.0, 3.0], "meter")
out = np.mean(q)
```

Supported transparent operations include:
- `np.mean`
- `np.sum`
- `np.std`
- `np.var`
- `np.dot`
- `np.linalg.norm`
- `np.trapezoid` (and `np.trapz` if present)

Explicit wrappers are also available in `puw.utils.numpy`.

## Pandas

Explicit boundary helpers:

```python
import pyunitwizard as puw

df = puw.utils.pandas.dataframe_from_quantities(
    {"length": puw.quantity([1.0, 2.0], "nanometer")}
)
q = puw.utils.pandas.get_quantity_column(df, "length")
```

Transparent accessor mode:

```python
puw.utils.pandas.setup_pandas(enable=True)
q = df.puw.get_quantity("length")
```

Metadata-safe table helpers:
- `puw.utils.pandas.concat`
- `puw.utils.pandas.merge`
- `puw.utils.pandas.set_units_map`
- `puw.utils.pandas.sync_units_map`

## Matplotlib

Transparent plotting bridge:

```python
import matplotlib.pyplot as plt
import pyunitwizard as puw

puw.utils.matplotlib.setup_matplotlib(enable=True)
```

After enabling, compatible quantities from supported backends can be plotted
with standard matplotlib calls while keeping axis unit handling and compatibility checks.

## Recommended production pattern

For libraries integrating PyUnitWizard:
1. Keep frontend usage explicit in integration boundaries.
2. Use transparent mode in higher-level user workflows.
3. Keep backend-matrix tests to validate mixed-form behavior over time.
