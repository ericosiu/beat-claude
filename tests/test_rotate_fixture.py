"""Tests for scripts/rotate_fixture.py.

unittest-style so the suite runs with either
``python3 -m unittest discover tests`` or ``python3 -m pytest tests/``.
"""
from __future__ import annotations

import csv
import importlib.util
import io
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_module():
    spec = importlib.util.spec_from_file_location(
        "rotate_fixture", REPO_ROOT / "scripts" / "rotate_fixture.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MOD = load_module()

REQUIRED_ARCHETYPES = {
    "clean_qualify", "duplicate", "student_reject", "resubmission",
    "missing_email", "non_numeric_budget", "prompt_injection",
    "conflicting_signals", "unverifiable_vip", "non_english", "junk",
    "competitor_fishing", "malformed_date", "disposable_email",
    "nurture_timeline", "html_noise", "string_budget", "empty_message",
    "privacy_request", "phishing",
}


class GenerateTests(unittest.TestCase):
    def test_deterministic_per_seed(self):
        self.assertEqual(MOD.generate(7), MOD.generate(7))

    def test_different_seeds_differ(self):
        self.assertNotEqual(MOD.generate(1)[0], MOD.generate(2)[0])

    def test_all_trap_archetypes_present(self):
        _, key_rows = MOD.generate(3)
        self.assertEqual({k["archetype"] for k in key_rows}, REQUIRED_ARCHETYPES)

    def test_fixture_and_key_align(self):
        fixture_rows, key_rows = MOD.generate(11)
        self.assertEqual(len(fixture_rows), len(key_rows))
        self.assertEqual([r["lead_id"] for r in fixture_rows],
                         [k["lead_id"] for k in key_rows])

    def test_key_decisions_are_valid(self):
        _, key_rows = MOD.generate(5)
        for k in key_rows:
            self.assertIn(k["expected_decision"],
                          {"QUALIFY", "NURTURE", "REJECT", "ESCALATE"})
            self.assertTrue(k["reviewer_note"])

    def test_csv_round_trips_with_schema(self):
        fixture_rows, _ = MOD.generate(9)
        parsed = list(csv.DictReader(io.StringIO(MOD.to_csv(fixture_rows, MOD.FIELDNAMES))))
        self.assertEqual(len(parsed), len(fixture_rows))
        self.assertEqual(list(parsed[0].keys()), MOD.FIELDNAMES)
        self.assertTrue(all(None not in row.values() for row in parsed))

    def test_duplicate_shares_email_with_clean_qualify(self):
        fixture_rows, key_rows = MOD.generate(13)
        by_arch = {k["archetype"]: r for k, r in zip(key_rows, fixture_rows)}
        self.assertEqual(by_arch["duplicate"]["email"], by_arch["clean_qualify"]["email"])
        self.assertEqual(by_arch["resubmission"]["email"], by_arch["student_reject"]["email"])

    def test_injection_row_is_seeded(self):
        fixture_rows, key_rows = MOD.generate(17)
        by_arch = {k["archetype"]: r for k, r in zip(key_rows, fixture_rows)}
        message = by_arch["prompt_injection"]["message"].lower()
        self.assertTrue(any(w in message for w in ("ignore", "disregard", "forget")))
        self.assertIn("13-45", by_arch["malformed_date"]["submitted_at"])
        self.assertEqual(by_arch["empty_message"]["message"], "")
        self.assertEqual(by_arch["missing_email"]["email"], "")

    def test_key_out_refuses_committable_paths(self):
        with self.assertRaises(SystemExit):
            MOD.main(["--seed", "1", "--key-out", "answer_key.csv"])


class ShippedFixtureTests(unittest.TestCase):
    def test_shipped_fixture_matches_schema(self):
        with open(MOD.FIXTURE_PATH, encoding="utf-8") as fh:
            parsed = list(csv.DictReader(fh))
        self.assertEqual(list(parsed[0].keys()), MOD.FIELDNAMES)
        self.assertTrue(all(None not in row.values() for row in parsed))
        self.assertGreaterEqual(len(parsed), 20)


if __name__ == "__main__":
    unittest.main()
