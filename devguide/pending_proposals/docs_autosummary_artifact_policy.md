# Proposal: make the autosummary artifact policy match what the build produces

**Status:** proposal (2026-08-15). Small and janitorial, but the current state is a rule that
silently does not apply, which is worse than no rule.
**Scope:** `.gitignore`, `docs/clean_api.py` wiring. No documentation content changes.

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
