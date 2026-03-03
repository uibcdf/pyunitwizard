# Implementation Patterns

Use these patterns to keep changes stable.

## 1. Boundary normalization

Normalize inputs at public API boundaries, not deep in business logic.

## 2. Explicit checks

Use explicit compatibility and dimensionality checks before conversion-sensitive operations.

## 3. Stable defaults

Configure parser/form/standards once and avoid ad-hoc runtime reconfiguration.

## 4. Backend isolation

Keep backend-specific behavior inside `forms/*` adapters; avoid leaking it into `api/*`.

## 5. Contract tests first

For regressions or new branches, add/adjust tests before implementation changes.
