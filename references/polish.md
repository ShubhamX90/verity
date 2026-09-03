# Non-native English polish

A separate pass from `de-ai-slop.md` — different failure mode, different fix. De-AI-slop detection targets *already-grammatical* text that reads as AI-flavored (vague filler, inflated register, manufactured structure). This file targets genuine grammatical, idiomatic, and register errors a non-native English speaker is statistically likely to produce — articles, prepositions, tense-by-authorship, hyphen misuse — which have nothing to do with whether a passage sounds AI-written. Run them as independent passes; a sentence can need one, both, or neither. Adapted from `minhuw/claude-writer`'s `polish` skill, retargeted from that source's systems-venue framing (OSDI/NSDI/SOSP/SIGCOMM) to general ML/CS-conference register, and fitted to this skill's two-tier model — the rules below apply the same way regardless of which specific venue is active.

## When this applies

Any prose in the paper, drafted by any author — native and non-native English speakers alike produce some of these errors, though non-native speakers hit them more often. Nothing here is specific to identifying *who* wrote a passage; it's specific to a category of error, checked the same way regardless of source.

## Tier model — same split as everywhere else in this skill

**Scanning is Tier A.** Reading a passage and noting a grammar/register issue changes nothing and needs no approval.

**Rewriting is Tier B.** Every proposed fix is surfaced as `Before / After / Why`, grouped, and applied only after per-item approval — exactly the workflow in `prose-editing-policy.md`. A polish pass and a de-ai-slop pass over the same paragraph produce two independent batches of proposals; don't merge them into one undifferentiated list, since the "why" differs (grammatical correctness vs. AI-flavor removal) and you may want to accept one kind and reject the other.

**Before presenting a polish batch, run it through the self-certification check** in `self-certification.md`, same as any other Tier B batch — a rewrite aimed at fixing grammar can still accidentally change a claim (e.g. "fixing" a tense error by rephrasing a hedge into an assertion).

## Core rules

### Hyphen usage

Avoid a hyphen used to connect two independent clauses — that's a comma-splice-adjacent error, not a stylistic choice.

> *Before:* "The system is fast - it processes data quickly."
> *After:* "The system is fast, processing data quickly."
> *Why:* A hyphen (or an unspaced en-dash used this way) doesn't grammatically join two independent clauses in formal English; a comma with a participial phrase does.

**Exception:** compound adjectives are fine and unaffected by this rule — "state-of-the-art method," "well-known result," "off-the-shelf hardware."

This is a narrower, more specific rule than `de-ai-slop.md`'s em-dash guidance (which is about *rhetorical overuse* of em-dashes for dramatic pauses); this rule is about a *hyphen* used where the grammar calls for a comma or a period, a correctness issue rather than a style-overuse issue.

### Voice preference

Prefer active voice for directness and clarity in general prose — introduction, discussion, motivation, related work.

> *Before:* "The prototype was implemented by us over a period of three months."
> *After:* "We implemented the prototype over three months."
> *Why:* Active voice states who did what without an extra clause; here the actor (the authors) is exactly what a reader wants to know.

**This does not override `prose-editing-policy.md`'s passive-voice carve-out.** That file explicitly treats passive voice in methods/experiments sections as often correct and idiomatic ("the model is trained on...", "images are resized to...") and refuses to auto-rewrite it. This rule's "prefer active" applies to the sections named above — general narrative prose — not to methods/experiments passive constructions, which stay governed by `prose-editing-policy.md`'s more permissive stance. When in doubt: if the passive construction names a specific, standard experimental procedure and the actor is genuinely uninteresting ("the dataset is split 80/20"), leave it; if the passive construction is hiding who actually did something in a narrative sentence ("it was decided that..."), that's this rule's territory.

### Tense conventions

Present tense for the paper's own work; past tense for prior literature.

> *Before:* "We implemented a prototype that achieved 95% accuracy. Smith et al. propose a related technique."
> *After:* "We implement a prototype that achieves 95% accuracy. Smith et al. proposed a related technique."
> *Why:* The convention signals, at a glance and without re-reading citations, which claims are this paper's own (present tense, "what this artifact *is* and *does*") and which are prior work being described (past tense, "what happened when they did it"). Mixing the two forces a reader to work out attribution from context instead of grammar.

Note the overlap with `de-ai-slop.md`'s stance-and-claims guidance (also present in `prose-editing-policy.md`'s broader philosophy) — the two docs describe the same convention from different angles (register/grammar here, argumentative stance there); they agree, not conflict.

### Acronym handling

Define on first use, in the form `Full Term (ACRONYM)`; use the short form thereafter.

> *Before:* "NAT is widely used in network address translation deployments. Our method builds on NAT."
> *After:* "Network Address Translation (NAT) is widely used in production deployments. Our method builds on NAT."
> *Why:* A reader who hasn't seen the acronym before hits it as a wall; defining it once, at first appearance, costs nothing and removes the wall permanently.

**Mechanically checkable, unlike most of this file:** search the document for any acronym-looking token (a run of 2+ capital letters) and confirm its first occurrence in reading order is accompanied by the expanded form. This is a candidate for a future addition to `scripts/style_scan.py` if acronym-definition slips become a recurring issue in practice — not built in this pass, since the rest of this file's rules (hyphen-for-clauses, tense-by-authorship, active-voice-in-narrative-prose) don't reduce to a reliable regex the way this one sub-rule does, and a half-mechanized file is more confusing than a fully-manual one with an honest note about what could be automated later.

### Conciseness

Eliminate redundancy without sacrificing clarity or precision — with the active venue profile's page limit specifically in mind (`venue-profile.md`). This rule overlaps with `compression-toolkit.md`'s territory but isn't the same trigger: conciseness-as-grammar-hygiene (cutting a redundant phrase because it's redundant) applies during a normal polish pass; the compression toolkit is a separate, on-demand tool invoked specifically when the paper is over the page limit. Don't wait for a page-limit crisis to cut an obviously redundant phrase during a polish pass — but don't reach for the full 7-operation compression toolkit for a single-sentence fix either.

> *Before:* "In this work, we present and propose a new method that is novel and represents a new contribution to the field."
> *After:* "We propose a new method for this problem."
> *Why:* "present and propose," "novel," and "new contribution" are four ways of saying the same one thing.

## Grammatical correctness — read-through, not grep

Subject-verb agreement, article usage (a/an/the, or their omission — a common gap for speakers of article-less languages), and preposition choice ("different from" not "different than" or "different with"; "depend on" not "depend from") are real, common non-native-English errors, but none of them reduce reliably to a regex the way `de-ai-slop.md`'s Part 1a/1b lexical and structural tells do — catching them requires reading the sentence, not pattern-matching it. Apply this section by read-through, the same way `de-ai-slop.md`'s Part 1c/1d argument-level tells are applied: as a judgment pass, not a scanned one, with every fix still going through the standard Tier B `Before/After/Why` proposal.

## What this pass does not do

- It does not touch AI-flavored vocabulary or structure — that's `de-ai-slop.md`'s job, run as a separate pass.
- It does not rewrite technical content, restructure arguments, or make content-level judgment calls about what the paper should claim — same rewrite-safety-zones as every other prose pass (`prose-editing-policy.md`): math mode, verbatim/code/identifiers, cross-reference plumbing, and LaTeX comments are all off-limits here too.
- It does not replace a native-speaker or professional proofread before submission — this closes the most common and most mechanical gaps, not every possible English usage question.
