# De-AI-slop: detection and prevention

Two distinct halves, governed by two different rules — read the header of each part before using either.

**Part 1 (Detection)** is for text that already exists — yours or a co-author's. It's Tier A to scan, Tier B to rewrite: `scripts/style_scan.py` surfaces candidates freely, but nothing gets rewritten without a `Before / After / Why` proposal and your approval, per `prose-editing-policy.md`. Before any de-AI-slop rewrite batch is presented, it runs through the fresh-context check in `self-certification.md` — a rewrite aimed at removing filler can just as easily remove a hedge or a boundary condition that looked like filler but wasn't.

**Part 2 (Prevention)** is not a tier at all. It's a standing constraint on how new sentences get phrased the moment they're drafted — it doesn't wait for a scan-then-approve cycle, because there's no "old text" yet to scan. Composing a sentence that already avoids these patterns is cheaper than drafting slop and then flagging it.

Default posture, restated from `prose-editing-policy.md` because it governs everything below: **if a passage already reads naturally, leave it alone.** Every item in Part 1 is a candidate for your judgment, not a violation to be stamped out on sight — a scan that flags 40 things in a clean section is a badly-calibrated scan, not a thorough one.

**This list decays — treat it as a snapshot, not a permanent standard.** The clearest finding from the research behind this document (Geng & Trotta, arXiv:2502.09606) tracked word-frequency shifts in arXiv abstracts month-by-month and found that "delve," "intricate," "realm," and "showcasing" all *peaked and then declined* starting March–April 2024, coinciding with the words going viral as a public joke — authors and models both seem to have self-corrected once the tell became common knowledge. Meanwhile "significant" and "additionally" kept climbing over the same period, apparently because nobody was calling them out. The practical implication: a static word list systematically **under-catches whatever's currently well-known** (writers already avoid it) and **under-catches whatever's currently obscure** (nobody's built a check for it yet) — it's most useful for the words in between. Don't treat a clean scan as proof of clean prose; a sentence stuffed with "significant," "additionally," and "furthermore" is exactly as AI-flavored as one stuffed with "delve" and "boundaries," and the former will sail through a lot of naive checks precisely because those words feel too ordinary to suspect. See [Research basis and version awareness](#research-basis-and-version-awareness) at the end of this file for the full citation trail and what's confirmed vs. not.

---

## Part 1 — Detection (Tier A: scan and flag; Tier B: any actual rewrite)

Organized by tier of confidence, not as one flat list — (a) and (b) are close to mechanically detectable and are what `style_scan.py` actually greps for; (c) and (d) need a read-through and human/assistant judgment, and are documented here specifically so they don't get silently skipped just because they can't be grepped.

### 1a. Lexical tells

The word itself isn't always the problem — it's the word carrying no specific technical content in that sentence. The "keep if" column is what separates a real hit from a false positive; check it before flagging.

**These aren't folk wisdom — they're measured.** Multiple peer-reviewed studies tracked exact word-frequency shifts in scientific writing before and after ChatGPT's release, giving real fold-increases rather than impressions: Kobak et al. (*Science Advances* 2025, 15.1M PubMed abstracts) found "delves" appearing 28× more often than a pre-LLM baseline predicted, "underscores" 13.8×, "showcasing" 10.7×; Juzek & Ward (COLING 2025, 5.2M PubMed abstracts) independently found "delves" up 1,375–6,697% depending on the exact form; Liang et al. (*Nature Human Behaviour* 2025, 1.1M papers/preprints) estimated 22.5% of 2024 CS abstracts and 19.5% of CS introductions show detectable LLM-modification. The same word list shows up independently across every one of these studies, which is what makes it trustworthy — not any single source's say-so.

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
| unsupported "significantly" / bare "significant" | Statistical-sounding word used without a number — one of the two words that *kept climbing* after the 2024 public callout of "delve" et al. (Geng & Trotta), so it's under-suspected precisely because it sounds ordinary | Keep only when a delta, percentage, or p-value appears in the same sentence or the next one — see 1c |
| additionally / furthermore (mid-sentence, not just as a sentence-opener) | The other word that kept climbing while "delve" declined — see the note above the table | Rare; usually deletable, letting the prior sentence's logic carry the connection |
| elucidate / encompass / streamline / unveil | Filler substitutes for "explain"/"include or cover"/"simplify"/"reveal" — confirmed excess-frequency words in Kobak et al. and Juzek & Ward | Never carries technical content beyond the plain verb |
| transformative | Unearned-impact superlative, same family as "groundbreaking" (see 1c) | Only if the specific transformation is named in the same sentence, not asserted alone |
| garnered | Filler for "received"/"got" (as in "garnered attention") | Never |
| boast(s) (non-literal, "the model boasts 95% accuracy") | Filler for "has"/"achieves" | Never — always downgrade to the plain verb |
| commendable | Vague-positive filler, confirmed at a 9.8× frequency increase specifically in post-2022 peer-review text (Kobak et al.–adjacent ICLR-review analysis) — a tell to watch for especially in mock-review output (`mock-review.md`), not just paper prose | Almost never in a paper's own self-description; in reviewer-voice output, always replace with the specific thing being commended |
| meticulous(ly) | Vague-positive filler for "careful"/"thorough" | Only if paired with the specific procedure that was careful (e.g. "meticulous hyperparameter logging" naming what was logged) |
| advancements (plural, as in "recent advancements") | Filler for "progress"/"work" — an independently confirmed excess-frequency word (Kobak et al.) | Keep if naming the specific advance; cut if it's just scene-setting |

### 1b. Structural / rhetorical tells

These are patterns in how a sentence or paragraph is built, not individual words — some are directly greppable (`style_scan.py` catches the ones marked **[scanned]**), others need a read-through.

**The "it's not just X, it's Y" antithesis. [scanned]**
A rhetorical crutch that manufactures drama out of a claim that usually didn't need it — the two halves are rarely both true or both necessary.
> *Before:* "This isn't just a new architecture — it's a fundamentally different way of thinking about attention."
> *After:* "This architecture replaces the quadratic attention cost with a linear one."
> *Why:* The antithesis format asserts significance rather than stating what changed. The rewrite states the actual change and lets the reader judge its significance.

**AI-tool artifact leakage. [scanned, hard failure]**
Not a rhetorical tell at all — a literal, accidental technical error: markup left behind by copy-pasting from an AI tool's interface without stripping its internal citation/reference syntax. This is the one item in this entire document that isn't a judgment call — it's objectively broken, the same category as a CJK-leakage or unresolved-placeholder hit (`prose-editing-policy.md`'s hard-failure list). Documented as a real, recurring problem by Wikipedia's editor community (`Wikipedia:Signs of AI writing`), who catalog the exact artifact strings each tool leaves: ChatGPT's `contentReference`, `oaicite`, `turn0search0`-style tokens; Gemini's `[cite: 1]`/`[span_1]`; Grok's `grok_card`; Perplexity's `ppl-ai-file-upload`. If any of these appear in a paper's `.tex` source, it means text was pasted in from a chat interface without being cleaned up first — fix it immediately, no approval needed, since there's no "keep if" here.

**Rule-of-three / triadic listing when the content isn't genuinely three parallel things.**
AI-generated prose defaults to triads (three examples, three properties, three contributions) even when the underlying content has two ideas or five, because three *sounds* complete — this is one of the most consistently documented non-lexical AI tells across independent sources: GPTZero runs a dedicated article on it ("How to Break Free from GPT's Rule of Three"), and Wikipedia's `Signs of AI writing` gives it its own named subsection, both independently converging on the same pattern. Check: are these three items actually parallel in kind and weight, or was a third item invented/padded to complete the pattern?
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

**The colon-reveal. [scanned]**
A short setup clause, a colon, then a punchy one-word or short-phrase "payoff" — manufactured suspense borrowed from ad copy, not how a technical claim should land. Documented as a distinctive, specifically Claude-associated tic (Velitchkov, "22 Claude Clichés") as well as a generic cross-model pattern (SlopDetector's "The result?" / "The answer?" framing).
> *Before:* "We tested three architectures on the held-out set. The result: a clear winner."
> *After:* "Of the three architectures tested on the held-out set, the transformer variant wins by 4 points."
> *Why:* The colon-reveal performs a discovery the reader didn't ask to watch happen; the rewrite just states the finding.

**Forced/diplomatic balance.**
A "while X has benefits, it also has drawbacks" construction applied reflexively, giving every position equal weight regardless of what the actual evidence supports — documented independently by isitai.co.uk ("Diplomatic Balance") and workbravely.substack's "Institutional Rather Than Personal POV" (evidence treated with a uniformly even register, no selective emphasis where the evidence actually warrants it). This is a stricter, more general version of the hedge-then-assert pattern above — it's not that the sentence un-hedges, it's that *every* point in a paragraph gets the same weight whether or not the paper's own results support that.
> *Before:* "While our method shows promising results on synthetic benchmarks, it may also face challenges when applied to real-world data, and further work is needed to fully understand its limitations."
> *After:* "Our method has only been validated on synthetic benchmarks; we have not tested it on real-world data, and expect the sparsity assumption in Section 3 to break down when that assumption doesn't hold."
> *Why:* Genuine limitations are specific and asymmetric — some matter more than others. Forced balance flattens that, making a paper's honest uncertainty indistinguishable from its boilerplate throat-clearing.

**Empty-opener clichés. [scanned, partial]**
Stock scene-setting openers that could introduce literally any paper in any field — "In today's rapidly evolving landscape of X," "As the field continues to advance," "Picture this." Well-documented across sources (SlopDetector's "Empty-Opener Clichés," multiple independent blog catalogs converging on nearly identical example phrasing) as one of the most consistently recognized AI tells precisely because a human writer typically edits the first one out on a re-read and an LLM doesn't.
> *Before:* "In today's rapidly evolving landscape of machine learning, efficient attention mechanisms have become increasingly important."
> *After:* "Standard attention's quadratic cost limits sequence length in practice."
> *Why:* The specific claim (attention's cost limits sequence length) was always the real opening sentence; the "landscape" framing was a running-start that added nothing.

**Outline-like conclusions.**
A rigid conclusion formula — "Despite its [positive qualities], [subject] faces [challenges]... [speculative future work]" — documented by Wikipedia's `Signs of AI writing` as recognizable enough to have its own name. Distinct from (but overlaps with) the "conclusion that re-paraphrases the abstract" argument-level tell below — this is specifically about the rigid template shape, not just the content redundancy.
> *Before:* "Despite its strong empirical results, our method faces several limitations. Future work could explore extending it to additional domains."
> *After:* "Our method assumes i.i.d. sampling (Section 3); extending it to the streaming setting in Section 6 is the most immediate open problem."
> *Why:* The template version could close almost any paper unchanged; the rewrite names the specific assumption and the specific next step.

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

- **Unfalsifiable absolute gap-statement claims — an academic-writing-specific risk not covered by any of the generic tells above.** "No research has examined X," "little is known about Y," "no prior work has investigated Z" are stock phrases for introducing a research gap (documented as a recognized formulaic pattern by CASRAI's discourse-marker guidance), and LLM-assisted drafting leans on them by default because they're a safe-sounding way to motivate a contribution. The specific danger in a peer-reviewed submission: an absolute claim like "no research has examined X" is trivially falsifiable by a single counter-citation from a reviewer who happens to know the literature better than the drafting pass did — this isn't just an AI-slop style problem, it's a claim-accuracy problem that can cost the paper credibility on the spot. Every absolute gap claim needs an actual literature check before it ships, not just a rewrite.
  > *Before:* "No prior work has examined the interaction between sparse attention and quantization."
  > *After:* "Prior work on sparse attention (Smith et al.) and on quantization (Jones et al.) has proceeded independently; we are not aware of an existing study of their interaction, though we did not conduct an exhaustive search of the quantization literature specifically."
  > *Why:* The rewrite is both more honest about the limits of the literature check and harder for a reviewer to falsify with one citation.

### 1d. Detection heuristics (apply by judgment, not by grep)

Three quick tests worth running mentally on a paragraph that feels slightly off, even when nothing matches a specific pattern above:

1. **The delete-the-adjective test.** Remove every adjective/adverb from the sentence. Does it still make its point? If "our novel, comprehensive, robust approach significantly improves performance" reduces to "our approach improves performance" and loses nothing but word count, the adjectives were never doing work.

2. **The portability test.** Could this exact sentence be pasted into an unrelated paper in the same subfield without editing a single word? If yes, it's boilerplate — it isn't saying anything specific to *this* paper, *this* method, or *this* result. A sentence that only makes sense in this paper is a sentence with real content.

3. **The load-bearing-opener test.** Does the paragraph's first sentence state a claim the rest of the paragraph defends, or is it a throat-clearing lead-in (see 1b) that could be deleted with the second sentence promoted to first, unchanged? Most paragraphs pass this test worse than expected on a first draft — it's one of the highest-value single checks in this whole document.

4. **Sentence-length burstiness, checked at the section level, not the sentence level.** Human prose alternates short and long sentences irregularly (a coefficient of variation — standard deviation divided by mean sentence length — typically in the 0.6–1.2 range); LLM text tends toward a narrower, more uniform range (commonly cited around 0.2–0.4), because it isn't varying rhythm for effect the way a human writer does semi-consciously. `scripts/style_scan.py` computes this per file as a soft signal (see below) — but treat any single surface signal, including this one, with real skepticism: a thoughtful critique of the whole AI-tell genre (Kiraki, "The internet made a ban list for AI writing. I'm making a case for the defense") points out that individual patterns like em-dashes, triads, and antithesis all have centuries of legitimate rhetorical precedent (Didion used dashes; classical rhetoric has a name for antithesis), and that banning surface patterns in isolation risks flagging genuinely good, human writing while missing genuinely bad, human-written-but-still-boring prose. Low burstiness in one section of a paper you know a co-author wrote by hand is not evidence of anything — it's evidence to *look closer*, the same as every other item in this document.

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

- **1a (lexical)** and the greppable half of **1b (structural)** are what `scripts/style_scan.py` actually implements — every hit it reports is a candidate, never an automatic fix, per the tier model. This now includes the AI-tool-artifact check (the one genuine hard failure in this document), the colon-reveal and empty-opener patterns, and a per-file sentence-burstiness score.
- **1c (argument-level)** and **1d (heuristics)** are not implemented as patterns anywhere, deliberately — they need a read-through and judgment about what the paper is actually claiming and supporting, which a regex cannot assess. Apply them by hand (or have the assistant apply them while reading a section, surfacing findings the same way as any Tier B item) rather than expecting a scan to catch them.
- **Part 2** has no script at all. It's referenced whenever the assistant is composing new sentences for the paper — a drafting discipline, not a gate that runs after the fact.

## Research basis and version awareness

This document was substantially expanded from a dedicated research pass (three parallel investigations covering peer-reviewed literature, current industry/practitioner discourse, and structural-pattern documentation). Findings below are graded by confidence, matching the standard the research itself was held to — a claim this skill makes about someone else's prose should be at least as well-evidenced as the claims it asks you to cut from your own.

**High confidence (peer-reviewed or large-scale, directly verified):**
- Kobak, González-Márquez, Horvát & Lause, "Delving into LLM-assisted writing in biomedical publications through excess vocabulary," *Science Advances* 11(27), 2025 (arXiv:2406.07016) — 15.1M PubMed abstracts, 379 excess words identified, exact fold-increases for delve/underscore/showcasing.
- Liang, Izzo, Zhang et al., "Monitoring AI-Modified Content at Scale: A Case Study on the Impact of ChatGPT on AI Conference Peer Reviews," ICML 2024 (arXiv:2403.07183) — 6.5–16.9% of ICLR/NeurIPS/EMNLP/CoRL peer-review text estimated LLM-modified.
- Liang et al., "Quantifying large language model usage in scientific papers," *Nature Human Behaviour* (2025) — 1.1M papers, CS abstracts 22.5% / introductions 19.5% estimated LLM-modified as of late 2024.
- Juzek & Ward, "Why Does ChatGPT 'Delve' So Much?," COLING 2025 (arXiv:2412.11385) — 21 focal words, entropy analysis, explicitly tested and found only mixed evidence for the popular "RLHF annotator" causal explanation (see below).
- Geng & Trotta, "Human-LLM Coevolution: Evidence from Academic Writing" (arXiv:2502.09606) — the source of this document's opening "the list decays" claim; also found detector performance doesn't adapt as the underlying word distribution shifts, i.e. a detector (or a reference doc) tuned to 2023's tells silently degrades against 2025 text.
- GPTZero, "Introducing AI Patterns" and "How to Break Free from GPT's Rule of Three" — a commercial vendor, not peer-reviewed, but the rule-of-three documentation is specific, named, and independently corroborated by Wikipedia's community-maintained essay.
- Wikipedia:Signs of AI writing — not an academic source, but a large, actively-maintained, citably-versioned community document built from real-world review of thousands of submissions; the AI-tool-artifact strings (`oaicite`, `[cite: 1]`, `grok_card`, etc.) are the most directly actionable, lowest-false-positive-risk finding in the whole research pass.

**Medium confidence (real and specific, but commercial-vendor-reported or single-source):**
- Czuma, "Em-ergence of the em-dash..." (arXiv:2606.29540) and Freeburg, "The Last Fingerprint" (arXiv:2603.27006) — em-dash frequency shift with real numbers (human baseline ~3–4/1,000 words, unconstrained GPT-4.1 ~10–20/1,000 words), but single-author preprints, not yet peer-reviewed, and Freeburg's own finding is that em-dash rate is *model-dependent* (ranges from 0/1,000 to 9+/1,000 across 12 models) — not a universal signal, which is why this document still treats em-dash as a soft, per-paragraph flag rather than a hard density threshold.
- Pangram's ICLR 2026 peer-review analysis (21% flagged as fully AI-generated) — a detection vendor's self-published analysis with a commercial interest in the finding; corroborated as a real, ongoing controversy by *Nature*'s news desk, but the precise percentage should be treated as an estimate, not ground truth.
- Velitchkov, "22 Claude Clichés" — single-author blog, but specific and internally consistent; the source for the colon-reveal pattern's Claude-specific framing.

**Explicitly not confirmed — do not cite as settled fact if this document is extended further:**
- The "Nigerian-English-annotator" explanation for why "delve" specifically spiked (a popular hypothesis on social media) — the actual peer-reviewed COLING 2025 paper that tested this found only "mixed evidence," not confirmation.
- Any claim that OpenAI or Anthropic deliberately retrained a model to avoid specific words like "delve" or "boundaries" — no primary source from either company confirms this; the only confirmed *trained* behavior change found in this research was OpenAI's GPT-5 system card documenting a sycophancy reduction, which is a different phenomenon.
- "Constitutional AI causes forced-balance prose" as a direct causal mechanism — Anthropic's published constitution supports offering "balanced perspectives where relevant" as a value, but doesn't mandate a rigid hedge-template the way some secondary commentary implies.
- Specific numeric multipliers claimed for individual words in ICLR reviews (e.g. a specific "34.7×" figure for "meticulous") that could not be traced back to a specific, checkable table in a primary source.

**A caution this document takes seriously**: multiple sources (aggregated from university teaching-and-learning-center guidance) note that automated AI-detection tools have measurably higher false-positive rates against non-native English writers, whose phrasing can resemble certain LLM output for reasons that have nothing to do with AI assistance. This is exactly why every item in this document is a flagged candidate for your judgment, never an automatic rewrite or a ban — and it's a direct reason `polish.md`'s non-native-English grammar/register pass stays a separate, distinct discipline from this one rather than being merged into it.
