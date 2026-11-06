# Approved 0.29.1 publication decision

Owned by [release #138](https://github.com/uibcdf/pyunitwizard/issues/138).
The maintainer explicitly approved publication on 2026-11-06 UTC. The stable
tag/Release and exact-file promotion are complete; the proposal and execution
sequence below retain the reviewed identities. Published receipts are in
`evidence/release_0.29.1_2026-11-06.json`.

## Exact identity

| Item | Qualified identity |
| --- | --- |
| Version, tag and GitHub Release title | `0.29.1` |
| Original source and eventual tag target | `ab92f1e645dfdd291f76785795b0d15b6a8c1257` |
| Build | `py_0`, build number `0` |
| File | `pyunitwizard-0.29.1-py_0.tar.bz2` |
| Size | 96,418 bytes |
| SHA-256 | `5bdf9b137c8862f99fc26e6ea5aa6e2ecea5a46ee1dc5e71127565411fedbe27` |
| Qualified staging channel | `uibcdf/label/staging`, staging only before promotion |
| Producer | [42125299597/1](https://github.com/uibcdf/pyunitwizard/actions/runs/42125299597) |
| Installed qualifier and source | [42129616605/1](https://github.com/uibcdf/pyunitwizard/actions/runs/42129616605), original source above |

The staging-only registry identity, byte size and digest were independently
rechecked on 2026-11-06 UTC. The remote `0.29.1` tag was absent at that check.
Operational archival and evidence commits on main do not replace the original
source, redefine the candidate, or require a rebuilt file.

## Completed evidence

All 29 required exact-source native jobs and their named steps passed:
full matrix 42112262781/1, Release Gates 42112279815/1, policy 42112229284/1,
OpenFF 42112292554/1 and storage 42112305747/1. Ordinary CI 42112228639/1
also passed, including both coverage uploads. The pinned common dependency
preflight verifies the original candidate's 22 routes. See
[`evidence/release_0.29.1_source.json`](evidence/release_0.29.1_source.json).

The original archive's metadata, hard floors, SPDX expression, both original
license payloads, notice/catalogue resources and 92 tracked Python source files
were independently checked. Producer events, route and byte inspection are in
`evidence/release_0.29.1_{producer,route,staged_bytes}.json`.

All 30 installed cells passed: baseline/storage/prepared on Linux and macOS
arm64 over Python 3.11–3.14, and OpenFF over 3.12–3.14. Their 240 required
native steps executed successfully. Conda and pip closures match the exact
file, public provider versions/builds, Python minor and architecture.
The downloaded JUnit reports contain 10,100 passing entries, including 750
calorie, 120 policy-handshake and 60 concentration-reader cases without skips.
Required storage/OpenFF/prepared attribution guards are present and unskipped.
Intentional JSON and older-Ackredit prepared-API skips are explicitly classified
in [`evidence/release_0.29.1_installed.json`](evidence/release_0.29.1_installed.json).

Required resumable archival adoption #140 is complete. Hosted positive control
42134178934/1 verifies existing 0.29.0 source-only archival, with its semantic
receipt retained separately. This supplies no 0.29.1 DOI claim. The current
candidate predates the caller, so its first exact-tag probe will be manual on
main after publication, with fixed-cutoff scheduled recovery thereafter.

The proposed public release notes are
[`release_0.29.1_notes.md`](release_0.29.1_notes.md). They cover the Astropy
calorie/registry correction, justified NumPy/Pint floors, existing license
metadata and immutable Conda-provider adoption. They introduce no new stable
quantity-record/storage/dialect/attribution API or format admission.

## Approved final decision and execution

The maintainer approved the stable `0.29.1` tag and GitHub Release at the exact original source
above, followed by promotion of the already qualified file by its exact digest.
Preserve published 0.29.0 and all historical source/producer identities.

Reviewed execution sequence (completed):

1. Recheck the exact coordinates, then create tag and Release titled `0.29.1`
   using the prepared notes. Verify the staged release event does not rebuild.
2. Dispatch the existing exact-file promotion route with the original source,
   version `0.29.1`, build `0` and SHA-256 above. Independently verify public
   main labels and solver-index records; any read-only verifier retry must
   preserve the same file and promotion identity.
3. Complete clean public-channel receiving and served-documentation checks.
   Record the actual public/platform scope; staging alone is not receiving.
4. Dispatch the exact-tag Zenodo probe on main. Retain its semantic state and
   original publication clock; claim a version DOI only after verification.
5. Update the owner canonical `standards/PYUNITWIZARD_GUIDE.md` with the actual
   public floor and scope. Open the version-specific MolSysSuite notice with
   the real package/Release and canonical-guide commit/hash, leaving client
   synchronization and owner receiving to MolSysSuite as requested.
6. Synchronize #138, release notes, devguide indexes and the final evidence;
   archive the resolved preparation record and review task-owned temporary
   resources. Unrelated shared-environment conflicts remain in MolSysSuite #82.

The current preparation closeout changes documentation/evidence only. Its local
reporting and release-contract checks apply to those inputs; native checkpoints
on that documentation head remain operational evidence, separate from the
already qualified original source and installed file.


## Executed outcome — 2026-11-06 UTC

Release 436100116 and annotated tag 9209062767b4d50431c28e99db8c5d9402d723a1
identify original source ab92f1e. Promotion 42162820178/1 preserves the file
and digest; independent main-label and solver-index verification passes.
The staged release event 42162787779/1 verifies its decision and skips both
build branches. Public-only Linux/Python 3.14.10 receiving passes 132 selected
cases with one intentional strict-JSON skip and clean pip requirements.
Documentation 42162787792/1 and Pages 42162885745/1 publish actual 0.29.1 pages.
Zenodo probe 42162823352/1 independently verifies source record 23995546,
version DOI 10.5281/zenodo.23995546; it makes no Conda coverage claim.
Canonical guide commit de0969242d094f687ff047d08ac950031c882da8 and its digest
are delivered through MolSysSuite #172. Consumer receiving remains suite-owned.
