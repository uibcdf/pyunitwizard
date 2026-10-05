---
summary: Qualify and publish the 0.28.1 declaration-plan optimization.
issue: uibcdf/pyunitwizard#112
status: active
opened: 2026-10-05
closed:
verification: inspected
area: [release, distribution, attribution]
guard:
normative: devtools/conda-build/release_plan.toml
blocked_by: []
supersedes: []
---

# PyUnitWizard 0.28.1 publication

## What

Diego Prada authorized publication of 0.28.1 on 2026-10-05 before a development
pause. Include the completed declaration-plan optimization (#111), preserving
numerical behavior, public dependency floors and provisional interface status.
The completed 0.28.0 publication remains immutable historical evidence.

## How

Commit the staged build-0 decision and notes before freezing the candidate.
Execute all five exact-source mandatory workflows, inspect their native jobs
and scientific steps, then build one noarch Conda archive from that source.
Verify producer receipts, archive resources, source agreement and digest.

Qualify the original installed file outside the checkout in Linux and macOS
arm64 cells: baseline and CF/HDF5 on Python 3.11–3.14, OpenFF on Python
3.12–3.14, and prepared attribution on Python 3.11–3.14. Baseline retains public
Ackredit 0.9.0; the additional profile uses normally installed public Ackredit
0.10.1 and explicitly requires its prepared-credit and observer APIs. Execute
the #111 unit and real-provider guards, including invalidation, independent
captures, registry conflicts and offline saved-reference reading. Retain every
Conda/pip closure and independently verify native steps and source/file binding.

Record the exact candidate, file, runs and scope in an owning-issue pre-tag
receipt. Only then tag 0.28.1 and publish its stable GitHub Release. Promote
the unchanged staging bytes, verify public main label and solver index with
the pinned shared verifier, and exercise a fresh public-channel installation.
Archive this record and close #112 only after those observations succeed.

## Why and limits

The new installed prepared profile is a pre-public requirement, so staging is
appropriate even for a patch release. Ackredit 0.10.1 is an optional qualification
provider, not a new dependency minimum. Benchmark evidence from #111 retains its
original controlled provider identity and does not claim universal speedups or
qualify this new artifact. All record/storage and attribution provisional limits
remain. No PyPI publication, 1.0 admission, Windows support or MolSysMT adoption
is included. Required executed science and actual external ingestion cannot be
replaced by administrative checks or skipped APIs.

## Acceptance and recovery

- Exact-source mandatory gates and every declared installed profile execute.
- The stable tag, metadata and imported package agree on 0.28.1.
- Original producer, bytes and digest survive staging-to-main promotion.
- Independent public metadata/index checks and fresh installed guards pass.
- Receipts, release notes, archive indexes and GitHub state agree.

Failed source gates require a corrected candidate. A defective archive requires
an additive build number, never an overwritten coordinate. A verifier/index
failure is recovered at the read-only observation boundary without rebuilding,
moving tags or repeating promotion.
