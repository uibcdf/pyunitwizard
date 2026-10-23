# Development resource ownership review

Owner: PyUnitWizard maintainers; local review uibcdf/pyunitwizard#116,
coordinated by uibcdf/molsyssuite#104. Inspected baseline:
`a2d7e38f6d8dc8f4072cc19b09a8cacddf77899a`, 2026-10-22.
The accepted contract is `MOLSYSSUITE_GUIDE.md#temporary-development-resources`.
Guide delivery, source inspection, executed disposal and historical absence
are separate observations. This review makes no universal compliance claim.

## Applicable operations and dispositions

| Operation / owner | Resources and useful lifetime | Disposition and evidence |
|---|---|---|
| Concurrency tests / test parent | Synthetic clients until cold children complete or are killed/reaped | Existing parent `TemporaryDirectory` owns disposal on success/failure/start failure/timeout. Six actual lifecycle guards and eight real concurrency repetitions pass; #115 remains resolved. |
| Other test fixtures / pytest caller | Source copies, builder environments, HDF5 files, mock registries, Git repositories and saved attribution within explicit `tmp_path` | Fixture lifetime belongs to the test invocation. Default pytest retention is useful failure evidence, not a product cache. The caller retires a dedicated basetemp after inspecting/exporting required evidence; never pass an existing shared directory as basetemp. No global pytest-tree cleanup was executed. |
| Installed attribution test / pytest caller | Producer-source copy, isolated builder, installed target and consumer directory in `tmp_path` | Synchronous children finish before the test returns; caller evidence stays outside any disposable sub-operation. Actual installed-provider/scientific tests are not rerun for this lifecycle review. |
| Registry cache / application | Explicit opt-in Pint disk-cache destination | Persistent application-owned cache; not disposable task storage. No caller cache is deleted. Scope and refusal behavior remain in `tests/pint/test_registry_cache.py`. |
| Attribution benchmark / standalone caller | Process configuration and temporary dispatch/provider substitutions; output goes to stdout | Existing `finally` restores the substituted callables, while scoped provider contexts end on exit. Source review only here; the 2026-10-09 controlled restoration observations keep their original identity. No new performance or general configuration-restoration claim. |
| Report/index tools and vector generator / maintainer | Explicit maintained Markdown, metadata and published test vectors | Intended durable outputs, not scratch. Index regeneration is checked; vector generation is not executed. No report, historical record or vector is discarded as cleanup. |
| Dependency preflight and backlog tools / caller | Pinned provider checkout, synchronous children, bounded HTTP responses and caller-selected receipts | Consumers validate but do not delete the provider/source prefix or supplied receipts. Source inspection and selected dependency-route guards; no new solve or provider/public qualification. |
| Conda freezer/build / build caller | Ephemeral build source and build/test prefix | #117 reproduces masked freezer/installer failures. The corrected shell stops before installation on freezer failure and preserves installer failure status. Three real-script/control-installer cases pass; source version identity remains guarded. No actual Conda build, upload or public archive was qualified by these cases. |
| Release-route and installed verifier / caller | Explicit archive, receipt directory and installed prefix | Context-managed reads and synchronous checks; the tools consume caller inputs without deleting them. Publication and installed-byte evidence retain their own source/run/digest identities. Source inspection only in this review. |
| Autosummary cleaner / docs caller | Generated `autosummary` subtrees under the explicitly selected API root | Authored landing pages remain outside this generated scope. Three actual cleaner guards cover successful disposal, missing-root no-op and visible injected removal failure. No primary docs output was cleaned. |
| Notebook executor / docs caller | Requested notebooks, logs and tracked success timestamps | Caller intentionally requests in-place execution. Useful logs stay adjacent until inspected; failure invalidates the success marker. #118 corrects the CLI's masked failure status while processing the remaining batch. Six controlled child cases pass; no real notebook was executed. |
| Sphinx Makefile / docs caller | `docs/_build`, `docs/jupyter_execute` and generated API stubs | Generated outputs can stay while preview/debugging is useful. `make clean` targets only these documented destinations; cleaner exceptions propagate. No primary site build or cleanup is executed by this audit. The unsupported Windows wrapper remains source-only and does not create a Windows support claim. |
| Hosted source/release/docs/OpenFF/storage/install jobs / workflow runner | Checkout, `.governance-tools`, environment/cache/build outputs and job-private `RUNNER_TEMP` fixtures | Reviewed all 12 workflow files. Disposable workspace ownership belongs to the job, with useful receipts exported through its existing upload steps. Source inspection does not prove actual runner retirement or failure-path artifact retention. Hosted science/build/promotion gates remain independently required when their scope changes or publication is claimed. |

The selected cleanup guards inject an inner deletion error intentionally; those
fixtures belong to this review's outer temporary root. The tests assert that
the error remains visible and caller receipts survive. Disposal of the outer
root after evidence export does not relabel the inner failure as success.

## Retained resources and historical observations

- The primary checkout, shared `molsyssuite@uibcdf_3.14` environment and existing
  local build/docs/pytest outputs belong to the maintainer or their caller.
  They were not created by this review and are preserved. Their purpose is
  ordinary source/docs work and failure inspection; review them at the next
  affected build or by 2026-11-05, with the owner deciding explicit paths.
- The six explicit #115 paths registered in the central historical inventory
  are absent at this inspection. No deletion was performed here, and the
  deleting actor is unknown. This is not an exhaustive inventory of `/tmp`.
- Git lists four worktree registrations whose target directories are absent.
  Their metadata is retained as owner-managed provenance; this review neither
  removes branches nor prunes registrations belonging to earlier tasks.
  Future owner-authorized retirement must use Git after preserving references.
- This task's private root is the only disposable tree owned for retirement
  here. It holds controlled fixtures and check receipts through verification.
  Export the sanitized receipt to `devguide/evidence/`, then retire that exact
  root. Required public/source artifact evidence stays in its existing records.

## Scope, limitations and recovery

Selected Python 3.14 tests exercise actual shell/CLI/cleaner control flow,
existing client lifetime and caller-evidence preservation. They do not qualify
scientific notebook output, package installation, real solver/upload/promotion,
every OS cleanup fault or all provider branches. Injected failures establish
propagation, not actual permission failures on another platform.

The shared development environment still reports seven pre-existing dependency
conflicts owned by uibcdf/molsyssuite#82. No package or environment is modified;
these tests do not certify that closure. Wider science and public release gates
retain their independent routes, including the full Python 3.11–3.14 matrix.

No remaining cleanup implementation gap was reproduced after the focused
#117/#118 corrections in this bounded scope, so no new lifecycle exception is
claimed. New operations, changed destinations or an observed cleanup failure
require a fresh owner review; an unresolved limitation must name its operation,
owner, interim procedure, review date and removal condition in the owning issue.
Report the resulting disposition to MolSysSuite #104 without closing the shared
coordination issue or claiming attribution for previously absent resources.
