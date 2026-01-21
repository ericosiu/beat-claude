# Scoring Rubric: Engineer 004

This challenge-specific rubric supplements the [general scoring methodology](../../SCORING.md).

## Challenge-Specific Evaluation Points

### Strategic Depth (30 points)

**What we're looking for:**
- Understanding of event streaming vs. batch trade-offs
- Recognition of exactly-once semantics challenges
- Appreciation for multi-tenant isolation
- Realistic migration risk assessment

**Red flags:**
- Proposes complete rewrite without migration plan
- Ignores multi-tenancy entirely
- Underestimates operational complexity
- No consideration of failure modes

### Specificity (25 points)

**What we're looking for:**
- Concrete technology choices with rationale
- Actual cost estimates with line items
- Specific Kafka topic/partition design
- Clear data model with schemas

**Red flags:**
- "Use a message queue" without specifics
- Missing cost analysis
- Vague "use best practices" statements
- No schema design

### AI Fluency (20 points)

**What we're looking for:**
- Understanding of AI/ML pipeline integration potential
- Use of AI for anomaly detection
- Awareness of LLM-based log analysis
- Modern tooling choices

**Red flags:**
- Purely traditional architecture
- No mention of observability automation
- Ignores AI-assisted development practices

### Creativity (15 points)

**What we're looking for:**
- Non-obvious architectural choices
- Novel approaches to identity stitching
- Creative cost optimization
- Pattern recognition from similar systems

**Bonus points for:**
- Edge computing considerations
- Novel buffering strategies
- Creative use of serverless
- Experience-based insights from similar builds

### Communication (10 points)

**What we're looking for:**
- Clear diagrams (ASCII, Mermaid, or visual)
- Logical flow from problem to solution
- Appropriate detail level
- Trade-offs clearly articulated

---

## Hints for What Beats Claude

Claude's baseline answer is architecturally sound but textbook:
- Standard Kafka + Flink + ClickHouse stack
- Generic migration strategy
- Conservative technology choices

**To beat it, you might:**
- Propose a simpler architecture that still meets requirements
- Show deeper understanding of Kafka partition design for multi-tenant
- Demonstrate experience with similar migrations (what actually goes wrong)
- Challenge the ClickHouse choice with alternatives
- Show more sophisticated identity resolution
- Include monitoring/observability strategy
- Propose innovative cost optimization

**Claude's answer tends to be:**
- Correct but could be from any architecture blog
- Missing operational war stories
- Conservative on build-vs-buy decisions

The bar to beat is "senior engineer who read the docs." To win, show us you've built and operated systems like this.
