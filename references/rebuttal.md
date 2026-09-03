# Rebuttal — stub only

**Not built in this pass, on purpose.** Per Phase 2 (resolution #3), this only matters post-review, and there's no reason to build and maintain a workflow months before it's needed. This file exists so the decision that *was* made isn't lost or re-litigated when the time comes — read it, then build the actual `rebuttal.md` workflow + script at that point, not now.

## The decision, recorded

When rebuttal support is actually built:

- **Default data model**: issue-atomization (from `academic-research-plugin`'s `rebuttal` skill) over a flat Comment/Response/Modification triple (from `response-letter-bootstrap-skill`) — per-issue `issue_type` (novelty / empirical_support / baseline_comparison / theorem_rigor / assumptions / complexity / clarity / reproducibility / practical_significance / other), `severity`, `reviewer_stance`, `needs_experiment` flag, `status`. The richer triage is worth it even in scaffold-only mode — chosen over the simpler model specifically because it helps you see at a glance which reviewer points are quick clarifications versus which need new experiments before you can respond at all.

- **Non-negotiable regardless of data model**: **the skill only ever produces structured scaffolding — it never auto-drafts persuasive rebuttal prose.** This rules out porting `academic-research-plugin`'s response-mode auto-drafting behavior (the `[INSERT: ...]`-placeholder prose generation), even though its issue-atomization structure is the one being adopted. Combine that structure with `response-letter-bootstrap-skill`'s discipline of always leaving the actual response body as an empty `%% TODO` / placeholder for you to write — take the better data model, keep the more conservative drafting stance.

- **Not yet decided, flagged for a future go/no-go rather than decided now**: whether rebuttals live inside the paper's existing repo (a subfolder or branch) or as a separate auto-created private GitHub repo (as `response-letter-bootstrap-skill` does by default, via `gh repo create`). Given the paper already lives in one specific shared repo, a subfolder/branch is the more natural fit, but this wasn't actually decided — don't assume it when building this out.

- **Two mechanisms from `response-letter-bootstrap-skill` to carry forward regardless of which data model wins** (added per an independent audit finding — the decision above named the data model but dropped these two, and the point of this stub is to record what shouldn't need re-deciding later):
  - **Count-check before writing.** Count the numbered reviewer comments in the raw source, count the parsed issue entries, and abort with a clear error on any mismatch — the source skill calls this "the most important failure mode" it guards against (silently dropping a reviewer's point). This applies to the issue-atomization model exactly as it did to the flat triple model; the data model changed, the need to never silently drop an issue didn't.
  - **Verbatim-transcription discipline.** Never paraphrase, reorder, split, or summarize a reviewer's actual comment text when capturing it into whichever structure is used — transcribe it exactly (stripping only markup artifacts like pasted HTML tags, not wording). The atomization (type/severity/stance/etc.) is metadata layered on top of the verbatim quote, not a replacement for it.

## What triggers building this for real

The first round of real reviews landing on some paper this skill is used for (not before) — this file is a placeholder specifically because building and testing a rebuttal workflow now, before there are real reviews to test it against, would mean shipping something unverified.
