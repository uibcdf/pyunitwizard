# Backend Coverage and Expectations

PyUnitWizard gives you one public contract across multiple unit ecosystems.
That does not mean every backend behaves identically in every edge case.

When evaluating or operating an integration, it helps to think in two layers:
- the PyUnitWizard contract (construction, conversion, checks, standardization),
- backend-specific parsing and representation details.

In practical terms:
- Pint is often the easiest baseline for deterministic parser/form behavior.
- For standard nm, angstrom and pm in PyUnitWizard's Pint registry,
  `convert()` and `get_value(..., to_unit=...)` scale binary64 magnitudes with
  one rounding. For example, `puw.get_value(puw.quantity(5, 'angstrom',
  form='pint', parser='pint'), to_unit='nm')` gives `0.5`. This also applies
  to float64 arrays and exactly representable integer scalars. An explicit
  target is independent of session standards. Foreign registries, active
  Pint contexts and other conversions use the corresponding backend
  arithmetic. Adjacent input values can still round to the same output value.
- OpenMM, unyt, and Astropy are fully valid targets, but string parsing and
  representation conventions may differ from Pint-centric examples.
- Astropy accepts thermochemical `cal`, `calorie`, `kcal` and `kilocalorie`,
  including `kcal/mol`: one calorie is exactly 4.184 joules. For example,
  `puw.get_value(puw.quantity(12.552, 'kJ/mol', form='astropy.units'),
  to_unit='kcal/mol')` returns approximately 3. Unit objects and direct Astropy
  defaults use the same definition. PyUnitWizard scopes native caloric-unit
  activation to parsing and restores the Astropy registry after failures too.
  Conflicting named definitions are refused. Native Astropy unit contexts are
  process-wide; concurrent application-owned registry changes require external
  serialization, as with Astropy's own unit contexts.
- [OpenFF](openff.md) is an optional target with its own registry. Its official
  Conda 0.4.0 package needs Python 3.12–3.14 and Pint <0.26; crossings refuse
  definition disagreements and raw val/unit data is explicitly unsealed.

A safe rollout strategy is:
1. choose one backend as canonical in production,
2. define explicit parser/form defaults,
3. add cross-backend tests only after baseline behavior is stable,
4. document any backend-specific caveats for your users.

If your library supports multiple backends, include tests for:
- conversion equivalence,
- compatibility and dimensional checks,
- standardized output invariants.

Use the API reference while validating support details:
- [Users API Reference](../../api/users/api_user.rst)
- [Developers API Reference](../../api/developers/api_developers.rst)

## NumPy object arrays of numeric rows

Some neighbor-list APIs expose a NumPy `dtype=object` array with shape
`(n_structures, n_query_atoms)`, each element holding a one-dimensional
numeric NumPy array. Rows may have unequal lengths. Equal-length rows stored
this way remain object rows; they are not a dense numeric matrix.

The following contract covers direct `puw.quantity(rows, unit, form=...)`
construction, raw `get_value()` and explicit unit conversion of finite
float64 rows. Construction is qualified with both a native unit object and
a string unit parsed by Pint.

| Form | Construct and extract | Convert nm to angstrom |
| --- | --- | --- |
| `pint` | Retains numeric row buffers | Supported |
| `openmm.unit` | Retains numeric row buffers | Supported |
| `openff.units` (optional) | Retains numeric row buffers | Supported |
| `unyt` | Retains numeric row buffers | Refused for populated outer containers |
| `astropy.units` | Refused | No row quantity to convert |

Pint, OpenMM and unyt are tested with unequal lengths, equal lengths, empty
rows and an empty outer shape `(1, 0)`. Unyt can convert the empty outer
container; a populated outer container containing only empty rows still
fails native conversion. Astropy refuses all four object-row cases. The
optional OpenFF guard qualifies unequal rows. Translation among Pint,
OpenMM and unyt preserves row values and outer shape. Translation to Astropy
raises the same diagnostic as direct construction.

```python
import numpy as np
import pyunitwizard as puw

flat = np.array([0.2, 0.4, 0.6], dtype=np.float64)
rows = np.empty((1, 2), dtype=object)
rows[0, 0], rows[0, 1] = flat[:1], flat[1:]
quantity = puw.quantity(rows, "nm", form="pint", parser="pint")
assert puw.get_value(quantity)[0, 1] is rows[0, 1]
converted = puw.get_value(quantity, to_unit="angstrom", parser="pint")
np.testing.assert_allclose(converted[0, 1], [4.0, 6.0])
```

Direct construction retains the numeric rows and their backing buffers after
the original container is deleted. It shares their storage: caller edits to
a row are visible to the quantity. Copy the numeric rows first when isolation
is required. This guarantee does not cover backend-native multiplication by
a unit, outer-container identity, or allocation-free unit conversion.
Conversion leaves the input rows and the application's unit policy unchanged;
its numeric results follow backend arithmetic.

Unsupported construction or conversion raises
`puw.UnsupportedRepresentationError`, a `TypeError` subtype with catalog code
`PUW-ERR-REP-001`, naming the backend and operation. The message recommends
flat numeric values with CSR offsets, or processing each numeric row
separately. `get_value(..., to_unit=...)` has the same conversion limits.
Unit-dimension errors retain their native diagnostic, and dense object
arrays containing scalar numbers retain native constructor behavior.

For portable variable-length values, construct one quantity from the flat
numeric buffer and keep CSR offsets in the scientific schema owned by the
consumer. `QuantityRecord` continues to require numeric arrays and rejects
object arrays; object-row support does not provide pickle persistence.
