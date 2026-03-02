# Developer guide

This directory contains operational guidance for maintaining and releasing PyUnitWizard.

## Documents

- `smonitor.md`: diagnostics and instrumentation rules.
- `roadmap.md`: staged path from `0.17.x` to stable `1.0.0`.
- `release_1.0.0_checklist.md`: release gates and go/no-go checklist.

## Current baseline

- Active stabilization line: `0.17.x`.
- Stable target: `1.0.0`.
- Supported Python versions: `3.11`, `3.12`, and `3.13` (daily operation in `3.13`).

## Coordination scope

PyUnitWizard must stay aligned with:

- `argdigest`: argument normalization and API contract integration.
- `depdigest`: optional dependency governance and runtime loading.
- `smonitor`: diagnostics catalog, severity semantics, and traceability.
