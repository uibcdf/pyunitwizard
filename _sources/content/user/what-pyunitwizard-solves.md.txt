# What PyUnitWizard Solves

Most scientific libraries eventually face the same units problem: users provide
quantities in multiple representations, while internal code expects one stable
contract.

Without a boundary layer, this usually leads to implicit assumptions,
conversion drift, and hard-to-debug failures that appear only in certain
workflows.

PyUnitWizard addresses this by separating concerns:
- at the boundary, it parses, converts, checks, and standardizes quantities,
- inside your domain logic, you operate on predictable, normalized values.

This separation is the main reason teams adopt PyUnitWizard. It reduces hidden
units coupling and makes behavior easier to test, document, and support.

PyUnitWizard is not meant to replace domain modeling or numerical validation in
your library. It complements that logic by making unit handling explicit and
reproducible.

If this matches your integration problem, continue with
[Quick Start](quickstart.md).
