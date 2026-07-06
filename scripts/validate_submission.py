#!/usr/bin/env python3
"""Objective pre-screen linter for Beat Claude submission packets.

Candidates (and reviewers) can run this against a submission file or a
directory of submission files before review:

    python3 scripts/validate_submission.py path/to/submission.md
    python3 scripts/validate_submission.py path/to/submission_dir/ --strict

It checks three things:

1. Required packet sections (FAIL if missing): all 7 sections of the
   Required Submission Packet defined in README.md are present somewhere in
   the submission text.
2. Number source labels (advisory WARN): paragraphs containing numeric
   claims (percentages, dollar amounts, counts) should carry one of the
   [Observed] / [Estimated] / [Benchmarked] / [Assumed] labels from
   SCORING.md nearby. This is a heuristic; reviewers make the final call.
3. Evidence-tier citations (advisory WARN): major claims should reference
   the SCORING.md evidence tiers (Tier 0-5) in the evidence log.

Exit codes: 0 when all required sections are present (warnings allowed),
1 when required sections are missing, or when --strict is passed and any
warnings were produced.

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
        # Ignore numbers that only appear inside URLs/links.
        prose = URL_PATTERN.sub("", paragraph)
        if NUMBER_PATTERN.search(prose):
            snippet = " ".join(paragraph.split())[:100]
            flagged.append((line_no, snippet))
    return flagged


def count_evidence_tier_refs(text: str) -> int:
    return len(EVIDENCE_TIER_PATTERN.findall(text))


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

    # Check 2: number source labels (advisory).
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

    # Check 3: evidence-tier citations (advisory).
    tier_refs = count_evidence_tier_refs(combined)
    if tier_refs == 0:
        warnings += 1
        print("[WARN] Evidence tiers: no references to the SCORING.md evidence tiers "
              "(Tier 0-5) found; map each major claim to a proof tier in your evidence log", file=out)
    else:
        print(f"[PASS] Evidence tiers: {tier_refs} reference(s) to SCORING.md tiers found", file=out)

    print("", file=out)
    if failures:
        print("Result: FAIL (missing required packet sections)", file=out)
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
