# Public Review Guide: Product Designer 005

This guide is challenge-specific but intentionally high level. Read [SCORING.md](../../SCORING.md) first: the five evaluation dimensions, the evidence tiers, and the number source labels apply to every challenge. Private reviewer calibration, answer benchmarks, and follow-up exercises are not published.

## What Strong Submissions Demonstrate

### 1. A diagnosis that uses the data given
The brief includes step-level drop-off data and user quotes. Strong submissions read them together: where the funnel actually loses people, what the quotes say about why, and which assumptions in the current flow those two sources contradict. Redesigns that do not engage with the largest drop-off step have missed the brief.

### 2. Business constraints treated as design inputs
Invites drive growth and integrations drive retention, so simply deleting those steps is not a redesign, it is a trade the business did not agree to. Strong answers show how to reach first value fast while preserving (or re-sequencing) those two mechanisms, and name the trade-off they are accepting.

### 3. Re-entry design for skipped steps
Whatever gets deferred needs a credible path back into the product experience. Strong submissions design the moment and the trigger for reintroducing invites and integrations, not just the removal.

### 4. A V1 honestly scoped to one sprint
Two weeks of engineering is the whole budget. Strong answers separate the full vision from the V1 cut, justify what ships first by expected impact, and say what they deliberately left out.

### 5. Measurement beyond completion rates
Strong success metrics distinguish "finished onboarding" from "reached value", include leading indicators visible within days, and define what result would falsify the redesign.

### 6. An inspectable design artifact
Wireframes, a wireflow, an annotated prototype, or a decision log that shows the reasoning at each screen. Fidelity matters less than visible judgment; the brief explicitly allows rough formats.

## Challenge-Specific Failure Modes

- **The frictionless-everything answer.** Deleting every step in the name of activation, ignoring the stated virality and retention mechanics. This is the most common generic response to this brief.
- **A redesign without the data.** Proposals that never reference the funnel table or user quotes provided.
- **Sprint denial.** A V1 that plainly needs a quarter of engineering, with no cut lines.
- **Unlabeled conversion promises.** Predicting the improved rate without labeling it as an estimate and showing the reasoning.

## Evidence That Matters for This Brief

- **Tier 2** is the floor: the redesigned flow itself, as wireframes or a clickable prototype, with annotations explaining each decision.
- **Tier 3** strengthens it: usability notes, test recordings, or research records from real users you put through the flow or a comparable one.
- **Tier 4** is the differentiator: before/after conversion data from an onboarding redesign you actually shipped, method stated.
- Label every number: the brief's figures are given (benchmarked), your projections are estimates or assumptions, and any of your own past results should carry sources.

Strong or close submissions may be asked to walk through the flow live and defend one trade-off against a changed constraint.

## Fixture Verification

The brief requires working the fixture dataset in `fixtures/onboarding_sessions.csv`. Reviewers hold the private key of seeded issues, so the fastest ways to lose are: analysis that never cites the data, conclusions that treat a planted issue as clean signal, and recommendations the fixture contradicts. Strong submissions cite specific ids, catch most of the seeded issues, state the fixture checksum, and say what they refused to conclude because the sample is small.

---

Format, page limits, and the full submission packet are defined in the challenge [brief](brief.md) and the repository [README](../../README.md). You can pre-screen your packet with `python3 scripts/validate_submission.py`.
