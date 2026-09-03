# Writing craft: narrative, structure, and sentence-level clarity

Distilled from published writing advice by Neel Nanda, Andrej Karpathy, Sebastian Farquhar, Zachary Lipton, Jacob Steinhardt, Ethan Perez, and Gopen & Swan's *The Science of Scientific Writing* — venue-agnostic throughout. Every principle below is about what makes a paper's argument land with a reader, which doesn't change based on which conference it's submitted to; only the page limit and formatting rules do, and those come from the active venue profile (`venue-profile.md`), never from this file.

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

### Introduction structure

A workable template, adaptable to whatever length the active venue profile's page limit actually allows:

1. **Opening hook** (2–3 sentences) — the problem, and why it matters now, not eventually.
2. **Background/challenge** (a paragraph) — what makes this hard; what's been tried; why it's insufficient.
3. **Your approach** (a paragraph) — what's different, and the key insight that enables it.
4. **Contribution bullets** (2–4 items, 1–2 lines each) — specific and falsifiable.
5. **Results preview** (2–3 sentences) — the most impressive numbers, the scope of evaluation.
6. **Paper organization** (optional, 1–2 sentences).

**Contribution bullets, good vs. bad:**
> *Good:* "We prove that X converges in O(n log n) time under assumption Y." / "We introduce Z, a 3-layer architecture that reduces memory by 40%." / "We demonstrate that A outperforms B by 15% on benchmark C."
> *Bad:* "We study the problem of X" (not a contribution). "We provide extensive experiments" (vague). "We make several contributions to the field" (says nothing).

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

None of this is mechanically checkable the way `style_scan.py` checks for banned words — apply it the way `de-ai-slop.md`'s argument-level tells are applied, as a deliberate pass, and surface findings as ordinary Tier B proposals when they suggest a specific fix.
