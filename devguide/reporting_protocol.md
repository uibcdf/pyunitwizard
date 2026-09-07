# Reporting protocol

This document maps the common lifecycle accepted in `uibcdf/molsyssuite#11` to
PyUnitWizard. The central policy owns the shared meanings; this repository owns local
implementation issues, records, paths and validation.

## Ownership and identity

PyUnitWizard-specific bugs and proposals use `uibcdf/pyunitwizard#<number>`. Shared
policies, compatibility contracts and coordinated changes use `uibcdf/molsyssuite`.
Cross-repository references use `owner/repository#<number>`, never paths into sibling
developer guides.

Every queued document has an owning issue. Not every incoming issue needs a document:
create one after triage when the theme requires durable analysis. One independently
closable theme has one issue and may have more than one evidence document.

## Local paths

- `pending_bugs/`: open defects;
- `pending_proposals/`: open proposals;
- `solved_bugs/`: resolved, withdrawn or superseded defects;
- `completed_proposals/`: accepted and implemented proposals;
- `declined_proposals/`: withdrawn or superseded proposals;
- `archive/README.md`: generated combined index of every managed and legacy archive.

The five historical proposal records listed by
`devtools/devguide_reports.py::LEGACY_ARCHIVE` predate this protocol. They remain
immutable evidence without retrofitted issue metadata. No current or future report is
exempt.

## Required metadata

Every queued or managed archived report begins with YAML front matter containing:

```yaml
---
summary: One-line description.
issue: uibcdf/pyunitwizard#1
status: open
opened: 2026-09-07
closed:
severity: medium
verification: asserted
area: [core]
guard:
normative:
blocked_by: []
supersedes: []
---
```

`severity` is required only for bugs and is `critical`, `high`, `medium` or `low`.
Verification is `reproduced`, `measured`, `inspected`, `upstream` or `asserted`.
Statuses in the open set are `open`, `active`, `blocked` and `partial`; closed statuses
are `resolved`, `withdrawn` and `superseded`. A blocked report names its dependency in
`blocked_by`. A resolved report names a durable test in `guard` or an adopted rule in
`normative`.

## Filing

1. Decide ownership using the suite repository contract and open the owning issue first.
2. Copy `templates/report.md` into the appropriate pending queue.
3. Record expanded What / How / Why analysis, alternatives and acceptance criteria.
4. Run `python devtools/devguide_index.py` and commit the issue/document references
   together.

The issue body stays telegraphic: `What`, `How`, `Why`, and `Record`. Analysis changes in
the document; the issue is updated at triage and closure. An issue awaiting triage may
have no document, but a queued document may never have no issue.

## Closing

Set the closed status and date, name the guard or normative rule, move the record to its
mapped archive, regenerate indexes, and close the issue with the outcome, user-visible
consequence, guard and final record path. GitHub state and report state must agree.

Archive, never delete. Correct an open report in place. Append a dated correction to an
archived report instead of rewriting its historical claim.

## Offline checks

```bash
python devtools/devguide_index.py
python devtools/devguide_index.py --check
python -m pytest -q tests/test_reporting_protocol.py
```

These checks require no credentials or network access. GitHub synchronization is a
separate authenticated operation at filing and closure.
