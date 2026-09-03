# Git and LaTeX safety rules

Standing constraints for working in a shared, git-tracked, multi-author LaTeX repo. These apply regardless of autonomy tier — they're about *how* an edit is made and *how* a change is reviewed, not *whether* permission is needed first.

## No bulk regex on `.tex`/`.bib` files, ever

**No script in this skill may `sed`/regex-mutate a `.tex` or `.bib` file in place.** A script may *read* a file and *report* what it found (missing packages, broken citations, characters needing escaping, brace mismatches) — but applying any fix to a shared document always goes through individual `Read`/`Edit` calls, one location at a time, never a batch find-and-replace script.

This holds even for Tier A mechanical fixes. The tier determines whether you're asked for permission before a fix is applied; it does not determine whether a script gets authority to rewrite the file directly. Two scripts from the source material were excluded entirely for this reason (`clean_latex.py`, `fix_latex_errors.py` from `agent-research-skills`) — both did exactly this, and one additionally had confirmed no-op bugs in its "fix" functions. Their diagnostic value is preserved (`scripts/compile_check.sh`'s error translation covers the same ground), just not their write-access.

**Why this matters more here than in a single-author project**: a co-author's uncommitted or in-progress work can be sitting in the same file. A batch script that "fixes" special characters or brace mismatches has no way to know it's about to collide with someone else's edit; a sequence of individual, reviewable `Edit` calls does.

## Backup before any edit to a shared file

Cheap insurance, borrowed from `latex-precision-skill`: before modifying any `.tex` file, note its current state (via `git status`/`git diff` — the repo's own history is a better backup mechanism than an ad hoc `.bak` file, so prefer checking that the working tree is clean and the change is easy to `git diff` against, rather than littering the repo with `.bak.N` files).

**Noting a deliberate substitution, for the record:** `academic-research-plugin`'s `citation-assistant` (one of the Phase 1 source skills) used a different safety mechanism — never touch the original file at all, write every result to a timestamped `output/` directory plus a `changes.md` audit log. This skill uses git-diff-based safety (above) instead, on the reasoning that the paper's own git history is already a complete, append-only audit log, and a parallel `output/`-directory mechanism would just be a second, redundant one to keep in sync. Recorded here so the choice reads as deliberate rather than an accidental drop of the original source's mechanism.

## Co-authorship: dirty trees, staleness, and merge conflicts

Added per an independent audit finding: this skill is explicitly scoped to a repo shared with co-authors, but had no guidance at all for the actual mechanics of that — until now.

**At the start of any session that will edit the paper, check `git status` before doing anything else.** Three outcomes:
- **Clean, and up to date with the remote** (after a `git fetch`, `HEAD` matches `origin/<branch>` or is ahead of it) — proceed normally.
- **Dirty** (uncommitted changes present) — stop and ask before editing. Don't guess whether the uncommitted changes are your own leftover work from a prior session or a co-author's in-progress edit that hasn't been committed yet; the difference matters and only the user knows which it is. This is a Tier A *check* (just running `git status` and reporting), but acting on a dirty tree by editing anyway is exactly the scenario the no-bulk-regex rule above exists to guard against, extended to manual edits too.
- **Clean, but stale** (a co-author has pushed commits not yet pulled) — say so and suggest `git fetch && git status` / a pull before editing, rather than silently working on an outdated version of a file a co-author has since changed. Editing a stale file risks a conflict on the next pull that didn't need to happen.

**Never run `git pull`, `git fetch --prune`, `git rebase`, or anything that rewrites history on its own initiative** — consistent with the "never commit or push without an explicit request" rule below, extended to the rest of the git-history-modifying surface. A plain `git fetch` (which only updates remote-tracking refs, touches nothing local) is the one exception — safe enough to run proactively (Tier A) purely to answer "are we stale," since it can't itself create a conflict or lose work.

**If a merge conflict happens** (from the user's own `git pull`/`git merge`, not something this skill would trigger on its own): don't attempt an automated resolution. Conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) inside a `.tex` file are exactly the kind of ambiguous, content-level judgment call this skill's Tier B model exists for — surface the conflicting regions to the user the same way any other content decision is surfaced, and let them resolve it. This is a stronger version of the general rule (`SKILL.md` non-negotiable #3): a merge conflict is definitionally two different people's claims about what the paper should say, which makes it the least appropriate place for an autonomous fix, tiered or not.

## Never commit or push without an explicit request

This skill never runs `git commit`, `git push`, or `git checkout -- <file>` on its own initiative. Git operations are the user's call — consistent with `claude-latex-paper-skill`'s "leave git operations to the user's verdict" and the harness-wide rule to confirm before anything that touches shared state.

## Reviewing a co-author's changes: latexdiff + git

`scripts/latex_diff.sh` — **scoped down per your Phase 2 decision**: supports diffing a file against your current working copy, and against a single specific git revision (a commit SHA, branch name, or tag — e.g. `HEAD~1`, `abc1234`, `main`, `v1.0`). It does **not** support true two-revision (`rev1` vs. `rev2`) diffing — that capability was dropped rather than fixed, since the source implementation's advertised `--git-rev v1.0..v2.0` syntax never actually worked (it fed an invalid range straight into `git show`, which fails). If you need to compare two arbitrary historical revisions against each other rather than one revision against your current working copy, do it in two manual steps: `git show <rev>:<path> > /tmp/old.tex` twice, then a plain file-to-file `latex_diff.sh` call — the script supports that mode directly.

Usage:
```
latex_diff.sh document.tex --git-rev HEAD~1        # vs. a specific commit
latex_diff.sh document.tex --git-rev main            # vs. a branch tip
latex_diff.sh old.tex new.tex                         # direct file-to-file
latex_diff.sh main.tex --git-rev HEAD~3 --flatten     # multi-file (\input/\include) document
```

This is a **Tier A, read-only** workflow — it produces a diff/PDF for you to look at, never modifies either file. Good default for "what actually changed since the last time I looked" or "what did my co-author change in their last commit."

## Compilation

Always compile before judging layout — never assess figure placement, page count, or overfull boxes from the raw `.tex` source. `scripts/compile_check.sh` handles engine auto-detection, multi-pass compilation, and translates raw log errors into plain language. Its auto-fix behaviors (adding a missing float placement specifier, injecting `microtype` when overfull-hbox warnings appear) are Tier A — but still applied via individual `Edit` calls to the specific flagged line, never a blanket rewrite of the file, per the no-bulk-regex rule above.

## Template pitfalls (starting a new paper from a venue's official kit)

Five recurring failure modes when a paper repo is first set up from `templates/<venue><year>/` — each has already caused a real broken submission somewhere, which is why they're listed explicitly rather than left as "use common sense":

| Pitfall | What breaks | What to do instead |
|---|---|---|
| Copying only the `.tex` file, not the whole template directory | Missing `.sty`/`.bst`/class files — won't compile, or silently falls back to default LaTeX formatting that doesn't match the venue's required style | Copy the entire `templates/<venue><year>/` directory into the paper repo, every file, every time |
| Editing a `.sty`, `.bst`, or class file directly | Breaks the venue's required formatting in a way that may not be visible until a desk-rejection check catches it | Never edit style/class files — if the template genuinely seems wrong, that's a signal to re-fetch it from the official source, not to patch it locally |
| Adding packages the base template didn't already include, without checking for conflicts | Package-load-order conflicts, redefined commands, broken cross-references — often only surfacing several sections later | Add a new package only when actually needed, and compile immediately after to confirm nothing broke |
| Deleting the template's own placeholder/example content before the real content is ready | Loses the formatting reference the template author intended you to match (how a theorem environment, an author block, or a table caption is supposed to look) | Comment out placeholder content rather than deleting it, and remove the comments only once the paper is otherwise done |
| Going long stretches between compiles while drafting | LaTeX errors compound — a missing brace three sections back can produce a confusing, unrelated-looking error near the end of the document, costing far more time to trace than if it were caught immediately | Compile after every section (`scripts/compile_check.sh`), not just at natural stopping points |
