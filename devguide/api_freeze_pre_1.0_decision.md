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

## QuantityRecord scope reconciliation — 2026-10-04

Keep `QuantityRecord`, `QuantityRecordBundle`, `qrec/0.3` and
`qrec-bundle/0.3` provisional in the 1.0 scope. Closing the delivered MVP and
its design record under #82/#83 does not freeze the format or promote the API.
Future stable admission requires an explicit reviewed compatibility decision,
reader/writer contracts, release notes and exact-candidate evidence. Existing
stored bytes and frozen vectors remain unchanged by this reconciliation.

The deferred HDF5 binding (#101), tagged layout (#102), Arrow/Parquet (#103),
Zarr (#104), appended blocks (#105) and translation-hub evaluation (#106) have
independent owners and acceptance criteria. Unit dialects remain #85, OpenFF
remains #86, and live computation remains deferred under #87. New layouts and
bindings must not silently reinterpret the existing format identifier.

## Stated scalar uncertainty exception — 2026-10-04

Admit the bounded experimental `pyunitwizard.measurement.MeasurementRecord`
surface (#90) for Sabueso's stated scalar uncertainty. Its separate
`qrec-measurement/0.1` envelope reuses the existing bundle and canonical seal;
qrec/0.3, bundle/0.3 and the primary quantity APIs are unchanged. Keep it
provisional in 1.0 scope and explicitly name it in release notes. It does not
admit arrays, live arithmetic, error propagation or statistical estimation.
