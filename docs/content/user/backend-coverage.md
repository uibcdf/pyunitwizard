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
