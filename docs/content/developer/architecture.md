# Architecture

PyUnitWizard is organized around four layers:

1. `configure`: runtime backend/parser/standard-units state.
2. `forms`: backend-specific adapters (pint, openmm.unit, unyt, astropy, string).
3. `api`: backend-agnostic public operations (construct, convert, inspect, validate, standardize).
4. `utils`: frontend helpers that preserve quantity semantics (`sequences`,
   `numpy`, `pandas`, `matplotlib`).

## Architectural invariants

- Public API behavior must not depend on hidden global side effects.
- Backend adapters must keep conversions explicit and deterministic.
- Standardization must be reproducible for configured standard units.
- Diagnostics should be catalog-driven through SMonitor integration.
- Transparent frontend helpers (`setup_numpy`, `setup_pandas`,
  `setup_matplotlib`) must stay reversible and test-covered.
