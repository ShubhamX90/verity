# De-AI-slop: detection and prevention

Two distinct halves, governed by two different rules — read the header of each part before using either.

**Part 1 (Detection)** is for text that already exists — yours or a co-author's. It's Tier A to scan, Tier B to rewrite: `scripts/style_scan.py` surfaces candidates freely, but nothing gets rewritten without a `Before / After / Why` proposal and your approval, per `prose-editing-policy.md`. Before any de-AI-slop rewrite batch is presented, it runs through the fresh-context check in `self-certification.md` — a rewrite aimed at removing filler can just as easily remove a hedge or a boundary condition that looked like filler but wasn't.

**Part 2 (Prevention)** is not a tier at all. It's a standing constraint on how new sentences get phrased the moment they're drafted — it doesn't wait for a scan-then-approve cycle, because there's no "old text" yet to scan. Composing a sentence that already avoids these patterns is cheaper than drafting slop and then flagging it.

Default posture, restated from `prose-editing-policy.md` because it governs everything below: **if a passage already reads naturally, leave it alone.** Every item in Part 1 is a candidate for your judgment, not a violation to be stamped out on sight — a scan that flags 40 things in a clean section is a badly-calibrated scan, not a thorough one.

---

## Part 1 — Detection (Tier A: scan and flag; Tier B: any actual rewrite)

Organized by tier of confidence, not as one flat list — (a) and (b) are close to mechanically detectable and are what `style_scan.py` actually greps for; (c) and (d) need a read-through and human/assistant judgment, and are documented here specifically so they don't get silently skipped just because they can't be grepped.

### 1a. Lexical tells

The word itself isn't always the problem — it's the word carrying no specific technical content in that sentence. The "keep if" column is what separates a real hit from a false positive; check it before flagging.

| Word / phrase | Why it's a tell | Keep if... |
|---|---|---|
| leverage (verb) | Corporate-speak stand-in for "use" | Never — always downgrade to "use"/"employ" |
| delve into | Filler for "examine" | Never carries technical content |
| pivotal / paramount | Vague importance-signaling | The paper actually argues *why* it's the single most important factor, not just asserts it |
| underscore | Filler for "show"/"emphasize" | Never |
| notably | Filler intensifier, also a throat-clearing sentence-opener (see 1b) | Rarely — usually deletable with no loss |
| robust | Legitimate technical term (robustness to noise, robust optimization) *or* filler intensifier | Keep when paired with a specific perturbation/condition ("robust to label noise"); cut when it's just "robust results" with nothing to be robust *to* |
| seamless(ly) / holistic(ally) | Vague-positive filler | Never carries technical content |
| cutting-edge / groundbreaking | Unearned superlative (see 1c) | Almost never in your own paper's self-description — a claim, not a description |
| paradigm / realm / landscape / "evolving landscape" | Inflated register for "approach"/"area"/"field" | Never |
| "paradigm shift" | Overclaims the paper's contribution size | Only if the paper is *actually* arguing a field-level reframing, and says so explicitly with evidence — not as a throwaway phrase in the intro |
| burgeoning / multifaceted / nuanced | Vague-positive filler | Multifaceted/nuanced sometimes legitimate for a genuinely multi-dimensional claim — check whether the dimensions are actually named nearby |
| unprecedented | Unearned superlative | Never in self-description (see 1c) |
| showcase | Filler for "show"/"demonstrate" | Never |
| intricate | Vague-positive filler for "complex" | Only if the complexity is specific and named nearby |
| synergy / synergistic | Corporate-speak, rarely has technical content in ML papers | Almost never |
| "unlock the potential (of)" | Marketing-register filler | Never |
| "pave the way (for/to)" | Vague future-promise filler | Never — state what specifically becomes possible, or cut |
| "shed light on" | Filler for "clarify"/"show" | Never |
| "plays a crucial/pivotal role" | Vague importance-signaling without a mechanism | Only if the *specific mechanism* of that role is stated in the same sentence, not just asserted |
| "a testament to" | Filler closing flourish | Never |
| novel / comprehensive / holistic (as filler) | Self-congratulatory descriptor with no content | Only when followed immediately by what's specifically novel/comprehensive — otherwise cut the adjective entirely and let the sentence stand on the claim alone |
| unsupported "significantly" | Statistical-sounding word used without a number | Keep only when a delta, percentage, or p-value appears in the same sentence or the next one — see 1c |

### 1b. Structural / rhetorical tells

These are patterns in how a sentence or paragraph is built, not individual words — some are directly greppable (`style_scan.py` catches the ones marked **[scanned]**), others need a read-through.

**The "it's not just X, it's Y" antithesis. [scanned]**
A rhetorical crutch that manufactures drama out of a claim that usually didn't need it — the two halves are rarely both true or both necessary.
> *Before:* "This isn't just a new architecture — it's a fundamentally different way of thinking about attention."
> *After:* "This architecture replaces the quadratic attention cost with a linear one."
> *Why:* The antithesis format asserts significance rather than stating what changed. The rewrite states the actual change and lets the reader judge its significance.

**Reflexive rule-of-three when the content isn't genuinely three parallel things.**
AI-generated prose defaults to triads (three examples, three properties, three contributions) even when the underlying content has two ideas or five, because three *sounds* complete. Check: are these three items actually parallel in kind and weight, or was a third item invented/padded to complete the pattern?
> *Before:* "Our method is efficient, scalable, and robust."
> *After:* "Our method trains in under 2 GPU-hours and scales linearly to 10M parameters." *(if "robust" wasn't actually backed by a specific robustness experiment, it shouldn't be in the list at all — this isn't a rewording fix, it's a claim-accuracy fix)*
> *Why:* A padded third item is a content problem wearing a style problem's clothes — flag it as "is this claim actually supported," not just "reword this list."

**Em-dash-driven dramatic pauses.**
One em-dash per paragraph, used for a genuine aside, is fine. A string of them used to create false suspense before a reveal is a tell.
> *Before:* "The results were clear — and surprising — our baseline actually won."
> *After:* "Our baseline outperformed all proposed methods, an unexpected result we discuss in Section 5."
> *Why:* The dash-pause construction performs surprise rather than stating the finding; the rewrite states it directly and points to where it's explained.

**Throat-clearing meta-announcements. [scanned, partial]**
Sentences that announce what a section is about to do, instead of doing it.
> *Before:* "This section provides an overview of the experimental setup used to evaluate our method."
> *After:* "We evaluate on three benchmarks: CIFAR-10, CIFAR-100, and TinyImageNet."
> *Why:* The announcement sentence carries zero information a reader can't infer from the section heading. Delete it and start with the content.

**Hedge-then-assert framing.**
A sentence that hedges ("it could be argued that," "some might suggest that") immediately before asserting the thing anyway, as a rhetorical softener rather than genuine uncertainty.
> *Before:* "While it could be argued that scale alone drives these gains, our ablation shows otherwise."
> *After:* "Our ablation shows the gains persist at fixed scale, isolating the architectural contribution."
> *Why:* The hedge doesn't represent real uncertainty — the sentence immediately un-hedges. State the finding directly.

### 1c. Argument-level tells

These need judgment, not a pattern match — flag them during a read-through, and treat every flag as a candidate for discussion, not an automatic fix. Several of these are content problems (does the paper actually support this claim?), not style problems (does this sentence sound natural?) — that distinction matters for which tier the eventual fix falls into.

- **Vague superlatives with no attached number.** "Significantly outperforms" with no stated delta is an empty claim — a reviewer's first question is "by how much." Flag any such sentence for either a number (if one exists in the results) or a downgrade to a claim the paper can actually support.
  > *Before:* "Our method significantly outperforms all baselines."
  > *After:* "Our method outperforms the strongest baseline by 4.2 points (Table 2)."

- **Unearned claims** ("groundbreaking," "unprecedented," "revolutionary" applied to your own work). These are judgments other people make about a paper, not claims a paper makes about itself. If the paper is describing its own contribution this way, it's asserting a reception it hasn't earned yet.
  > *Before:* "We present a groundbreaking approach to few-shot learning."
  > *After:* "We present an approach to few-shot learning that requires no fine-tuning."

- **A conclusion that just re-paraphrases the abstract** instead of adding anything a reader hasn't already seen. Check: does the conclusion state a takeaway, a limitation, or a direction for follow-up work that isn't already in the abstract — or is it functionally the same three sentences reworded?

- **Related-work paragraphs that list rather than synthesize** — "X did Y. Z did W. Q did V." with no comparison or positioning between them is a bibliography with sentences around it, not related work. Check: does the paragraph ever say how these approaches relate to each other or to this paper's method, or does it only ever relate each one individually back to a generic "however, none of these..." closer?
  > *Before:* "Smith et al. proposed X. Jones et al. proposed Y. Lee et al. proposed Z. However, none of these approaches consider Q."
  > *After:* "Prior work on this problem splits into two families: X-based methods (Smith et al.), which assume access to labeled validation data, and Y-based methods (Jones et al.; Lee et al.), which instead rely on a fixed threshold. Both families require Q, which is often unavailable in practice — the gap this paper addresses."
  > *Why:* The rewrite groups the prior work by what actually distinguishes it and states the shared gap once, instead of restating the same generic complaint after each citation.

- **Generic rather than specific motivation.** A motivation paragraph that would be equally at home in almost any paper in the subfield ("As deep learning models grow larger, efficiency becomes increasingly important") isn't wrong, but it's not doing any work either — see the portability heuristic in 1d.

### 1d. Detection heuristics (apply by judgment, not by grep)

Three quick tests worth running mentally on a paragraph that feels slightly off, even when nothing matches a specific pattern above:

1. **The delete-the-adjective test.** Remove every adjective/adverb from the sentence. Does it still make its point? If "our novel, comprehensive, robust approach significantly improves performance" reduces to "our approach improves performance" and loses nothing but word count, the adjectives were never doing work.

2. **The portability test.** Could this exact sentence be pasted into an unrelated paper in the same subfield without editing a single word? If yes, it's boilerplate — it isn't saying anything specific to *this* paper, *this* method, or *this* result. A sentence that only makes sense in this paper is a sentence with real content.

3. **The load-bearing-opener test.** Does the paragraph's first sentence state a claim the rest of the paragraph defends, or is it a throat-clearing lead-in (see 1b) that could be deleted with the second sentence promoted to first, unchanged? Most paragraphs pass this test worse than expected on a first draft — it's one of the highest-value single checks in this whole document.

---

## Part 2 — Prevention: a standing constraint on drafting new text

This section is not a scan-then-approve workflow. It applies the moment new sentences are being composed for the paper — before there's any "old text" for Part 1 to scan. Treat it the way `prose-editing-policy.md`'s rewrite-safety-zones are treated: a constraint that's simply true throughout drafting, not a checklist run afterward.

**Concrete and specific over generic.** Before writing a claim, ask what number, mechanism, or named object could replace a vague placeholder. "Our method improves efficiency" is a draft-zero placeholder, not a finished sentence — replace it with the actual number, or don't write the sentence yet.
> Draft instinct to avoid: "This leads to substantial improvements in training speed."
> Compose instead: "This reduces training time from 14 to 6 GPU-hours."

**State the result before contextualizing it.** Lead with the finding, then the setup — not the reverse. A reader skimming under time pressure (which describes most conference reviewers at most venues) sees the claim first and decides whether the context is worth reading.
> Draft instinct to avoid: "In order to evaluate whether our approach generalizes across domains, we conducted experiments on five benchmark datasets spanning vision and language, and found that..."
> Compose instead: "Our approach generalizes across five benchmarks spanning vision and language, with no domain-specific tuning."

**Use the precise verb the claim actually needs, not a stock verb.** AI-drafted prose defaults to a small set of safe verbs ("leverages," "utilizes," "showcases," "demonstrates") regardless of what's actually happening. Match the verb to the actual action.
> Draft instinct to avoid: "Our model leverages attention to demonstrate improved performance."
> Compose instead: "Attention lets the model weight distant tokens directly, avoiding the recency bias of recurrent baselines."

**Don't manufacture a triad or parallel structure the content doesn't actually have.** If there are two contributions, state two. If there are five related-work threads, group them into however many genuinely distinct clusters exist — don't force a "three main approaches" framing because it reads more confidently than "two, plus one outlier worth mentioning." (See 1b's rule-of-three tell — this is the drafting-time version of the same discipline.)

**Never pad length by restating something already said elsewhere in different words.** If a sentence's only function is to remind the reader of a point made two paragraphs ago, either it belongs at that earlier point instead (structural issue) or it isn't needed at all. This is the drafting-time mirror of `compression-toolkit.md`'s operation 2 (paragraph merging) — better to never write the redundant version than to draft it and cut it later.

---

## How this maps to tooling

- **1a (lexical)** and the greppable half of **1b (structural)** are what `scripts/style_scan.py` actually implements — every hit it reports is a candidate, never an automatic fix, per the tier model.
- **1c (argument-level)** and **1d (heuristics)** are not implemented as patterns anywhere, deliberately — they need a read-through and judgment about what the paper is actually claiming and supporting, which a regex cannot assess. Apply them by hand (or have the assistant apply them while reading a section, surfacing findings the same way as any Tier B item) rather than expecting a scan to catch them.
- **Part 2** has no script at all. It's referenced whenever the assistant is composing new sentences for the paper — a drafting discipline, not a gate that runs after the fact.
