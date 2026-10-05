# Mini Library Walkthrough

This page shows a small but realistic integration pattern you can adapt to your
own scientific library.

Imagine your API receives user inputs in mixed unit representations. Your goal
is to keep those differences at the boundary and avoid unit-specific decisions
inside domain logic.

Create one centralized initialization point:

```python
# mylib/_units.py
import pyunitwizard as puw


def initialize_units():
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    puw.configure.set_standard_units(["nm", "ps", "kcal", "mole"])
```

Then normalize and validate at an API entry point:

```python
# mylib/api.py
import pyunitwizard as puw


def run(distance):
    q = puw.convert(distance, to_form="pint")
    if not puw.check(q, dimensionality={"[L]": 1}):
        raise ValueError("distance must have length dimensionality")
    return puw.standardize(q)
```

From the caller side, this can now be used predictably:

```python
result = run("10 angstrom")
print(puw.to_string(result))
```

The key benefit is that your API accepts flexible inputs while your internals
consume canonicalized data and your outputs remain standardized for downstream
libraries.

Continue with [Configuration](configuration.md) to make this runtime policy
explicit and test-friendly.
