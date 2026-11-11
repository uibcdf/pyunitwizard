---
summary: Check whether Pint is loaded before configuring its registry cache.
issue: uibcdf/pyunitwizard#144
status: partial
opened: 2026-11-10
closed:
verification: reproduced
area: [configuration, documentation]
guard: tests/test_consumer_guide_bootstrap.py::test_consumer_guide_bootstrap_preserves_existing_registry_and_policy
normative:
blocked_by: []
supersedes: []
---

# Cache configuration in the canonical consumer guide

The canonical bootstrap example used the absence of a policy to decide when
to configure both units and the Pint cache. An application can build a Pint
registry by creating a quantity before it sets a policy. A later cache
request then warns because the registry already exists. MolSysMT received
the loaded-library guard in `af46ea3f` under uibcdf/molsysmt#674.

The canonical example now checks the public `configure.report()` before
requesting the cache. The policy guard still controls form, parser and unit
standards. Fast tracks are declared outside both checks.

The regression executes the actual guide example in three fresh interpreters.
The old example fails the prior-Pint-use case with the late-cache warning.
The revised example passes cold start, prior Pint use without a policy and
an active application policy. The checks cover registry identity, the cache
setting, policy provenance and the named nanometer conversion.

Publish the canonical revision before delivering its commit and content
digest for MolSysSuite-owned client synchronization. The runtime warning
continues to describe real late setter calls.
