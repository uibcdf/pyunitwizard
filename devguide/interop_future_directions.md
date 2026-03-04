# Interoperability Future Directions

This document consolidates long-term ideas extracted from:
- `devguide/scientific-python-units-layer.md`
- `devguide/expansion.md`
- `devguide/units_interoperability/*`

Its purpose is to preserve useful strategic direction without mixing it with
release-operational documents.

## Scope

This file is conceptual and forward-looking.

For active execution and release decisions, use:
- `devguide/roadmap.md`
- `devguide/release_0.21.x_rc_checklist.md`
- `devguide/release_1.0.0_checklist.md`

## Current baseline (already implemented)

As of `0.20.0`, PyUnitWizard already includes:
- runtime interoperability across `pint`, `openmm.unit`, `unyt`,
  `astropy.units`, `physipy`, and `quantities`,
- transparent frontend bridges for `numpy`, `pandas`, and `matplotlib`,
- cross-backend integration coverage for frontend workflows.

Future ideas below should be evaluated as post-`1.0.0` or optional expansion,
unless explicitly promoted to roadmap.

## Strategic directions worth keeping

1. Quantity interoperability protocol hardening
- Keep defining a stable minimum protocol for quantity behavior
  (value extraction, unit extraction, compatibility, conversion).
- Use this as the basis for backend onboarding and conformance tests.

2. Canonical dimensional model stewardship
- Maintain locked dimensional semantics across backends.
- Formalize drift detection for dimensional representation changes.

3. Conformance-suite maturity
- Expand backend-independent tests from contract checks to stronger
  conformance criteria.
- Keep optional backend support gated by explicit test evidence.

4. Serialization contract
- Evaluate a canonical serialization/deserialization API for quantities
  (`value`, `unit`, `dimensionality`, `form`) for JSON/YAML/data pipelines.
- Treat schema stability as a versioned contract once introduced.

5. Ecosystem integrations beyond current frontend bridges
- Explore pragmatic interop with `SciPy`, selected `scikit-learn` workflows,
  and data-pipeline tooling where unit loss is common.
- Prioritize explicit boundary helpers first, transparent mode second.

6. Performance and ergonomics
- Continue tracking conversion/introspection baselines by release line.
- Evaluate caching/lazy mechanisms only when they preserve determinism and
  diagnostic clarity.

7. Optional advanced domains
- Symbolic physics (`sympy`) for formula-level dimensional reasoning.
- Uncertainty-aware ecosystems (candidate research area).
- Data-model integration patterns (`pydantic`) for API payloads/contracts.

## Prioritization criteria

Promote an idea from this document to active roadmap only if:
- it addresses a real interoperability pain in current users/integrators,
- contract behavior can be tested reproducibly,
- maintenance cost is acceptable for core maintainers,
- it does not destabilize the `1.0.0` compatibility target.

## Non-goals

- Replacing existing unit libraries.
- Building a monolithic abstraction that hides backend semantics completely.
- Adding broad integrations without contract tests and migration guidance.

## Promotion workflow

When an item is promoted:
1. Add it to `devguide/roadmap.md` with explicit target line.
2. Add required checks to the active release checklist.
3. Add test evidence requirements in integration/conformance suites.
4. Keep this document as strategic history and prune promoted details.
