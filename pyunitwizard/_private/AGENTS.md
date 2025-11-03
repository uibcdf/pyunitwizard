# Internal helpers guidelines

This directory contains internal-only helpers used by the public `pyunitwizard` package. None of the modules here are meant to be imported directly by users, and they may change without notice.

## Import discipline
- Avoid importing optional third-party dependencies at module import time. Delay those imports until they are needed inside functions to keep the public import path lightweight and failure-free.

## Behavioral consistency
- Keep helper semantics aligned with the public API in `pyunitwizard`. When adjusting logic here, double-check that the corresponding public-facing behaviors remain synchronized and update tests when necessary.
