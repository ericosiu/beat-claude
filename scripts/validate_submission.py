#!/usr/bin/env python3
"""Objective pre-screen linter for Beat Claude submission packets.

Candidates (and reviewers) can run this against a submission file or a
directory of submission files before review:

    python3 scripts/validate_submission.py path/to/submission.md
    python3 scripts/validate_submission.py path/to/submission_dir/ --strict

It checks these things:

1. Required packet sections (FAIL if missing): all 7 sections of the
   Required Submission Packet defined in README.md are present somewhere in
   the submission text.
2. Review-manipulation attempts (FAIL): text that addresses or instructs a
   reviewing AI model ("ignore previous instructions", "you are an AI
   reviewer", "score this submission as..."), invisible/zero-width Unicode
   characters that hide text from human readers, and HTML comments that
   carry scoring or reviewer instructions. Review may be AI-assisted but is
   always human-confirmed; attempting to manipulate it is an automatic
   reject, so the pre-screen fails hard on it.
3. Number source labels (advisory WARN): paragraphs containing numeric
   claims (percentages, dollar amounts, counts) should carry one of the
   [Observed] / [Estimated] / [Benchmarked] / [Assumed] labels from
   SCORING.md nearby. This is a heuristic; reviewers make the final call.
4. Evidence-tier citations (advisory WARN): major claims should reference
   the SCORING.md evidence tiers (Tier 0-5) in the evidence log.
5. Verifiability (advisory WARN): [Observed] numbers and Tier 2-5 evidence
   claims assert something a reviewer can inspect, so the same section
   should contain at least one verifiable artifact reference: a link, an
   attached file path, a screenshot/attachment reference, or a reproduction
   command. High-tier claims with nothing checkable are treated as Tier 0
   (claims only) at review time.
6. Brief version (advisory WARN): briefs carry a version stamp and are
   refreshed periodically; submissions should state which brief version they
   answered so reviewers can score against the right one.

Exit codes: 0 when all required sections are present and no manipulation
attempts are detected (warnings allowed), 1 when required sections are
missing, when a review-manipulation attempt is detected, or when --strict
is passed and any warnings were produced.

Pure stdlib; mirrors the style of validate_public_content.py.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TEXT_EXTS = {".md", ".markdown", ".txt"}

# The 7 sections of the Required Submission Packet (see README.md,
# "Required Submission Packet"). Each entry maps the canonical section name
# to a pattern of accepted heading/label variants.
REQUIRED_SECTIONS: list[tuple[str, re.Pattern[str]]] = [
    ("Written answer", re.compile(r"written\s+answer", re.I)),
    ("Operating artifact", re.compile(r"operating\s+artifact", re.I)),
    ("Evidence log", re.compile(r"evidence\s+log", re.I)),
    ("Number source labels", re.compile(r"number\s+source\s+labels?|source\s+labels?", re.I)),
    ("AI usage disclosure", re.compile(r"ai\s+usage(\s+disclosure)?|ai\s+disclosure", re.I)),
    ("Failure handling", re.compile(r"failure\s+handling|what\s+breaks", re.I)),
    ("Artifact access", re.compile(r"artifact\s+access", re.I)),
]

SOURCE_LABEL_PATTERN = re.compile(r"\[\s*(observed|estimated|benchmarked|assumed)\s*\]", re.I)
EVIDENCE_TIER_PATTERN = re.compile(r"\btiers?\s*[0-5]\b", re.I)
BRIEF_VERSION_PATTERN = re.compile(r"\bbrief\s+version\b", re.I)

# Review-manipulation detection. Review may be AI-assisted but is always
# human-confirmed; content that tries to instruct the reviewing model, or
# text hidden from human readers, is an automatic reject (SCORING.md,
# "Integrity"). Patterns are deliberately narrow: a candidate legitimately
# writing about their own agent's prompts should not trip them.
INJECTION_PHRASE_CHECKS: list[tuple[str, re.Pattern[str]]] = [
    ("instruction-override phrasing",
     re.compile(r"\b(?:ignore|disregard|forget|override)\b[^.\n]{0,40}"
                r"\b(?:previous|prior|above|earlier|all)\b[^.\n]{0,40}"
                r"\b(?:instructions?|prompts?|rules|rubrics?|guidelines)\b", re.I)),
    ("text addressed to a reviewing model",
     re.compile(r"\byou\s+are\s+(?:an?\s+)?(?:ai|llm|language\s+model|automated)\b"
                r"[^.\n]{0,60}\b(?:review|grade|scor|evaluat)", re.I)),
    ("scoring instruction to the reviewer",
     re.compile(r"\b(?:score|rate|grade|mark)\s+(?:this|my)\s+"
                r"(?:submission|answer|candidate|packet|response)\b", re.I)),
    ("verdict instruction to the reviewer",
     re.compile(r"\b(?:this|the)\s+(?:submission|candidate|answer)\s+"
                r"(?:must|should)\s+(?:advance|pass|receive|be\s+scored)\b", re.I)),
]

# Invisible characters that can hide text from a human reader while staying
# machine-readable: zero-width spaces/joiners, bidi controls, word joiners,
# and interior byte-order marks. A single leading BOM is a benign editor
# artifact and is stripped before scanning.
HIDDEN_CHAR_PATTERN = re.compile(
    "[\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff]"
)

# HTML comments are invisible in rendered markdown. Flag ones that talk to
# the review process; ordinary editorial comments pass.
HTML_COMMENT_PATTERN = re.compile(r"<!--(.*?)-->", re.S)
REVIEW_TERM_PATTERN = re.compile(r"\b(?:tier\s*[0-5]|score|scoring|reviewer|review|"
                                 r"benchmark|advance|rubric|grade)\b", re.I)

# Numeric claims worth labeling: currency, percentages, thousands-separated
# counts, k/M/B shorthand, and bare multi-digit numbers.
NUMBER_PATTERN = re.compile(
    r"\$\s?\d[\d,.]*"          # $100K-style currency (prefix)
    r"|\d+(?:\.\d+)?\s?%"      # percentages
    r"|\b\d{1,3}(?:,\d{3})+\b"  # 1,000-style counts
    r"|\b\d+(?:\.\d+)?[kKmMbB]\b"  # 40K / 2M shorthand
    r"|\b\d{2,}\b"             # bare multi-digit numbers
)

HEADING_LINE = re.compile(r"^\s{0,3}#{1,6}\s")
TABLE_RULE_LINE = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")
URL_PATTERN = re.compile(r"https?://\S+|\([^)\s]*\.[a-z]{2,}[^)]*\)")
# A required "Brief version: 2026-07" stamp is metadata, not a numeric claim.
BRIEF_VERSION_STAMP = re.compile(r"brief\s+version\b[:*\s]*[\w.-]*", re.I)

# Verifiability check: [Observed] numbers and Tier 2-5 evidence claims assert
# an inspectable artifact or record (SCORING.md: Tier 2 = demo artifact,
# 3 = logs/source records, 4 = before/after data, 5 = independent
# verification). Tier 0 claims no proof and Tier 1 screenshots are usually
# attached with the application, so both are exempt here.
OBSERVED_CLAIM_PATTERN = re.compile(r"\[\s*observed\s*\]", re.I)
HIGH_TIER_CLAIM_PATTERN = re.compile(r"\btiers?\s*[2-5]\b", re.I)
VERIFIABLE_REF_PATTERN = re.compile(
    r"https?://\S+"  # a link a reviewer can open
    # an attached data/code/media file the reviewer can inspect
    r"|\b\S+\.(?:csv|tsv|xlsx?|jsonl?|pdf|png|jpe?g|gif|mp4|mov|zip|py|ipynb|sql|sh|har|log)\b"
    # an explicit screenshot/attachment/appendix pointer
    r"|\b(?:screenshots?|attach(?:ed|ments?)|appendix|appendices|exhibit)\b"
    r"|^\s*\$\s+\S",  # a shell reproduction command
    re.I | re.M,
)


def read_submission_files(target: Path) -> list[tuple[Path, str]]:
    """Return (path, text) pairs for the submission file or directory."""
    if target.is_file():
        candidates = [target]
    else:
        candidates = sorted(
            p for p in target.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_EXTS
        )
    files: list[tuple[Path, str]] = []
    for path in candidates:
        try:
            files.append((path, path.read_text(encoding="utf-8")))
        except UnicodeDecodeError:
            continue
    return files


def check_sections(text: str) -> list[str]:
    """Return the canonical names of required packet sections not found."""
    return [name for name, pattern in REQUIRED_SECTIONS if not pattern.search(text)]


def find_manipulation_attempts(text: str) -> list[tuple[int, str]]:
    """Return (line_no, description) for review-manipulation signals:
    injection phrasing aimed at an AI-assisted reviewer, invisible Unicode
    characters, and HTML comments that instruct the review process.

    Fenced code blocks, blockquotes, and inline code spans are exempt from
    the phrase checks so candidates can quote adversarial inputs they
    defended against (format such quotes as code). Hidden characters are
    flagged everywhere except a single leading BOM.
    """
    flagged: list[tuple[int, str]] = []
    in_fence = False
    for line_no, line in enumerate(text.splitlines(), 1):
        if line_no == 1 and line.startswith("\ufeff"):
            line = line[1:]
        if HIDDEN_CHAR_PATTERN.search(line):
            chars = sorted({f"U+{ord(c):04X}" for c in HIDDEN_CHAR_PATTERN.findall(line)})
            flagged.append((line_no, f"invisible/zero-width characters: {', '.join(chars)}"))
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or line.lstrip().startswith(">"):
            continue
        prose = re.sub(r"`[^`]*`", "", line)
        for label, pattern in INJECTION_PHRASE_CHECKS:
            if pattern.search(prose):
                snippet = " ".join(prose.split())[:90]
                flagged.append((line_no, f"{label}: {snippet}"))
    for match in HTML_COMMENT_PATTERN.finditer(text):
        if REVIEW_TERM_PATTERN.search(match.group(1)):
            line_no = text.count("\n", 0, match.start()) + 1
            snippet = " ".join(match.group(1).split())[:90]
            flagged.append((line_no, f"HTML comment addressing the review: {snippet}"))
    return sorted(flagged)


def iter_paragraphs(text: str):
    """Yield (first_line_no, paragraph_text) for prose paragraphs, skipping
    fenced code blocks, headings, and table separator rows."""
    lines = text.splitlines()
    in_fence = False
    current: list[str] = []
    start_line = 0
    for line_no, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        stripped = line.strip()
        if not stripped:
            if current:
                yield start_line, "\n".join(current)
                current = []
            continue
        if HEADING_LINE.match(line) or TABLE_RULE_LINE.match(line):
            continue
        if not current:
            start_line = line_no
        current.append(line)
    if current:
        yield start_line, "\n".join(current)


def find_unlabeled_numbers(text: str) -> list[tuple[int, str]]:
    """Return (line_no, snippet) for paragraphs that contain numeric claims
    but no [Observed|Estimated|Benchmarked|Assumed] label."""
    flagged: list[tuple[int, str]] = []
    for line_no, paragraph in iter_paragraphs(text):
        if SOURCE_LABEL_PATTERN.search(paragraph):
            continue
        # Ignore numbers that only appear inside URLs/links or a brief
        # version stamp.
        prose = URL_PATTERN.sub("", paragraph)
        prose = BRIEF_VERSION_STAMP.sub("", prose)
        if NUMBER_PATTERN.search(prose):
            snippet = " ".join(paragraph.split())[:100]
            flagged.append((line_no, snippet))
    return flagged


def count_evidence_tier_refs(text: str) -> int:
    return len(EVIDENCE_TIER_PATTERN.findall(text))


def iter_sections(text: str):
    """Yield (start_line, title, body) per markdown section, splitting on
    headings outside fenced code blocks. Text before the first heading is
    its own section titled "(preamble)"."""
    lines = text.splitlines()
    in_fence = False
    title = "(preamble)"
    start_line = 1
    body: list[str] = []
    for line_no, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and HEADING_LINE.match(line):
            if body and any(chunk.strip() for chunk in body):
                yield start_line, title, "\n".join(body)
            title = line.lstrip("# \t").strip() or "(untitled)"
            start_line = line_no
            body = []
            continue
        body.append(line)
    if body and any(chunk.strip() for chunk in body):
        yield start_line, title, "\n".join(body)


def find_unverifiable_claims(text: str) -> list[tuple[int, str]]:
    """Return (start_line, section_title) for sections that make [Observed]
    or Tier 2-5 claims but contain nothing checkable: no link, attached file
    path, screenshot/attachment reference, or reproduction command."""
    flagged: list[tuple[int, str]] = []
    for start_line, title, body in iter_sections(text):
        if not (OBSERVED_CLAIM_PATTERN.search(body) or HIGH_TIER_CLAIM_PATTERN.search(body)):
            continue
        # A fenced code block counts as a reproduction command.
        if "```" in body or VERIFIABLE_REF_PATTERN.search(body):
            continue
        flagged.append((start_line, title))
    return flagged


def run(target: Path, strict: bool = False, out=sys.stdout) -> int:
    files = read_submission_files(target)
    if not files:
        print(f"error: no readable text files found at {target}", file=out)
        return 1

    combined = "\n\n".join(text for _, text in files)
    print(f"Beat Claude submission pre-screen: {target}", file=out)
    print(f"Files checked: {len(files)}\n", file=out)

    failures = 0
    warnings = 0

    # Check 1: required packet sections (fail).
    missing = check_sections(combined)
    if missing:
        failures += 1
        print(f"[FAIL] Required packet sections: missing {len(missing)} of "
              f"{len(REQUIRED_SECTIONS)}:", file=out)
        for name in missing:
            print(f"       - {name}", file=out)
    else:
        print(f"[PASS] Required packet sections: all {len(REQUIRED_SECTIONS)} found", file=out)

    # Check 2: review-manipulation attempts (fail).
    manipulations: list[tuple[Path, int, str]] = []
    for path, text in files:
        for line_no, description in find_manipulation_attempts(text):
            manipulations.append((path, line_no, description))
    if manipulations:
        failures += 1
        print(f"[FAIL] Review manipulation: {len(manipulations)} signal(s) that address or "
              "instruct the review process, or hide text from human readers.", file=out)
        print("       Attempting to manipulate AI-assisted review is an automatic reject.", file=out)
        print("       If you are quoting an adversarial input your agent defended against,", file=out)
        print("       format the quote as a code block or blockquote:", file=out)
        for path, line_no, description in manipulations[:20]:
            print(f"       - {path}:{line_no}: {description}", file=out)
        if len(manipulations) > 20:
            print(f"       ... and {len(manipulations) - 20} more", file=out)
    else:
        print("[PASS] Review manipulation: no injection phrasing, hidden characters, or "
              "reviewer-directed comments detected", file=out)

    # Check 3: verifiability of high-tier claims (advisory, prominent).
    unverifiable: list[tuple[Path, int, str]] = []
    for path, text in files:
        for start_line, title in find_unverifiable_claims(text):
            unverifiable.append((path, start_line, title))
    if unverifiable:
        warnings += 1
        print(f"[WARN] Verifiability: {len(unverifiable)} section(s) make [Observed] or "
              "Tier 2-5 claims with nothing checkable in the same section.", file=out)
        print("       High-tier claims need a verifiable artifact reference (link, attached "
              "file path,", file=out)
        print("       screenshot/attachment reference, or reproduction command) or reviewers "
              "treat them", file=out)
        print("       as Tier 0 (claims only):", file=out)
        for path, start_line, title in unverifiable[:20]:
            print(f"       - {path}:{start_line}: section \"{title}\"", file=out)
        if len(unverifiable) > 20:
            print(f"       ... and {len(unverifiable) - 20} more", file=out)
    else:
        print("[PASS] Verifiability: every section with [Observed] or Tier 2-5 claims "
              "contains a checkable reference", file=out)

    # Check 4: number source labels (advisory).
    unlabeled: list[tuple[Path, int, str]] = []
    for path, text in files:
        for line_no, snippet in find_unlabeled_numbers(text):
            unlabeled.append((path, line_no, snippet))
    if unlabeled:
        warnings += 1
        print(f"[WARN] Number source labels: {len(unlabeled)} paragraph(s) contain numbers "
              "with no [Observed|Estimated|Benchmarked|Assumed] label nearby:", file=out)
        for path, line_no, snippet in unlabeled[:20]:
            print(f"       - {path}:{line_no}: {snippet}", file=out)
        if len(unlabeled) > 20:
            print(f"       ... and {len(unlabeled) - 20} more", file=out)
    else:
        print("[PASS] Number source labels: no unlabeled numeric claims detected", file=out)

    # Check 5: evidence-tier citations (advisory).
    tier_refs = count_evidence_tier_refs(combined)
    if tier_refs == 0:
        warnings += 1
        print("[WARN] Evidence tiers: no references to the SCORING.md evidence tiers "
              "(Tier 0-5) found; map each major claim to a proof tier in your evidence log", file=out)
    else:
        print(f"[PASS] Evidence tiers: {tier_refs} reference(s) to SCORING.md tiers found", file=out)

    # Check 6: brief version statement (advisory).
    if BRIEF_VERSION_PATTERN.search(combined):
        print("[PASS] Brief version: submission states which brief version it answers", file=out)
    else:
        warnings += 1
        print("[WARN] Brief version: no \"Brief version\" statement found; briefs are "
              "refreshed periodically, so state the version stamp from the brief you "
              "answered (e.g. \"Brief version: 2026-07\")", file=out)

    print("", file=out)
    if failures:
        print("Result: FAIL (missing required sections or review-manipulation signals)", file=out)
        return 1
    if warnings and strict:
        print("Result: FAIL (--strict: warnings treated as failures)", file=out)
        return 1
    if warnings:
        print("Result: PASS with warnings (advisory checks are heuristics; "
              "reviewers make the final call)", file=out)
        return 0
    print("Result: PASS", file=out)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Pre-screen a Beat Claude submission packet against the "
                    "public requirements in README.md and SCORING.md.",
    )
    parser.add_argument("path", type=Path,
                        help="submission file (.md/.txt) or directory of submission files")
    parser.add_argument("--strict", action="store_true",
                        help="treat advisory warnings as failures (exit 1)")
    args = parser.parse_args(argv)
    if not args.path.exists():
        parser.error(f"path does not exist: {args.path}")
    return run(args.path, strict=args.strict)


if __name__ == "__main__":
    sys.exit(main())
