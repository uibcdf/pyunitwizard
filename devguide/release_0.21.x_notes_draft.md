# Release 0.21.x RC Notes (Draft)

This draft captures the candidate release notes for the `0.21.x` RC window
before `1.0.0`.

Checkpoint note:
- RC close checklist completed and stabilization-window tag `0.21.0` created.
- RC maintenance patch tag `0.21.1` created for post-close hardening.

## Scope

`0.21.x` is a stabilization and consolidation line. The objective is to freeze
behavior introduced through `0.20.x` and remove ambiguity in contracts.

The line focuses on:
- contract hardening (minimum quantity protocol and transparent frontend mode),
- regression coverage in parser/conversion/configuration behavior,
- cross-repo ecosystem validation with `argdigest`, `depdigest`, and `smonitor`,
- documentation synchronization for pre-`1.0.0` go/no-go.

## Compatibility statement

- Supported Python versions: `3.11`, `3.12`, `3.13`.
- Operational baseline during RC work: Python `3.13`.
- Runtime backends:
  - hard dependency: `pint`,
  - optional/soft backends: `openmm.unit`, `unyt`, `astropy.units`,
    `physipy`, `quantities`.
- Transparent integrations remain additive and backward compatible:
  - NumPy,
  - Pandas,
  - Matplotlib.

## Key hardening items in current RC cycle

1. Minimum protocol evidence is now test-backed:
- `tests/test_minimum_quantity_protocol_contract.py`

2. Transparent frontend contract remains test-backed:
- `tests/test_frontend_transparent_mode_contract.py`

3. Conversion/parser robustness regression covered:
- unit-only `to_unit` strings (for example `"meter"`, `"centimeter"`) are
  handled robustly across parsers, including parser paths that require
  quantity-like strings internally.
- evidence: `tests/test_conversion_branches.py`

4. Quantities backend unit-conversion bugfix:
- fixed recursion when `forms/api_quantities.py::convert` receives unit-like
  inputs.
- regression covered in `tests/forms/test_api_physipy_and_quantities.py`.

5. Coverage/CI alignment for optional backends:
- `.coveragerc` cleaned from stale omit entry.
- CI test environment now installs `physipy` and `quantities`, reducing
  local-vs-Codecov drift.

## Migration notes for integrators

No breaking API changes are planned within `0.21.x`.

Recommended actions for library maintainers:
1. Keep explicit parser/form configuration in integration entrypoints.
2. Prefer contract tests around `convert`, `get_value`, `get_unit`, `check`.
3. Validate optional backend paths in environments where those backends are
   expected to be available.
4. Treat `pyunitwizard.main` as deprecated and import from `pyunitwizard`.

## Known risks and watchpoints during RC

1. Optional backend behavior depends on installed extras and upstream
   implementations.
2. Cross-repo drift risk exists if sibling libraries evolve diagnostics or
   dependency contracts without synchronized updates.
3. Release-gate continuity must be monitored in CI matrix runs
   (`ubuntu`/`macos`, Python `3.11`/`3.12`/`3.13`).

## Non-goals for `0.21.x`

- Promoting serialization draft to stable public contract.
- Introducing new broad integration surfaces that increase API/behavioral risk.

## Promotion gate to `1.0.0`

`0.21.x` can close when:
- RC checklist items are complete (`devguide/release_0.21.x_rc_checklist.md`),
- `release_1.0.0_checklist.md` is actionable and current,
- no blocker/high-severity incidents remain open in core paths.
