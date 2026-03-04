# API Freeze Decision (Pre-1.0)

This document records the pre-`1.0.0` API decision for the active `0.21.x` RC
window.

## Decision

No planned breaking API change remains before `1.0.0`.

## Scope covered by freeze

The freeze applies to public behavior in:
- construction (`quantity`, `unit`),
- conversion/extraction (`convert`, `get_value`, `get_unit`),
- compatibility/validation (`are_compatible`, `check`, `get_dimensionality`),
- configuration entrypoints (`configure.*` public methods),
- transparent frontend helpers (`utils.numpy`, `utils.pandas`, `utils.matplotlib`).

## Rationale

1. Contract coverage is already in place for the most critical behavior.
2. RC objective is consolidation and stability, not surface expansion.
3. Integrator migration risk is lower when behavior is frozen during the RC
   window.

## Known exception

`pyunitwizard.main` remains a compatibility alias with deprecation semantics.
This is not a planned breaking change in `0.21.x`; removal, if ever needed,
must occur after `1.0.0` with explicit migration notes.

## Evidence anchors

- Public API layout and deprecation contract:
  - `tests/test_api_layout.py`
- Minimum quantity protocol contract:
  - `tests/test_minimum_quantity_protocol_contract.py`
- Transparent frontend contract:
  - `tests/test_frontend_transparent_mode_contract.py`
- Conversion regression hardening:
  - `tests/test_conversion_branches.py`

## Change-control policy until `1.0.0`

Allowed:
- bug fixes,
- diagnostics clarity improvements,
- tests and docs hardening.

Not allowed:
- breaking rename/removal of public API,
- silent semantic changes in existing public behavior,
- new broad public surfaces without explicit RC checklist update.
