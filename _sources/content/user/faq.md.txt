# FAQ

## I use a library that already integrates PyUnitWizard. Do I need to configure it myself?

Usually no. In most integrations, maintainers configure PyUnitWizard at library
startup. As an end user, your main responsibility is to provide explicit units
in inputs and avoid ambiguous bare numbers.

## Do I need to use only one backend library?

No. PyUnitWizard is designed to interoperate across supported backends.
Integrators commonly start with one backend for determinism and then expand
coverage once tests are stable.

## What is the safest initial adoption strategy for maintainers?

Adopt incrementally: one backend, one canonical parser/form, explicit standard
units, and boundary-level checks before broader rollout.

## Should runtime be configured on every function call?

No. Configuration is application/library state and should be centralized.
Per-call reconfiguration increases drift and test flakiness.

## Can strings be passed as quantities?

Yes, when a compatible parser backend is loaded and configured.

## How do we avoid flaky tests?

Reset and reconfigure PyUnitWizard explicitly in test setup for each scenario.
Avoid relying on implicit global state across test files.

## What does PyUnitWizard add beyond backend-specific APIs?

A single cross-backend contract for parsing, conversion, compatibility checks,
and output standardization at the boundaries of scientific libraries.
