---
summary: Adopt the shared issue-backed developer-guide lifecycle.
issue: uibcdf/pyunitwizard#72
status: resolved
opened: 2026-09-07
closed: 2026-09-07
verification: reproduced
area: [governance, tooling]
guard: tests/test_reporting_protocol.py
normative: devguide/reporting_protocol.md
blocked_by: []
supersedes: []
---

# Adopt the shared issue-backed developer-guide lifecycle

## What

PyUnitWizard had separate pending, completed and declined proposal directories, but no
pending bug queue, stable issue identity, generated archive index or offline lifecycle
guard.

## How

The repository now implements the common statuses and metadata while preserving its
established completed and declined proposal archives. Historical records are explicitly
listed as pre-adoption evidence rather than rewritten. New scripts validate metadata and
generate the pending and combined archive indexes without network access.

The active unit-configuration proposal affected several suite members. Its complete
analysis moved to `uibcdf/molsyssuite#18`, where the shared work is now owned, before the
local pending copy was removed.

## Why

Issues now provide stable public identity and state; developer-guide records retain the
measurements and reasoning. The offline gate prevents these two concepts from silently
drifting at the repository boundary.

## Decision

Accepted and implemented. All future durable bug and proposal records follow
`devguide/reporting_protocol.md`; resolved material is archived rather than deleted.
