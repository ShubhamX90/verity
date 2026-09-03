# Prose editing policy

Governs every workflow that touches the paper's actual wording: the mechanical style scan, the de-AI vocabulary pass, and (separately, on-demand only) the compression toolkit. This file is the prose-specific expansion of the two-tier autonomy model in `SKILL.md` — read that first if you haven't.

## Default posture: leave it alone

**If a passage already reads naturally — varied rhythm, no buzzwords, clean logic — leave it untouched.** Editing for the sake of editing degrades text. This is the governing philosophy for every prose pass this skill runs, full stop. There is no mandatory per-edit audit gate and no "always run the full checklist" requirement — that was considered in Phase 1 and deliberately rejected in favor of this threshold-based approach.

## Scanning is always Tier A. Rewriting is always Tier B.

This is the one subtlety worth restating precisely, because it's what lets "proactively flag issues" and "never auto-rewrite content" coexist without contradiction:

- **Running `scripts/style_scan.py` and showing you the list of hits is Tier A.** It's read-only. It changes nothing. Run it whenever it's useful, without asking first.
- **Acting on any hit that changes the wording is Tier B.** Every proposed rewrite — however small — is surfaced individually and waits for your approval before being applied, using this format (from `claude-latex-paper-skill`'s per-item-verdict pattern):

```
<file>:<line>  [Critical | Major | Minor]
Before: <current text>
After:  <proposed text>
Why:    <the rule or reason>
```

Findings are grouped, most-severe first, and only the items you accept are applied — in one batch, then re-scanned to confirm the fix didn't introduce a new issue (a rewritten sentence can reintroduce a banned word; this happens often enough to be worth the extra pass).

## What the mechanical scan flags (all soft — suggestions, not hard bans)

**See `de-ai-slop.md` for the full detection-and-prevention reference** — lexical tells, structural/rhetorical tells, argument-level tells, and detection heuristics, each with real before/after examples, plus the standing drafting-time constraints for *new* text (which aren't tiered at all — see that file's Part 2). This section stays a short pointer rather than duplicating that content.

One deliberate change from `paper-writing-skill`'s original grep-based gate, which `de-ai-slop.md`'s detection half is adapted from: **no rule in this list is a hard ban.** Every hit is a flagged suggestion for you to accept, reject, or ignore — including passive voice, which is flagged like anything else below rather than banned.

- Em-dashes (more than one per paragraph)
- AI-overused vocabulary and structural tells from `de-ai-slop.md` Parts 1a/1b
- Throat-clearing openers ("It is worth noting that," "First and foremost," "Moreover," "Furthermore" as sentence-openers)
- Wordiness ("in order to" → "to," "the fact that," "due to the fact that")
- Weak qualifiers ("rather," "very," "quite," "somewhat," "fairly")
- **Passive voice** — flagged, never auto-rewritten. ML methods and experiments sections routinely and correctly use passive voice ("the model is trained on...", "images are resized to..."); a zero-tolerance ban (as `paper-writing-skill` originally specifies it) fights standard field register and was explicitly dropped in Phase 2. Passive-voice hits appear in the scan output like any other Minor-severity item, and most will be correctly rejected rather than accepted.
- Term drift — the same concept named two different ways across sections.

`de-ai-slop.md`'s argument-level tells (1c) and detection heuristics (1d) are **not** part of this scanned list — they need a read-through and judgment, not a grep, and are documented separately for that reason. Apply them by hand when reviewing a section.

## What the scan treats as a hard failure (not a suggestion — these are objectively broken, not judgment calls)

Adapted from `claude-latex-paper-skill`'s `verify_paper.py`. These aren't content decisions, so they don't go through the propose-and-wait flow — they're just wrong and get flagged for immediate fixing:

- Leaked non-English characters (if the working conversation ever runs in a language other than English — the analogue of translation source-leakage).
- Unresolved `[CLAIM NEEDS EVIDENCE]`, `PLACEHOLDER_`, or `TODO` markers left in what's presented as finished text.
- `\cite{key}` with no matching `.bib` entry.

## Composing new text: see `de-ai-slop.md` Part 2

Everything above governs *editing existing prose*. Drafting brand-new sentences for the paper is governed by a separate, non-tiered standing constraint — concrete over generic, result before context, precise verbs, no manufactured triads, no restating what's said elsewhere — laid out in full in `de-ai-slop.md`'s Part 2. It applies the moment text is composed, not after a scan.

## Rewrite safety zones — never touched, character-for-character, by any prose pass

A style or de-AI pass edits prose only. These are off-limits regardless of how natural or awkward they look — a "cleaner" rewrite that changes any of these is a bug, not an improvement:

- Math mode: `$...$`, `\[...\]`, `equation`/`align` bodies.
- `verbatim`, `\texttt{}`, code, paths, filenames, identifiers.
- Cross-reference plumbing: `\label`, `\ref`, `\cref`, `\cite` keys, and numbers/units inside `siunitx` (`\SI`, `\num`, `S` columns).
- LaTeX comments (`% ...`) — author notes, not reader-facing prose.

## The length rule

A de-AI rewrite **subtracts, it does not add**: the reworded passage should be no longer than the original. If a proposed fix needs more words, it's not polish — it's a content change (a claim, evidence, or a boundary condition), and should be flagged as such rather than folded into a vocabulary swap.

## The compression toolkit is separate and on-demand only

See `compression-toolkit.md`. It is **not** part of the default prose-editing pass described above — it only runs when you say you're over a page limit or ask for it directly. Running the mechanical scan does not trigger compression, and finishing a compression pass doesn't mean the mechanical scan should now run as a matter of course either. These are two independent tools, invoked separately, for two different problems (AI-slop / naturalness vs. length).
