---
summary: Qualify and publish 0.28.0 with the exact staged Conda artifact.
issue: uibcdf/pyunitwizard#110
status: active
opened: 2026-10-05
closed:
verification: inspected
area: [release, distribution, interoperability]
guard:
normative: devtools/conda-build/release_plan.toml
blocked_by: []
supersedes: []
---

# PyUnitWizard 0.28.0 publication

## What

The maintainer authorized preparation and publication of 0.28.0 on 2026-10-05,
after the bounded QuantityRecord, MeasurementRecord, OpenFF and CF/HDF5 route
completed. The latest public version is 0.27.0. Publish the completed provider
capabilities through Conda while retaining their provisional status.

## How

Commit the reviewed staged decision and release notes before freezing the
candidate. Run the full Linux/macOS baseline matrix, release contracts/package/docs,
suite policy, six OpenFF cells and eight CF/HDF5 cells at that exact candidate.
Inspect native jobs and scientific steps as well as aggregate conclusions.

Build one final noarch `pyunitwizard-0.28.0-py_1.tar.bz2` file from the immutable SHA,
using an ephemeral build-local version tag, never an early public tag. Verify
producer receipts and its SHA-256. Test that exact installed archive outside
the checkout in baseline (eight), storage (eight) and OpenFF (six) cells, with
public SMonitor, DepDigest, ArgDigest and Ackredit providers. Each cell checks
installed provenance, version and relevant record/integration contracts. Retain
the resolved dependency closure. Provider optionality does not excuse skipped
scientific tests in the profile that claims that provider.

The existing installed verifier omitted required ArgDigest provenance. A new
negative case supplies a staging-channel ArgDigest with otherwise valid runtime
metadata; it failed before the verifier added the public 0.14.0 coordinate.
The rejection cases now isolate the expected provenance/digest failure instead
of accepting an unrelated distribution-version error.

Before the public tag, attach a reviewable receipt to the owning issue naming
the immutable candidate, all run/step results, artifact identity, complete
tested scope and any missing evidence. Keeping this receipt in the issue avoids
changing the candidate merely to insert its own hash. Then create the canonical
0.28.0 tag and stable GitHub Release, promote the exact staging digest, verify
the public registry and solver index independently, and run a clean public-channel
installation. Archive this record only after public availability is proven.

## Why and limits

Source-qualified development receipts retain their historical producer identities
and do not qualify a different public artifact. Staging is selected because new
optional interfaces, a new measurement envelope and a changed ArgDigest floor
require pre-public installed evidence. The unchanged package remains noarch Python;
its native third-party providers are separately resolved by Conda.

Only the Conda route is claimed. No PyPI publication, stable 1.0 promotion,
Windows/Intel macOS support, UCUM/ASDF/QUDT, append/streaming, large-file performance
or MolSysMT source adoption is included. The known Ackredit observer deferrals
remain visible in test skips; real-provider attribution guards execute.

Codecov #107 stays open unless actual coverage and test-result ingestion recovers.
Keep fail-on-upload handling and its real failed result. If external ingestion
still fails, any permitted publication exception must be an explicit dated
decision for this candidate, version and artifact, naming the owner, compensating
evidence, public limitation and expiry; it cannot waive scientific or installed
gates. Publication authority and execution evidence are separate facts.

The central release/distribution/publication contracts were read at MolSysSuite
`04480983260804113022bc20c214875a5eb5611e`. The unchanged local producer/promotion
route is retained; changed installed qualification expands its scientific scope.
Use the shared pinned independent public verifier for the final poststate.

## Pre-publication correction — 2026-10-05

Initial candidate `8fbcaa8703069c2c91cef45c9a6871238b1c214e` passed source matrices
37280526908 (baseline), 37280534128 (OpenFF), 37280537579 (storage), release gates
37280530465 and policy 37280479219. Its routine CI 37280478449 failed only Codecov
coverage ingestion. Staging producer 37282788783 successfully uploaded build
`py_0`. Preserve that file and original producer evidence; it is not the final
publication candidate and must not be overwritten or promoted.

The central administrative publisher audit then identified missing pinned
independent public verification and failure-path receipt retention in the
promotion workflow. The corrected workflow calls the shared verifier at
MolSysSuite `04480983260804113022bc20c214875a5eb5611e` and retains its evidence and
the promotion receipt with `always()`. The audit passes after this correction.
An early dependency-contract review also adds explicit NumPy and preserves the
SMonitor >=0.16.0 / DepDigest >=0.11.0 floors in seven runtime environments.
Build/setup environments are classified as tools-only; the Conda recipe's run
closure already agrees with project metadata. Negative preflight observations
reject a missing recipe dependency, a stale environment floor and an ArgDigest
source identity below the public floor. No required sibling source install is
claimed.

The corrected candidate requires fresh consuming source gates and a new archive
coordinate, `py_1`. Record both histories and qualify only the final installed
bytes. These administrative checks do not qualify science or waive #107.

## Acceptance and recovery

- Exact-source required gates and all declared installed profiles pass.
- Canonical tag, package metadata and stable GitHub Release agree on 0.28.0.
- Public main label and solver index match the tested staging archive digest.
- A clean public solve installs that file and exercises new record/storage APIs.
- Owning issue, receipts, release notes and archived outcome agree.

On a failed source gate, fix and qualify a new candidate before staging. On a
defective or already occupied artifact coordinate, use an additive build number;
never overwrite the original file. On a post-promotion verifier failure, inspect
read-only registry/index state and rerun only the observation boundary. Do not
move a public tag or republish bytes to force a green workflow.
