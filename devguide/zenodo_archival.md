# Zenodo release verification

PyUnitWizard is registered as primary/stabilizing with required archival.
Follow the [common archival policy](../MOLSYSSUITE_GUIDE.md#release-archival-and-doi-claims)
and [MolSysSuite procedure](https://github.com/uibcdf/molsyssuite/blob/main/devguide/zenodo_policy.md).
Adoption is owned by [#140](https://github.com/uibcdf/pyunitwizard/issues/140).

The stable concept DOI is `10.5281/zenodo.8088374`. The maintained caller
`.github/workflows/zenodo_archival.yaml` delegates to the immutable shared
verifier at `20628bd5dba6d759669b0d444fe657eb1edad33f`. It performs bounded
public reads, installs no scientific runtime and changes no deposit, hook,
release or package. Zenodo requests are anonymous. GitHub authentication is
used only for public release discovery.

## Events and evidence

Published releases, including prereleases, request an exact-tag probe. A
manual optional `tag` input supports exact historical or missed releases;
an empty tag performs discovery from the fixed adoption timestamp
`2026-11-05T00:00:00Z`. The six-hour schedule (`17 */6 * * *` UTC) retains
unverified covered releases after later versions arrive. Never move that
cutoff to hide delayed ingestion or reset the original publication clock.

The shared tool retains the original GitHub `published_at` timestamp and
the 72-hour outer recovery window. `ingestion_pending` before that deadline
can be operational success; only `verified` proves archival. `invalid`,
overdue `absent` and `temporarily_unavailable` remain distinct. Scheduled
execution may be delayed; the maintainer dispatches a manual probe and owns
overdue follow-up. Generic receptor output reports job execution only; read
the retained semantic JSON before making any DOI claim.

Verify repository/tag identity, version, software/open access, distinct
concept/version DOIs and every archived file's name, size and checksum.
Source-snapshot verification does not cover Conda files or release assets.
Do not replay deliveries, change account integration or create a deposit
as an automatic response to a failed probe. Inspect only authorized,
least-disclosure connection projections when account diagnosis is needed.

## Metadata and the 0.29.1 candidate

The existing repository has neither `CITATION.cff` nor `.zenodo.json`.
There are therefore no conflicting repository citation files to reconcile.
Its existing GitHub/Zenodo integration metadata is retained; no creator,
ORCID or license choice is invented here. Zenodo describes citation files
as an optional metadata enhancement in its
[CITATION.cff documentation](https://help.zenodo.org/docs/github/describe-software/citation-file/).
Adding either format later requires owner review and shared-field validation.
The implementation license and catalogue's separate attribution remain in
their original source notices and distribution metadata.

The qualified 0.29.1 Conda archive retains original source
`ab92f1e645dfdd291f76785795b0d15b6a8c1257`, producer 42125299597/1 and SHA-256
`5bdf9b137c8862f99fc26e6ea5aa6e2ecea5a46ee1dc5e71127565411fedbe27`.
Its release tag must keep that original source. This default-branch
operational caller does not rebuild or retag the archive. Because the
original source predates the caller, **dispatch the first 0.29.1 exact-tag
probe manually on main immediately after public release publication**.
The fixed-cutoff schedule provides subsequent discovery/recovery. Future
release tags containing the caller also receive the published-release event.

## Existing observed baseline — 2026-11-05

The pinned public verifier independently reports 0.29.0 as `verified`:
record `23604831`, version DOI `10.5281/zenodo.23604831`, concept DOI
`10.5281/zenodo.8088374`, one `uibcdf/pyunitwizard-0.29.0.zip` source snapshot,
2,615,648 bytes, checksum `md5:c2763f48efabc952875fa4e0152ec0b6`.
A least-disclosure GitHub projection observes one active Zenodo release hook;
no receiver configuration or credentials are retained. That observation is
not proof of future ingestion. This baseline makes no 0.29.1 archival claim.

Before closing a future release, retain its exact semantic probe and notify
MolSysSuite with actual coverage. The suite owns its collective inventory;
this repository does not edit sibling receipts or citation metadata.
