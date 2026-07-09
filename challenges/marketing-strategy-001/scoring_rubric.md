# Public Review Guide: Marketing Strategy 001

This guide is challenge-specific but intentionally high level. Read [SCORING.md](../../SCORING.md) first: the five evaluation dimensions, the evidence tiers, and the number source labels apply to every challenge. Private reviewer calibration, answer benchmarks, and follow-up exercises are not published.

## What Strong Submissions Demonstrate

### 1. Prioritization with an explicit "not doing" list
The brief asks for two or three channels and a clear statement of what you will not do. Strong submissions treat the runway pressure as the dominant constraint and cut accordingly. A plan that tries every channel signals that no real choice was made.

### 2. A budget model a reviewer can interrogate
The operating artifact that fits this brief best is a working allocation model: spend by channel over time, with every conversion and cost assumption labeled and adjustable. Strong models show what happens when an assumption misses, not just the happy path.

### 3. A credible beta-to-paid conversion motion
The company's biggest asset is its existing free beta base. Strong answers reason about who those users are, why they would start paying, and what the founder-led sales constraint means for sequencing. Plans that ignore the existing users to chase cold acquisition usually miss the point.

### 4. Pricing reasoned from the buyer, not from the product
Strong pricing sections start from what the stated buyer values and how they budget, then justify the model and packaging. Pricing pulled from thin air, or copied from competitors without reasoning, is both a labeling problem and a judgment problem.

### 5. Milestones that are falsifiable
Day 30/60/90 checkpoints should be specific enough that a reviewer could tell, on that day, whether the plan is working and what you would change if it is not. "Momentum building" is not a milestone.

### 6. Respect for the team you were given
A founder at half-time plus two engineers is the entire go-to-market capacity. Strong plans fit that capacity; weak plans quietly assume a marketing department that does not exist.

## Challenge-Specific Failure Modes

- **The channel laundry list.** Every acquisition channel named, none owned, budget spread thin. This is the most common generic-AI shape for this brief.
- **Runway blindness.** A plan whose payback timeline outlives the company. Strong candidates connect spend, sales cycle, and cash explicitly.
- **Unlabeled benchmark rates.** Conversion and cost figures asserted as fact. Every rate in this plan is an estimate, benchmark, or assumption and must be labeled as such.
- **Pricing as an afterthought.** A single price named with no packaging logic, no connection to the paid-growth goal, and no risk discussion.

## Evidence That Matters for This Brief

- **Tier 2** is the floor: the budget/funnel model itself, inspectable, with formulas and labeled assumptions.
- **Tier 3** strengthens it: sources for each benchmarked rate, comparable-case citations, or research records behind your channel choices.
- **Tier 4-5** is rare but decisive here: results from a comparable launch you actually ran, with before/after data or a confirming stakeholder.
- The evidence log should map each major bet (channel choice, price point, milestone) to its proof tier, so the reviewer can see which parts are grounded and which are honest assumptions.

Strong or close submissions may be asked to defend the model live with a changed constraint. Build it so a variable can change without the plan collapsing.

## Fixture Verification

The brief requires working the fixture dataset in `fixtures/beta_accounts.csv`. Reviewers hold the private key of seeded issues, so the fastest ways to lose are: analysis that never cites the data, conclusions that treat a planted issue as clean signal, and recommendations the fixture contradicts. Strong submissions cite specific ids, catch most of the seeded issues, state the fixture checksum, and say what they refused to conclude because the sample is small.

---

Format, page limits, and the full submission packet are defined in the challenge [brief](brief.md) and the repository [README](../../README.md). You can pre-screen your packet with `python3 scripts/validate_submission.py`.
