# Collective Evidence Pack

This file is the PyUnitWizard-side collective evidence record for cross-repo
validation with:
- `../smonitor`
- `../depdigest`
- `../argdigest`

## Scope

This pack reports:
- reproducible local evidence available in this repository,
- cross-repo references relevant for RC closure,
- what remains a release-owner coordination action.

## Checkpoint metadata

- Date: `2026-03-04`
- Active RC line: `0.21.x`
- Latest stabilization-window tag: `0.21.0`
- Latest RC maintenance tag: `0.21.1`
- Head reference for this pack: `7816587`

## Local quality baseline

- Full suite baseline:
  - `pytest --import-mode=importlib -q --cov=pyunitwizard --cov-config=.coveragerc --cov-report=term-missing` -> `391 passed`, `94%` coverage
- Docs build baseline:
  - `make -C docs html` -> success

## Contract evidence index

- API/deprecation layout contract:
  - `tests/test_api_layout.py`
- Minimum protocol contract:
  - `tests/test_minimum_quantity_protocol_contract.py`
- Transparent frontend contract:
  - `tests/test_frontend_transparent_mode_contract.py`
- Conversion regression hardening:
  - `tests/test_conversion_branches.py`
- SMonitor catalog and profile contracts:
  - `tests/test_smonitor_catalog_contract.py`
  - `tests/test_smonitor_profiles_contract.py`
- DepDigest contract:
  - `tests/test_depdigest_contract.py`
- Cross-library smoke and sibling precedence:
  - `tests/integration/test_ecosystem_smoke.py`
  - `tests/integration/test_local_sibling_repos.py`

## RC stability and ecosystem references

- Stability ledger:
  - `devguide/stability_monitoring_0.21.x.md`
- Ecosystem validation ledger:
  - `devguide/ecosystem_validation_0.21.x.md`
- RC close readiness:
  - `devguide/rc_close_readiness_0.21.x.md`

## Current collective status from PyUnitWizard perspective

- integration smoke with `argdigest`: done
- integration smoke with `depdigest`: done
- integration smoke with `smonitor`: done
- local sibling smoke: done
- unresolved cross-repo drift in current RC pass: not detected

## Remaining non-local closure step

Release-owner explicit approval to close RC (`devguide/release_0.21.x_rc_checklist.md`).
