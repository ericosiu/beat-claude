# Beat Claude

**The hiring challenge for AI-native operators**

Single Grain is looking for people who can use AI as leverage and still beat a generic AI answer with judgment, proof, and execution.

Beat Claude is the public hiring challenge that runs through `/apply` and our careers page. This public repo contains candidate briefs and public guidance only. Private reviewer benchmarks, calibration notes, and follow-up prompts are not published here.

## How It Works

1. Pick a challenge from [`/challenges`](challenges/).
2. Read the brief and note any assumptions you need to make.
3. Build the required operating artifact.
4. Submit your written answer, artifact access, and evidence packet.
5. Reviewers evaluate your work using private benchmark material and evidence checks.
6. Strong submissions may receive a source check, artifact walkthrough, or follow-up exercise.
7. If your work shows better judgment, proof, and execution than a generic AI response, we want to talk.

## Why This Exists

AI can produce competent knowledge work quickly. We are looking for people who can do what AI still struggles with: judgment under constraints, creative leaps, practical execution, source checking, and knowing what should stay human.

If you only paste the brief into an AI tool, you will usually get a generic answer. Generic answers do not advance.

## The Rules

Use whatever tools you want: AI, research, collaborators, spreadsheets, code, workflows, prototypes, or public data.

To stand out, add something a generic model output could not reliably produce from the brief alone:

- A real operating artifact.
- Source-labeled numbers.
- Evidence that you tested, built, validated, or modeled something.
- Clear tradeoffs and failure handling.
- A sharp explanation of what AI should not do.

**Time commitment:** Each challenge is designed to take **1-2 hours**. Written submissions are capped at **4 pages** unless the brief says otherwise. Artifact links, code, sheets, dashboards, and short demos can be included separately.

## Public Guide, Private Review

The public scoring guide is intentionally high level. We do not publish detailed scoring keys, reviewer calibration, answer benchmarks, or all follow-up prompts because that rewards rubric gaming.

Review may include:

- Blind review against private benchmarks.
- A follow-up exercise after submission.
- A short live walkthrough of your artifact.
- A proof check for numbers, source records, logs, or assumptions.
- A second reviewer when decisions are close.

See [`SCORING.md`](SCORING.md) for the public guide.

## Required Submission Packet

Every challenge submission should include:

1. **Written answer**: the strategy, plan, design, or build explanation.
2. **Operating artifact**: a sheet, repo, workflow, Loom, dashboard, scorecard, process doc, prototype, log export, or other artifact a reviewer can inspect.
3. **Evidence log**: proof tier for each major claim, using the tiers in [`SCORING.md`](SCORING.md).
4. **Number source labels**: every number labeled as observed, estimated, benchmarked, or assumed.
5. **AI usage disclosure**: tools used, what they did, what you changed, and what you checked.
6. **Failure handling**: what breaks the plan or artifact, how you would detect it, and what stays human.
7. **Artifact access**: working links, permissions, sample data, no-login demo instructions, and any setup notes needed for review.

Submissions without an operating artifact or source-labeled numbers are unlikely to advance.

**Pre-screen your packet:** run `python3 scripts/validate_submission.py path/to/your_submission.md` to check that all 7 sections are present, your numbers carry source labels, and nothing in your packet trips the review-manipulation detector before you submit. See [`submissions/README.md`](submissions/README.md) for details.

**Brief versions:** every brief carries a version stamp (for example, `Brief version: 2026-07`) and briefs are refreshed periodically. State the version you answered in your written answer. Circulated answers to old brief versions are easy to spot and do not advance — see the [Integrity section of SCORING.md](SCORING.md#integrity).

**Fixture datasets:** role challenges include a small synthetic dataset in their `fixtures/` folder with seeded issues we hold the key to. The brief tells you what to do with it; strong submissions work the data, cite specific rows, and catch what's planted. Fixtures rotate between hiring rounds, so shared answers go stale by design.

## Candidate Confidentiality and Data Policy

Do not include confidential, proprietary, regulated, or sensitive personal data in your submission. Use public sources, synthetic data, anonymized samples, or your own work product. Do not submit passwords, API keys, customer lists, employee records, compensation details, private analytics exports, or anything you do not have permission to share. If a task would normally require private data, state the assumption and show the artifact with safe sample data.

## Start Here

**Don't see your role below? Start with the General Challenge or an Internship Challenge.**

| Challenge | Role Target | Difficulty |
|-----------|-------------|------------|
| [**General 000**](challenges/general-000/) | **Anyone, show us how you think** | **Open** |
| [**Intern 011**](challenges/intern-011/) | **Internship, any role. Build an AI agent.** | **Hard** |
| [**AI Automation Intern 012**](challenges/ai-automation-intern-012/) | **AI automation internship. Run your agent on our fixture data.** | **Hard** |

**We are actively hiring multiple AI automation interns on a rolling basis.** If you build agents and automations, start with [AI Automation Intern 012](challenges/ai-automation-intern-012/): it runs against a seeded fixture dataset in this repo, so your submission is verifiable and shared answers go stale by design.

## Role-Specific Challenges

| Challenge | Role Target | Difficulty |
|-----------|-------------|------------|
| [Marketing Strategy 001](challenges/marketing-strategy-001/) | CMO / VP Marketing | Hard |
| [Paid Media 002](challenges/paid-media-002/) | Paid Media Director | Medium |
| [SEO Strategy 003](challenges/seo-strategy-003/) | Head of SEO | Hard |
| [Engineer 004](challenges/engineer-004/) | Senior Engineer | Hard |
| [Product Designer 005](challenges/product-designer-005/) | Senior Product Designer | Medium |
| [Sales AE 006](challenges/sales-ae-006/) | Account Executive | Medium |
| [YouTube Strategist 007](challenges/youtube-strategist-007/) | YouTube Strategist | Hard |
| [Head of Talent 008](challenges/talent-manager-008/) | Head of Talent, end-to-end people function | Hard |
| [Ops COO 009](challenges/ops-coo-009/) | COO / GM | Hard |
| [Sales Director 010](challenges/sales-director-010/) | Sales Director, player-coach | Hard |

## How to Submit

Apply through our careers page: **[singlegrain.com/careers](https://www.singlegrain.com/careers/)**

Upload your challenge answer and include links to any artifacts.

## What Happens Next

1. Your submission is anonymized.
2. A reviewer scores your answer using private benchmark guidance.
3. We check evidence quality, source labels, and artifacts.
4. Strong submissions may receive a follow-up exercise or live walkthrough.
5. If your work clears review, we reach out to schedule a conversation.

## Leaderboard

Top performers: [Hall of Fame](leaderboard/HALL_OF_FAME.md)

---

## About Single Grain

[Single Grain](https://www.singlegrain.com) is a digital marketing agency working with companies like Amazon, Uber, and Salesforce. We're building an AI-forward team that uses technology as leverage, not as a crutch.

## How the Whole System Works

Curious how the challenge is built and defended — the fixture system, versioning, validators, CI, and what stays private? See [ARCHITECTURE.md](ARCHITECTURE.md).

## Questions and GitHub Issue Policy

Use GitHub issues only for general public clarification that would help every candidate equally, such as broken links, typo fixes, or ambiguous public instructions.

Do **not** ask for role-specific coaching, hidden evaluation criteria, sample answers, private benchmarks, or approval of your planned approach in a public issue. If the brief lacks information, state a reasonable assumption in your submission and label it as assumed.

Apply at [singlegrain.com/careers](https://www.singlegrain.com/careers/).

---

*Inspired by [Anthropic's performance take-home](https://github.com/anthropics/original_performance_takehome)*
