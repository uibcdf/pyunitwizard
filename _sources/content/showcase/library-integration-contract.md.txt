# Library Integration Contract

This showcase is for maintainers integrating PyUnitWizard into a scientific
library with a public API consumed by many users.

The core idea is simple: put unit decisions at the boundary, not in business
logic. When inputs enter your API, normalize and validate. When outputs leave
your API, standardize.

A practical contract usually has three parts:
- one centralized initialization path (`puw.configure`),
- boundary-level conversion and dimensional checks,
- standardized outputs in release-critical paths.

This contract makes runtime behavior more reproducible and reduces support
incidents caused by hidden assumptions about units.

## When to use this pattern

Use this pattern when your public API accepts heterogeneous quantity inputs and
you need deterministic behavior across modules and releases.

## When not to use this pattern

Do not start here if your library still has unstable API boundaries. First
stabilize the public entry points, then add the PyUnitWizard contract there.

A minimal flow looks like this:

```python
import pyunitwizard as puw

puw.configure.reset()
puw.configure.load_library(["pint"])
puw.configure.set_default_form("pint")
puw.configure.set_default_parser("pint")
puw.configure.set_standard_units(["nm", "ps", "kcal", "mole"])


def run(distance):
    q = puw.convert(distance, to_form="pint")
    if not puw.check(q, dimensionality={"[L]": 1}):
        raise ValueError("distance must have length dimensionality")
    return puw.standardize(q)
```

When this pattern is in place, maintainers can reason about unit behavior as an
explicit API contract rather than as scattered implicit conventions.

Notebook companion:
- [In_Your_Library.ipynb](../user/In_Your_Library.ipynb)
- [Configuration.ipynb](Configuration.ipynb)
