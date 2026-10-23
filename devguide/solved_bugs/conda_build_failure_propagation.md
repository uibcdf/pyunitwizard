---
summary: Stop Conda build installation after a failed prerequisite.
issue: uibcdf/pyunitwizard#117
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: medium
verification: reproduced
area: [build, distribution]
guard: tests/test_conda_build_failures.py
normative:
blocked_by: []
supersedes: []
---

# Conda build failure propagation

What — The actual build shell continued after freezer/installer failure and its
final echo returned success. Two real-script regressions fail against
`a2d7e38f6d8dc8f4072cc19b09a8cacddf77899a`; the successful path already passes.

How — Enable Bash fail-fast handling and quote the selected interpreter. The
guard runs the copied actual script and real version freezer against private
source, with a controlled installer that never installs anything. A rejected
version prevents reaching that installer; an installer exit of 19 is preserved;
successful version identity, final success output and caller receipts survive.

Why — A failed prerequisite cannot authorize prefix mutation or a false success
result. The three cases pass after the fix. This does not prove a historical
public artifact was defective or test an external Conda wrapper's behavior.

Parent review: #116 and `devguide/resource_lifecycle_review.md`. No package
bytes, dependency floor, recipe coordinate or publication claim changes.
