"""Repo-integrity tests for challenge fixture datasets.

Every fixture a brief references must exist and be loadable, so a brief
never sends candidates to a broken or missing dataset.

unittest-style so the suite runs with either
``python3 -m unittest discover tests`` or ``python3 -m pytest tests/``.
"""
from __future__ import annotations

import csv
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHALLENGES = REPO_ROOT / "challenges"

FIXTURE_REF = re.compile(r"((?:\.\./[\w-]+/)?)fixtures/([\w.-]+\.(?:csv|jsonl))")


def referenced_fixtures() -> dict[Path, list[Path]]:
    """Map each brief to the fixture paths it references, resolving
    cross-challenge references like ``../other-challenge/fixtures/x.csv``."""
    refs: dict[Path, list[Path]] = {}
    for brief in sorted(CHALLENGES.glob("*/brief.md")):
        found = set(FIXTURE_REF.findall(brief.read_text(encoding="utf-8")))
        refs[brief] = sorted(
            (brief.parent / prefix / "fixtures" / name).resolve()
            for prefix, name in found
        )
    return refs


def own_fixtures(brief: Path, fixtures: list[Path]) -> list[Path]:
    """Fixtures that live in the brief's own challenge folder."""
    return [f for f in fixtures if f.parent.parent == brief.parent.resolve()]


class FixtureIntegrityTests(unittest.TestCase):
    def test_every_referenced_fixture_exists_and_is_nonempty(self):
        refs = referenced_fixtures()
        self.assertTrue(any(refs.values()), "no fixture references found in any brief")
        for brief, fixtures in refs.items():
            for fixture in fixtures:
                with self.subTest(brief=brief.parent.name, fixture=fixture.name):
                    self.assertTrue(fixture.is_file(), f"missing fixture: {fixture}")
                    self.assertGreater(fixture.stat().st_size, 0)

    def test_every_fixture_on_disk_is_referenced_by_its_brief(self):
        refs = referenced_fixtures()
        for fixture_dir in sorted(CHALLENGES.glob("*/fixtures")):
            brief = fixture_dir.parent / "brief.md"
            referenced = {p.name for p in own_fixtures(brief, refs.get(brief, []))}
            for fixture in sorted(fixture_dir.iterdir()):
                with self.subTest(fixture=fixture):
                    self.assertIn(fixture.name, referenced,
                                  f"{fixture} exists but {brief} never references it")

    def test_csv_fixtures_parse_with_uniform_columns(self):
        for brief, fixtures in referenced_fixtures().items():
            for fixture in fixtures:
                if fixture.suffix != ".csv" or not fixture.is_file():
                    continue
                with self.subTest(fixture=fixture.name):
                    with open(fixture, encoding="utf-8", newline="") as fh:
                        rows = list(csv.reader(fh))
                    self.assertGreaterEqual(len(rows), 11, "fixture suspiciously small")
                    widths = {len(row) for row in rows}
                    self.assertEqual(len(widths), 1, f"ragged rows in {fixture.name}")
                    ids = [row[0] for row in rows[1:]]
                    self.assertEqual(len(ids), len(set(ids)), "duplicate primary ids")

    def test_briefs_with_fixtures_state_rotation_and_checksum(self):
        # Only briefs whose own folder carries a fixture must state the
        # checksum/rotation block; merely pointing at another challenge's
        # fixture (e.g. intern-011 -> intern-012) doesn't require it.
        for brief, fixtures in referenced_fixtures().items():
            if not own_fixtures(brief, fixtures):
                continue
            text = brief.read_text(encoding="utf-8")
            with self.subTest(brief=brief.parent.name):
                self.assertIn("shasum -a 256", text)
                self.assertRegex(text, re.compile(r"rotates?\s+between\s+hiring\s+rounds", re.I))


if __name__ == "__main__":
    unittest.main()
