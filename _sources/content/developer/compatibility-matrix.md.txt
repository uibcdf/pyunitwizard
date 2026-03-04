# Compatibility Matrix

PyUnitWizard coordinates with sibling infrastructure libraries. This page
defines the minimum versions expected during the current RC stabilization path.

| Component | Minimum Version | Role |
|---|---:|---|
| `argdigest` | `0.9.0` | quantity-aware contract pipelines and caller-context error mapping |
| `depdigest` | `0.9.1` | runtime dependency introspection and optional backend governance |
| `smonitor` | `0.11.4` | diagnostics, signaling, catalog-backed codes and hints |

## Operational rules

When this matrix changes:

1. Update `devguide/compatibility_matrix.md`.
2. Update release notes and RC checklist evidence.
3. Re-run ecosystem smoke checks and local sibling checks.

This matrix is a compatibility floor. It does not imply pinning these exact
versions in downstream environments.
