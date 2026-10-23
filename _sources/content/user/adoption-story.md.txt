# Adoption Story: From Drift to Determinism

This short scenario reflects a common migration in scientific libraries.

Before PyUnitWizard, a library accepted mixed quantity inputs across modules.
Some functions expected backend-native objects, others accepted strings, and
some silently assumed default units for bare numbers. The result was familiar:
subtle conversion drift, inconsistent error behavior, and hard-to-reproduce bug
reports.

The team introduced PyUnitWizard in one boundary module first. They centralized
configuration, set a canonical parser/form, and added dimensional checks at
public entry points. Output paths were standardized before data crossed module
boundaries.

After this change, two things improved immediately:
- user errors became earlier and easier to interpret,
- regression tests captured unit assumptions explicitly.

Only after this baseline was stable did the team expand coverage to more API
entry points and additional backends.

The key lesson is not speed, but sequencing. A small deterministic boundary
layer usually outperforms a broad but implicit migration.

If you are starting now, follow this order:
1. [What PyUnitWizard Solves](what-pyunitwizard-solves.md)
2. [Quick Start](quickstart.md)
3. [Mini Library Walkthrough](mini-library-walkthrough.md)
4. [Integrating Your Library](integrating-your-library.md)
