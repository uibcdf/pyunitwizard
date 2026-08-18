# Developer Introduction

PyUnitWizard is a compatibility layer for scientific units across multiple
backends. As a contributor, your goal is to keep that layer predictable,
explicit, and stable for downstream libraries.

Contributions are usually strongest when they preserve three principles:
- deterministic runtime behavior through explicit configuration,
- backend-agnostic public API semantics,
- contract-first testing for compatibility-sensitive changes.

Use the main [Developer](../index.md) path for implementation and release work.
This page is only a short orientation entry point.
