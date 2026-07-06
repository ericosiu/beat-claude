"""Tests for scripts/validate_submission.py.

unittest-style so the suite runs with either
``python3 -m unittest discover tests`` or ``python3 -m pytest tests/``.
"""
from __future__ import annotations

import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_module():
    spec = importlib.util.spec_from_file_location(
        "validate_submission", REPO_ROOT / "scripts" / "validate_submission.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MOD = load_module()

COMPLETE_SUBMISSION = """# Written Answer

My plan focuses on two channels. [Estimated] Ramp-up should take 6 weeks.

## Operating Artifact

Budget model spreadsheet, view-only link below.

## Evidence Log

- Claim: prior campaign improved conversion. Tier 3 (analytics export).
- Claim: workflow runs end to end. Tier 2 (demo recording).

## Number Source Labels

- [Observed] 48 leads entered the sheet last week.
- [Benchmarked] 2% to 5% reply rate from public outbound benchmarks.

## AI Usage Disclosure

Used an LLM for first-draft copy; I rewrote the pricing logic and checked the math.

## Failure Handling

What breaks it: API rate limits under load; detected via a daily error digest.

## Artifact Access

View-only link with sample data, no login required.
"""

INCOMPLETE_SUBMISSION = """# My Strategy

We will grow traffic by 40% and spend $100K over 90 days.

## AI Usage Disclosure

I used AI tools for drafting.
"""


class HelperTests(unittest.TestCase):
    def test_all_sections_found(self):
        self.assertEqual(MOD.check_sections(COMPLETE_SUBMISSION), [])

    def test_missing_sections_reported(self):
        missing = MOD.check_sections(INCOMPLETE_SUBMISSION)
        self.assertIn("Written answer", missing)
        self.assertIn("Operating artifact", missing)
        self.assertIn("Evidence log", missing)
        self.assertIn("Artifact access", missing)
        self.assertNotIn("AI usage disclosure", missing)

    def test_what_breaks_counts_as_failure_handling(self):
        self.assertNotIn("Failure handling", MOD.check_sections("### What breaks it\n"))

    def test_unlabeled_numbers_flagged(self):
        flagged = MOD.find_unlabeled_numbers("We doubled output.\n\nRevenue grew 40% last quarter.\n")
        self.assertEqual(len(flagged), 1)
        self.assertIn("40%", flagged[0][1])

    def test_labeled_numbers_not_flagged(self):
        flagged = MOD.find_unlabeled_numbers("[Observed] Revenue grew 40% last quarter.\n")
        self.assertEqual(flagged, [])

    def test_numbers_in_code_fences_and_headings_ignored(self):
        text = "## 90-Day Plan\n\n```\nx = 100\n```\n\nNo claims here.\n"
        self.assertEqual(MOD.find_unlabeled_numbers(text), [])

    def test_numbers_only_in_urls_ignored(self):
        text = "See https://example.com/report/2024/40 for details.\n"
        self.assertEqual(MOD.find_unlabeled_numbers(text), [])

    def test_evidence_tier_refs_counted(self):
        self.assertEqual(MOD.count_evidence_tier_refs("Tier 3 proof and tier 2 demo."), 2)
        self.assertEqual(MOD.count_evidence_tier_refs("No proof levels named."), 0)


class RunTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def write(self, name: str, text: str) -> Path:
        path = self.dir / name
        path.write_text(text, encoding="utf-8")
        return path

    def run_validator(self, target: Path, strict: bool = False):
        out = io.StringIO()
        code = MOD.run(target, strict=strict, out=out)
        return code, out.getvalue()

    def test_complete_submission_passes(self):
        path = self.write("submission.md", COMPLETE_SUBMISSION)
        code, report = self.run_validator(path)
        self.assertEqual(code, 0)
        self.assertIn("[PASS] Required packet sections", report)
        self.assertIn("Result: PASS", report)

    def test_missing_sections_fail(self):
        path = self.write("submission.md", INCOMPLETE_SUBMISSION)
        code, report = self.run_validator(path)
        self.assertEqual(code, 1)
        self.assertIn("[FAIL] Required packet sections", report)
        self.assertIn("Result: FAIL", report)

    def test_unlabeled_numbers_warn_but_pass(self):
        text = COMPLETE_SUBMISSION + "\nOur pipeline produced 500 records overnight.\n"
        path = self.write("submission.md", text)
        code, report = self.run_validator(path)
        self.assertEqual(code, 0)
        self.assertIn("[WARN] Number source labels", report)
        self.assertIn("Result: PASS with warnings", report)

    def test_strict_turns_warnings_into_failures(self):
        text = COMPLETE_SUBMISSION + "\nOur pipeline produced 500 records overnight.\n"
        path = self.write("submission.md", text)
        code, report = self.run_validator(path, strict=True)
        self.assertEqual(code, 1)
        self.assertIn("--strict", report)

    def test_missing_tier_references_warn(self):
        text = COMPLETE_SUBMISSION.replace("Tier 3", "strong").replace("Tier 2", "solid")
        path = self.write("submission.md", text)
        code, report = self.run_validator(path)
        self.assertEqual(code, 0)
        self.assertIn("[WARN] Evidence tiers", report)

    def test_directory_input_combines_files(self):
        # Sections split across multiple files still satisfy the packet check.
        self.write("answer.md", COMPLETE_SUBMISSION.split("## Evidence Log")[0])
        self.write("evidence.md", "## Evidence Log" + COMPLETE_SUBMISSION.split("## Evidence Log")[1])
        code, report = self.run_validator(self.dir)
        self.assertEqual(code, 0)
        self.assertIn("Files checked: 2", report)

    def test_empty_directory_fails(self):
        code, report = self.run_validator(self.dir)
        self.assertEqual(code, 1)
        self.assertIn("no readable text files", report)

    def test_main_help_and_missing_path(self):
        with self.assertRaises(SystemExit) as ctx:
            MOD.main([str(self.dir / "does-not-exist.md")])
        self.assertNotEqual(ctx.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
