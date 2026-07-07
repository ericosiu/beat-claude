# Public Review Guide: General 000

This guide is challenge-specific but intentionally high level. Read [SCORING.md](../../SCORING.md) first: the five evaluation dimensions, the evidence tiers, and the number source labels apply to every challenge. Private reviewer calibration, answer benchmarks, and follow-up exercises are not published.

## What Strong Submissions Demonstrate

### 1. Verifiable proof, not pedigree
The core of this challenge is Part 2. Strong submissions pick two or three pieces of work and make each one checkable: a link a reviewer can open, a before/after a reviewer can compare, a result a reviewer could confirm with the source. The delta you caused matters more than the title you held.

### 2. A role only you could have written
Part 1 reads like a specific person describing specific work, not a job description. Strong answers name the work they want to own, connect it to something Single Grain visibly does, and describe a first 90 days that follows logically from their proof in Part 2.

### 3. An AI edge shown through built things
The strongest Part 3 answers describe workflows the candidate actually runs: what the AI does, what the human does, what changed about their output. "I use it daily" is a claim; a described pipeline with its known failure points is evidence.

### 4. Predictions with reasoning attached
The 2-year prediction question rewards a falsifiable point of view. Strong answers commit to specifics in their own field and explain the mechanism, including the uncomfortable parts. Hedged futurism reads as generic.

### 5. Selection over coverage
The brief allows 4 pages; strong submissions often use fewer. Choosing the two best proofs beats listing ten weak ones. Reviewers notice what you chose to leave out.

### 6. A voice worth talking to
This challenge explicitly applies the Dinner Test from the brief. Submissions that sound like a person with opinions, taste, and self-awareness outperform submissions that sound like a well-prompted model.

## Challenge-Specific Failure Modes

- **Claims without receipts.** Impressive numbers with no artifact, link, screenshot, or way to verify. Per SCORING.md, this is Tier 0 evidence and it reads as such.
- **The resume in paragraph form.** Responsibilities and team sizes instead of outcomes and deltas. The brief warns about this directly.
- **AI-hype filler.** Generic commentary about AI transforming everything, with no personal workflow, no named win, and no honest read on limits.
- **Playing it safe.** Comprehensive, balanced, forgettable. This challenge rewards a sharp claim about what you are exceptional at, backed up.

## Evidence That Matters for This Brief

- **Tier 2-3** is the realistic floor for your proof-of-ability examples: live artifacts, repos, published work, exports, or records a reviewer can inspect.
- **Tier 4-5** carries the most weight here: before/after results with a stated method, or outcomes a third party (client, employer, user, public metric) can confirm.
- Label every number in your proof examples as observed, estimated, benchmarked, or assumed. Unverifiable precision in Part 2 damages trust in the whole submission.
- Your evidence log should make the reviewer's verification path obvious: claim, tier, where to look.

Strong or close submissions may receive a source check or a live walkthrough. Assume anything you cite will be tested.

---

Format, page limits, and the full submission packet are defined in the challenge [brief](brief.md) and the repository [README](../../README.md). You can pre-screen your packet with `python3 scripts/validate_submission.py`.
