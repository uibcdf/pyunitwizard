# Sibling Compatibility Matrix

This matrix records the sibling-library floors for the 0.26.0 Python 3.14
release path. Earlier release lines retain their own historical contracts.

| Component | Minimum Version | Role in the 0.26.0 path |
|---|---:|---|
| `argdigest` | `0.13.0` | validated sibling for quantity-aware contract pipelines; not a PyUnitWizard runtime dependency |
| `depdigest` | `0.11.0` | required runtime dependency for optional backend governance |
| `smonitor` | `0.16.0` | required runtime dependency for diagnostics and catalog-backed signals |

## Policy

- The matrix defines 0.26.0 compatibility floors, not preferred pins.
- PyUnitWizard's declared runtime requirements are SMonitor and DepDigest;
  ArgDigest is a validated sibling rather than an installed requirement.
- Any matrix change must be reflected in:
  - this file,
  - release notes for the affected tag,
  - RC checklist evidence for integration smoke checks.
- Before `1.0.0`, matrix floors must be validated in clean environments and in
  local sibling workflows (`../argdigest`, `../depdigest`, `../smonitor`).
