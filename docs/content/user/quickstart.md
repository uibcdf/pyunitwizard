# Quick Start

This walkthrough is intentionally short. Its purpose is to let you verify, in a
few minutes, whether PyUnitWizard matches your workflow expectations.

We will configure a single backend, construct one quantity, convert it, and
validate that compatibility and dimensional checks behave as expected.

Start by installing the package:

```bash
conda install -c uibcdf pyunitwizard
```

or:

```bash
pip install pyunitwizard
```

Now configure runtime behavior explicitly:

```python
import pyunitwizard as puw

puw.configure.reset()
puw.configure.load_library(["pint"])
puw.configure.set_default_form("pint")
puw.configure.set_default_parser("pint")
```

At this point, parsing and output form are deterministic, which is the first
requirement for reproducible library behavior and stable tests.

Create and convert a quantity:

```python
distance = puw.quantity(1.0, "nanometer")
distance_angstrom = puw.convert(distance, to_unit="angstrom")
print(puw.to_string(distance_angstrom))
```

You should obtain a value equivalent to `10.0 angstrom`.

Finally, verify compatibility and dimensional assumptions:

```python
a = puw.quantity(1.0, "nanometer")
b = puw.quantity(10.0, "angstrom")

print(puw.are_compatible(a, b))
print(puw.check(a, dimensionality={"[L]": 1}))
```

Both checks should return `True`.

If you prefer notebook examples for this same flow, open:
- [Importing.ipynb](Importing.ipynb)
- [Quantities_and_Units.ipynb](Quantities_and_Units.ipynb)
- [Convert.ipynb](Convert.ipynb)

If this behavior is what you need, continue with
[Mini Library Walkthrough](mini-library-walkthrough.md).
