# Scientific Script Workflow

This showcase is for scientists using a library that already embeds
PyUnitWizard.

In this context, the goal is not framework design. The goal is writing scripts
that are clear, reproducible, and easy to debug when unit assumptions fail.

A robust script workflow follows three habits:
- pass explicit units in inputs,
- check compatibility before combining quantities,
- keep the smallest reproducible snippet when reporting an issue.

## When to use this pattern

Use this pattern when you consume integrated libraries in notebooks or scripts
and need reliable day-to-day unit handling without diving into internals.

## When not to use this pattern

Do not use this as a substitute for library integration design. If you maintain
the host library, use the integration and QA showcases first.

Example pattern:

```python
import pyunitwizard as puw

length_a = puw.quantity(1.0, "nanometer")
length_b = puw.quantity(10.0, "angstrom")

if puw.are_compatible(length_a, length_b):
    merged = puw.convert(length_b, to_unit="nanometer")
```

When a check fails, inspect dimensionality directly instead of guessing:

```python
print(puw.get_dimensionality(length_a))
```

This small discipline usually resolves most day-to-day unit incidents quickly.

Notebook companion:
- [Quick_Guide.ipynb](Quick_Guide.ipynb)
- [Convert.ipynb](../user/Convert.ipynb)
- [Check.ipynb](../user/Check.ipynb)
