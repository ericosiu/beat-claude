# Public Review Guide: SEO Strategy 003

This guide is challenge-specific but intentionally high level. Read [SCORING.md](../../SCORING.md) first: the five evaluation dimensions, the evidence tiers, and the number source labels apply to every challenge. Private reviewer calibration, answer benchmarks, and follow-up exercises are not published.

## What Strong Submissions Demonstrate

### 1. Diagnosis before prescription
The brief gives several plausible causes for the decline: content decay, technical debt, a faster competitor, and shifting search results. Strong submissions separate these causes, estimate the contribution of each (labeled), and let the diagnosis drive the plan. Weak submissions jump straight to a standard playbook.

### 2. A triage system for the existing content library
Hundreds of aging posts cannot all be refreshed. Strong answers show a decision framework: which posts to refresh, consolidate, prune, or leave alone, and in what order, with the reasoning visible. The best artifacts for this brief are exactly this: an audit sheet or refresh model a reviewer can inspect.

### 3. Competitive judgment about which battles to fight
The brief names a well-funded competitor publishing aggressively. Strong submissions choose where to compete head-on, where to flank, and where to concede, and explain why. Pretending the competitor can be out-published on this budget is a judgment failure.

### 4. Engineering asks sized to the constraint
One sprint per quarter is the entire technical budget. Strong plans rank technical fixes by expected impact per unit of engineering time and state what gets cut. Plans requiring continuous engineering support ignore the brief.

### 5. A 90-day traction story for leadership
Recovery takes longer than a quarter, but leadership wants signal early. Strong submissions pick early indicators that honestly predict recovery and explain what they will do if those indicators do not move.

### 6. Conversion, not just traffic
The task includes improving conversion from organic visitors. Strong answers connect the content plan to the visitor's intent and the path to the product, not just to rankings.

## Challenge-Specific Failure Modes

- **The generic audit-everything opener.** A quarter spent auditing before anything ships, despite the explicit 90-day traction constraint.
- **Playbook recitation.** Refresh content, fix technical issues, build links — with no prioritization, sequencing, or connection to this site's actual situation.
- **Unlabeled recovery projections.** Traffic recovery curves asserted without labeling the assumptions behind them.
- **Budget-blind link building.** Link strategies whose real-world cost exceeds the stated budget, or that risk the domain's credibility.

## Evidence That Matters for This Brief

- **Tier 2** is the floor: the audit sheet, keyword map, or refresh-prioritization model itself.
- **Tier 3** strengthens it: real analytics or crawler exports (from your own past work, sanitized) showing you have run this motion before, or sources for every benchmarked figure.
- **Tier 4** is the differentiator: before/after data from a decline you actually reversed, with the method stated.
- Your evidence log should distinguish what you observed from public tools, what you benchmarked from named sources, and what you assumed about this company's data you cannot see.

Strong or close submissions may be asked to defend the triage framework live against a messy sample of real posts.

---

Format, page limits, and the full submission packet are defined in the challenge [brief](brief.md) and the repository [README](../../README.md). You can pre-screen your packet with `python3 scripts/validate_submission.py`.
