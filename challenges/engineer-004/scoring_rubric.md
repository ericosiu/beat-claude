# Public Review Guide: Engineer 004

This guide is challenge-specific but intentionally high level. Read [SCORING.md](../../SCORING.md) first: the five evaluation dimensions, the evidence tiers, and the number source labels apply to every challenge. Private reviewer calibration, answer benchmarks, and follow-up exercises are not published.

## What Strong Submissions Demonstrate

### 1. Alternatives considered, not just components named
Strong designs explain why each technology was chosen over the obvious alternatives, in terms of this brief's latency target, event volume, team size, and budget ceiling. A component diagram without rejected options reads as a tutorial, not a decision.

### 2. Arithmetic that survives inspection
Throughput, storage, and cost claims should come with visible back-of-envelope math, and every input labeled as observed, benchmarked, or assumed. Strong submissions size the system for the stated spike multiplier and show the cost estimate against the stated ceiling.

### 3. A migration plan that takes the constraint seriously
Existing integrations cannot break and the SDK cannot change. Strong answers show a phased cutover with validation (for example, parallel-run comparison), a rollback trigger, and a definition of "data accuracy verified" that is testable. This section separates operators from diagram authors.

### 4. Failure design for the unhappy paths
The current system loses events under load. Strong designs state their delivery guarantees precisely, show where backpressure and buffering live, what degrades first under overload, and how loss or duplication would be detected rather than assumed away.

### 5. Compliance treated as architecture
Deletion requests, multi-tenancy, and audit requirements shape data layout and retention. Strong submissions design for them up front; bolting them on later is a known trap for this kind of pipeline.

### 6. Scope discipline
Two dedicated engineers and a phased timeline are the real budget. Strong answers say what the MVP excludes and what they would do differently with more time or money, as the brief asks.

## Challenge-Specific Failure Modes

- **Buzzword architecture.** Naming a fashionable stack with no data-flow reasoning, sizing math, or connection to the constraints. This is the default generic-AI answer for this brief.
- **The skipped migration.** A clean greenfield design that never explains how 500+ customers move without breakage. The migration is most of the actual risk.
- **Unlabeled performance claims.** Latency and throughput figures asserted without stating whether they are benchmarked, estimated, or assumed.
- **Over-engineering.** A design that a dozen-person company could not build or operate, ignoring the team and budget in the brief.

## Evidence That Matters for This Brief

- **Tier 2** is the floor: the architecture diagram plus a design doc a reviewer can interrogate; better, a small repo or runnable prototype of the riskiest component.
- **Tier 3** strengthens it: benchmark runs, load-test output, traces, or cost calculations with sources shown.
- **Tier 4** is the differentiator: measured before/after from a comparable system you actually built or fixed, method stated.
- In your evidence log, tie each headline claim (latency, loss rate, cost) to its tier. "It should handle it" is Tier 0.

Strong or close submissions may be asked to walk through the design live with a changed constraint, such as a tighter budget or a new compliance requirement.

## Fixture Verification

The brief requires working the fixture dataset in `fixtures/event_sample.jsonl`. Reviewers hold the private key of seeded issues, so the fastest ways to lose are: analysis that never cites the data, conclusions that treat a planted issue as clean signal, and recommendations the fixture contradicts. Strong submissions cite specific ids, catch most of the seeded issues, state the fixture checksum, and say what they refused to conclude because the sample is small.

---

Format, page limits, and the full submission packet are defined in the challenge [brief](brief.md) and the repository [README](../../README.md). You can pre-screen your packet with `python3 scripts/validate_submission.py`.
