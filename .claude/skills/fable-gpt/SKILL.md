---
name: fable-gpt
description: >-
  Orchestrator/executor workflow for pairing Claude with OpenAI Codex (GPT-5.5)
  inside Claude Code. Claude plans, understands the repo, decomposes tasks, and
  reviews; Codex executes heavy implementation, debugging, test-fixing, and
  multi-file refactors via the codex-rescue sub-agent. Invoke at the start of a
  session when you want to delegate heavy coding to Codex and conserve Claude
  tokens.
---

# Fable-GPT: Claude + Codex orchestration

Pair Claude (orchestrator) with OpenAI Codex / GPT-5.5 (executor) so heavy
implementation runs on Codex while Claude keeps ownership of planning and
review. Based on the workflow from https://x.com/cjzafir/status/2074875092090470469

## Prerequisites (one-time, on a LOCAL Claude Code CLI)

This workflow needs the Codex plugin and an authenticated Codex/ChatGPT account.
Set it up once on your own machine — **it does not work in a sandboxed/remote
Claude Code environment where OpenAI domains (`api.openai.com`, `chatgpt.com`,
`auth.openai.com`) are firewalled off, since Codex can't authenticate or reach
GPT there.**

1. Install the plugin (verify the marketplace source before trusting it):
   ```
   /plugin marketplace add openai/codex-plugin-cc
   /plugin install codex@openai-codex
   /reload-plugins
   ```
2. Finish setup — run `/codex:setup`. Install the Codex CLI if missing.
3. Authenticate once with your ChatGPT/Codex account when prompted.
4. Verify Codex runs from inside Claude Code and the `codex:codex-rescue`
   sub-agent is available. Do not change project code during setup.

## Roles

- **Claude = orchestrator.** Owns planning, repo understanding, architecture
  decisions, task decomposition, and final review.
- **Codex (`codex-rescue`) = executor.** Handles heavy implementation,
  debugging, test fixing, refactoring, and multi-file edits.

## Delegation loop

1. Claude scopes the task and writes a focused, specific spec for Codex — one
   clear objective, the exact files in play, and the acceptance check.
2. Delegate with `/codex:rescue`. Prefer model **GPT-5.5 (xtra high)**.
3. Keep each Codex task narrow. Split large work into separate delegations
   rather than one sprawling prompt.
4. When Codex returns, **Claude inspects the diff before accepting it** — read
   the changes, run tests/typecheck, confirm it matches the spec. Do not blindly
   trust Codex output.
5. Claude does the final review and integration.

## Operating notes

- Subagents: if you're on a plan that allows parallel Codex agents, 5–7 at once
  is a practical ceiling for focused sub-tasks.
- Context hygiene: context rot is real. Clear the conversation after a few
  compactions and use a handoff/summary to preserve state across resets.
- Reserve Codex for heavy lifting; keep light reasoning, planning, and review on
  Claude.

## Reality check

Treat throughput/savings claims from the source thread (e.g. "60% token
savings", "never hit limits") as anecdotal, not guaranteed. The genuine value is
the division of labor: Claude for judgment, Codex for volume implementation,
with a human-reviewed gate in between.
