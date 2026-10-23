---
summary: Report failed notebook execution through the docs CLI exit status.
issue: uibcdf/pyunitwizard#118
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: medium
verification: reproduced
area: [docs, development]
guard: tests/test_notebook_cli.py
normative:
blocked_by: []
supersedes: []
---

# Notebook CLI failure status

What — The actual CLI returned zero after a controlled Jupyter child exited 7,
although it wrote the failure log and invalidated its timestamp correctly.
Two regressions fail before implementation, while the successful path passes.

How — Return the batch result after processing every requested notebook and use
it as the CLI status. A supplied missing path also reports failure. Six
controlled-child cases cover success/failure/mixed batches selected as explicit
files and a directory. They preserve caller notebook bytes and receipts, retain
diagnostics and permit success timestamps only for successful notebooks.

Why — Automation must observe failure without losing useful logs or silently
skipping the remainder. The guard invokes the actual CLI with an owned fake
Jupyter executable; it executes no scientific notebook. These cases pass after
the fix, with the original logging/timestamp policy preserved.

Parent review: #116 and `devguide/resource_lifecycle_review.md`. No product API,
notebook result or published documentation site is qualified by this control
flow test. Primary notebooks and generated output remain untouched.
