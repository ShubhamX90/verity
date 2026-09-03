# Self-certification check

Closes a real gap surfaced during an independent audit of this skill: every other check either runs automatically (Tier A) or waits for your approval (Tier B) — but nothing checked whether the *proposal itself* was trustworthy before it reached you. A single pass that drafts an edit and then judges its own edit is exactly the failure mode one of this skill's source materials (SNL-UCSB's `paper-writing-skill`) named directly in its own design notes: "the failure mode was not too few rules but self-certification... self-audit rationalizes its own phrasing." This is a deliberately lighter fix than that source's full red-team architecture (multiple gates, a 31-item semantic rubric, a resumable loop) — more than this skill needs — but keeps the one piece of it that matters most: an edit shouldn't be checked by the same context that produced it.

## The rule

**Before any Tier B batch is presented for approval, it goes through one fresh-context check first.** "Fresh-context" means the check sees only the proposed `Before`/`After` pairs and the paper text immediately around them — not the reasoning, the source material, or the conversation that produced the edit. Its only question: does `After` still say what the paper actually claims, or did something get lost, changed, or overstated in the rewrite?

## Mechanism

Prefer a fresh subagent (the `Agent` tool available to whatever is driving this skill) given only:
- The paper's current text at and immediately around each proposed edit location — enough surrounding context to judge the claim, not the whole paper.
- Each proposed `Before → After` pair.
- One question: "Does `After` preserve what `Before` claims — the same facts, the same qualifications/boundaries, the same evidence pointers (numbers, table/figure references, citations)? Flag any change in a claim, not just a change in wording."

Nothing else — no "why this edit was proposed," no access to the conversation that generated it. A subagent with no stake in having produced the edit has no reason to rationalize it.

**Fallback**, if spawning a fresh subagent isn't practical in a given moment: a deliberate context reset within the same session — re-read only the `Before`/`After` pairs as if encountering them for the first time, not by re-reading the reasoning that led to them, before presenting the batch. This fallback is weaker (it's still the same context, just with a forced framing change) and should be used only when a fresh subagent genuinely isn't available, not as a default shortcut taken for convenience.

## What it checks — and what it doesn't

**Checks:** claim preservation only. Did a boundary condition quietly disappear ("on this benchmark" dropped)? Did a qualified claim become unqualified ("often improves" → "improves")? Did a number, citation key, or figure/table reference get altered or dropped in the rewrite? Did the compression toolkit's "cut vs. move to appendix" distinction (`compression-toolkit.md`) collapse into a silent deletion?

**Does not check:** whether the rewrite is good style (that's what produced the proposal — re-litigating style isn't this check's job), whether the *original* claim was itself correct (a different, earlier problem — this check assumes `Before` was fine and asks only whether `After` still says the same thing), or anything the mechanical scanners already cover (`style_scan.py`, `check_citations.py`, etc.). This check exists specifically for the judgment call those scripts can't make.

## Output format

A one-line addition to the same `Before/After/Why` block already shown to you — not a separate report to cross-reference:

```
<file>:<line>  [Critical | Major | Minor]
Before: <current text>
After:  <proposed text>
Why:    <the rule or reason for the original proposal>
Self-check: OK — claim preserved
```

or

```
Self-check: FLAGGED — <what changed that shouldn't have>
```

A flagged item still goes to you for the final call — this check has no unilateral veto power. It exists so you're seeing an honest flag rather than a rewrite that quietly drifted from what it claims to be doing.

## Where this is wired in

Every Tier B workflow in this skill that produces a rewrite batch runs through this check before presentation:

- `compression-toolkit.md` — every compression operation's proposed cuts.
- `de-ai-slop.md` Part 1 — every proposed de-AI-slop rewrite.
- `polish.md` — every proposed grammar/register rewrite.
- `citation-verification.md` — the one Tier B step there (inserting a *new* `\cite{}` into the paper text): the self-check asks whether the citation is attached to the claim it actually supports, not a nearby-but-different one.

**Not applied to Tier A actions** — those don't change what the paper claims by definition, so there's nothing for a self-certification check to catch that the tier system doesn't already prevent by construction.
