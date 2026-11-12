---
summary: Bound installed-consumer source snapshots to current nonignored file inputs.
issue: uibcdf/pyunitwizard#153
status: resolved
opened: 2026-11-12
closed: 2026-11-12
severity: low
verification: reproduced
area: [tests, resources, packaging]
guard: tests/test_source_fixture_snapshot.py::test_nested_installed_source_snapshot_preserves_current_nonignored_inputs
normative:
blocked_by: []
supersedes: []
---

# Installed fixture source inputs

The release 0.29.5 full run placed its owned basetemp under ignored
`.governance-tools`. The installed-consumer fixture recursively copied the
checkout into a descendant of that directory, including its own destination.
The run was interrupted after 386.98 seconds with 1,148 passes and three
executed skips: this is incomplete evidence, not a passing suite.

Use Git's finite tracked/current nonignored file inventory to snapshot source
bytes, preserving current working-tree edits and new nonignored inputs while
excluding tooling, caches, Git administration and ignored private material.
The behavioral guard uses a nested destination, changed tracked bytes and new
source, and stops before building an environment. It rejects recursive tree
traversal and verifies the resulting snapshot. No scientific runtime changes.

## Resolution and guard

The source fixture obtains one finite Git inventory of tracked and current
nonignored files and copies their working-tree bytes. It does not recursively
traverse output or copy ignored tooling/private input. The bounded regression
first rejects the old tree traversal, then verifies modified tracked source,
a new nonignored module and absence of Git administration, ignored private
material and the nested temporary tree. The full installed-consumer smoke
subsequently completes as part of the 1,165-pass local suite. No test is waived
and no scientific runtime behavior is changed.

## Public source delivery — 2026-11-12

Delivered in stable source 0.29.5 at `1783fab011a99567f26e988479ee7dd74c494c6f`.
The runtime correction is in the qualified public Conda archive; the source
fixture correction remains test-only. All 29 source jobs and 30 installed
cells pass, with every new cold-admission case executed. Clean public
receiving passes 141 selected tests and actual SDK origin controls. See the
[release record](../completed_proposals/release_0.29.5.md) for exact file/digest,
qualified limits and MolSysSuite/OpenCASTp receiving ownership.
