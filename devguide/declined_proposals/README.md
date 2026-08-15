# Declined proposals

This directory preserves proposals that were considered and **not** adopted.
They are kept as design evidence and as a record of the reasoning, so the same
ground is not re-argued from scratch, but they are not part of the backlog.

A declined proposal is separate from a completed one: nothing here was built.
Each document states the condition, if any, under which it could be revisited.

- `rusterization_pyunitwizard_core.md`: declined as unnecessary. The Python
  fast-path work removed the overhead that motivated a native core; the
  remaining per-call cost is dominated by the unit backend itself.
