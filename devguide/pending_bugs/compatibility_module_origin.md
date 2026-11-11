---
summary: Give the pyunitwizard.main compatibility module a verifiable provider origin.
issue: uibcdf/pyunitwizard#146
status: active
opened: 2026-11-10
closed:
severity: medium
verification: reproduced
area: [core, interoperability, provenance]
guard: tests/test_api_layout.py::test_main_compatibility_module_exposes_its_creator_origin
normative:
blocked_by: []
supersedes: []
---

# Give the compatibility module a verifiable creator origin

## What

The virtual `pyunitwizard.main` alias has no file/spec origin. Python source
introspection treats it as a built-in module, and MolSysSuite's loaded-origin
checker rejects it after an otherwise successful ordinary installation.
DockingMT #74 observes this in run 42960218358, Python 3.11 job 130325030977,
on provider f82b618 and installed SDK 95f693b. Its ten normal-policy storage
cases pass before the origin gate fails; pm/fs and full product receiving stay
pending. This does not indicate incorrect quantity or storage values.

## How

Declare the actual package initializer that creates this virtual module as
its file/spec origin and package parent. The stdlib module spec has no loader;
it records the creator without executing the initializer as a different module.
Preserve lazy API forwarding, function identity and one-time deprecation.
Add a regression through `inspect.getsourcefile` and `importlib.util.find_spec`.
The advance consumer-impact notice is MolSysSuite #184.
The patch is reviewed against current base 9f59894; the creator bytes are equal
to f82b618 before this fix. No shared developer checkout is modified.

## What is measured and what is assumed

The consumer's isolated target fixture uses the retained original provider
wheel and actual pinned SDK, with borrowed dependencies explicitly outside its
whole-closure claim. Before the patch: two failed/six passed, covering the real
origin rejection and source-introspection failure. After the patch: eight
passed, including all five unchanged API tests and rejection of an outside
origin; one expected deprecation warning remains. No scientific import or
quantity calculation executes. The original interpreter, exits, events, files
and resource records remain with DockingMT #74, review 2026-11-14.

These focused results do not replace this branch's complete required tests or
future DockingMT receiving. Full routine-Python qualification is required before
opening the requested PR; merge acceptance and consumer pin/receiving remain
owner actions. No version, package publication or dependency floor is changed.

## Acceptance criteria

The metadata regression and existing API tests pass; the actual common checker
accepts the creator and retains outside-prefix/source rejection. Complete
required source checks pass before integration. After owner review/merge,
archive this record and close #146 with the delivered commit/guard; DockingMT
then receives the new exact provider reference under #74. Source delivery is
separate from a public PyUnitWizard release or package.
