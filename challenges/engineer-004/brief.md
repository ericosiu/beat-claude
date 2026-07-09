# Challenge: Engineer 004

## System Design: Real-Time Analytics Pipeline

### The Situation

You're joining a marketing technology company as a senior engineer. The company has a product that tracks website visitor behavior and needs to rebuild their analytics pipeline.

**Company Context**
- Series B martech startup ($20M raised)
- Core product: Website personalization platform
- Engineering team: 12 engineers (3 senior, 6 mid, 3 junior)
- Current tech stack: Python, Node.js, PostgreSQL, Redis, AWS

**Current System (broken)**
- Receives ~50M events/day from JavaScript SDK
- Events: page views, clicks, form submissions, custom events
- Current latency: 15-30 minutes from event to dashboard
- Customers complaining: want real-time (<5 second) visibility
- System crashes during traffic spikes (Black Friday, product launches)
- Data accuracy issues: ~3% event loss during peak periods

**Customer Requirements**
- Real-time dashboards showing visitor behavior
- Ability to trigger personalization based on recent behavior
- Segment users by behavior patterns (viewed pricing 3x, etc.)
- Export data to customer data warehouses (Snowflake, BigQuery)
- GDPR/CCPA compliance (data deletion requests)

**Constraints**
- Budget: $50K/month infrastructure ceiling
- Timeline: MVP in 3 months, full system in 6 months
- Team: 2 senior engineers can be dedicated full-time
- Cannot break existing integrations during migration

### Your Task

Design the **architecture for a real-time analytics pipeline** that solves the latency, reliability, and scale problems.

### What to Submit

Your design should include:

1. **Architecture & Technology Choices**
   - High-level system diagram with key components and data flow from SDK to dashboard
   - What technologies/services for each component? Why these over alternatives?
   - How do you structure event data and handle user identity/stitching?

2. **Scale, Reliability & Migration**
   - How do you handle 50M+ events/day and 10x traffic spikes with zero data loss?
   - How do you move from current system without breaking things? Rollback plan?
   - How do you validate data accuracy?

3. **Trade-offs & Risks**
   - What are you optimizing for vs. sacrificing?
   - What could go wrong? What would you do differently with more time/budget?

### Constraints

- Must run on AWS (existing infrastructure)
- Cannot require customers to update SDK (breaking change)
- Must support multi-tenant architecture (500+ customers)
- Compliance: SOC 2, GDPR, CCPA


## Ground It in the Sample Data (Required)

This folder includes a fixture dataset: [`fixtures/event_sample.jsonl`](fixtures/event_sample.jsonl). It is a small synthetic snapshot of the situation above, and it contains seeded issues - not everything in it should be taken at face value. We know exactly what is planted in it, so your reading of the data tells us immediately whether the analysis is real.

- Your design must state, anomaly class by anomaly class, how the pipeline handles what is actually in this sample. Cite specific `event_id`s. A small script that detects the anomalies is a strong artifact.
- Call out at least three things in the data you would **not** act on at face value, and why.
- State the fixture checksum you worked from: `shasum -a 256 fixtures/event_sample.jsonl`.

Fixtures rotate between hiring rounds; answers built against an old fixture will not match the current one. See the [Integrity section of SCORING.md](../../SCORING.md#integrity).

## Required Submission Packet

Include these items with your submission:

1. **Written answer**: the main response to the brief.
2. **Operating artifact**: Engineering operating artifact, such as a repo, runnable script, architecture diagram, test plan, benchmark, trace, or log export.
3. **Evidence log**: list major claims and the proof tier for each, using the tiers in [SCORING.md](../../SCORING.md).
4. **Number source labels**: label every number as observed, estimated, benchmarked, or assumed.
5. **AI usage disclosure**: name the tools you used, what they helped with, what you changed, and what you checked yourself.
6. **What breaks it**: describe the most likely failure modes, bad inputs, missing data, or constraints that would make your answer wrong.
7. **What stays human**: explain which decisions or approvals should not be automated and why.

A polished written answer without an artifact and source-labeled numbers is unlikely to advance.

### Evaluation Criteria

See [SCORING.md](../../SCORING.md) for how submissions are evaluated.

Your answer will be compared against the private reviewer benchmark for the same brief in a blind review.

### Format

Submit as PDF or Markdown. **Maximum 4 pages** (diagrams don't count toward limit). Diagrams encouraged (ASCII, Mermaid, or images). Estimated time: 1-2 hours.

---

**Questions about the brief?** Open an issue only for general public clarification. For role-specific ambiguity, state your assumptions in the submission.

**Brief version:** 2026-07. State this version in your written answer. Briefs are refreshed periodically; we review against the version you cite.

**Ready to submit?** Apply through our careers page: **[singlegrain.com/careers](https://www.singlegrain.com/careers/)**
Upload your challenge answer (PDF or Markdown) along with your application.
