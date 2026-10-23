---
summary: Scope the parse-to-string test's Pint policy instead of inheriting ambient state.
issue: uibcdf/pyunitwizard#129
status: resolved
opened: 2026-10-23
closed: 2026-10-23
severity: low
verification: reproduced
area: [tests, parsing]
guard: tests/test_parse.py::test_parse_to_string
normative:
blocked_by: []
supersedes: []
---

# Parse-to-string test policy isolation

What — Candidate `376fbfe43f4775ff9862b507c98e41f75ca88227` failed its full
matrix on macOS/Python 3.13, run 40009069466, job 120604443323. The test assumed
an earlier test had configured a parser; running the existing selector alone
also failed locally with `LibraryWithoutParserError` for `string`.

How — Use the existing `loaded_libraries(["pint"])` test helper to declare
the intended parser/backend policy. Scalar and array assertions are unchanged.
The selected test now passes alone and in its module. Production parser
selection, absence behavior and session defaults are unchanged.

Why — Test execution order must not supply hidden configuration. An inert
string destination does not itself choose a computing parser. The guard is the
original selector, now independently executable; no retry or weaker assertion
is substituted for the failing case.

Release #128 must qualify the corrected source candidate and its exact artifact;
the failed original matrix is retained as history, not relabelled successful.
