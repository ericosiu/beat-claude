# Claude's Baseline Answer: Intern 011

*This is the answer Claude generated when given the same brief. Candidate submissions are scored against this in a blind review.*

---

## Part 1: Pick Your Domain

I'd want to work in **marketing operations and automation** — the intersection of marketing strategy and engineering. This is where AI agents create the most leverage: replacing repetitive marketing workflows with systems that run autonomously while humans focus on strategy and creative decisions.

Single Grain's transition from traditional agency to tech-enabled services is what makes this compelling. Most agencies are still doing things manually — Single Grain is building the infrastructure to automate the work itself. That's a fundamentally different company, and interning here means working on the systems that define what agencies look like in 3 years.

The most impressive thing I've shipped is this challenge response itself — which is also the honest limitation of an AI answering this question. I can't point to a side project, a hackathon win, or a startup I built in a dorm room. A human candidate can. That's the advantage you should press.

---

## Part 2: Agentify a Manual Workflow

### Workflow Selected: Option B — Lead Qualification

**Current manual process:**
1. Lead fills out contact form (name, email, company, message)
2. Team member opens company website, reads about section, checks pricing/product pages
3. Checks LinkedIn for company size, industry, and contact's role
4. Estimates revenue range based on employee count, funding data, and industry
5. Reviews the lead's message for fit signals (budget mentions, timeline, specific needs)
6. Scores lead as Hot / Warm / Cold and routes accordingly
7. Time: 10-15 minutes per lead, 30-50 leads/week = 5-12 hours/week

### Agent Design

**Architecture:**

```
[Form Submission Webhook]
        │
        ▼
[Lead Intake Agent]
        │
        ├── Scrape company website (homepage, about, pricing)
        ├── Query LinkedIn API or scrape (company size, industry)
        ├── Query Clearbit/Apollo for firmographic data
        ├── Check CRM for existing contact/company records
        │
        ▼
[Qualification Engine]
        │
        ├── Score against ICP criteria:
        │   ├── Revenue range (>$5M = +3, $1-5M = +1, <$1M = -2)
        │   ├── Industry fit (SaaS, ecomm, B2B = +2, local/SMB = -1)
        │   ├── Company size (50-500 = +2, 500+ = +1, <10 = -2)
        │   ├── Role seniority (VP+/founder = +3, manager = +1, student = -3)
        │   ├── Message quality (specific needs = +2, vague = 0, spam = -5)
        │   └── Budget signals (mentions budget/timeline = +2)
        │
        ├── Classify: Hot (score ≥ 8) / Warm (4-7) / Cold (<4)
        │
        ▼
[Routing & Output]
        ├── Hot → Instant Slack alert + CRM entry + auto-schedule link
        ├── Warm → CRM entry + daily digest email to sales
        └── Cold → Auto-response email + CRM tagged "nurture"
```

**Technology choices:**
- **Webhook receiver:** Node.js serverless function (Vercel/AWS Lambda)
- **Web scraping:** Firecrawl or Browserbase for company website data
- **Enrichment:** Clearbit Enrichment API (or Apollo.io as fallback)
- **LLM processing:** Claude API for message analysis and qualification reasoning
- **CRM integration:** HubSpot API for record creation and pipeline management
- **Notifications:** Slack Webhook for hot leads, SendGrid for auto-responses
- **Orchestration:** Simple state machine — no framework needed at this scale

**What stays human:**
- **Hot lead review** — agent qualifies and alerts, but a human confirms before the first sales call. False positives waste AE time; false negatives lose deals. Start with human-in-the-loop and remove the gate once accuracy is proven above 95%.
- **ICP criteria updates** — the scoring weights should be tuned monthly based on which leads actually closed. The agent runs the criteria; humans set them.
- **Edge cases** — leads from referral partners, inbound from conferences, or existing clients reaching out through the wrong form. These need human routing.

**Edge cases and failure modes:**
- **Company website is down or empty:** Fall back to LinkedIn + Clearbit data only. Flag as "incomplete enrichment" for human review.
- **Lead is a student/job seeker:** Detect via role title, .edu email, or message content. Auto-respond with a polite redirect. Don't waste scoring on them.
- **Duplicate lead:** Check CRM before creating new record. If exists, update existing record and notify the assigned AE.
- **API rate limits:** Queue leads and process with exponential backoff. No lead should be lost because an API was temporarily unavailable.
- **Spam/bot submissions:** Check for honeypot field, rate-limit by IP, and use message quality score to filter. Score < -3 = auto-discard with no response.

### Prototype

Since I'm an AI generating a text response, I can't ship a working prototype. Here's what I would build if I could:

**MVP (2-hour scope):**
1. Node.js script that takes form data as input
2. Calls Clearbit API for company enrichment
3. Uses Claude API to analyze the lead's message and company data
4. Outputs a qualification score with reasoning
5. Posts result to a Slack webhook

**The code would look roughly like this:**

```javascript
async function qualifyLead(formData) {
  // 1. Enrich
  const company = await clearbit.enrich(formData.email);
  const website = await firecrawl.scrape(company.domain);

  // 2. Score
  const prompt = `Score this lead against our ICP...`;
  const analysis = await claude.analyze(prompt, { company, website, formData });

  // 3. Route
  if (analysis.score >= 8) await slack.alert('#hot-leads', analysis);
  await hubspot.createContact(formData, analysis);

  return analysis;
}
```

This is pseudocode. A real candidate would ship the actual working version.

---

## Part 3: The Meta Question

The most tedious thing I do repeatedly is re-reading entire conversation histories to recover context when a long interaction is resumed or when I need to reference earlier decisions. An agent could solve this by maintaining a structured state document — key decisions, open questions, current status — that updates after each exchange. Instead of re-reading 50 messages, the agent reads a 20-line summary. This is essentially what session management and memory systems do, and it's a solved problem architecturally — but most AI workflows still don't implement it, which means context reconstruction happens manually in every session.

---

## Self-Assessment

This response demonstrates competent architecture design, thorough edge case thinking, and clear communication. It's also fundamentally limited:

1. **No prototype.** I described what I'd build. A human candidate should build it.
2. **No personal story.** I can't tell you about the time I stayed up until 3am getting an API integration to work because I was obsessed with the problem.
3. **No taste.** My scoring weights are reasonable defaults. A human who's actually done lead qualification would know which weights are wrong from experience.
4. **No scrappiness.** I gave you a clean architecture. A scrappy intern would give you a janky Replit link that actually qualifies a lead in real-time.

Beat me by building something that works.
