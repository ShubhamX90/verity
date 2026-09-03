# Compression toolkit

**On-demand only.** This toolkit runs when you say you're over a page limit or ask for it directly — never automatically as part of a normal editing pass. See `prose-editing-policy.md` for the (separate, default) mechanical scan and de-AI pass; this file is specifically for cutting length.

Every operation below produces Tier B proposals (`Before / After / Why`, per-item approval, applied only after you accept) — nothing here is auto-applied. Compression is a content-level operation by definition: it removes material, which changes what the paper says and how much space each idea gets.

## The 7 operations, applied in order

1. **Sentence shortening** — remove subordinate clauses, redundant qualifiers, throat-clearing. "Every word must earn its place."
2. **Paragraph merging** — when multiple paragraphs make the same point with different examples, merge into one paragraph using the strongest example. Multiple examples of the same point dilute rather than strengthen.
3. **Removal of generic adjectives** — "significant," "substantial," "impressive," "promising," "novel," "innovative" replaced with a specific number, a named mechanism, or deleted outright. Generic adjectives are space-consuming non-information.
4. **Removal of tutorial explanation** — delete paragraphs explaining concepts the target venue's audience already knows (general optimization theory, standard ML definitions, textbook background — what counts as "already known" varies by venue and subfield, so calibrate to who actually reads this venue). This is usually the single largest source of cuttable material. Exception: keep it if redefining the known concept is itself part of the paper's contribution.
5. **Conversion to claim-first sentences/headings** — "Experimental Results" → "System X outperforms all baselines by 2–4×." Lead with the claim, not the section label.
6. **Evaluation compression via takeaways** — replace several paragraphs of per-condition results with grouped results plus one synthesizing takeaway paragraph.
7. **Figure/table promotion** — move dense numerical comparisons out of prose and into a table or figure; replace a prose list of numbers with a pointer + interpretation ("Table 3 shows X; our method outperforms...").

## Reduction target and calibration

| Reduction | What it signals |
|---|---|
| 10–20% | Draft was already close to final form — light polish, not real compression. |
| **30–50%** | **Normal.** You now know what matters vs. what was interesting to write about. |
| 50–65% | Crisis compression — the framing changed fundamentally, not just the wording. |
| >65% | Likely needs a structural rewrite, not compression — flag this rather than mechanically pushing through it. |

**Do not pad to fill the page limit.** A short paper with appropriate content is better than a padded one that happens to reach the page limit — this matches your own stated editing habit (cut what doesn't earn its place, move the rest to the appendix rather than deleting outright — see the next section).

## Cut vs. move to appendix

Per your own stated working method: **non-essential content moves to the appendix rather than being deleted outright**, where the compression operations above would otherwise delete it. This applies most naturally to operation 4 (tutorial explanation) and parts of operation 6 (detailed per-condition results that don't fit the main-text narrative but are worth keeping for a thorough reader) — propose "move to appendix" as an explicit alternative alongside "delete" wherever it's plausible, not just "delete" as the only option in the `Before/After/Why` block.

## Workflow

1. You say you're over the limit (or ask directly) — this is the trigger, never inferred automatically from section length.
2. Run the 7 operations in order against the section(s) you specify. Report character/word count before and after for each section.
3. Before presenting, run the full batch through the fresh-context check in `self-certification.md` — every proposed cut is a claim-preservation risk by nature (that's what compression *is*), so this step is never skipped here.
4. Surface every proposed cut as a `Before / After / Why` item, each with its self-certification result — including whether it's proposed as a deletion or an appendix move — grouped by severity/impact, most-impactful first.
5. Apply only the accepted set, in one batch.
6. Re-run `scripts/style_scan.py` afterward — compression edits are exactly the kind of rewrite that can accidentally reintroduce a flagged word or break a cross-reference.
