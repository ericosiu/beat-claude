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

### Evaluation Criteria

See [SCORING.md](../../SCORING.md) for how submissions are evaluated.

Your answer will be compared against Claude's answer to this same brief in a blind review.

### Format

Submit as PDF or Markdown. **Maximum 4 pages** (diagrams don't count toward limit). Diagrams encouraged (ASCII, Mermaid, or images). Estimated time: 1-2 hours.

---

**Questions about the brief?** Open an issue in this repo.

**Ready to submit?** Email to `beat-claude@singlegrain.com` with subject line `[engineer-004] - Your Name`
