---
summary: Qualify and publish 0.29.0 as the next additive interoperability checkpoint.
issue: uibcdf/pyunitwizard#128
status: active
opened: 2026-10-23
closed:
verification: inspected
area: [release, packaging, documentation]
guard:
normative: devtools/conda-build/README.md
blocked_by: []
supersedes: []
---

# Release 0.29.0

What — Publish 0.29.0 with the delivered record extensions (#102/#103/#104/#105)
and completed bounded interoperability inventory #85 (#125/#126/#127).
This supersedes the uncreated 0.28.2 plan. Public version remains 0.28.1 until
the actual publication route succeeds.

How — Preserve provisional status and existing qrec bytes. Execute all required
exact-source gates, stage one immutable Conda file, verify that same digest in
all baseline/storage/OpenFF/prepared installed cells, then publish the canonical
0.29.0 tag and GitHub Release (title exactly `0.29.0`). Promote unchanged bytes,
verify public index/installation and served documentation. Retain receipts for
source, producer, installed file and public poststate; source tests do not waive
installed gates. Notify MolSysSuite in a version-specific issue at each actual
release/package event, stating explicitly what remains pending.

Why — Additive tagged/append/storage and dialect APIs merit a minor release and
a qualified public checkpoint before further development. User authorization
includes direct upstream pushes and publication during this session.

## Required scope

- Baseline Linux/macOS Python 3.11–3.14; actual optional storage/dialect
  providers in source and outside-checkout installed tests without scope skips.
- Actual OpenFF 0.4.0/Pint 0.24–0.25 Python 3.12–3.14; prepared attribution
  and public Ackredit fallback remain separate installed profiles.
- Packaged vocabulary JSON/license resources and real consumer fixtures.
- Clean lint/format, reporting/dependency-policy checks, Sphinx docs and actual
  applicable coverage uploads.
- Guide synchronization belongs to MolSysSuite; source provider delivery does
  not claim adoption in client repositories.

Publication evidence, package digest, release URL and notice issue remain pending.
