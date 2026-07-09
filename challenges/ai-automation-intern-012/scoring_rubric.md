# Public Review Guide: AI Automation Intern 012

This guide is challenge-specific but intentionally high level. Read [SCORING.md](../../SCORING.md) first: the five evaluation dimensions, the evidence tiers, and the number source labels apply to every challenge. Private reviewer calibration, answer benchmarks, the seeded-trap answer key, and follow-up fixtures are not published.

## What Strong Submissions Demonstrate

### 1. A complete run against the fixture
Every row of `fixtures/inbound_leads.csv` appears in the decisions file with a decision, reason, and confidence, and the run log shows the run that produced it. Partial runs and hand-written "outputs" are the fastest way to lose: reviewers know the fixture, so fabricated decisions are obvious.

### 2. The traps, found and named
The fixture seeds duplicates, missing and malformed fields, conflicting signals, sensitive requests, and adversarial text. Strong submissions catch most of them, route the right ones to a human with a stated reason, and explain in the write-up why each trap row is a trap. Confidently qualifying a trap row is the core failure this challenge is built to catch.

### 3. Data treated as data
At least one row tries to give your agent instructions. Strong agents classify it on its merits and flag the manipulation attempt; weak agents obey it. Reviewers check this row first.

### 4. Escalation with judgment
`ESCALATE` is not a dumping ground. Strong submissions escalate the rows where a wrong automated call is costly or the input is untrustworthy, and decide the rest. Escalating everything and escalating nothing are both weak.

### 5. A bad output, owned
The required bad-output example is a judgment probe. Strong answers show a genuine miss from their own run, how they caught it, and what changed. "My agent got everything right" reads as untested.

### 6. Scoping under a time limit
A working loop with honest gaps beats an unfinished platform. Strong submissions say what they would harden before this ran on real volume.

## Challenge-Specific Failure Modes

- **The fabricated run.** A decisions file with no log, or decisions that don't match what the described agent would produce. The fixture is seeded so this surfaces fast.
- **The obedient agent.** Following instructions embedded in lead text.
- **The happy-path demo.** Clean rows handled, messy rows skipped or silently mangled.
- **The stale answer.** A submission built against an old fixture version; the checksum and version stamp expose it.

## Evidence That Matters for This Brief

- **Tier 2** is the floor: the agent itself, inspectable or watchable, plus the decisions file.
- **Tier 3** is where strong submissions live: run logs, prompt traces, and per-row outputs a reviewer can trace to the fixture.
- **Tier 4** is the differentiator: a measured comparison, such as agent decisions versus your own manual pass, with disagreements analyzed and every number labeled.
- Label your numbers (row counts, accuracy claims, time spent) as observed, estimated, benchmarked, or assumed.

Strong or close submissions may be asked to re-run the agent live on a fresh fixture.

---

Format, page limits, and the full submission packet are defined in the challenge [brief](brief.md) and the repository [README](../../README.md). You can pre-screen your packet with `python3 scripts/validate_submission.py`.
