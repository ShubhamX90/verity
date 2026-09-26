# Writing craft: narrative, structure, and sentence-level clarity

Distilled from published writing advice by Neel Nanda, Andrej Karpathy, Sebastian Farquhar, Zachary Lipton, Jacob Steinhardt, Ethan Perez, and Gopen & Swan's *The Science of Scientific Writing*, plus a research advisor's own structural guidance on abstracts, introductions, related work, and results (the register/length-cap note, the accessibility note, the six-move abstract frame, and the related-work/methodology/results/conclusion/failed-experiments subsections below) — venue-agnostic throughout. Every principle below is about what makes a paper's argument land with a reader, which doesn't change based on which conference it's submitted to; only the page limit and formatting rules do, and those come from the active venue profile (`venue-profile.md`), never from this file.

Two halves, same split as `de-ai-slop.md`: **Part 1 (Composing)** is a standing discipline that applies while drafting new material — not tiered, the same way `de-ai-slop.md`'s Part 2 isn't tiered, because there's no "before" text yet for a tier model to gate a rewrite of. **Part 2 (Reviewing against this craft)** is Tier A — a read-through judgment pass over an existing draft, the same spirit as `de-ai-slop.md`'s argument-level tells (1c/1d): not mechanically scannable, but worth checking deliberately rather than trusting impression.

---

## Part 1 — Composing

### The narrative principle

From Neel Nanda: *"A paper is a short, rigorous, evidence-based technical story with a takeaway readers care about."*

Every paper's narrative rests on three pillars, and they need to be unambiguous by the end of the introduction:

| Pillar | What it means | Failure mode if missing |
|---|---|---|
| **The What** | One to three specific, falsifiable claims within a cohesive theme | "We study X" — not a claim, a topic |
| **The Why** | Rigorous evidence supporting those claims — honestly-tuned baselines, experiments that distinguish competing hypotheses | "We show decent results" — evidence that doesn't discriminate between explanations |
| **The So What** | Why the claims matter to problems the target community already recognizes | A contribution nobody outside the paper's own framing would care about |

From Andrej Karpathy: *"A paper is not a random collection of experiments you report on. The paper sells a single thing that was not obvious or present before. The entire paper is organized around this core contribution with surgical precision."* This holds whether the contribution is a new method, a theoretical result, or improved understanding of something existing — a new method is not the only kind of legitimate contribution.

**The test**: if you cannot state the contribution in one sentence, there isn't a paper yet — there's a collection of experiments waiting for one. Everything else (related work, discussion, even most of the experiments) exists to support that one sentence, not to stand alongside it as equally important.

### Register: full sentences, and a sentence-length cap

Write in complete, academic-register sentences throughout, not sentence fragments or noun-phrase bullets standing in for prose. Bullets are fine for a genuinely enumerable, parallel list — contribution bullets, dataset statistics, a checklist — never as a substitute for an argument that needs a subject, a verb, and a stated logical connection between two ideas.

Long sentences fight the reader-expectation principles below before a reader even finishes parsing them. If a sentence runs past roughly 25 words, look for the natural place to split it into two or three — usually exactly where a subordinate clause or a coordinating conjunction already sits. `scripts/style_scan.py` flags any sentence over this length as a candidate, the same way it flags any other soft suggestion; not every long sentence needs splitting (one built from a single list of genuinely parallel items can legitimately run long), but most first-draft ones do.

### Accessibility: write the abstract and introduction for a non-expert reader

The abstract and the introduction are read by far more people, and far more carefully, than any other section — including reviewers skimming outside their own subarea, and readers with only beginner-level exposure to ML or LLMs generally. Both sections should be understandable to that reader, not just to a specialist in this paper's own subarea.

Two concrete implications:

- **Don't introduce new terminology here.** Use simple language and commonly known terms and metrics wherever the choice exists — F1, recall, precision, accuracy, and latency are all safe to use without definition; a metric invented specifically for this paper is not, and quoting it in the abstract without at least a clause of intuition for what it measures is a weak choice. Save the paper's own specialized vocabulary for the sections that need it, defining each term the first time it appears there (see `polish.md`'s acronym-handling rule, which applies just as well to any first-used technical term, not only to acronyms).
- **Don't overload these two sections with numbers.** An abstract that reports five or six statistics next to terms the reader hasn't seen defined yet is harder to follow than one that reports the single most important result and lets the results section carry the rest. This is the same discipline behind the 5-sentence formula's fifth move below ("your single most remarkable number") and the introduction structure's cap on how many numbers belong in its results-preview paragraph.

This is a corrective specifically aimed at LLM-drafted prose: a model asked to draft an abstract has already read the rest of the paper and tends to forget that its reader hasn't, packing in defined-nowhere metrics and jargon that only make sense once the paper's own vocabulary is in place.

### Where reader attention actually goes

Reviewer behavior is remarkably consistent across venues: the abstract is read essentially 100% of the time, the introduction is skimmed by the large majority of reviewers, figures get examined before the methods section by most readers, and full methods sections are read only once interest is already established by the earlier material. The practical implication: **front-load the paper's value.** Spend roughly equal effort on the abstract, the introduction, the figures, and everything else combined — not because the "everything else" doesn't matter, but because a reader who isn't convinced by the first three never reaches it in the state of mind that would make the rest land.

### The 5-sentence abstract formula

From Sebastian Farquhar. Five moves, in order:

1. **What you achieved** — "We introduce...", "We prove...", "We demonstrate..."
2. **Why this is hard and important**
3. **How you do it** — with the specialist keywords a reader would search for
4. **What evidence you have**
5. **Your single most remarkable number or result**

> *Worked example:*
> "We prove that gradient descent on overparameterized neural networks converges to global minima at a linear rate. [1 — what] This resolves a fundamental question about why deep learning works despite non-convex optimization landscapes. [2 — why it matters] Our proof relies on showing that the Neural Tangent Kernel remains approximately constant during training, reducing the problem to kernel regression. [3 — how, with keywords] We validate our theory on CIFAR-10 and ImageNet, showing that predicted convergence rates match experiments within 5%. [4 — evidence] This is the first polynomial-time convergence guarantee for networks with practical depth and width. [5 — the remarkable result]"

**What to delete**: from Zachary Lipton, *"If the first sentence can be pre-pended to any ML paper, delete it."* Openings like "Large language models have achieved remarkable success...", "Deep learning has revolutionized...", "In recent years, neural networks have..." are true of every paper in the subfield and therefore say nothing about this one. Start with the specific contribution instead.

### An alternative frame: six short moves

A complementary way to check an abstract's shape, describing much of the same content as Farquhar's five moves above but in a different order — use whichever framing exposes a gap more clearly, or check both, since they emphasize slightly different things (Farquhar's leads with the result; this one leads with the gap in existing work):

1. **Background** — the problem or domain, one sentence.
2. **The gap** — what existing work does not do, one sentence.
3. **The contribution** — motivated by that gap, one to two sentences.
4. **The methodology** — one to two sentences.
5. **The results** — one to two sentences.
6. **The impact** — the main takeaway or implication, one sentence.

Moves 1-2 here correspond roughly to Farquhar's move 2 ("why this is hard and important"); move 3 corresponds to Farquhar's move 1; moves 4-6 correspond to Farquhar's moves 3-5. An abstract that satisfies one formula usually satisfies the other. Treat a mismatch as a signal that one of the two gaps (background/existing-work, or contribution/motivation) has been merged together too tightly to tell apart, itself worth checking during a review pass, not just while drafting.

### Introduction structure

A workable template, adaptable to whatever length the active venue profile's page limit actually allows:

1. **Opening hook** (2–3 sentences) — the problem, and why it matters now, not eventually.
2. **Background/challenge** (a paragraph) — what makes this hard; what's been tried; why it's insufficient.
3. **Your approach** (a paragraph, sometimes two) — what's different, and the key insight that enables it. If the method has multiple stages, give each stage its own sentence stating what it does and which specific problem it solves — a reader should be able to reconstruct the method's shape from this paragraph alone, before ever reaching the methodology section. State the paper's research questions or objectives explicitly here if doing so sharpens what's being tested, rather than leaving them implicit until the results section.
4. **Contribution bullets** (2–4 items, 1–2 lines each, rarely more than 4) — specific and falsifiable. A common shape for an empirical paper is one bullet per method or system introduced, one per dataset or benchmark introduced (if any), and one for the evaluation itself (breadth of datasets, models, and baselines) — but state whatever the paper's actual contributions are, not this list for its own sake.
5. **Results preview** (2–3 sentences) — the single most important result, not a list of secondary ones. State it as an improvement over the strongest baseline ("outperforms the strongest baseline by 4 points") rather than as a bare, uncontextualized statistic ("achieves 91.3% accuracy") — the improvement framing is what tells a skimming reader whether the number is good. Cap this paragraph at two or three numbers total and at most two insights or consequences; the full results section is where the rest belongs.
6. **Paper organization** (optional, 1–2 sentences).

**Contribution bullets, good vs. bad:**
> *Good:* "We prove that X converges in O(n log n) time under assumption Y." / "We introduce Z, a 3-layer architecture that reduces memory by 40%." / "We demonstrate that A outperforms B by 15% on benchmark C."
> *Bad:* "We study the problem of X" (not a contribution). "We provide extensive experiments" (vague). "We make several contributions to the field" (says nothing).

### Related work: survey and differentiate

A related-work section — or the related-work paragraph folded into the introduction, at shorter venues — has to do two things: survey the landscape, and position this paper within it. A section that only surveys, without saying what this paper does that the surveyed work does not, has done half the job.

Structure it as two to three subsections, each covering one coherent cluster of prior work grouped by what the papers in it actually share, not an arbitrary bucket of "other related work." Each subsection has two parts:

1. **A survey paragraph** (the longer part) — summarize the cluster by what it has in common: its general approach, its typical findings, what it has established. Group papers by shared method or assumption, not as a list of "X did A. Y did B. Z did C." (See `de-ai-slop.md` 1c for the "list rather than synthesize" tell this paragraph needs to avoid.)
2. **A differentiation paragraph** (two to four sentences, the short part) — state specifically what this paper does that the cluster does not, or which of the cluster's assumptions this paper relaxes. If a paper in the cluster is concurrent or parallel work rather than something being built on, say so directly instead of treating it as already-established prior work.

Never skip the differentiation paragraph, even when the difference feels obvious while writing it — a reader who has read only the survey paragraph should not have to infer the contribution themselves.

### Methodology: step by step, with a diagram and worked examples

Describe the method as a sequence a reader could actually follow: what goes in, what comes out, and the concrete steps that turn the one into the other, in the order they actually happen. Where a step is more easily shown than described in prose — an example input and the model's output on it, a worked case, the exact prompt template used — include it; a single concrete example next to the abstract procedure description resolves more reader confusion than another paragraph of description would. A workflow diagram earns its place here specifically because a method spread across several paragraphs of prose is hard for a reader to reconstruct as a single mental picture; see `figures-tables-diagrams.md` for the standard this skill holds a figure to before it goes in the paper, and for the note on budgeting real time to prepare it rather than generating one in a few minutes.

### Results: organize around research questions, not around tables

Pick a small list of research questions (RQs) the experiments actually answer, and organize the results section around them rather than around whichever tables happen to exist. For each RQ:

1. State any experimental-setup detail specific to that RQ that hasn't already been covered in the general experimental-setup section.
2. Present the table or figure that answers it.
3. Before writing the explanation, decide what the single main takeaway is, and what (if any) secondary takeaways are — then write toward those, not toward re-describing every cell in the table.
4. Explain the table or figure by stating those takeaways directly, in roughly two paragraphs. A results section that restates every number in prose is redundant with the table sitting right next to it (see `compression-toolkit.md` operation 7, the same discipline applied here at draft time instead of at compression time).

### Conclusion: the past-tense abstract, not a repeat of it

A conclusion should read like a past-tense, one-to-two-paragraph version of the abstract's shape (what was done, what was found), but it earns its place in the paper only if it adds something the abstract didn't already say: a genuine limitation, a concrete direction for follow-up work, or an implication worth spelling out now that the results are in front of the reader. A conclusion that only reorders the abstract's own sentences is redundant with it — see `de-ai-slop.md` 1c's "conclusion that just re-paraphrases the abstract" tell, and 1b's "outline-like conclusions" tell for the specific rigid template (limitations, then generic "future work could explore...") to avoid defaulting into.

### Where failed experiments go

An experiment that didn't work usually belongs in one of three places, not automatically in the paper's main narrative: left out entirely, if it isn't relevant to the argument being made; moved to the appendix (with a pointer from the main text — see `compression-toolkit.md`'s cut-vs-appendix distinction), if it's still relevant enough to be worth a curious reader's time; or, occasionally, kept in the main text specifically because its failure is what motivates the method that follows, presenting the failed approach first and using its specific shortcoming to motivate the design choice that fixes it. Use the third option only when the failed attempt is actually doing that argumentative work, not as a default place to record everything that didn't pan out.

### Sentence-level clarity: Gopen & Swan's 7 reader-expectation principles

From George Gopen and Judith Swan's *The Science of Scientific Writing*: readers have structural expectations about where information appears in a sentence, and violating them forces the reader to spend effort on parsing structure instead of absorbing content. *"If the reader is to grasp what the writer means, the writer must understand what the reader needs."*

| Principle | Rule | Mnemonic |
|---|---|---|
| Subject-Verb Proximity | Keep the grammatical subject and verb close together | "Don't interrupt yourself" |
| Stress Position | Put the most important information at the sentence's end | "Save the best for last" |
| Topic Position | Establish perspective/context at the sentence's start | "First things first" |
| Old Before New | Familiar information first, new information last | "Build on known ground" |
| One Unit, One Function | Each sentence/paragraph serves exactly one purpose | "One idea per container" |
| Action in the Verb | Express the action in the verb, not a nominalized noun | "Verbs do, nouns sit" |
| Context Before New | Explain before presenting something new | "Set the stage first" |

Each with a before/after:

> **Subject-Verb Proximity** — *Weak:* "The model, which was trained on 100M tokens and fine-tuned on domain-specific data using LoRA with rank 16, achieves state-of-the-art results." *Strong:* "The model achieves state-of-the-art results after training on 100M tokens and fine-tuning with LoRA (rank 16)."
>
> **Stress Position** — *Weak:* "Accuracy improves by 15% when using attention." *Strong:* "When using attention, accuracy improves by 15%."
>
> **Topic Position** — *Weak:* "A novel attention mechanism that computes alignment scores is introduced." *Strong:* "To address the alignment problem, we introduce a novel attention mechanism."
>
> **Old Before New** — *Weak:* "Sparse attention was introduced by Child et al. The quadratic complexity of standard attention motivates this work." *Strong:* "Standard attention has quadratic complexity. To address this, Child et al. introduced sparse attention."
>
> **Action in the Verb** — *Weak:* "We performed an analysis of the results." *Strong:* "We analyzed the results."
>
> **Context Before New** — *Weak:* "Equation 3 shows that convergence is guaranteed when the learning rate satisfies..." *Strong:* "For convergence to be guaranteed, the learning rate must satisfy the condition in Equation 3..."

### Word choice and precision

From Zachary Lipton: eliminate hedging unless genuine uncertainty exists. "Provides *very* tight approximation" reads as insecure; "provides tight approximation" reads as confident. Drop vacuous intensifiers (very, extremely, highly, "significantly" when it isn't a statistical claim — see `de-ai-slop.md` 1c for the unsupported-"significantly" pattern specifically) — they signal insecurity, not strength.

From Jacob Steinhardt: precision beats brevity. Replace vague terms with the specific number or mechanism:

| Vague | Specific |
|---|---|
| performance | accuracy, latency, throughput |
| improves | increases accuracy by X%, reduces latency by Y |
| large | 1B parameters, 100M tokens |
| fast | 3x faster, 50ms latency |
| good results | 92% accuracy, 0.85 F1 |

Pick one term per concept and hold it for the whole paper — "model" vs. "network" vs. "architecture," "training" vs. "learning" vs. "optimization," "sample" vs. "example" vs. "instance" — inconsistent terminology reads as sloppy even when the underlying claim is solid.

**Avoid vocabulary that signals incremental work when the contribution isn't incremental**: "combine," "modify," "expand," "extend" all suggest stapling existing ideas together, even when what actually happened is a genuine new method. Prefer "develop," "propose," "introduce" when that's the more accurate description of what was done — this is about matching the verb to the actual claim, not about inflating a genuinely incremental contribution into something it isn't (that would be an unearned claim — see `de-ai-slop.md` 1c).

Micro-level tips, from Ethan Perez: minimize bare pronouns ("this," "it") — pair them with a noun ("this result," "this modification") so the reference is unambiguous. Unfold awkward possessives ("the model's accuracy" → "the accuracy of the model") when a sentence feels stiff. Active voice by default in narrative prose, consistent with `polish.md`'s voice-preference rule and its carve-out for methods/experiments passive constructions.

---

## Part 2 — Reviewing against this craft (Tier A, judgment-based, not scripted)

Same spirit as `de-ai-slop.md`'s 1c/1d — these need a read-through, not a grep, and are candidates for discussion rather than automatic fixes:

- **Can the contribution be stated in one sentence?** If not, that's a structural problem no sentence-level polish fixes — flag it as a Tier B structural concern, not a wording issue.
- **Are the three pillars (What/Why/So What) clear by the end of the introduction?** If a reader would need to reach the experiments section to understand why the paper matters, the introduction isn't doing its job yet.
- **Does every experiment support a specific, stated claim** — or are there results in the paper that don't map to anything the introduction promised?
- **Does the abstract follow the 5-sentence shape**, even loosely? An abstract that's all context and no result, or all result and no motivation, is missing a move.
- **Is there a generic opening sentence** that could be prepended to any paper in the subfield? (Directly the de-ai-slop.md 1d "portability test," applied specifically to the abstract/intro's first sentence.)
- **Is terminology consistent** for each core concept across the whole paper, not just within a section?
- **Would a reader with only beginner-level ML/LLM exposure follow the abstract and introduction?** If understanding either requires already knowing this paper's own jargon or a metric it invents, that's an accessibility gap, not a style nitpick — see this file's Accessibility note above.
- **Does each related-work subsection end with an explicit differentiation paragraph**, not just a survey of the cluster? A related-work section that never says what this paper does differently hasn't done its job.
- **Is each results subsection organized around a stated research question**, with a clear main takeaway — or does it just walk through a table cell by cell?
- **Does the conclusion say something the abstract didn't already say?**

None of this is mechanically checkable the way `style_scan.py` checks for banned words — apply it the way `de-ai-slop.md`'s argument-level tells are applied, as a deliberate pass, and surface findings as ordinary Tier B proposals when they suggest a specific fix.
