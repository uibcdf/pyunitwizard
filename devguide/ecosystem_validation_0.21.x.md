# Ecosystem Validation Evidence (`0.21.x`)

This document captures RC evidence for ecosystem-level validation with sibling
libraries.

## Validation date

- 2026-03-04

## Environment

- Local workspace with sibling repos available:
  - `../argdigest`
  - `../depdigest`
  - `../smonitor`
- Python environment: `molsyssuite@uibcdf_3.13`.

## Executed command

```bash
conda run -n molsyssuite@uibcdf_3.13 \
  pytest -q tests/integration/test_ecosystem_smoke.py \
  tests/integration/test_local_sibling_repos.py
```

Result:
- `6 passed`.

## Coverage by checklist requirement

1. Integration smoke checks with `argdigest`
- Covered by `test_argdigest_pyunitwizard_rule_pipeline_smoke`.
- Covered by `test_argdigest_pyunitwizard_standardize_and_convert_pipeline`.

2. Integration smoke checks with `depdigest`
- Covered by dependency-introspection smoke tests in
  `tests/integration/test_ecosystem_smoke.py`.

3. Integration smoke checks with `smonitor`
- Covered by catalog-code registration smoke in
  `tests/integration/test_ecosystem_smoke.py`.

4. Local sibling smoke validation
- Covered by `tests/integration/test_local_sibling_repos.py` (import precedence
  and basic contract checks against sibling repositories).

5. Cross-repo contract drift check
- No unresolved drift was detected in this validation pass.
