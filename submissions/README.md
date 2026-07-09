# How to Submit

## Submission Process

1. **Pick a challenge** from [`/challenges`](../challenges/).
2. **Create your answer** as PDF or Markdown.
3. **Prepare your artifact access**: links, permissions, sample data, setup steps, and any no-login demo instructions.
4. **Apply through our careers page:** **[singlegrain.com/careers](https://www.singlegrain.com/careers/)**.
5. Upload your challenge answer and include artifact links with your application.

## Required Submission Packet

Every submission should include:

1. **Written answer**: concise response to the brief.
2. **Operating artifact**: sheet, repo, workflow, Loom, dashboard, scorecard, model, prototype, process doc, or other artifact a reviewer can inspect.
3. **Evidence log**: major claims mapped to proof tiers in [SCORING.md](../SCORING.md).
4. **Number source labels**: label every number as observed, estimated, benchmarked, or assumed.
5. **AI usage disclosure**: tools used, what they did, what you changed, what you verified, and known weak spots.
6. **Failure handling**: what breaks the plan or artifact, how you would detect it, and what stays human.
7. **Artifact access**: working links, permissions, sample data, and setup notes.

## Pre-Screen Your Packet (Optional but Recommended)

Before you submit, you can run the same objective pre-screen linter reviewers use for a first pass:

```bash
python3 scripts/validate_submission.py path/to/your_submission.md
# or a folder of files:
python3 scripts/validate_submission.py path/to/your_submission_dir/
# treat advisory warnings as failures:
python3 scripts/validate_submission.py path/to/your_submission.md --strict
```

What it checks:

1. **Required packet sections (fail)**: all 7 sections above are present. The linter looks for the section names (or close variants such as "What breaks it" for failure handling), so use them as headings or labels in your document.
2. **Review manipulation (fail)**: text that addresses or instructs a reviewing AI model, invisible/zero-width characters that hide text from human readers, or HTML comments aimed at the review process. This is an automatic reject at review time — see the [Integrity section of SCORING.md](../SCORING.md#integrity). If you are quoting an adversarial input your own agent defended against, put the quote in a code block or blockquote and the linter will not flag it.
3. **Verifiability (advisory)**: sections that make `[Observed]` or Tier 2-5 claims should contain something a reviewer can check — a link, an attached file path, a screenshot reference, or a reproduction command.
4. **Number source labels (advisory)**: paragraphs with numeric claims should carry an `[Observed]`, `[Estimated]`, `[Benchmarked]`, or `[Assumed]` label, per [SCORING.md](../SCORING.md).
5. **Evidence-tier citations (advisory)**: your evidence log should map major claims to the SCORING.md proof tiers (Tier 0-5).
6. **Brief version (advisory)**: your written answer should state the version stamp of the brief you answered (for example, `Brief version: 2026-07`). Briefs are refreshed periodically and reviews use the version you cite.

A passing pre-screen does not mean a passing review; it only confirms the packet is complete and your numbers are labeled. The advisory checks are heuristics — reviewers make the final call.

## Verification

We spot-verify submissions. Claimed artifacts may be requested live, numbers may be re-derived with you in the interview, and `[Observed]` or Tier 2-5 claims that give reviewers nothing to check are scored as Tier 0 (claims only). Review may also include comparison against a fresh model-generated answer to the same brief, produced at review time — pasting our public materials into an AI tool gets you to that baseline, not past it. See the [Verification section in SCORING.md](../SCORING.md#verification).

## Candidate Confidentiality and Data Policy

Use public sources, synthetic data, anonymized samples, or your own work product. Do not submit confidential customer data, employee records, compensation details, passwords, API keys, private analytics exports, private CRM exports, or anything you do not have permission to share.

If a realistic answer would require private data, state the assumption, label it as assumed, and show your artifact with safe sample data.

## Rules

- **One submission per challenge** unless invited otherwise.
- **Use any tools you want**: AI, research, collaborators, spreadsheets, code, workflows, prototypes, or public data.
- **No plagiarism**: your work, your thinking, your verification.
- **Maximum 4 pages** unless the challenge says otherwise. We value clarity and prioritization, not volume.
- **No hidden access needed**: if the brief lacks information, state a reasonable assumption rather than asking for private details.

## Questions and GitHub Issue Policy

Open a GitHub issue only for general public clarification that benefits all candidates equally: broken links, typo fixes, contradictory public instructions, or repo access issues.

Do **not** use public issues to ask for role-specific coaching, private benchmarks, sample answers, hidden criteria, or approval of your planned approach. For role-specific ambiguity, state your assumptions in the submission and explain how they affect your plan.

You may also include role-specific context with your application through the [Single Grain careers page](https://www.singlegrain.com/careers/).

## What Happens Next

| Step | Timeline |
|------|----------|
| Submission received | Immediate confirmation |
| Blind review | Usually within 2 weeks |
| Results | Email notification |

Your submission will be anonymized, reviewed with private benchmark guidance, and evaluated by Single Grain team members. We may request source proof, an artifact walkthrough, or a follow-up exercise.

See [SCORING.md](../SCORING.md) for the public review guide.
