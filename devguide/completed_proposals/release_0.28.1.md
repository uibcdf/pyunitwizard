---
summary: Qualify and publish the 0.28.1 declaration-plan optimization.
issue: uibcdf/pyunitwizard#112
status: resolved
opened: 2026-10-05
closed: 2026-10-05
verification: inspected
area: [release, distribution, attribution]
guard: tests/test_noarch_conda_publication.py::test_installed_prepared_profile_requires_public_provider_and_real_guards
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

## Published outcome — 2026-10-05

Stable GitHub Release and the independently dereferenced remote annotated tag
0.28.1 target source `25a4bc2468da4ef3af2a638c0bf068becf2acfb4`.
Producer 37307676226 built `pyunitwizard-0.28.1-py_0.tar.bz2`, SHA-256
`d4654faf93ed4181bf331f7d382379e78f02784f71f678ad19d0ac43d8062cc6`.
All five required source workflows passed their 29 scientific/policy jobs;
routine CI 37302733837 actually uploaded both Codecov reports. Installed
qualification 37308199459 passed all 30 cells and the producer verifier. Native
step verification, original-source binding, complete closures and JUnit cases
confirm every prepared guard executed without skips on public Ackredit 0.10.1.
The copied installed lane excludes the nested source wheel builder because it
qualifies the original Conda bytes; exact-source suites execute that separate
builder. Existing strict-JSON and unavailable-API classifications remain honest.

Promotion 37309227696 preserved the original digest. The pinned independent
verifier confirms public main label and solver index. Release-event run
37309188484 checks the staged decision without rebuilding, and documentation
publication 37309188386 succeeds. A fresh public-only Linux/Python 3.14 solve
imports the original digest and executes immutable/empty record, measurement,
affine CF, HDF5 roundtrip/refusal and 43 attribution guards. Its freely resolved
SMonitor 0.18.0 / DepDigest 0.13.0 closure is retained separately from the pinned
0.16.0 / 0.11.0 installed matrix; no broader matrix claim for those versions is
implied. Pip reports no broken requirements. No publication exception was needed.

Local source tests on public Ackredit 0.10.1 pass 854 cases with one intentional
strict-JSON case skip and an additional OpenFF module collection skip. The compact
summary counted executed cases; the retained JUnit XML distinguishes the collection
skip. The pre-tag comment's local count omits that collection detail; it does not
replace the six executed exact-source and six installed OpenFF cells above.
An earlier thin environment failed CF native-library collection;
the full scientific base provides the corrected run without relabeling history.
The owning-issue pre-tag decision is
https://github.com/uibcdf/pyunitwizard/issues/112#issuecomment-5994351044.
Full safe receipts are `devguide/evidence/release_0.28.1_2026-10-05.json`; all
30 closures and individual installed case classifications are retained in
`devguide/evidence/release_0.28.1_installed_closures.json`.

The selected guard protects the new public-provider prepared profile, inclusion
of real regression/reader guards and rejection of skipped prepared cases. It
does not replace executed science or independently observed public availability.
All provisional and unsupported-scope limits above remain in force.
