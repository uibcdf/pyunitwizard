---
summary: Avoid building filtered diagnostics for expected negative quantity probes.
issue: uibcdf/pyunitwizard#141
status: resolved
opened: 2026-11-06
closed: 2026-11-11
verification: measured
area: [introspection, diagnostics, performance]
guard: tests/test_introspection_probe.py::test_filtered_probe_skips_payload_and_follows_live_debug_level
normative:
blocked_by: []
supersedes: []
---

# Expected negative probe cost

PharmacophoreMT's cached generation repeatedly asks whether ordinary metadata
is a quantity. Its profile identifies repeated construction of the DEBUG
probe-miss event as a material cost. SMonitor separately tracks registration
and path-resolution work for events that reach its catalog. [Provider issue](https://github.com/uibcdf/smonitor/issues/63)

The probe-miss helper reads SMonitor's public current level before computing
`repr(value)` or entering catalog emission. At the known thresholds from INFO
through CRITICAL, SMonitor discards DEBUG before routing or buffering. DEBUG
and unfamiliar levels retain the catalog path and the current capture policy.
The decision is made per call so a later DEBUG configuration is effective.

The fresh-process regression checks INFO, DEBUG and WARNING in one process.
The earlier code called `repr` at INFO. The candidate defers it until DEBUG
and delivers the same catalog code, source context and value. The string
probes now finish first-use Pint setup before configuring the diagnostic
level. On SMonitor 0.16.0, legacy first-use registration can otherwise change
the level during the first probe.

Both the development provider and the public SMonitor 0.16.0 `py_1` artifact
pass the 26 focused introspection and extraction tests. The minimum-provider
run loads Pytest Receptor explicitly so the newer SMonitor plugin installed
in the development environment cannot be mixed with the older runtime.

In four fresh processes ordered baseline/candidate/candidate/baseline, six
timings per variant of 2,000 warmed negative probes at INFO give medians
211.29 ms and 13.14 ms. Every result is false and no probe event reaches the
buffer. Baseline source is `555e70c`. This measures the probe itself. A
complete PharmacophoreMT performance comparison belongs to consumer receiving.

The change shipped in 0.29.2. All 30 installed cells and the clean public
installation executed the live-level regression.
[Publication record](release_0.29.2.md)
