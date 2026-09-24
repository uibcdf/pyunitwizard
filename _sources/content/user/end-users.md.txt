# End Users

This page is for scientists and practitioners using a library that already
integrates PyUnitWizard.

You usually do not need to configure PyUnitWizard directly. What matters is
understanding how to provide quantity inputs that your host library can parse
reliably, and how to react when a units-related check fails.

In practical terms, PyUnitWizard in your host library means:
- string quantities are often accepted (for example `"10 angstrom"`),
- compatible units are converted safely when needed,
- dimensional mismatches are rejected early with clearer messages.

A robust day-to-day workflow is simple:
1. provide explicit units in inputs,
2. avoid bare numbers unless the host library documents a default unit,
3. when you hit an error, inspect compatibility/dimensionality assumptions first.

For daily usage, this short sequence is usually enough:
- [Quick Start](quickstart.md)
- [Troubleshooting](troubleshooting.md)
- [FAQ](faq.md)

Notebook companion for script users:
- [Convert.ipynb](Convert.ipynb)
- [Check.ipynb](Check.ipynb)
- [Strings.ipynb](Strings.ipynb)

If you report a bug to maintainers, include:
- the exact input quantity values and units,
- the expected result and observed result,
- the smallest script that reproduces the issue.
