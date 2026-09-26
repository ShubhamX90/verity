# Mock review

Two distinct, complementary modes — correcting the Phase 1 audit brief's initial assumption that these were one skill under two names. Both are **Tier A**: each produces a new standalone report file and never touches the paper itself.

## Mode 1 — Formal mock review (per-venue schema)

Simulates a real reviewer for the active venue. Use when you want a realistic sense of how the paper would score, not writing advice. Distinct per-venue schemas exist for NeurIPS, ICML, CVPR, ACL, AAAI, ICCV, and ICLR, plus a generic fallback schema for any other venue — use whichever matches the active venue profile (`venue-profile.md`).

**Verification status, honestly stated**: only the **ICLR** schema below has actually been checked against a real, populated venue profile (`venues/iclr2027.md`) built the way `venue-profile.md` requires — fetched from live official pages, not asserted from memory. The other six schemas were carried over from source material during this skill's construction and have **not** been independently re-verified against each venue's own live review-form documentation. Before actually using one of those six for a real review, verify it the same way `venue-profile.md` requires for any other venue-specific fact — check the venue's own reviewer guidelines page — rather than trusting it as-is just because it's written down here. This file should be updated to record a schema as verified once that's actually been done for it, the same way `venues/iclr2027.md` records its own verification date.

**ICLR schema** (verified):
- Summary
- Strengths
- Weaknesses
- Questions
- Minor Issues
- Soundness (1–5)
- Presentation Quality (1–5)
- Originality (1–5)
- Significance (1–5)
- Overall Recommendation (Accept / Borderline / Reject)
- Confidence (1–5)

**Other venues' schemas (not yet independently re-verified — check before relying on these for a real review)**: NeurIPS uses a 1–10 overall score; ACL uses Soundness/Presentation/Originality/Significance on a 1–5 scale with a separate Overall 1–5; ICML, CVPR, AAAI, and ICCV each have their own fields and scales. Use whichever matches the active venue, not the ICLR one by default — but verify it first if it hasn't been checked yet. For a venue with no dedicated schema at all, use the generic fallback: Summary / Strengths / Weaknesses / Questions / Overall Recommendation / Confidence.

**Severity/tone**: adjustable — lenient (lead with strengths, more benefit of the doubt), standard (balanced), strict (lead with weaknesses, demand explicit evidence, no benefit of the doubt on ambiguous points). This is a prompt-level tone instruction, not a scoring formula — it shifts framing and the score band the review lands in, not a coded weight.

**Bonus**: also runs a missing-related-work search, producing a table (Paper Title / Key Contribution / Relevance / Should Be Cited In Section) — useful independent of the review itself.

## Mode 2 — Constructive advisor pass ("paper-polishing" territory)

Different framing: not a reviewer deciding accept/reject, but an advisor helping you fix the paper before it's reviewed. Analyzes correctness (equations, proofs, notation), motivation, methodology gaps, presentation quality, visualization/figure improvements, and missing citations.

**Output**: overall assessment, strengths, critical/major issues, section-by-section comments, and a **prioritized revision checklist**:

```markdown
## Revision Checklist
- [ ] **Priority 1 (Critical):** <action item with specific location>
- [ ] **Priority N (Major):** <action item with specific location>
- [ ] **Priority N (Minor):** <action item with specific location>
```
(ordered strictly critical → major → minor)

This is the mode to reach for when you want "what should I fix, in what order," not "would this get accepted."

## Common, avoidable rejection reasons — check both modes against this list

A checklist of specific, well-documented ways a paper gets rejected for reasons that have nothing to do with the underlying idea's merit. Mode 1 should reflect these in its Weaknesses section when applicable; Mode 2 should surface any hit as a Critical or Major item in the revision checklist, not bury it among minor wording notes.

- **Formatting or styling problems, or a paper that's simply hard to read.** The mechanical side of this is `pre-submission-checklist.md`'s job, but a reviewer notices readability problems `chktex` doesn't catch too — see `writing-craft.md`'s Part 2 review pass.
- **Highly relevant or very recent work not cited or compared against.** `find_uncited_claims.py` (`citation-verification.md`) flags candidate uncited claims; a mock review should separately ask whether the related-work section's clusters (`writing-craft.md`) are missing an obviously relevant recent paper, which is a literature-coverage question a citation scanner can't answer on its own.
- **Hallucinated or malformed references** — see `reference-audit.md`. A single fabricated reference is disqualifying at most venues regardless of how strong the rest of the paper is.
- **Novelty not stated clearly and consistently throughout the paper**, not just once in the introduction and then never reinforced.
- **Experiments not rigorous enough**: too few datasets, too few models, no ablation study isolating each component's individual contribution, or too few baselines. If the paper claims a system with several components, check specifically whether an ablation exists for each one — a paper that claims four components and ablates none of them individually hasn't actually shown which parts matter.
- **No real-world dataset** — evaluating only on synthetic or self-generated data, with nothing evaluated against a real-world source, is a specific and common weakness worth flagging by name rather than folding into a generic "evaluation could be broader."
- **Missing real-world motivation** — no stated practical use case, relevance, or utility for the problem the paper defines, beyond "this is an interesting benchmark."
- **Claims inconsistent across sections.** The single most mechanically checkable item on this list: does the abstract's headline number match the results section's actual number? A mismatch (abstract says 10%, results table says 8%) is a correctness problem, not a style one, and should be flagged as such regardless of which section is "wrong."
- **A stated claim or research question that the experiments don't actually evaluate.** Check every research question named in the introduction (see `writing-craft.md`'s results-by-RQ structure) against whether the results section actually contains an experiment answering it.
- **An LLM used as a judge or evaluator without first establishing its reliability.** This needs a human evaluation alongside it, with at least two human annotators, and the inter-annotator agreement reported both between the humans and between the humans and the LLM judge. A paper that reports only an LLM-judge score, with no human numbers to calibrate it against, should be flagged for this specifically, not just noted as "evaluation could be stronger."

## When to use which

- Want a realistic accept/reject read and reviewer-style scores → Mode 1.
- Want a prioritized action list to work through before anyone else sees it → Mode 2.
- Both are safe to run repeatedly and in either order — neither modifies the paper, and running one doesn't invalidate the other.

## Not built here: rebuttal support

See `rebuttal.md` — deliberately a stub for now, this file only covers pre-submission/pre-review mock feedback.
