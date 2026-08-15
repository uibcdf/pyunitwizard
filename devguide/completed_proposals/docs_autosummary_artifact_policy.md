# Proposal: make the autosummary artifact policy match what the build produces

**Status:** implemented (2026-08-15) as option **C**, plus one fix this document had missed.
See §8 for what was done and how it was verified.
**Scope:** `.gitignore`, `docs/clean_api.py` and its wiring, and the prose in `docs/AGENTS.md`
and `docs/README.md` that asked for the now-automated manual step. No documentation content
changes.

---

## 1. Observation

A working copy that has built the docs carries an untracked directory:

```
?? docs/api/users/autosummary/
```

36 generated `.rst` stubs. It shows up in `git status` on every unrelated command.

## 2. This is not a missing rule — it is a rule that does not match

`.gitignore:112` already states the intent:

```
/docs/api/_autosummary
```

That pattern cannot match what Sphinx writes, for three independent reasons:

| | pattern | reality |
|---|---|---|
| directory name | `_autosummary` | `autosummary` |
| depth | directly under `docs/api/` | under `docs/api/users/`, `docs/api/developers/` |
| anchoring | leading `/` pins it to that exact path | trees are nested per audience |

The entry looks like a survivor of an earlier docs layout. Nobody noticed, because a `.gitignore`
line that matches nothing fails silently — the only symptom is the permanent `??` in `git status`,
which reads as normal noise rather than as a broken rule.

## 3. The surrounding policy is already clear and already correct

These artifacts are *meant* to be transient, and the repository says so in three places:

- `docs/README.md`: the generated output "is temporary and must be recreated locally".
- `docs/AGENTS.md:93`: "Ensure no generated artifacts (`_build/`, `.nbconvert.log`, temporary
  autosummary directories) are staged."
- `docs/clean_api.py`: exists for exactly this, deleting every `autosummary/` directory under
  `docs/api/`.

So nothing about the intent needs deciding. The gap is purely mechanical: the intent is written
down, and the two mechanisms that should enforce it either do not match (`.gitignore`) or are not
wired to anything (`clean_api.py` is referenced only as a manual step in `AGENTS.md:22,73` — it
appears in no Makefile target and no workflow).

## 4. Options

**A. Fix the pattern only.** Replace line 112 with something that matches, e.g.
`docs/api/**/autosummary/`. One line, no behaviour change anywhere else.

**B. Leave it visible on purpose.** Argue that the `??` in `git status` is the reminder to run
`clean_api.py`, and that silencing it lets stale API pages survive longer.

**C. Fix the pattern and wire `clean_api.py` into the docs build**, so staleness stops depending on
whether anyone remembered.

## 5. Recommendation

**C**, with **A** as the acceptable minimum.

Option B does not really hold up: the entry on line 112 shows the intent was always to ignore these,
and staleness is handled by `clean_api.py`, not by anyone reading `git status`. A permanent untracked
entry does not function as a reminder — it trains readers to skim past `git status` output, which
costs more than it saves the first time it hides something real.

The reason to prefer C over A is that A leaves the same failure mode in place, just quieter: the
discipline stays in a human's memory. Wiring `clean_api.py` into the docs build makes stale stub
removal a property of building, and `AGENTS.md:22,73` can then describe the build rather than ask
for a separate remembered step.

Note that ignoring these paths also *helps* the requirement in `AGENTS.md:93` — artifacts that git
ignores cannot be staged by accident.

## 6. How to verify

```bash
# the pattern currently matches nothing:
git check-ignore -v docs/api/users/autosummary/ || echo "not ignored"

# after the change it should name the responsible line:
git status --porcelain | grep autosummary || echo "clean"
```

## 7. Provenance

Observed in a clean checkout of `main` at `ade72c1` while reviewing sibling repositories for
pending devguide work. Not a regression from that commit; the mismatch predates it.

## 8. Closure

Implemented as **C**. Four changes, none of which touch documentation content.

### 8.1 A third silent failure, not diagnosed above

§3 says `clean_api.py` "is not wired to anything". That was true but incomplete. The script
also could not have worked as documented:

```python
api_directory = 'api'   # resolved against the current working directory
```

`docs/AGENTS.md:22,73` and `docs/README.md` both told the reader to run `python docs/clean_api.py`
**from the repository root**. There, `os.walk('api')` walks a path that does not exist, yields
nothing, and exits 0 without printing:

```
$ python -c "import os; print(len(list(os.walk('api'))))"   # from repo root
0
```

So the one mechanism §3 credits as handling staleness had never removed a stub via its own
documented invocation. This matters for the recommendation: wiring an unrunnable script into the
build would have produced a build that still silently did nothing. Fixing the path is a
precondition for C, not a nicety.

That makes three independent silent failures in one small policy — a `.gitignore` line matching
nothing, a script matching nothing, and a `make clean` rule (`rm -rf autosummary/*.rst`, relative
to `docs/`, where no such directory exists) also matching nothing. Each was individually
invisible; together they left the intent stated in three places and enforced in none.

### 8.2 What changed

| file | change |
|---|---|
| `.gitignore:114` | `/docs/api/_autosummary` → `docs/api/**/autosummary/`, with a comment naming both audience trees |
| `docs/clean_api.py` | path resolved from `__file__`, so it works from any CWD; reports when there is nothing to delete; `pathlib`/`rglob`; Spanish comment removed per root `AGENTS.md` §4.1 |
| `docs/Makefile` | new `clean-api` target; `html` depends on it, so stale stubs are removed *before* each build; `clean` reuses it in place of the rule that matched nothing |
| `docs/AGENTS.md`, `docs/README.md` | describe the build doing this, instead of asking for a remembered step |

`html` cleans *before* building rather than after: autosummary regenerates the current surface on
every run, so pre-cleaning is what prevents a page for a deleted symbol from surviving. Cleaning
afterwards would delete the stubs the build just produced.

### 8.3 Verification

The two commands from §6 now behave as that section predicted:

```
$ git check-ignore -v docs/api/users/autosummary/
.gitignore:114:docs/api/**/autosummary/	docs/api/users/autosummary/

$ git status --porcelain | grep autosummary || echo "clean"
clean
```

Beyond §6, the full loop was exercised:

- `python docs/clean_api.py` **from the repository root** removed the 36 stubs — the invocation
  that was a no-op before this change;
- `make -C docs clean-api` removed fixtures planted in *both* `api/users/` and `api/developers/`,
  confirming the depth problem from §2 is covered, and is idempotent on a second run;
- `make html` completed (`build succeeded`), regenerated all 36 stubs, and left
  `git status --short` reporting only the five intended source files.

### 8.4 Not touched

CI needed no change. `.github/workflows/sphinx_docs_to_gh_pages.yaml` delegates to
`uibcdf/action-sphinx-docs-to-gh-pages@main` and builds from a clean checkout, where no stale
stub can exist — the staleness this proposal addresses is a property of long-lived working
copies only. The review checklist at `docs/AGENTS.md:93` also stands as written: ignored files
cannot be staged by accident, which is the outcome it was asking reviewers to confirm.
