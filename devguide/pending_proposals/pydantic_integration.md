---
summary: Define whether PyUnitWizard needs a Pydantic integration contract.
issue: uibcdf/pyunitwizard#52
status: open
opened: 2025-10-23
closed:
verification: asserted
area: [integration, serialization]
guard:
normative:
blocked_by: []
supersedes: []
---

# Define whether PyUnitWizard needs a Pydantic integration contract

## What

Evaluate a post-1.0 integration with Pydantic only after identifying a concrete public
contract. Possible scopes include validating quantity-bearing model fields, serializing
them, generating schemas, or some explicitly chosen combination.

## How

Begin from representative MolSysSuite and external-user models rather than from a direct
dependency addition. Specify accepted inputs, unit preservation, validation errors,
serialization format and optional-dependency behavior before implementing adapters.

## Why

Pydantic is widely used at application boundaries, but the original issue contains no
use case showing which PyUnitWizard responsibility is missing. A generic integration
could couple the library to framework version changes without improving its core unit
interoperability contract.

## What is measured and what is assumed

No behavior or demand has been measured. The usefulness of an integration remains an
assumption, which is why `verification` is `asserted`.

## What was refuted

Adding Pydantic merely because it is popular is not sufficient. The 2026-08-13 triage
explicitly deferred implementation until a validation, serialization or combined
contract, real use cases, a maintainer and reproducible tests exist.

## Scope and exclusions

This proposal is post-1.0 and does not block the stabilization wave. It does not propose
making Pydantic a mandatory runtime dependency.

## Acceptance criteria

1. At least one real integration use case identifies behavior PyUnitWizard should own.
2. The validation and serialization boundary is written explicitly.
3. Optional dependency and supported Pydantic-version policies are defined.
4. A maintainer accepts ownership and reproducible behavior tests are designed.
5. The proposal is then accepted into an implementation plan or withdrawn with the
   evidence recorded here and on `uibcdf/pyunitwizard#52`.
