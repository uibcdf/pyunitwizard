# Sibling Compatibility Matrix

This matrix defines the minimum sibling-library versions validated for the
PyUnitWizard `0.19.x` release-candidate window.

| Component | Minimum Version | Role |
|---|---:|---|
| `argdigest` | `0.9.0` | quantity-aware contract pipelines and caller-context error mapping |
| `depdigest` | `0.9.1` | runtime dependency introspection and optional backend governance |
| `smonitor` | `0.11.4` | diagnostics, signaling, catalog-backed codes and hints |

## Policy

- The matrix defines compatibility floors, not preferred pins.
- Any matrix change must be reflected in:
  - this file,
  - release notes for the affected tag,
  - RC checklist evidence for integration smoke checks.
- Before `1.0.0`, matrix floors must be validated in clean environments and in
  local sibling workflows (`../argdigest`, `../depdigest`, `../smonitor`).
