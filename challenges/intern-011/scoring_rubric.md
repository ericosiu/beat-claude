# Public Review Guide: Intern 011

This guide is challenge-specific but intentionally high level. Read [SCORING.md](../../SCORING.md) first: the five evaluation dimensions, the evidence tiers, and the number source labels apply to every challenge. Private reviewer calibration, answer benchmarks, and follow-up exercises are not published.

## What Strong Submissions Demonstrate

### 1. A prototype that actually runs
This challenge weights the build heavily. Strong submissions ship something a reviewer can execute or watch working: a repo with demo instructions, a runnable link, or a short video of the agent processing real-looking input. The polish bar is low; the "it works" bar is absolute.

### 2. The three test cases, honestly run
The brief requires a normal case, a messy case, and a case where the agent should stop or escalate. Strong submissions show real inputs and real outputs for all three, including the escalation actually triggering. Describing the cases without running them is the tell of a paper design.

### 3. A bad output, owned
The required bad-output example is a judgment probe. Strong answers show a genuine failure from their own prototype, explain how they detected it, and what the fix or human route was. Submissions that claim their agent had no bad outputs read as either untested or untruthful.

### 4. Human-in-the-loop choices with reasons
Strong designs are explicit about which steps a person still reviews and why those steps specifically: where errors are costly, where judgment or tone matters, where the data is untrustworthy. "Human reviews everything" and "fully autonomous" are both weak answers here.

### 5. Scoping judgment under a time limit
The brief allows building only the hardest part if time runs out. Strong submissions choose the genuinely hard part, show it working, and map the honest gap to a next step. Over-scoping a six-month system is a named losing pattern.

### 6. Builder instinct in the small answers
Parts 1 and 3 reward specificity: a verifiable "most impressive thing", and a meta-question answer that shows you reflexively see manual work as automatable. Creative, concrete, personal beats broad and safe.

## Challenge-Specific Failure Modes

- **The strategy doc.** Architecture prose and tool lists with no working build. The brief says this loses, and it does.
- **The happy-path demo.** A prototype shown only on clean input, with edge cases and failures untested or hidden.
- **Pasted output.** Submitting lightly edited generic-AI text as the design. Reviewers compare against exactly that baseline.
- **Hidden gaps.** Claiming completeness instead of showing what works, what breaks, and what stays human, as the brief instructs.

## Evidence That Matters for This Brief

- **Tier 2** is the expected floor: the prototype itself, inspectable or watchable.
- **Tier 3** is where strong submissions live: code, prompts, test inputs, output logs, and failure notes a reviewer can trace.
- **Tier 4** is the differentiator: a before/after of the manual workflow versus the agent, with time or quality measured and every number labeled.
- Label your workflow numbers (time per task, volume, error rates) as observed, estimated, benchmarked, or assumed. Estimates are fine; unlabeled precision is not.

Strong or close submissions may be asked to run the prototype live on a new input, so make sure it runs somewhere other than your machine's memory.

---

Format, page limits, and the full submission packet are defined in the challenge [brief](brief.md) and the repository [README](../../README.md). You can pre-screen your packet with `python3 scripts/validate_submission.py`.
