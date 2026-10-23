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

## Record translation evaluation

`devtools/benchmark_record_translation.py` owns a reusable
`compare_translation(quantity, target_form, target_unit, ...)` operation and a
CLI using the published TopoMT coordinate fixture. Install the optional OpenMM,
unyt and Astropy backends from the development profile before running:

```bash
python devtools/benchmark_record_translation.py --iterations 100 --repeats 7 > comparison.json
# Synthetic array-size control derived by repeating those coordinates:
python devtools/benchmark_record_translation.py --tile 1000 --iterations 20 --repeats 7 > comparison-large.json
```

The five cost scopes are distinct: `direct` translates a live quantity;
`via_pint` uses an explicit live Pint bridge without constructing a record;
`via_record` constructs and seals a new record before reading it; `read_existing`
starts with an already validated immutable record; `read_wire` decodes and
verifies a prepared base64 representation before reading. Wire encoding, imports
and setup are outside timing. None of the reader-only paths measures the cost
of producing a record, and no path removes Pint.

Every route must match the explicit Pint reference's negotiated unit, numeric
values, shape and dtype before and after timing. The tool supports finite
quantities, rotates route order, retains raw samples and pins both telemetry
modes while restoring caller policy and the prior telemetry enabled state on
success or failure. These runs do not benchmark optional attribution capture.
The CLI records actual Python/platform, source hashes, fixture provenance and
installed metadata separately. A tiled input is a synthetic scaling control,
not an observed growing-data consumer or installed/public artifact qualification.
