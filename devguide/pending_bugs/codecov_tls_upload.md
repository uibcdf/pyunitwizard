---
summary: CI coverage uploads fail at Codecov download and ingestion endpoints.
issue: uibcdf/pyunitwizard#107
status: active
opened: 2026-10-04
closed:
severity: medium
verification: reproduced
area: [ci, coverage]
guard:
normative: .github/workflows/CI.yaml
blocked_by: []
supersedes: []
---

# Codecov TLS upload

What — CI run 37268781842, attempts 1 and 2 at cda2108, passes scientific
tests and fails `Upload coverage reports to Codecov` with EPROTO / TLS alert 40
before the old Node downloader obtains the CLI. The exact-source full matrix,
release gates and policy are green; the aggregate CI result is failure.

How — Replace Codecov action v4 with the official current release v7.1.1.
This uses the maintained wrapper and updated PGP-key retrieval. Use supported
`files` instead of deprecated `file`, explicitly select coverage.xml/junit.xml
and fail on upload errors for truthful evidence. Keep validation and credentials
unchanged. Do not bypass TLS or declare upload success from a test-only step.

Why — Repeating the same external failure does not establish a successful
checkpoint. The maintained uploader removes the failing older integration
path; execution must confirm actual successful uploads before closure.

Source — [official action migration and release](https://github.com/codecov/codecov-action).
Offline YAML parsing and existing workflow/reporting checks precede push;
the executed exact-head coverage and test-result steps provide the regression
evidence. No mirror test of the chosen action version substitutes for execution.

## Follow-up diagnosis — 2026-10-05

Current action v7.1.1 still encounters TLS alert 40 downloading the CLI from
cli.codecov.io (run 37269791533). The missing signature is consequential to
that failed download, not a reason to disable validation. Use the official
PyPI Codecov CLI 11.3.1 in an isolated venv and the documented action `binary`
input, retaining normal package installation and upload error handling. This
uses the provider's supported alternate distribution; no insecure TLS or
unchecked CDN binary is accepted. Executed upload results remain required.

The official installed CLI successfully passes download/setup, but run
37270848222 then fails requests to ingest.codecov.io after retries. Thus the
external outage also affects ingestion, beyond the old downloader. Tests and
style pass; no successful coverage upload or aggregate green CI is claimed.
Keep #107 active until the service recovers and exact-head coverage/test-result
uploads execute successfully. Do not keep changing unrelated scientific code
or suppress upload errors to manufacture a green result.

## Interoperability checkpoint — 2026-10-05

At `778964021d07169f7327c674cadfbc4c2b6a23ac`, routine CI 37272521807
passes 753 tests with 14 skips and style checks, then fails coverage ingestion
after retries. OpenFF six-cell matrix 37272537988 passes full suites and
installed outside-checkout guards; the original runtime source's eight-cell
baseline matrix and release gates also pass. Those scientific results neither
clear this upload debt nor qualify public publication. Coverage and test-result
uploads must execute successfully on the exact recovery candidate before #107
can close. Keep the existing service-recovery route and fail-on-upload handling.
