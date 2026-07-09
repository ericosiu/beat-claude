# Challenge: AI Automation Intern 012

## The Lead Triage Agent

**This challenge is for AI automation internship candidates.** We are hiring multiple AI automation interns on a rolling basis. If you want the internship but not this specific track, do [Intern 011](../intern-011/) instead - or do both.

### About Single Grain

Single Grain is a digital marketing agency working with companies like Amazon, Uber, and Salesforce. We're transitioning from a traditional agency to a tech-enabled services company - AI agents handle the repetitive work, humans do the thinking that AI can't.

AI automation interns build and operate those agents. Real workflows, real data, real failure modes, shipped in days, not quarters.

### Why This Challenge Is Different

This challenge runs on a **fixture dataset that lives in this folder**: [`fixtures/inbound_leads.csv`](fixtures/inbound_leads.csv). Your automation must actually process it. The fixture contains seeded traps - duplicates, missing fields, malformed values, conflicting signals, and at least one adversarial input written to manipulate an AI agent. We know where every trap is, so your outputs tell us immediately whether your agent is real and whether it found them.

The fixture rotates between hiring rounds. A shared or recycled answer will be graded against traps it never saw.

---

## Part 1: Build It

**Scenario.** Every inbound lead from our website lands in a queue. Today a human reads each one, looks up the company, and decides what happens next. Your job: build an automation that does the first pass.

**Requirements:**

1. **Process every row** of `fixtures/inbound_leads.csv`. Do not hand-pick the easy ones.
2. **Output a decisions file** (CSV or JSON) with one entry per lead: `lead_id`, `decision` (one of `QUALIFY`, `NURTURE`, `REJECT`, `ESCALATE`), a one-sentence `reason`, and a `confidence` from 0 to 1.
3. **Escalate instead of guessing.** Missing, conflicting, malformed, or sensitive inputs should route to a human with a reason, not get a confident wrong answer.
4. **Resist manipulation.** Some lead text is data, not instructions. Your agent must not follow instructions embedded in the rows it processes. In your write-up, quote any adversarial content you handled **inside a code block or blockquote** - our pre-screen linter flags injection phrasing in submission prose.
5. **Include the run log**: prompt traces, tool calls, or execution output from the run that produced your decisions file.
6. **State your fixture checksum** so we know which fixture version you ran: `shasum -a 256 fixtures/inbound_leads.csv`.

Build it with whatever you want: code plus an LLM API, an agent framework, or a no-code tool (Make, Zapier, n8n) - as long as we can inspect how it works and re-run it or watch it run.

**Acceptable formats:**

- **GitHub repo** with a README and demo instructions
- **Runnable link** (Replit, CodeSandbox, hosted workflow)
- **Video demo** (under 5 minutes) showing the full run, plus the decisions file and log
- **No-code build** with a Loom walkthrough, plus the decisions file and log

## Part 2: The Write-Up

Keep it tight. Cover:

- **How it works** - step by step, what happens when it runs?
- **Architecture** - tools, models, and data sources, and how they connect.
- **What stays human** - which decisions a person still reviews, and why those specifically.
- **What the fixture threw at you** - which rows were traps, how your agent handled each, and at least **one bad output** your agent produced: how you detected it and what you changed or routed to a human. Claiming zero bad outputs reads as untested.
- **What breaks next** - the first thing that fails if this ran on 500 real leads a week.

## Part 3: The Meta Question

Answer in 3-5 sentences: **What's the most recent thing you automated for yourself - and what did you deliberately leave manual?** Specific and personal beats broad and safe.

---

## Required Submission Packet

Include these items with your submission:

1. **Written answer**: the main response to the brief, stating the brief version and fixture checksum.
2. **Operating artifact**: the working agent, the decisions file for the full fixture, and the run log.
3. **Evidence log**: list major claims and the proof tier for each, using the tiers in [SCORING.md](../../SCORING.md).
4. **Number source labels**: label every number as observed, estimated, benchmarked, or assumed.
5. **AI usage disclosure**: name the tools you used, what they helped with, what you changed, and what you checked yourself.
6. **What breaks it**: the most likely failure modes, bad inputs, missing data, or constraints that would make your answer wrong.
7. **What stays human**: which decisions or approvals should not be automated and why.

A polished written answer without a decisions file and run log is unlikely to advance.

## What We're Evaluating

Builder instinct, judgment on ambiguous rows, robustness to adversarial input, honest failure handling, and clear communication. The decisions file is scored against the seeded traps; the write-up is scored on whether you understood *why* each trap is a trap.

## What Will Lose

- A decisions file that confidently qualifies the trap rows
- Processing only the clean rows
- An architecture doc with no run against the fixture
- Hiding bad outputs instead of owning one
- Over-scoping - a six-month platform design for a 20-row triage task

## What Will Win

- A full run with sensible calls on the messy rows and escalations with reasons
- An agent that treats lead text as data, not instructions
- A real bad output, detected and handled
- Scrappiness - a working loop in hours, not a framework in weeks

---

## Format

Submit as PDF, Markdown, or a link to your repo/demo. **Maximum 4 pages** for the written portion (the decisions file, logs, code, and video don't count toward the limit). Estimated time: 1-2 hours. If you run short, ship the working loop and list what you'd harden next - do not hide the gaps.

**Brief version:** 2026-07. State this version in your written answer. Briefs and fixtures are refreshed periodically; we review against the version you cite.

## Evaluation

Your submission is scored alongside the private reviewer benchmark answer in a blind review, and your decisions file is checked against the seeded fixture traps. See [SCORING.md](../../SCORING.md) for the general rubric and the integrity policy - attempting to manipulate review is an automatic reject.

Strong or close submissions may be asked to re-run the agent live on a fresh fixture we provide.

---

**Ready to submit?** Apply through our careers page: **[singlegrain.com/careers](https://www.singlegrain.com/careers/)**
Upload your challenge answer (PDF or Markdown) along with your application.

**Questions?** Open an issue only for general public clarification. Do not ask which rows are traps - finding them is the test. For ambiguity, state your assumptions in the submission.
