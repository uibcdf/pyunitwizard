# Performance Baseline

This directory stores lightweight baseline scripts for release-candidate
performance checks.

Current baseline script:

- `conversion_baseline.py`: measures median/min/max time per call for hot
  API paths (`convert`, `get_form`, `is_quantity`, string parsing,
  dimensionality extraction, and standardization).

Run:

```bash
python benchmarks/conversion_baseline.py
```

Every case is timed in both telemetry modes, and SMonitor is pinned explicitly
for each block rather than inherited: telemetry is enabled by default on
import, so an unpinned run silently measures whatever ambient configuration it
found. Results land in two keys:

- `results`: telemetry enabled, which is the mode users actually run in;
- `results_telemetry_disabled`: the same cases with SMonitor off.

The difference between them is the instrumentation cost per case, which is the
figure that is otherwise invisible and the reason both modes are recorded.

The RC process stores snapshots under `devguide/` so regressions can be
compared between candidate tags. When quoting these numbers as provenance,
record `git describe --tags --always` alongside the `versions` block: that
block reports installed distribution metadata, which in a development checkout
reflects the last install rather than the working tree.
