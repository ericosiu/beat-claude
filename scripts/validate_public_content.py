#!/usr/bin/env python3
"""Lightweight public-content hardening checks.

Scans repository text files and paths (excluding generated/vendor dirs) for
public anti-gaming leaks: answer-key references, overly-specific private
business details, psychometric/medical-style assessments, internal agent names,
and accidental secrets.

Existing challenge ``claude_baseline.md`` files are allowed only when they are
short withheld-benchmark placeholders and contain no answer content.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__"}
TEXT_EXTS = {".md", ".txt", ".yml", ".yaml", ".json", ".toml", ".py"}

ANSWER_KEY_CHECK = ("public answer-key filename/reference", re.compile(r"claude_baseline", re.I))
CHECKS: list[tuple[str, re.Pattern[str]]] = [
    ANSWER_KEY_CHECK,
    ("over-specific public scoring", re.compile(r"exact\s+point\s+bands?|private\s+curveballs?", re.I)),
    ("internal revenue detail", re.compile(r"\b(MRR|P\s*&\s*L|profit\s+and\s+loss|revenue\s+target|multi-million\s+annual)\b", re.I)),
    ("HR/compensation specifics", re.compile(r"\b(compensation\s+bands?|comp\s+bands?|salary\s+band|offer\s+acceptance\s+rate|90-day\s+new\s+hire\s+retention|time-to-fill|mis-hire|FAANG)\b", re.I)),
    ("CEO psychometrics or medical-style self-assessment", re.compile(r"\b(MMPI|ENTJ|enneagram|8w7|Kolbe|psychometric|personality\s+assessment)\b", re.I)),
    ("internal agent/system names", re.compile(r"\b(Oracle|Cyborg|Flash|Alfred|Single\s+Brain|Mission\s+Control)\b", re.I)),
    ("internal product-level targets", re.compile(r"\b(ClickFlow|Karrot)\b.*\b(MRR|target|quota|churn|lost\s+\d+\s+customers)\b|\b(MRR|target|quota|churn)\b.*\b(ClickFlow|Karrot)\b", re.I)),
    ("secret or credential", re.compile(r"\b(api[_-]?key|secret[_-]?key|password\s*=|BEGIN\s+(RSA|OPENSSH|PRIVATE)\s+KEY|credentials?)\b", re.I)),
]

ALLOWLIST = {
    Path("scripts/validate_public_content.py"),
}

WITHHELD_PLACEHOLDER_MARKERS = (
    "This public repository does not include model-generated answer keys",
    "Reviewers use a private benchmark and reviewer guide outside this repository",
    "Do not treat this placeholder as guidance for the content, structure, or target answer",
)
ANSWER_CONTENT_PATTERN = re.compile(
    r"(^|\n)```|(^|\n)#{2,}\s+(executive summary|answer|solution|approach|plan|recommendations?)\b",
    re.I,
)


def iter_files() -> list[Path]:
    files: list[Path] = []
    for p in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        if p.is_file() and p.suffix.lower() in TEXT_EXTS:
            files.append(p)
    return sorted(files)


def is_allowed_withheld_baseline(rel: Path, text: str) -> bool:
    """Allow only existing challenge placeholder baselines, not answer content."""
    if len(rel.parts) != 3 or rel.parts[0] != "challenges" or rel.name != "claude_baseline.md":
        return False
    if not all(marker in text for marker in WITHHELD_PLACEHOLDER_MARKERS):
        return False
    if len(text.splitlines()) > 20:
        return False
    if ANSWER_CONTENT_PATTERN.search(text):
        return False
    return True


def main() -> int:
    failures: list[str] = []
    for path in iter_files():
        rel = path.relative_to(ROOT)
        if rel in ALLOWLIST:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        allowed_withheld_baseline = is_allowed_withheld_baseline(rel, text)

        for label, pattern in CHECKS:
            if allowed_withheld_baseline and (label, pattern) == ANSWER_KEY_CHECK:
                continue
            if pattern.search(rel.as_posix()):
                failures.append(f"{rel}: path: {label}")

        for line_no, line in enumerate(text.splitlines(), 1):
            for label, pattern in CHECKS:
                if allowed_withheld_baseline and (label, pattern) == ANSWER_KEY_CHECK:
                    continue
                if pattern.search(line):
                    failures.append(f"{rel}:{line_no}: {label}: {line.strip()[:160]}")
    if failures:
        print("Public content validation failed:\n")
        print("\n".join(failures))
        return 1
    print("Public content validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
