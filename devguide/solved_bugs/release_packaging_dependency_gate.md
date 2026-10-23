---
summary: Execute the packaging job's declared dependency gate before building artifacts.
issue: uibcdf/pyunitwizard#130
status: resolved
opened: 2026-10-23
closed: 2026-10-23
severity: medium
verification: reproduced
area: [ci, release, dependencies]
guard: tests/test_dependency_routes.py::test_source_workflows_execute_default_qualification_before_tests_or_builds
normative: devtools/conda-build/README.md
blocked_by: []
supersedes: []
---

# Packaging dependency gate delivery

What — The release plan declared `Check dependency contract` for
`Packaging Smoke (Python 3.13)`, but that job omitted the step. Release-gates
run 40010914448 at `941546008b60da57ab61e56958560bda55a6c0c3` appeared green;
independent native verification correctly rejected packaging job 120610759926.
All other declared source job/step requirements were inspected and present.

How — Add the existing dependency-check operation before `Build artifacts` in
the owning packaging job, retain the plan requirement, and review/update the
workflow's dependency-route hash. Strengthen the existing guard to inspect each
runtime job independently; a check elsewhere in the workflow cannot satisfy it.
The strengthened guard failed on the original workflow before the correction.

Why — Declared gates must actually execute in their required scope. Removing a
requirement or treating a check in another job as packaging evidence would weaken
publication. No staging artifact or public release existed when this was found.

The library code and scientific inputs remain unchanged. Release #128 qualifies
the corrected source head through all mandatory native workflows before any
build/upload. Older green workflow conclusions retain their original scope;
they are not relabelled as complete source qualification.
