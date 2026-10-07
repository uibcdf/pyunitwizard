---
summary: Remove parent-owned synthetic client packages after concurrent child success, failure and timeout.
issue: uibcdf/pyunitwizard#115
status: resolved
opened: 2026-10-07
closed: 2026-10-07
severity: medium
verification: reproduced
area: [testing, development]
guard: tests/test_concurrent_registry_resources.py
normative:
blocked_by: []
supersedes: []
---

# Concurrent client fixture ownership

## What

The cold-interpreter RACE harness created an unmanaged mkdtemp directory with
two synthetic clients, source files and bytecode. Both normal and failing exits
left that directory behind. Eight repetitions multiplied the retained fixtures.
The initial shared screen used e128e3e2a96e3676d08838158c8d3fd784fcde83;
the same defect remains at fetched repair baseline
2ab37a525ce99728ad8aee846b4a4f7acc4f1b65. Coordination: uibcdf/molsyssuite#104.

## How

The existing test parent owns a TemporaryDirectory and passes its path as the
child interpreter's sole argument. RACE still creates both clients, inserts
their root into sys.path, starts both import threads behind the same barrier,
joins both and reports the original error. Only root acquisition changes.
The context spans subprocess.run and its existing result assertion; it cleans
on success, child failure, start failure and TimeoutExpired. subprocess.run
terminates and reaps the timed-out child before the context removes its files.
Removal errors propagate with an earlier child assertion in exception context.
The existing 300-second timeout, capture settings and eight attempts remain.

## Why

The parent must retain ownership through child completion or termination.
A child-only context cannot guarantee cleanup when the parent kills that child.
Standard managed storage supplies the needed lifecycle without a new shared
cleaner, registry behavior or thread synchronization mechanism.

## What is measured and what is assumed

Six lifecycle regressions fail against the repair baseline and pass after the
fix in molsyssuite@uibcdf_3.14, Python 3.14.7. They invoke the actual existing
test and actual RACE source, using synthetic configuration callbacks in real
cold child processes. They exercise success, reported configuration failure,
a real timeout with the child reaped, two visible removal errors (including
preserved child-failure context), and inability to start the subprocess.
Client sources must exist while the two threads configure; caller-owned
receipts and parent workspace survive fixture cleanup. Deliberately failed
removals stay confined to this task's pytest fixture tree.

All eight original race repetitions also pass with real PyUnitWizard; nine
reporting checks pass (23 selected tests total). Whole-repository Ruff and
generated-index checks pass. The qualified environment and primary editable
receptor origins are unchanged; seven existing dependency conflicts remain
tracked in uibcdf/molsyssuite#82. Exact-head hosted push evidence is recorded
in the closing owner issue and central rollout receipt after execution.

## What was refuted

Success-only unlinking misses failed assertions and timeouts. Child-owned
cleanup is insufficient for termination. A blanket temporary-directory cleaner
or copied shared framework is unnecessary. The regression failures concern
fixture lifetime; they do not demonstrate a new registry/configuration defect.

## Scope and exclusions

Only the concurrency test harness and its lifecycle guard/documentation change.
Registry semantics, barriers, eight repetitions, optional OpenFF integration,
installed APIs, guides and release decisions are unchanged. No optional full
matrix, OpenFF/storage interoperability or publication workflow is dispatched.
No primary clone, caller environment or unrelated /tmp resource is modified.
The existing ordinary push CI remains applicable. Full component tool and
retrospective resource reviews remain pending under uibcdf/molsyssuite#104.

## Acceptance criteria

The module guard is addressable and collectively protects six reproduced
failure mechanisms. The actual eight race repetitions remain green. Sources
exist through both import threads; parent cleanup follows child completion or
termination; failures remain visible and caller evidence survives. Record exact
native CI and remove the clean task clone/fixtures after final qualification.

## Fetched-base integration checkpoint — 2026-10-07

The first isolated clone copied primary local main at 2ab37a525ce99728ad8aee846b4a4f7acc4f1b65.
Fetching the real remote exposed three already published governance commits,
ending at e128e3e2a96e3676d08838158c8d3fd784fcde83. The non-fast-forward push
was rejected; no remote rewrite occurred. Integrate the local repair onto that
fetched base and regenerate the generated archive index to preserve both records.
The original concurrency test bytes are identical in both bases (SHA-256
88326f9e20359ac166a72596988030bdd430488606c7e9d6f2ab03eae9731a13),
so its before/after lifecycle and eight race results remain applicable.

The integration rerun passes nine reporting and nine dependency-route tests,
plus whole-repository Ruff. The owner's actual preflight rejects an unpinned
current central checkout, as required; retrying with its unchanged exact provider
20628bd5dba6d759669b0d444fe657eb1edad33f verifies all 22 declared-and-installed
public-bound routes. No weakening of that provider pin or runtime checks.
Final native gates must qualify the resulting integrated head.
