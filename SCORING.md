# Public Scoring Guide

This is the public evaluation guide for Beat Claude, Single Grain's hiring challenge.

It is intentionally high level. Detailed scoring notes, reviewer calibration, answer benchmarks, and follow-up prompts are private so the challenge tests judgment instead of rubric matching.

## How We Evaluate

Submissions go through blind review using private reviewer guidance for the same brief. Reviewers look for work that shows real operating judgment, not polished prompt output.

Strong submissions usually have:

1. **Strategic judgment**: clear choices, tradeoffs, constraints, risks, and second-order effects.
2. **Execution detail**: a concrete plan that could be used tomorrow by a real team.
3. **Evidence quality**: proof that claims are grounded in work, data, customer insight, or a real artifact.
4. **AI fluency**: smart use of AI with clear limits, human checkpoints, and failure handling.
5. **Communication**: concise, structured, direct, and easy to review.

## What Strong Work Shows

A generic model can produce a competent strategy document. Strong candidates show something the brief alone cannot reliably produce:

- An operating artifact we can inspect.
- Specific judgment based on real constraints.
- Evidence that you tested, built, modeled, or validated something.
- A clear view of what breaks, what stays human, and why.
- Domain taste, creative pattern recognition, or practical experience.

Generic answers do not advance.

## Required Evidence Standards

Every submission should include an evidence log. Label your proof with the highest tier you can support:

| Tier | Evidence type | What it means |
|------|---------------|---------------|
| 0 | Claims only | You asserted it, but did not show proof. |
| 1 | Screenshots | Static proof of a screen, doc, result, or workflow. |
| 2 | Demo artifact | A sheet, repo, Loom, workflow, prototype, dashboard, or mock that can be reviewed. |
| 3 | Logs or source records | Exports, raw data, source records, commits, prompt traces, CRM notes, analytics pulls, or similar. |
| 4 | Before and after data | Measured change with a clear benchmark and method. |
| 5 | Independent verification | A user, customer, system, reviewer, or production process confirms the result. |

Lower tiers can be useful context. Higher tiers usually carry more weight.

## Number Source Labels

Every number in your submission must be labeled by source type:

- **Observed**: measured directly from a real system, dataset, user, or experiment.
- **Estimated**: your own estimate based on stated reasoning.
- **Benchmarked**: pulled from a named external benchmark, public source, or comparable case.
- **Assumed**: a placeholder assumption used to make the plan concrete.

Examples:

- "[Observed] 48 leads entered the sheet last week."
- "[Estimated] This should take 6 hours to build because two APIs are already connected."
- "[Benchmarked] 2 percent to 5 percent reply rate based on prior cold outbound benchmarks."
- "[Assumed] $100/hour blended cost for internal time."

Unlabeled numbers hurt the review. Fake precision hurts more than honest assumptions.

## Operating Artifact Requirement

A written answer alone is not enough. Include at least one operating artifact that shows how you work.

Examples:

- A spreadsheet model with formulas and assumptions.
- A repo, script, prompt chain, or automation workflow.
- A Loom walkthrough of a working prototype.
- A dashboard with source data.
- A Slack workflow, CRM view, hiring scorecard, process cadence, or calendar plan.
- A before and after comparison with raw inputs and outputs.

The artifact does not need to be perfect. It needs to be real enough for a reviewer to inspect your judgment.

## AI Usage Disclosure

Use AI if it helps. We expect it. Tell us how you used it.

Include:

- Tools used.
- What AI helped with.
- What you personally decided.
- What you checked or changed.
- Any known weak spots in the output.

Undisclosed AI use is not the issue. Passing off generic AI work as proven operating judgment is the issue.

## Follow-Up and Live Walkthrough

After submission, strong candidates may receive a private follow-up exercise or live walkthrough request. This can include:

- A changed constraint.
- A messy data sample.
- A request to explain the artifact live.
- A request to show source records, logs, or assumptions.
- A failure case that tests whether the plan still works.

This step is part of the review process. It exists to separate real operators from prompt-optimized answers.

## Failure Modes That Lose

Submissions are unlikely to advance if they:

- Optimize for the public guide instead of solving the business problem.
- Use polished language without an operating artifact.
- Include numbers with no source labels.
- Invent proof, metrics, customers, users, or system outputs.
- Ignore constraints in the brief.
- Hide what stays human or where AI fails.
- Submit a one-off AI demo that only works on the happy path.
- Sound like a generic AI answer with light editing.

## Format and Length

Most challenges have a 4-page maximum for the written answer. Diagrams, artifact links, code, sheets, and short Loom demos do not count toward the written page limit unless the brief says otherwise.

Short and sharp is better than long and vague.

## Frequently Asked Questions

**Q: Can I use AI?**

Yes. Use whatever tools help you produce better work. Disclose how you used them.

**Q: How long until I hear back?**

Usually within 2 weeks. We review submissions in batches.

**Q: Can I resubmit?**

One submission per challenge unless we invite a follow-up.
