# Public Review Guide: Sales AE 006

This guide is challenge-specific but intentionally high level. Read [SCORING.md](../../SCORING.md) first: the five evaluation dimensions, the evidence tiers, and the number source labels apply to every challenge. Private reviewer calibration, answer benchmarks, and follow-up exercises are not published.

## What Strong Submissions Demonstrate

### 1. A diagnosis grounded in the facts provided
The brief seeds specific signals: the finance blocker's history, the disengaged executive, the champion's incentives, the timing of budgets and the incumbent's renewal. Strong submissions read those facts and commit to a specific theory of why the deal is actually stalled, then build the plan from that theory.

### 2. Stakeholder strategy with a theory of each person
Strong answers treat each named stakeholder as someone with their own risk, incentive, and preferred proof, and design a distinct move for each, within the brief's constraints (limited executive meetings, no going around the champion). Generic "multi-thread the account" advice does not clear the bar.

### 3. An objection strategy that addresses risk, not just price
The blocker's stated concern is cost, but the brief hints the real concern may be implementation risk. Strong submissions distinguish the stated objection from the likely underlying one and choose proof (references, phasing, terms) accordingly, while respecting the discount policy.

### 4. Urgency built from the buyer's calendar
The fiscal-year timing, expiring budget, and incumbent renewal are the buyer's own deadlines. Strong plans create urgency from those facts without manufactured pressure. Pushiness is a failure mode the brief warns about explicitly.

### 5. An executable action sequence
The ten actions should have owners, dates, dependencies, and a reason each moves the deal. The strongest artifacts look like a real mutual action plan or account plan a manager could inspect mid-quarter.

### 6. An honest walk-away analysis
Strong submissions state the conditions under which they would stop pushing, and what protecting the champion relationship is worth relative to the quarter.

## Challenge-Specific Failure Modes

- **Framework recitation.** Naming a sales methodology and restating its steps instead of applying judgment to these stakeholders and this timeline.
- **Discount-led rescue.** Leading with price against a competitor's discount, breaking the stated policy or gutting the deal's value story.
- **Champion bypass.** Plans that quietly route around the champion despite the explicit constraint.
- **Happy-path sequencing.** Ten actions that all assume every meeting is accepted and every stakeholder cooperates, with no branch for the likely "no".

## Evidence That Matters for This Brief

- **Tier 2** is the floor: the account plan, mutual action plan, call plan, or stakeholder map itself.
- **Tier 3** strengthens it: sanitized records from real deals you have run (sequences, notes, close plans) that show this is your actual operating style.
- **Tier 4-5** is the differentiator: a comparable stalled deal you revived, with the before/after and someone who could confirm it.
- Label the numbers you introduce (win-probability estimates, timeline assumptions) and keep the brief's given facts distinct from your inferences.

Strong or close submissions may be asked to role-play a stakeholder conversation or defend the plan when one assumption is flipped.

## Fixture Verification

The brief requires working the fixture dataset in `fixtures/crm_activity_log.csv`. Reviewers hold the private key of seeded issues, so the fastest ways to lose are: analysis that never cites the data, conclusions that treat a planted issue as clean signal, and recommendations the fixture contradicts. Strong submissions cite specific ids, catch most of the seeded issues, state the fixture checksum, and say what they refused to conclude because the sample is small.

---

Format, page limits, and the full submission packet are defined in the challenge [brief](brief.md) and the repository [README](../../README.md). You can pre-screen your packet with `python3 scripts/validate_submission.py`.
