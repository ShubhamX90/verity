#!/usr/bin/env bash
# latex_diff.sh — latexdiff wrapper with git integration. Tier A, read-only:
# produces a diff .tex (and optionally a compiled diff PDF); never modifies
# either input file.
#
# Deliberately scoped down from the source material this was adapted from
# (latex-document-skill's latex_diff.sh): that script advertised a
# "diff between two git tags" mode via --git-rev v1.0..v2.0, but the
# actual implementation only ever resolved one revision and diffed it
# against the current working file — a v1.0..v2.0 range fed to `git show`
# is not valid syntax and would fail. Rather than fix that (a real feature,
# more work than this pass justified), this version only ever supports
# what actually works:
#
#   1. Two arbitrary files, diffed directly against each other.
#   2. One git revision (a commit SHA, branch, or tag) diffed against your
#      current working copy of the same file.
#
# There is no "revision vs. revision" mode. If you need that, do it in two
# manual steps and fall back to mode 1:
#   git show <rev1>:<path> > /tmp/old.tex
#   git show <rev2>:<path> > /tmp/new.tex
#   latex_diff.sh /tmp/old.tex /tmp/new.tex
#
# Usage:
#   latex_diff.sh OLD.tex NEW.tex [--output FILE] [--flatten] [--compile]
#   latex_diff.sh document.tex --git-rev HEAD~1 [--output FILE] [--flatten] [--compile]
#
# Requires latexdiff on PATH (and, for --compile, a working LaTeX install).

set -uo pipefail

FLATTEN=0
COMPILE=0
OUTPUT=""
GIT_REV=""
POSITIONAL=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output) OUTPUT="$2"; shift 2 ;;
    --flatten) FLATTEN=1; shift ;;
    --compile) COMPILE=1; shift ;;
    --git-rev) GIT_REV="$2"; shift 2 ;;
    --help|-h) grep -E '^# ' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) POSITIONAL+=("$1"); shift ;;
  esac
done

if ! command -v latexdiff &>/dev/null; then
  echo "error: 'latexdiff' not found on PATH. Install it first " \
       "(e.g. 'brew install latexdiff' on macOS, 'apt install latexdiff' on Debian/Ubuntu)." >&2
  exit 3
fi

OLD=""
NEW=""
TMPFILE=""
cleanup() { [[ -n "$TMPFILE" && -f "$TMPFILE" ]] && rm -f "$TMPFILE"; }
trap cleanup EXIT

if [[ -n "$GIT_REV" ]]; then
  if [[ "$GIT_REV" == *".."* ]]; then
    echo "error: '$GIT_REV' looks like a two-revision range (contains '..'). This script only" >&2
    echo "supports one revision vs. your current working copy, not revision-vs-revision —" >&2
    echo "'git show <rev1>..<rev2>:<path>' does not do what you'd expect (it exits 0 with EMPTY" >&2
    echo "output, not an error, which would silently produce a garbage diff if this script let" >&2
    echo "it through). For revision-vs-revision, do it in two manual steps instead:" >&2
    echo "  git show <rev1>:<path> > /tmp/old.tex" >&2
    echo "  git show <rev2>:<path> > /tmp/new.tex" >&2
    echo "  $(basename "$0") /tmp/old.tex /tmp/new.tex" >&2
    exit 2
  fi
  if [[ ${#POSITIONAL[@]} -ne 1 ]]; then
    echo "error: --git-rev mode takes exactly one .tex file (the current working copy). Got: ${POSITIONAL[*]:-<none>}" >&2
    exit 2
  fi
  NEW="${POSITIONAL[0]}"
  if [[ ! -f "$NEW" ]]; then
    echo "error: file not found: $NEW" >&2
    exit 2
  fi
  REPO_ROOT="$(git -C "$(dirname "$NEW")" rev-parse --show-toplevel 2>/dev/null)" || {
    echo "error: $NEW is not inside a git repository" >&2
    exit 2
  }
  REL_PATH="$(cd "$(dirname "$NEW")" && git rev-parse --show-prefix)$(basename "$NEW")"
  # Trailing X's only, nothing after them — GNU mktemp accepts a literal
  # suffix after the X placeholder, but BSD/macOS mktemp does not, and
  # silently returns the template unrandomized instead of erroring. A
  # missing .tex extension doesn't matter here: latexdiff reads by content,
  # not by filename.
  if ! TMPFILE="$(mktemp "${TMPDIR:-/tmp}/latexdiff_old.XXXXXX")"; then
    echo "error: mktemp failed to create a temp file for the old revision" >&2
    exit 2
  fi
  if ! git -C "$REPO_ROOT" show "${GIT_REV}:${REL_PATH}" > "$TMPFILE" 2>/dev/null; then
    echo "error: could not resolve '${GIT_REV}:${REL_PATH}' — check the revision exists and the path is correct at that revision" >&2
    exit 2
  fi
  if [[ ! -s "$TMPFILE" ]]; then
    echo "error: 'git show ${GIT_REV}:${REL_PATH}' produced empty output — this usually means the" >&2
    echo "revision spec wasn't a single valid revision. Refusing to diff against an empty file." >&2
    exit 2
  fi
  OLD="$TMPFILE"
  SAFE_REV="$(printf '%s' "$GIT_REV" | tr -c 'A-Za-z0-9._-' '_')"
  DEFAULT_OUTPUT="diff_${SAFE_REV}_vs_current_$(basename "${NEW%.tex}").tex"
else
  if [[ ${#POSITIONAL[@]} -ne 2 ]]; then
    echo "error: file-to-file mode takes exactly two .tex files (OLD NEW). Got: ${POSITIONAL[*]:-<none>}" >&2
    exit 2
  fi
  OLD="${POSITIONAL[0]}"
  NEW="${POSITIONAL[1]}"
  for f in "$OLD" "$NEW"; do
    if [[ ! -f "$f" ]]; then
      echo "error: file not found: $f" >&2
      exit 2
    fi
  done
  DEFAULT_OUTPUT="diff_$(basename "${OLD%.tex}")_$(basename "${NEW%.tex}").tex"
fi

OUTPUT="${OUTPUT:-$DEFAULT_OUTPUT}"

LATEXDIFF_ARGS=(--allow-spaces)
[[ "$FLATTEN" -eq 1 ]] && LATEXDIFF_ARGS+=(--flatten)

echo "diffing: ${OLD}$( [[ -n "$GIT_REV" ]] && echo " (at ${GIT_REV})" ) -> ${NEW}"
if ! latexdiff "${LATEXDIFF_ARGS[@]}" "$OLD" "$NEW" > "$OUTPUT" 2> /tmp/latexdiff_stderr.$$; then
  echo "error: latexdiff failed:" >&2
  cat /tmp/latexdiff_stderr.$$ >&2
  rm -f /tmp/latexdiff_stderr.$$
  exit 1
fi
rm -f /tmp/latexdiff_stderr.$$
echo "wrote $OUTPUT"

if [[ "$COMPILE" -eq 1 ]]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  if [[ -x "$SCRIPT_DIR/compile_check.sh" ]]; then
    "$SCRIPT_DIR/compile_check.sh" "$OUTPUT"
  else
    echo "warning: compile_check.sh not found next to this script — compiling directly with pdflatex" >&2
    pdflatex -interaction=nonstopmode "$OUTPUT" || echo "compilation reported issues — check the log" >&2
  fi
fi
