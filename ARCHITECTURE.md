# How This Repo Works

This is the system-level overview of Beat Claude — how the pieces fit together, what defends the challenge against gaming, and how to maintain it. Candidates should start with the [README](README.md); this document is for maintainers, reviewers getting oriented, and the curious.

Beat Claude is the **public half** of Single Grain's hiring assessment. The private half — reviewer benchmarks, calibration notes, fixture answer keys, and follow-up exercises — lives outside this repo by design, and the tooling here actively enforces that separation.

## Repo Map

```
├── README.md                  # Candidate-facing entry point: rules, challenge index, packet
├── SCORING.md                 # Public evaluation guide: dimensions, evidence tiers, integrity policy
├── ARCHITECTURE.md            # This file
├── challenges/<name>/
│   ├── brief.md               # The challenge, version-stamped, with a required fixture section
│   ├── scoring_rubric.md      # Public, challenge-specific review guidance
│   ├── fixtures/              # Seeded dataset the candidate must actually work
│   └── (placeholder file)     # Withheld-benchmark notice; validator enforces its wording and size
├── submissions/README.md      # How to submit + what the pre-screen linter checks
├── leaderboard/HALL_OF_FAME.md
├── scripts/
│   ├── validate_submission.py     # Candidate/reviewer pre-screen linter
│   ├── validate_public_content.py # Repo-level leak and tamper guard (runs in CI)
│   └── rotate_fixture.py          # Maintainer tool: regenerate the intern-012 fixture + key
├── tests/                     # Guard the scripts and the repo's structural invariants
└── .github/workflows/         # CI: content validation + full test suite on every push/PR
```

## The Candidate Flow

1. Pick a challenge; the brief states its **version stamp** (e.g. `2026-07`).
2. Work the **fixture dataset** in the challenge folder: cite row ids, flag planted issues, state the fixture checksum.
3. Assemble the 7-part submission packet (README, "Required Submission Packet").
4. Self-check with `python3 scripts/validate_submission.py my_submission.md`.
5. Apply via the careers page. Review is blind, against private benchmark material, with spot verification and possible live follow-up.

## The Anti-Gaming System

The design goal: make the cheap attacks detectable by mechanism, so human judgment is spent only where it is genuinely needed. Layers, from outermost in:

1. **Fresh-baseline comparison.** Submissions are compared against a model-generated answer to the same brief produced at review time. Pasting the brief into an AI tool reaches that baseline; it never exceeds it.
2. **Evidence discipline.** Every number needs a source label; every high-tier claim needs something checkable (link, file, reproduction step). Unverifiable high-tier claims are downgraded to "claims only."
3. **Manipulation detection.** The pre-screen linter hard-fails on text that addresses a reviewing AI model, invisible/zero-width characters, and HTML comments aimed at the review. Quoted adversarial examples in code blocks/blockquotes are exempt. Manipulation is an automatic reject (SCORING.md, Integrity).
4. **Brief versioning.** Every brief carries a version stamp candidates must cite. Circulated answers to old versions identify themselves.
5. **Seeded fixtures.** Every role challenge ships a small synthetic dataset containing planted issues (duplicates, inflated metrics, compliance traps, adversarial inputs). Reviewers hold the private key of what is planted, so analysis quality is checked against ground truth rather than by impression. Candidates state the fixture checksum, which pins the exact dataset they worked from.
6. **Rotation.** Fixtures and briefs are refreshed between hiring rounds, so shared answers and leaked keys expire. The trap *categories* are public (rubrics name them); the per-rotation specifics are not.
7. **Live verification.** Strong or borderline submissions may be asked to re-run their work live on a fresh fixture, walk through the artifact, or re-derive their numbers. This is the backstop the automated layers funnel into.

No single layer is decisive; the system works because defeating all seven simultaneously requires doing the actual work — at which point the candidate has passed, not cheated.

## Tooling

### `scripts/validate_submission.py` — submission pre-screen
Run against a file or directory of `.md`/`.txt`. Checks, in order: required packet sections (**FAIL** if missing), review-manipulation signals (**FAIL**), verifiability of high-tier claims (warn), number source labels (warn), evidence-tier citations (warn), brief-version statement (warn). Exit 0 = pass (warnings allowed), exit 1 = fail; `--strict` promotes warnings to failures. Candidates and reviewers run the identical tool, so the first review pass is reproducible by the person being reviewed.

### `scripts/validate_public_content.py` — repo leak guard (CI)
Scans every text file for things that must never be public: answer-key references, private-key material, internal business specifics, and over-specific scoring detail. Challenge placeholder files are allowed only as short withheld-benchmark notices with exact required wording — so a benchmark answer cannot be committed even accidentally. An inline allow-marker exists for intentional mentions but is deliberately ignored under `challenges/**`, keeping candidate-facing files tamper-proof.

### `scripts/rotate_fixture.py` — fixture rotation (maintainers)
Regenerates the intern-012 fixture from the trap-archetype bank, deterministic per `--seed`, and emits the reviewer answer key **locally only** (stdout, or `--key-out` restricted to the gitignored `private/` directory). Role-challenge fixtures are rotated by editing the file against the private key spec.

## CI and Tests

`.github/workflows/validate-public-content.yml` runs on every push and PR: the leak guard, then the full test suite. The tests guard the invariants rather than just the code:

- `test_validate_submission.py` — linter behavior, including that manipulation detection fails hard and quoted adversarial input stays exempt.
- `test_validate_public_content.py` — the leak guard itself.
- `test_rotate_fixture.py` — rotation determinism, archetype coverage, and that answer keys cannot be written to a committable path.
- `test_challenge_fixtures.py` — every fixture a brief references exists, parses with uniform columns and unique ids, and every brief with a fixture states the checksum and rotation rules. A brief can never point at a missing or broken dataset.

## Maintenance Runbook

**Each hiring round:** rotate fixtures (script for intern-012; edit-against-key for role challenges), bump each touched brief's version stamp, update the private playbook's key tables and checksums, archive the old key tables for straggler submissions.

**Adding a challenge:** copy an existing folder's structure (brief with version stamp + fixture section, rubric with fixture-verification section, placeholder file, `fixtures/` dataset), add it to the README tables, record its answer key privately. CI enforces most of the structure automatically.

**After each review batch:** log per-trap catch rates; retire traps everyone catches, review traps nobody catches. This calibration loop is what keeps the fixtures discriminating.

**Never in this repo:** answer keys, rotation seeds, reviewer calibration notes, benchmark answers, real candidate data. The reviewer playbook (procedure + keys + current checksums) lives in the private reviewer drive. If a key leaks, rotate that fixture — the version/checksum system expires the leak.

---

**Brief version note:** this document describes the system as of brief version 2026-07.
