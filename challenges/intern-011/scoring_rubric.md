# Scoring Rubric: Intern 011

## Overview

Candidates submit three parts: their domain choice, an agent design + working prototype, and a meta question about their automation instincts. The prototype is the differentiator.

## Scoring Criteria (100 points)

### Builder Instinct — 30 points

The core question: **Did they ship something that works?**

| Score | Criteria |
|-------|----------|
| 24-30 | Working prototype that handles the core workflow. Code or no-code, doesn't matter — it runs. Demo shows real or realistic data flowing through. Clear README or walkthrough. |
| 15-23 | Partial prototype — built the hardest part, explained the rest. Shows real technical or tool competence. |
| 6-14 | Described what they'd build in detail but didn't build it. Architecture is sound but no working code/demo. |
| 0-5 | No prototype, no demo, no code. Pure strategy doc. |

### Agent Design Quality — 25 points

Is the architecture sound and production-aware?

| Score | Criteria |
|-------|----------|
| 20-25 | Clear data flow, appropriate tool/API choices, handles edge cases explicitly, knows what stays human and why. Could see this working in production with more time. |
| 12-19 | Good architecture but misses some edge cases or makes questionable tool choices without justification. |
| 5-11 | Surface-level design. "Use GPT to do it" without specifics on prompts, data handling, or failure modes. |
| 0-4 | No real architecture. Vague hand-waving about AI. |

### Creative Problem Framing — 20 points

Did they see something non-obvious?

| Score | Criteria |
|-------|----------|
| 16-20 | Reframed the problem in a way that makes the solution better. Saw angles the brief didn't suggest. Combined tools or approaches in unexpected ways. |
| 10-15 | Some creative choices but mostly followed the obvious path. |
| 4-9 | Entirely conventional approach. No surprises. |
| 0-3 | Copy-paste thinking. Took the brief literally with no original insight. |

### AI Fluency — 15 points

Do they understand AI's capabilities and limitations?

| Score | Criteria |
|-------|----------|
| 12-15 | Uses the right models for the right tasks. Understands token limits, context windows, prompt design. Knows when AI is the wrong tool. Shows evidence of daily AI use. |
| 7-11 | Reasonable AI usage but some misunderstandings about capabilities or limitations. |
| 3-6 | Treats AI as magic — "just feed it to GPT" without understanding what that means technically. |
| 0-2 | Little evidence of working with AI tools. |

### Communication — 10 points

| Score | Criteria |
|-------|----------|
| 8-10 | Tight, scannable, no filler. Technical choices are explained clearly. Shows personality. |
| 5-7 | Readable but some filler or poor organization. |
| 2-4 | Wordy, buried lead, hard to follow. |
| 0-1 | Confusing, unprofessional, or clearly unedited. |

## Bonus Points

### The Scrappiness Bonus (+5 max)

Awarded when a candidate does something notably resourceful:
- Built with free-tier tools only
- Shipped in significantly under 2 hours and it shows polish
- Found a clever workaround for a limitation
- Used a tool in a way it wasn't designed for (and it worked)

## Red Flags (Auto-Deduct)

| Red Flag | Deduction |
|----------|-----------|
| No prototype or demo of any kind | -15 |
| Submission reads like raw AI output | -15 |
| Claims to have built something but provides no link, code, or video | -10 |
| Designed a system that would take 6 months to build (over-scoped) | -5 |
| Didn't answer the meta question | -5 |

## What Beats Claude on This Challenge

Claude's baseline will produce a well-structured architecture doc with clean diagrams and thorough edge case analysis. It will be competent and comprehensive.

But Claude can't:
- **Ship a working prototype** with real judgment calls baked in
- **Make scrappy trade-offs** about what to build in 2 hours vs. what to skip
- **Show a personal automation instinct** in the meta question
- **Demonstrate taste** about what should stay human vs. what should be automated

Any candidate who submits a working demo — even a rough one — automatically differentiates from Claude's baseline. The bar isn't polish. The bar is: *did you build it?*
