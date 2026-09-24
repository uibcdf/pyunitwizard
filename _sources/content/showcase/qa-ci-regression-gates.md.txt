# QA and CI Regression Gates

This showcase is for maintainers who need stable behavior across releases.

Unit regressions often appear as subtle behavior drift: a parser default changes,
a conversion path shifts backend form, or standardization rules are bypassed in
one endpoint. The best defense is a small set of explicit gates.

A practical release gate set for PyUnitWizard integrations includes:
- deterministic runtime configuration checks,
- boundary tests for conversion success and expected failures,
- dimensional compatibility assertions for representative workflows,
- standardization invariants on public outputs.

## When to use this pattern

Use this pattern when your library is already integrated and you want to
protect behavior through CI and release cycles.

## When not to use this pattern

Do not begin with full release gates before the first integration path is
stable. Establish boundary contracts first, then harden with CI gates.

Example assertions to keep in CI:

```python
import pyunitwizard as puw

puw.configure.reset()
puw.configure.load_library(["pint"])
puw.configure.set_default_form("pint")
puw.configure.set_default_parser("pint")

q = puw.quantity(1.0, "nanometer")
assert puw.check(q, dimensionality={"[L]": 1})
assert puw.are_compatible(q, puw.quantity(10.0, "angstrom"))
```

## Regression case: parser drift detected before release

Symptom:
A release candidate starts failing on user inputs such as `"10 angstrom"`
that were accepted in previous versions.

Gate that detects it:
A boundary test validates that configured parser and conversion path are stable
for representative string inputs.

```python
import pyunitwizard as puw

puw.configure.reset()
puw.configure.load_library(["pint"])
puw.configure.set_default_parser("pint")

q = puw.quantity("10 angstrom")
assert puw.check(q, dimensionality={"[L]": 1})
```

Correction:
The team restores explicit parser configuration in the initialization path and
adds this test permanently to prevent recurrence.

These tests are lightweight but high-leverage: they fail early when integration
contracts drift.

Notebook companion:
- [PyUnitWizard_Showcase.ipynb](PyUnitWizard_Showcase.ipynb)
- [Dimensionality.ipynb](../user/Dimensionality.ipynb)
- [Standardize.ipynb](../user/Standardize.ipynb)
