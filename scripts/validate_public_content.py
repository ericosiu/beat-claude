#!/usr/bin/env python3
"""Lightweight public-content hardening checks.

Scans repository text files and paths (excluding generated/vendor dirs) for
public anti-gaming leaks: answer-key references, overly-specific private
business details, psychometric/medical-style assessments, internal agent names,
and accidental secrets.

Existing challenge ``claude_baseline.md`` files are allowed only when they are
short withheld-benchmark placeholders and contain no answer content.

Scoping notes:

- The business/keyword checks target public-facing docs (challenges/**,
  top-level markdown, templates). Files under ``scripts/`` and ``tests/`` are
  excluded from those checks because code and test fixtures legitimately use
  words like "credential" or "password" without leaking anything. Actual
  secret material (private key blocks) stays a global check because it is
  never legitimate anywhere in this repo, code included.
- A line containing the marker ``beatclaude: allow`` is skipped by all
  line-level checks, so intentional mentions do not require editing this
  checker. Use sparingly and only for clearly benign content.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__"}
TEXT_EXTS = {".md", ".txt", ".yml", ".yaml", ".json", ".toml", ".py"}

# Inline per-line allowlist marker: lines containing this string are skipped
# by all line-level checks (path-level checks still apply).
INLINE_ALLOW_MARKER = "beatclaude: allow"

ANSWER_KEY_CHECK = ("public answer-key filename/reference", re.compile(r"claude_baseline", re.I))

# Checks that apply to every scanned file. Leaking an answer-key reference or
# private key material is a problem anywhere in the repo, including code.
# The key pattern anchors on the PEM dashes and tolerates the algorithm
# word(s) real headers carry (RSA/OPENSSH/EC/ENCRYPTED/...), which
# "BEGIN <one-word> KEY" missed; prose about keys never matches.
GLOBAL_CHECKS: list[tuple[str, re.Pattern[str]]] = [
    ANSWER_KEY_CHECK,
    ("private key material", re.compile(r"-----BEGIN\s+(?:[A-Z0-9]+\s+)*PRIVATE\s+KEY-----", re.I)),
]

# Business-specific keyword checks, scoped to public-facing content only
# (everything except scripts/ and tests/ -- see module docstring).
SCOPED_CHECKS: list[tuple[str, re.Pattern[str]]] = [
    ("over-specific public scoring", re.compile(r"exact\s+point\s+bands?|private\s+curveballs?", re.I)),
    ("internal revenue detail", re.compile(r"\b(MRR|P\s*&\s*L|profit\s+and\s+loss|revenue\s+target|multi-million\s+annual)\b", re.I)),
    ("HR/compensation specifics", re.compile(r"\b(compensation\s+bands?|comp\s+bands?|salary\s+band|offer\s+acceptance\s+rate|90-day\s+new\s+hire\s+retention|time-to-fill|mis-hire|FAANG)\b", re.I)),
    ("CEO psychometrics or medical-style self-assessment", re.compile(r"\b(MMPI|ENTJ|enneagram|8w7|Kolbe|psychometric|personality\s+assessment)\b", re.I)),
    ("internal agent/system names", re.compile(r"\b(Oracle|Cyborg|Flash|Alfred|Single\s+Brain|Mission\s+Control)\b", re.I)),
    ("internal product-level targets", re.compile(r"\b(ClickFlow|Karrot)\b.*\b(MRR|target|quota|churn|lost\s+\d+\s+customers)\b|\b(MRR|target|quota|churn)\b.*\b(ClickFlow|Karrot)\b", re.I)),
    ("secret or credential", re.compile(r"\b(api[_-]?key|secret[_-]?key|password\s*=|credentials?)\b", re.I)),
]

ALLOWLIST = {
    Path("scripts/validate_public_content.py"),
}

# Directories whose files are code, not public candidate-facing content.
# Scoped (business keyword) checks do not apply there.
CODE_DIRS = {"scripts", "tests"}

WITHHELD_PLACEHOLDER_MARKERS = (
    "This public repository does not include model-generated answer keys",
    "Reviewers use a private benchmark and reviewer guide outside this repository",
    "Do not treat this placeholder as guidance for the content, structure, or target answer",
)
WITHHELD_BASELINE_MAX_LINES = 20
ANSWER_CONTENT_PATTERN = re.compile(
    r"(^|\n)```|(^|\n)#{2,}\s+(executive summary|answer|solution|approach|plan|recommendations?)\b",
    re.I,
)


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for p in root.rglob("*"):
        if any(part in SKIP_DIRS for part in p.relative_to(root).parts):
            continue
        if p.is_file() and p.suffix.lower() in TEXT_EXTS:
            files.append(p)
    return sorted(files)


def is_code_path(rel: Path) -> bool:
    return bool(rel.parts) and rel.parts[0] in CODE_DIRS


def is_challenge_baseline_path(rel: Path) -> bool:
    """True for challenges/<name>/claude_baseline.md paths."""
    return len(rel.parts) == 3 and rel.parts[0] == "challenges" and rel.name == "claude_baseline.md"


def withheld_baseline_problems(text: str) -> list[str]:
    """Return the specific reasons a baseline file fails the withheld-placeholder
    exemption. Empty list means the file is an allowed placeholder."""
    problems: list[str] = []
    for marker in WITHHELD_PLACEHOLDER_MARKERS:
        if marker not in text:
            problems.append(f'missing required withheld-placeholder marker: "{marker}"')
    line_count = len(text.splitlines())
    if line_count > WITHHELD_BASELINE_MAX_LINES:
        problems.append(
            f"exceeds the {WITHHELD_BASELINE_MAX_LINES}-line placeholder cap ({line_count} lines)"
        )
    if ANSWER_CONTENT_PATTERN.search(text):
        problems.append(
            "contains answer-style content (code fence or an answer/solution/approach/plan heading)"
        )
    return problems


def checks_for(rel: Path) -> list[tuple[str, re.Pattern[str]]]:
    if is_code_path(rel):
        return list(GLOBAL_CHECKS)
    return GLOBAL_CHECKS + SCOPED_CHECKS


def validate(root: Path) -> list[str]:
    failures: list[str] = []
    for path in iter_files(root):
        rel = path.relative_to(root)
        if rel in ALLOWLIST:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        checks = checks_for(rel)

        # Challenge baseline files get a dedicated exemption path with specific
        # error messages instead of the generic answer-key violation.
        is_baseline = is_challenge_baseline_path(rel)
        if is_baseline:
            for problem in withheld_baseline_problems(text):
                failures.append(f"{rel}: withheld-baseline exemption failed: {problem}")

        for label, pattern in checks:
            if is_baseline and (label, pattern) == ANSWER_KEY_CHECK:
                continue
            if pattern.search(rel.as_posix()):
                failures.append(f"{rel}: path: {label}")

        for line_no, line in enumerate(text.splitlines(), 1):
            if INLINE_ALLOW_MARKER in line:
                continue
            for label, pattern in checks:
                if is_baseline and (label, pattern) == ANSWER_KEY_CHECK:
                    continue
                if pattern.search(line):
                    failures.append(f"{rel}:{line_no}: {label}: {line.strip()[:160]}")
    return failures


def main() -> int:
    failures = validate(ROOT)
    if failures:
        print("Public content validation failed:\n")
        print("\n".join(failures))
        return 1
    print("Public content validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
