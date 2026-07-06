"""Tests for scripts/validate_public_content.py.

unittest-style so the suite runs with either
``python3 -m unittest discover tests`` or ``python3 -m pytest tests/``.
"""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_module():
    spec = importlib.util.spec_from_file_location(
        "validate_public_content", REPO_ROOT / "scripts" / "validate_public_content.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MOD = load_module()

VALID_PLACEHOLDER = """# Private Reviewer Benchmark Withheld: test-000

This public repository does not include model-generated answer keys, reviewer benchmarks, calibration notes, or private evaluation prompts.

Candidates should build their own operating artifact. Reviewers use a private benchmark and reviewer guide outside this repository to reduce rubric gaming.

Do not treat this placeholder as guidance for the content, structure, or target answer.
"""

BASELINE_NAME = "claude_baseline.md"  # beatclaude: allow


class ValidatePublicContentTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def write(self, rel: str, text: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def validate(self):
        return MOD.validate(self.root)

    def test_valid_withheld_placeholder_passes(self):
        self.write(f"challenges/test-000/{BASELINE_NAME}", VALID_PLACEHOLDER)
        self.assertEqual(self.validate(), [])

    def test_placeholder_with_code_fence_fails(self):
        self.write(
            f"challenges/test-000/{BASELINE_NAME}",
            VALID_PLACEHOLDER + "\n```python\nprint('answer')\n```\n",
        )
        failures = self.validate()
        self.assertTrue(failures)
        self.assertTrue(any("answer-style content" in f for f in failures), failures)

    def test_placeholder_with_approach_heading_fails(self):
        self.write(
            f"challenges/test-000/{BASELINE_NAME}",
            VALID_PLACEHOLDER + "\n## Approach\n\nDo the thing.\n",
        )
        failures = self.validate()
        self.assertTrue(any("answer-style content" in f for f in failures), failures)

    def test_placeholder_over_line_cap_fails(self):
        padding = "\n".join(f"Extra line {i}." for i in range(25))
        self.write(f"challenges/test-000/{BASELINE_NAME}", VALID_PLACEHOLDER + padding)
        failures = self.validate()
        self.assertTrue(any("line placeholder cap" in f for f in failures), failures)

    def test_placeholder_missing_marker_reports_which(self):
        text = VALID_PLACEHOLDER.replace(
            "Do not treat this placeholder as guidance for the content, structure, or target answer.",
            "See the brief.",
        )
        self.write(f"challenges/test-000/{BASELINE_NAME}", text)
        failures = self.validate()
        self.assertTrue(
            any("missing required withheld-placeholder marker" in f for f in failures), failures
        )

    def test_blocked_business_term_fails(self):
        self.write("challenges/test-000/brief.md", "We publish the salary band for each role.\n")
        failures = self.validate()
        self.assertTrue(any("HR/compensation specifics" in f for f in failures), failures)

    def test_non_baseline_file_named_like_baseline_flagged(self):
        self.write(f"notes/{BASELINE_NAME}", "Some stray file.\n")
        failures = self.validate()
        self.assertTrue(any("public answer-key filename/reference" in f for f in failures), failures)

    def test_baseline_reference_in_doc_flagged(self):
        self.write("README.md", f"See {BASELINE_NAME} for the answers.\n")
        failures = self.validate()
        self.assertTrue(any("public answer-key filename/reference" in f for f in failures), failures)

    def test_allowlisted_path_skipped(self):
        # scripts/validate_public_content.py is allowlisted even when it
        # contains otherwise-blocked terms.
        self.write("scripts/validate_public_content.py", "pattern = 'salary band'\n")
        self.assertEqual(self.validate(), [])

    def test_code_dirs_exempt_from_keyword_checks(self):
        # Generic secret/credential keywords in code and tests are handled by a
        # dedicated secret scanner, not this public-content lint.
        self.write("scripts/some_tool.py", "creds = load_credentials()\n")
        self.write("tests/test_some_tool.py", "password = 'not-a-real-one'\n")
        self.assertEqual(self.validate(), [])

    def test_private_key_material_flagged_even_in_code_dirs(self):
        # Actual secret material is a global check: the code-dir exemption for
        # generic keywords must not exempt pasted private keys.
        header = "-----BEGIN RSA " + "PRIVATE KEY-----"
        self.write("scripts/deploy_helper.py", f'KEY = """{header}\nMIIEow...\n"""\n')
        failures = self.validate()
        self.assertTrue(any("private key material" in f for f in failures), failures)

    def test_real_pem_header_variants_flagged_in_docs(self):
        for variant in ("RSA ", "OPENSSH ", "EC ", "ENCRYPTED ", ""):
            with self.subTest(variant=variant or "pkcs8"):
                path = self.write(
                    "notes.md", "-----BEGIN " + variant + "PRIVATE KEY-----\n"
                )
                failures = self.validate()
                self.assertTrue(
                    any("private key material" in f for f in failures), failures
                )
                path.unlink()

    def test_keyword_checks_still_apply_to_docs(self):
        self.write("submissions/notes.md", "Store your credentials in a vault.\n")
        failures = self.validate()
        self.assertTrue(any("secret or credential" in f for f in failures), failures)

    def test_inline_allow_marker_skips_line(self):
        self.write(
            "submissions/notes.md",
            "Never share credentials in a submission. <!-- beatclaude: allow -->\n",
        )
        self.assertEqual(self.validate(), [])

    def test_clean_repo_passes(self):
        self.write("README.md", "# Hello\n\nNothing sensitive here.\n")
        self.write("challenges/test-000/brief.md", "# Challenge\n\nDo good work.\n")
        self.assertEqual(self.validate(), [])

    def test_real_repo_passes(self):
        self.assertEqual(MOD.validate(REPO_ROOT), [])


if __name__ == "__main__":
    unittest.main()
