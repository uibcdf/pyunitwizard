# Proposal: a cheap way to ask *"is this quantity already canonical?"*

**Status:** implemented (2026-08-13). **Everything measured**, with the command next to it.
**Origin:** ArgDigest, while deciding whether to add a value-certification mechanism. It
was designed, built, tested and then declined, because the problem it solved turned out
to be this one.
**Relation to [`python_overhead_before_rusterization.md`](python_overhead_before_rusterization.md):**
same family, different consequence. That proposal shows the API costs 15x what pint
does. This one shows that one specific missing predicate makes downstream libraries
convert unconditionally — or build a caching layer to avoid asking.

---

## 1. The measurement

PyUnitWizard has no cheap way to answer *"is this quantity already in the unit I want?"*.
Asking costs more than converting.

| call | 10 elements | 5000 elements |
|---|---:|---:|
| `puw.get_unit(q)` | 407 µs | 363 µs |
| `puw.check(q, unit='nm')` | 918 µs | 887 µs |
| `puw.get_value_and_unit(q)` | 426 µs | 380 µs |
| **`q.units` — the pint attribute underneath** | **0.78 µs** | **0.88 µs** |
| `str(q.units) == 'nanometer'` | 7.71 µs | 7.78 µs |

```bash
python -c "
import timeit, numpy as np, pyunitwizard as puw
puw.configure.load_library(['pint']); puw.configure.set_default_form('pint')
q = puw.quantity(np.random.random((5000,3)), 'nanometers')
for label, fn in (('puw.get_unit', lambda: puw.get_unit(q)),
                  ('puw.check   ', lambda: puw.check(q, unit=\"nm\")),
                  ('q.units     ', lambda: q.units)):
    print(label, round(timeit.timeit(fn, number=1000)/1000*1e6, 2), 'us')"
```

**Two things stand out.**

The cost is **flat with array size** — 407 µs for 10 elements, 363 µs for 5000. Whatever
this is, it is not work on the data. It is fixed API overhead, which is the same
conclusion `python_overhead_before_rusterization.md` reached from a different entry
point.

And the capability already exists: the pint quantity underneath answers in **0.78 µs**.
`puw.get_unit` wraps that into something **~450x slower**. Nothing is missing at the
bottom; the fast path is simply not exposed.

## 2. Why this specific gap matters more than its size suggests

A unit-aware library wants to write this:

```python
def digest_coordinates(coordinates):
    if already_in_nanometers(coordinates):
        return coordinates              # nothing to do
    return convert(coordinates)
```

Today `already_in_nanometers` costs more than `convert`, so the guard is worse than
useless and every library skips it and converts unconditionally.

**Measured downstream.** MolSysMT's `digest_coordinates` costs **0.659 ms on input that
is already in nanometers** — indistinguishable from the 0.670 ms it costs when a real
conversion is needed. A user workflow like

```python
coords  = msm.get(molsys, coordinates=True)                      # canonical already
com     = msm.structure.get_center_of_mass(molsys, coordinates=coords)
rmsd    = msm.structure.get_rmsd(molsys, coordinates=coords, reference=ref)
inertia = msm.structure.get_inertia_tensor(molsys, coordinates=coords)
```

burns ~2.6 ms re-canonicalizing a value that never stopped being canonical. These are
public API boundaries, so validation genuinely belongs there — what does not belong is
being unable to notice it has nothing to do.

## 3. The consequence we nearly shipped

ArgDigest reached the point of designing a mechanism to work around this: certify a
value by identity when a digester canonicalizes it, so later calls could skip the work
without asking. It was built and measured — 3.5 µs to issue a claim, 0.46 µs to consult
one — and it worked.

It was **declined**, and this proposal is why. A registry of already-canonical values,
with claims bound to digesters and guards against mutation, is a large amount of
machinery whose entire purpose is to avoid asking a question that should cost 1 µs. The
right fix is one predicate here, not a caching layer in every consumer.

That is the part worth taking seriously: **a missing cheap predicate does not stay
missing.** Each downstream library eventually builds its own way around it, and they
will not agree with each other.

## 4. What is proposed

A predicate that costs what the underlying attribute costs:

```python
puw.is_unit(q, 'nanometers')    # -> bool, no conversion, no value extraction
```

Requirements:

- **No value extraction.** It answers about the unit, so it must not touch the magnitude.
  That is what makes it flat *and* cheap rather than only flat.
- **Cost of the same order as the underlying form's own attribute access** — around 1 µs
  for pint, not 400.
- **Honest across forms.** Where a form cannot answer cheaply, saying so is better than
  answering slowly: a `None` that means *"ask me the expensive way if you really need
  it"* lets the caller decide, and matches how ArgDigest already treats undecidable
  domains.

Whether it is a new function or a fast path inside `puw.check` is an implementation
choice. What matters is that a caller can ask without paying more than the answer is
worth.

## 4.1 Implementation result

The public predicate is `puw.has_unit(quantity_or_unit, target_unit, parser=None)`.
It returns `True` or `False` when exact unit metadata can be compared cheaply and
`None` when the input is textual or the backend cannot decide without general
parsing/conversion. It never extracts the magnitude, supports external Pint
registries, and is used as the fast path for `check(..., unit=...)`.

On the implementation host, with a warm cache and telemetry disabled:

| call | time |
|---|---:|
| `puw.has_unit(q, "nm")` | 2.58 µs |
| `puw.has_unit(external_pint_q, "nm")` | 2.42 µs |
| `puw.check(q, unit="nm")` | 4.81 µs |
| `puw.get_unit(q)` | 99.15 µs |
| `q.units` | 0.76 µs |

Contract and cross-backend evidence lives in `tests/test_has_unit.py`.

### 4.2 Propagation through normalization paths

The predicate is also used by the general conversion and normalization routes. An
exact-unit `convert()` returns the original object when the requested form and output
type also match. `standardize()` recognizes the first configured standard for each
dimensionality without recomputing the input dimensionality, and `ensure_quantity()`
uses that metadata to satisfy a compatible dimensionality requirement. Registered
`fast_track` normalizers use `has_unit()` instead of the general `get_unit()` API.

On the same implementation host, for a warm Pint quantity containing a `(5000, 3)`
float array, with telemetry disabled:

| already-canonical path | time |
|---|---:|
| `puw.fast_track.to_nanometers(q)` | 3.37 µs |
| `puw.convert(q, to_unit="nm")` | 16.23 µs |
| `puw.standardize(q)` | 5.56 µs |
| `puw.ensure_quantity(q, dimensionality={"[L]": 1})` | 14.94 µs |

Identity, dimensionality, duplicate-standard, and cross-form regression coverage lives
in `tests/test_conversion_branches.py`, `tests/test_specialized.py`,
`tests/test_standardize.py`, and `tests/test_ensure_quantity.py`.

## 5. What this does not claim

It does not claim `get_unit` and `check` are wrong — they do more, and their generality
has a price. It claims the price is not always worth paying and there is currently no
way to opt out.

It also does not settle whether the fix belongs before or after rusterization. If the
overhead is decorator and telemetry, as `python_overhead_before_rusterization.md`
measured, then this predicate may fall out of that work for free, and this document is
then a reason to prioritise it rather than a separate task.

## 6. Related

- `uibcdf/argdigest` → `devguide/pending_proposals/value_certification/` — the mechanism
  declined in favour of this, preserved with its code and measurements.
- `uibcdf/molsysmt#147` — digestion placed on internal predicates, a different cause with
  a similar symptom.
