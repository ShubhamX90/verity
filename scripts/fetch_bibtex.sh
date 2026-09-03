#!/usr/bin/env bash
# fetch_bibtex.sh — fetch a verified BibTeX entry for a DOI or arXiv ID.
# Never hand-constructs an entry: DOI goes through CrossRef content negotiation,
# arXiv IDs go through arXiv's own native BibTeX export endpoint. If neither
# resolves, this script fails loudly rather than printing anything — the
# caller (citation-verification.md's workflow) is responsible for falling
# back to a PLACEHOLDER_ cite key and telling the user, never for inventing
# a substitute entry.
#
# Usage:
#   fetch_bibtex.sh <DOI_or_arXiv_ID> [<ID2> ...] [--output file.bib] [--append]
#
# Examples:
#   fetch_bibtex.sh 10.48550/arXiv.1706.03762
#   fetch_bibtex.sh 1706.03762
#   fetch_bibtex.sh 10.1038/nature14539 1706.03762 --output refs.bib --append
#
# Safe-by-default on --output: writing to a new or empty file needs no flag;
# writing to an EXISTING, NON-EMPTY file without --append is refused (exit
# 4) rather than silently overwritten — --append is how you add entries to
# a real refs.bib, not an optional extra.
#
# Exit codes: 0 = all IDs resolved, 1 = no ID given, or one or more IDs
# failed to resolve (failures are reported on stderr with the ID; nothing
# is silently dropped), 4 = refused to overwrite an existing non-empty
# --output file (use --append).

set -euo pipefail

OUTPUT=""
APPEND=0
IDS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output) OUTPUT="$2"; shift 2 ;;
    --append) APPEND=1; shift ;;
    --help|-h)
      grep -E '^# ' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *) IDS+=("$1"); shift ;;
  esac
done

if [[ ${#IDS[@]} -eq 0 ]]; then
  echo "error: no DOI or arXiv ID given. Run with --help for usage." >&2
  exit 1
fi

ARXIV_RE='^[0-9]{4}\.[0-9]{4,5}(v[0-9]+)?$'
DOI_RE='^10\.[0-9]{4,9}/.+$'

fetch_one() {
  local id="$1"
  local bibtex=""

  if [[ "$id" =~ $ARXIV_RE ]]; then
    bibtex="$(curl -sL --max-time 15 --fail "https://arxiv.org/bibtex/${id}" 2>/dev/null || true)"
  elif [[ "$id" =~ $DOI_RE ]]; then
    bibtex="$(curl -sL --max-time 15 --fail -H "Accept: application/x-bibtex" "https://doi.org/${id}" 2>/dev/null || true)"
  else
    echo "FAILED  ${id}  — not a recognized DOI (10.NNNN/...) or arXiv ID (YYMM.NNNNN)" >&2
    return 1
  fi

  # A real entry starts with @; anything else (HTML error page, empty
  # response, a JSON error body) means the fetch didn't actually succeed
  # even if curl's exit code was 0 for some intermediate redirect.
  if [[ -z "$bibtex" || "${bibtex:0:1}" != "@" ]]; then
    echo "FAILED  ${id}  — no valid BibTeX returned" >&2
    return 1
  fi

  echo "$bibtex"
  echo ""
  return 0
}

FAIL_COUNT=0
RESULT=""
for id in "${IDS[@]}"; do
  if entry="$(fetch_one "$id")"; then
    RESULT+="$entry"$'\n'
  else
    FAIL_COUNT=$((FAIL_COUNT + 1))
  fi
done

if [[ -n "$OUTPUT" ]]; then
  if [[ "$APPEND" -eq 1 ]]; then
    printf '%s' "$RESULT" >> "$OUTPUT"
  elif [[ -s "$OUTPUT" ]]; then
    # Refuse to silently destroy an existing, non-empty file. --append is
    # opt-in on purpose elsewhere in this script, but overwriting someone's
    # shared refs.bib because --append was forgotten is exactly the kind of
    # silent data loss the no-bulk-regex rule (git-and-latex-safety.md)
    # exists to prevent — a whole-file overwrite is worse than a regex
    # mutation, not exempt from the same concern.
    echo "error: $OUTPUT already exists and is not empty. Refusing to overwrite it." >&2
    echo "Use --append to add these entries to it, or remove/rename it first if you really mean to replace it." >&2
    exit 4
  else
    # New file, or an existing-but-empty file (e.g. a stub .bib) — safe to write.
    printf '%s' "$RESULT" > "$OUTPUT"
  fi
  echo "wrote $(( ${#IDS[@]} - FAIL_COUNT ))/${#IDS[@]} entries to $OUTPUT" >&2
else
  printf '%s' "$RESULT"
fi

if [[ "$FAIL_COUNT" -gt 0 ]]; then
  echo "${FAIL_COUNT}/${#IDS[@]} ID(s) failed to resolve — see stderr above. Do not hand-construct these entries; mark PLACEHOLDER_ and tell the user." >&2
  exit 1
fi
exit 0
