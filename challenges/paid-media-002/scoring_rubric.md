# Public Review Guide: Paid Media 002

This guide is challenge-specific but intentionally high level. Read [SCORING.md](../../SCORING.md) first: the five evaluation dimensions, the evidence tiers, and the number source labels apply to every challenge. Private reviewer calibration, answer benchmarks, and follow-up exercises are not published.

## What Strong Submissions Demonstrate

### 1. Scaling gated by evidence, not by the calendar
The brief asks for a month-by-month ramp. Strong plans define decision points: what observed efficiency at each spend level triggers the next increase, a hold, or a pullback. Weak plans just draw a straight line to the target spend.

### 2. Channel-specific architecture, not a generic account plan
Buying behavior on search, professional networks, and social differs, and the brief's audience is a niche vertical with a limited addressable market. Strong submissions show campaign structures, audience segmentation, and creative logic tailored per channel, and reason about saturation before proposing new channels.

### 3. Efficiency math that acknowledges lag
With a sales cycle measured in weeks, spend scales faster than closed-won data arrives. Strong answers pick leading indicators, explain their attribution approach and its known blind spots, and avoid pretending the funnel reports in real time.

### 4. A creative system that survives the constraints
Team is maxed out and hiring is frozen for a quarter. Strong plans show how creative volume and freshness scale anyway (process, contractors, tooling, AI-assisted production with human review), while respecting the brand guidelines in the brief.

### 5. An artifact that does budgeting work
The strongest artifacts are working models or trackers: spend progression with labeled efficiency assumptions at each level, an experiment log with decision rules, or a build sheet a media buyer could execute from.

### 6. Named risks with detection plans
Strong submissions say what blows up efficiency at higher spend (audience saturation, creative fatigue, funnel bottlenecks downstream of media), how each would show up in the data, and what the response is.

## Challenge-Specific Failure Modes

- **Linear scaling.** Multiplying current spend without addressing why efficiency holds as budgets rise in a bounded market.
- **Asserted efficiency numbers.** Projected acquisition costs at higher spend levels stated as fact. These are estimates or benchmarks and must be labeled.
- **Ignoring the operating constraints.** Plans that require immediate headcount, or that quietly drop the seasonality and brand-guideline constraints in the brief.
- **Channel tourism.** Adding several new channels at once with no test design, success criteria, or kill rules.

## Evidence That Matters for This Brief

- **Tier 2** is the floor: the scaling model, experiment tracker, or account architecture itself, inspectable with labeled assumptions.
- **Tier 3** strengthens it: named sources for benchmarked rates, or records from real accounts you have scaled (sanitized).
- **Tier 4** is the differentiator: before/after data from a scaling exercise you actually ran, with method stated.
- Map each major claim (efficiency at each spend level, channel mix, creative cadence) to a tier in your evidence log. Reviewers specifically check whether projected performance is labeled honestly.

Strong or close submissions may be asked to walk through the model with a changed constraint, such as a mid-ramp efficiency miss.

## Fixture Verification

The brief requires working the fixture dataset in `fixtures/campaign_export.csv`. Reviewers hold the private key of seeded issues, so the fastest ways to lose are: analysis that never cites the data, conclusions that treat a planted issue as clean signal, and recommendations the fixture contradicts. Strong submissions cite specific ids, catch most of the seeded issues, state the fixture checksum, and say what they refused to conclude because the sample is small.

---

Format, page limits, and the full submission packet are defined in the challenge [brief](brief.md) and the repository [README](../../README.md). You can pre-screen your packet with `python3 scripts/validate_submission.py`.
