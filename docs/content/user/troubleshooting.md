# Troubleshooting

When unit behavior fails, most incidents fall into a small set of patterns.
This page helps you identify those patterns quickly.

## Parser cannot interpret a string quantity

This usually means runtime parser configuration is incomplete or the input
syntax does not match the selected parser.

Start by checking parser state:

```python
import pyunitwizard as puw

print(puw.configure.get_default_parser())
print(puw.configure.get_parsers_loaded())
```

If the expected parser is missing, load/configure it in your centralized
initialization path rather than patching ad hoc in business code.

Example symptom in host libraries:
- `ValueError: could not parse quantity '10 A'`

Typical fix:
- ensure parser backend is loaded,
- align input syntax with the configured parser.

## Conversion fails or returns an unexpected form

In most cases, either the destination backend is not loaded or the two
quantities are not dimensionally compatible.

Confirm loaded libraries and compatibility before conversion. This avoids
failures that appear later as obscure downstream errors.

Example symptom:
- conversion from a length quantity to a time unit unexpectedly fails.

Typical fix:
- verify dimensional compatibility with `are_compatible(...)` before conversion.

## Dimensional check fails unexpectedly

If a dimensional check fails, first inspect the parsed dimensionality instead of
assuming the input unit meant what you expected:

```python
print(puw.get_dimensionality(quantity))
```

This often reveals a parser mismatch or an input typo.

## Standardized output is not what your team expects

When standardization looks wrong, the root cause is often incomplete or
misaligned standard units configuration.

```python
print(puw.configure.get_standard_units())
```

Review standard units as part of project configuration, not per-function logic.

## Tests are flaky across files

Flaky behavior is typically caused by shared mutable configuration across test
modules.

Use this pattern consistently:
- reset configuration in test setup,
- apply explicit scenario configuration in each test module.

Notebook support for troubleshooting patterns:
- [Check.ipynb](Check.ipynb)
- [Dimensionality.ipynb](Dimensionality.ipynb)
- [Similarity.ipynb](Similarity.ipynb)
