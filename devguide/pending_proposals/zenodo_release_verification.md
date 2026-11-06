---
summary: Adopt resumable Zenodo verification before the next public release.
issue: uibcdf/pyunitwizard#140
status: active
opened: 2026-11-05
closed:
verification: measured
area: [release, governance, documentation]
guard:
normative: devguide/zenodo_archival.md
blocked_by: []
supersedes: []
---

# Resumable Zenodo release verification

What — The registered required archival mode has an existing verified concept
and delivery route, but the repository lacks bounded publication/manual and
scheduled discovery under MolSysSuite #49. Adopt the common caller before
the 0.29.1 public decision, while preserving its qualified Conda source/file.

How — Pin the shared read-only verifier at
`20628bd5dba6d759669b0d444fe657eb1edad33f`, retain the stable concept DOI,
use published release/manual exact tags and six-hour scans from a fixed cutoff,
and record semantic states rather than inferring archival from green jobs.
The first current-candidate probe is explicitly manual on main after publication;
future tags containing the caller also have the release event. Register the
tooling-only route and protect immutable delegation, read-only permissions,
exact-tag routing and non-rolling discovery with regression-first tests.

Why — A missing record during ingestion is not failure or success. The original
72-hour clock, complete bounded discovery and owner follow-up must survive
later releases, reruns and expired artifacts. This is operational verification,
not a scientific/runtime change or authority to replay hooks/create deposits.

Measured baseline — The pinned provider's public exact-tag 0.29.0 probe reports
verified source snapshot record 23604831/version DOI 10.5281/zenodo.23604831;
one 2,615,648-byte ZIP has checksum md5:c2763f48efabc952875fa4e0152ec0b6.
One active release hook is observed through an in-memory presence/activity
projection only. Citation files are absent; the existing integration metadata
is retained and no new author/ORCID/license choice is made. No 0.29.1 record
exists by implication. The current artifact/installed qualification retains
source ab92f1e and the original producer/digest under #138.

Acceptance — Contract tests first fail without the caller, then pass; dependency,
reporting/receptor and applicable lint checks pass; a hosted exact-tag probe of
the already published 0.29.0 validates actual delegation and returns verified
public evidence. Retain its source/run/attempt and semantic result before
archiving this adoption record. Each future release owns its own observed
archival state and actual file coverage separately.

Local controls — The missing caller first fails two guards; after delegation
is added, both pass and the selected reporting/dependency/receptor controls
pass 21 cases without skips. The main-branch inventory now verifies 23 routes,
including this tooling-only caller; the original Conda candidate's 22-route
receipt remains bound to ab92f1e. Ruff lint/format and the ten-rule receptor
configuration pass. Sanitized evidence is retained in
`devguide/evidence/zenodo_adoption_local_2026-11-05.json` and the separate
public 0.29.0 probe; no hook configuration is retained. A hosted exact-tag
positive control remains due before resolving this operational adoption.
