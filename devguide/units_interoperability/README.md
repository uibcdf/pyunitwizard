# PyUnitWizard Units Interoperability Development Guide

Historical note:
- This folder contains conceptual drafts and decomposition notes.
- The consolidated forward-looking summary is now maintained in
  `devguide/interop_future_directions.md`.
- Active operational planning is maintained outside this folder in
  `devguide/roadmap.md` and release checklists.

This development guide documents the vision, motivation, architecture,
and roadmap for evolving **PyUnitWizard** into a **units interoperability
layer for the Scientific Python ecosystem**.

The goal is not to replace existing unit libraries, but to provide a
lightweight interoperability layer that allows them to work together
reliably.

Supported ecosystems include:

- Pint
- unyt
- astropy.units
- openmm.unit

The documents in this guide describe:

• the motivation for the project
• the interoperability problem
• design principles
• architectural strategy
• interoperability specifications
• implementation roadmap

Suggested repository location:

pyunitwizard/devtools/units_interoperability/
