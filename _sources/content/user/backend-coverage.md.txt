# Backend Coverage and Expectations

PyUnitWizard gives you one public contract across multiple unit ecosystems.
That does not mean every backend behaves identically in every edge case.

When evaluating or operating an integration, it helps to think in two layers:
- the PyUnitWizard contract (construction, conversion, checks, standardization),
- backend-specific parsing and representation details.

In practical terms:
- Pint is often the easiest baseline for deterministic parser/form behavior.
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
