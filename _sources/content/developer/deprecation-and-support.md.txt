# Deprecation and Support

Use explicit deprecation policy for compatibility-sensitive paths.

## Current deprecation focus

- `pyunitwizard.main` compatibility alias remains available in pre-1.0 line.
- Deprecation warnings must be deterministic and tested.

## Rules

- Document deprecations in docs and release notes.
- Keep fallback behavior stable during deprecation windows.
- Avoid silent removals in stabilization branches.
