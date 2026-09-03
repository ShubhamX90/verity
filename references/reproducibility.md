# Reproducibility audit

Adapted from `reproducibility-checklist` (originally a generic ML-pipeline checklist, not paper-writing-specific). Entirely **Tier A** — read-only auditing, feeds into whatever reproducibility statement the active venue profile calls for (many venues have one; check `venue-profile.md`) rather than writing it for you.

## What it checks

`scripts/reproducibility_audit.py` walks six categories:

1. **Random seeds** — every stochastic call (train/test split, model init, data augmentation, sampling) has a fixed seed; the seed value is documented somewhere findable.
2. **Library versions** — Python version and key library versions are captured (from a `requirements.txt`/`environment.yml`/`pyproject.toml`/lockfile, or a recorded `pip freeze`).
3. **Data version** — a SHA-256 hash of the dataset file(s), source path or query, and row/column counts are recorded somewhere.
4. **Code version** — the git commit SHA is recorded, and the working tree was clean (no uncommitted changes) at the time results were produced.
5. **Environment** — a requirements/lock file exists; hardware (CPU/GPU, memory) and compute cost (wall time, GPU-hours) are documented.
6. **Results determinism** — same code + data + seed reproduces the same metrics within floating-point tolerance; any known non-determinism (GPU ops, multi-threaded data loading) is documented rather than silently present.

## Scoring

**Corrected per an independent audit finding** — this section previously described the *original source's* 17-point/4-tier rubric, which drifted from what actually got built during this skill's own port and was never reconciled. What follows now matches `scripts/reproducibility_audit.py` as shipped, not the source it was adapted from.

Five of the six categories are automatically scored, capped per category: Random seeds (0-3), Library versions (0-2), Data version (0-2), Code version (0-2), Environment (0-1) — **10 points total.** Category 6 (Results determinism) is deliberately excluded from the numeric score — it needs an actual re-run to verify, which the script can't do on your behalf — and is always reported separately as a manual-check reminder.

| Score (of 10 automatable points) | Rating |
|---|---|
| ≥ 85% | Good — most of what's automatically checkable looks solid |
| 50–84% | Fair — real gaps, worth closing before relying on this for the Reproducibility Statement |
| < 50% | Poor — significant gaps |

There is no "Excellent" tier — a perfect automatable score still leaves category 6 (determinism) unverified, which is exactly why it's excluded from the number rather than assumed. The script prints both the per-category breakdown and this overall rating; read the breakdown, not just the final line, since a single weak category (e.g. no seeds at all) can be worth closing even inside an overall "Good" score.

## Pointing this at the real repo

`scripts/reproducibility_audit.py --requirements <path>` needs the real project's actual `requirements.txt`/`environment.yml`/`pyproject.toml` passed explicitly — there is no built-in default dependency list to fall back on (a hardcoded generic list was considered and deliberately not shipped, since checking for libraries the paper may not even use would be worse than an honest "not checked"). Without `--requirements`, the Library-versions and Environment categories score 0 with a note saying so, rather than silently guessing. Same principle as `figures-tables-diagrams.md`'s placeholder mapping: the mechanism is ready, it just needs the real repo's actual path the first time this runs against it.

## Feeding into the Reproducibility Statement

The active venue profile describes what its reproducibility statement (if it has one) should contain — typically a recommended, paragraph-long pointer to whatever in the paper/appendix/supplementary materials supports reproducibility. Run this audit before drafting that paragraph — it's a much better source than trying to recall from memory what was and wasn't pinned down. A score in the "Fair" or "Poor" range is a signal to close specific gaps (per the "Common Reproducibility Failures" table below) before writing the statement, not a signal to write an optimistic statement anyway.

## Common failures → fixes (from the source material, unchanged — these are generic and hold regardless of the specific repo)

| Failure | Cause | Fix |
|---|---|---|
| Different metrics on re-run | Missing seed in a data split or model init | Pass `random_state`/equivalent to every stochastic call |
| Can't reinstall the same environment | No pinned versions | `pip freeze > requirements.txt` (or equivalent) at experiment time |
| Data changed between runs | No data hash captured | Hash data files before training |
| Code changed since the experiment | No git SHA recorded | Record `git rev-parse HEAD` in the experiment log |
| GPU gives different results across runs | Non-deterministic CUDA ops | Document it, or enable deterministic-algorithm flags where the framework supports it |
