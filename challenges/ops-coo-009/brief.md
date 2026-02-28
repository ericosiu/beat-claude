# Challenge: Ops COO 009

## Running the Operating System of an AI-Native Company

### The Situation

You're the new COO / GM at a marketing agency that's mid-transition from traditional services to tech-enabled services (TES). The company has built an AI agent system that generates 50+ outputs per day. Nobody converts those outputs into outcomes. You're here to fix that.

**The Company: Single Grain**
- ~45-person digital marketing agency (SEO, Paid Media, Creative, CRO)
- Working with Amazon, Uber, Salesforce-class clients
- Average agency deal: $20-30K MRR
- Two TES/SaaS products (ClickFlow + Karrot): $12K combined MRR, targeting $83K MRR by end of year, with new signups coming in daily
- Goal: 50% TES revenue by 2028

**The CEO: Eric Siu**
- ENTJ/8w7, Kolbe Quick Start 9, Follow Thru 2
- Hosts Leveling Up podcast, co-hosts Marketing School with Neil Patel
- Self-rated: Follow-Through C-tier, Organization C-tier, Workflow Consistency D-tier
- Starts 10 things, finishes 3. Your job: make it 10 for 10
- Currently spends 60+ minutes/day on operational approvals (should be 15)

**The AI Agent System**

| Agent | Function | Daily Output |
|-------|----------|-------------|
| Oracle | SEO/content intelligence — scans GSC/GA4, surfaces quick wins, drafts content | 8-12 keyword recommendations, content briefs |
| Flash | Content repurposing — turns YouTube videos into social clips, newsletters | 5-10 content pieces across platforms |
| Cyborg | Talent/outreach — sources candidates, sends personalized outreach | 10-15 prospect profiles, outreach sequences |
| Alfred | Orchestration/chief of staff — coordinates agents, generates briefings | Daily briefings, cross-agent task routing |

**Total:** 48 crons across 4 agents. 50+ messages/day. 15+ items hit the review queue daily. Average queue age: 2+ days. Eric is the bottleneck.

**The Dashboard (Single Brain)**
- Mission Control homepage with agent status, KPIs, pending actions
- Pipeline page showing AI-surfaced prospects in various stages
- Campaign manager for multi-step outreach sequences
- Currently live but underutilized — Eric checks it sporadically

**Your Team on Day One**
- You
- The AI agent system (your primary workforce)
- Eric (CEO — your boss and your biggest operational challenge)
- Shaun (CTO — maintains the tech layer)
- Sales team (one closer, one BDR, one hybrid)

---

## Your Task

You inherit this system on Monday. The review queue has 23 pending items, some 4 days old. ClickFlow just lost 2 customers this month (no one followed up on churn signals). Oracle surfaced 15 quick-win keywords last week — none have been actioned. Three sales prospects went cold because outreach follow-ups expired.

**Create your operational takeover plan.** Address all four parts below.

---

### Part 1: First 48 Hours (Triage)

The house is on fire. You have 23 pending items, 2 churning customers, and a CEO who's already moved on to his next big idea.

- What do you do first? Walk us through your first 48 hours, hour by hour.
- How do you triage the 23 pending items without knowing the system yet?
- Which of the three fires (queue backlog, ClickFlow churn, stale prospects) do you handle first, and why?
- What do you need from Eric in these first 48 hours? Be specific — he's got 30 minutes for you.

### Part 2: The Risk Tiering System

Eric can't review 15+ items daily. Design a system that reduces his daily load to 3-5 items.

- Define your green/yellow/red tiers with specific examples of what goes in each
- What auto-executes without human review? What's the risk tolerance?
- How do you handle the inevitable mistake — an auto-approved item that shouldn't have been?
- Show us the actual decision tree or criteria, not just the concept

### Part 3: The Elon Algorithm Audit

You've been here 30 days. Time to audit the 48 crons. Here's a sample of 8 with descriptions of what each one does:

| Cron | Agent | Frequency | What It Does | Output | Action Rate |
|------|-------|-----------|-------------|--------|-------------|
| GSC Quick Win Scan | Oracle | Daily | Pulls Google Search Console data to find pages ranking positions 8-20 that could move to page 1 with minor optimization (title tag changes, content additions, internal linking) | 8-12 keyword recommendations with specific pages and suggested changes | 12% actioned |
| LinkedIn Prospect Sourcer | Cyborg | 2x daily | Searches LinkedIn for prospects matching our ICP (marketing leaders at companies $10M-$500M revenue), enriches profiles with company data, and drafts personalized outreach messages | 10-15 prospect profiles with draft outreach sequences | 8% converted to meetings |
| Content Repurpose — YouTube | Flash | Daily per video | Takes new YouTube uploads from Eric's channel, pulls transcript, identifies 3-5 clip-worthy moments, generates platform-specific posts (LinkedIn, X, Instagram) with hooks and captions | 5-8 social posts per video, formatted per platform | 35% published |
| Deal Revival Scan | Alfred | Weekly | Scans CRM for deals marked closed-lost or stalled in the last 90 days, cross-references with recent company news (funding, leadership changes, hiring signals) to identify re-engagement opportunities | 3-5 stale deals with trigger events and suggested re-approach angles | 60% followed up |
| Competitor Pricing Monitor | Oracle | Daily | Scrapes competitor websites and G2/Capterra for pricing changes, new plan tiers, or promotional offers across 12 tracked competitors | Price change alerts with before/after comparison | 3% led to action |
| Churn Signal Detector | Alfred | Daily | Monitors ClickFlow product usage data — flags accounts with declining logins, reduced feature usage, or support ticket spikes compared to their 30-day average | Risk flags with usage trend data and days since last login | 20% investigated |
| Weekly Content Calendar | Flash | Weekly | Aggregates trending topics from Oracle's keyword data + social listening, maps them to Eric's content pillars, and generates a 15-post editorial calendar with suggested formats and hooks | 15-post calendar with topic, format, platform, and draft hook for each | 50% used |
| Candidate Outreach Follow-up | Cyborg | Daily | Re-engages candidates who didn't respond to initial outreach after 5 days — sends a templated follow-up referencing their recent LinkedIn activity or company news | Automated re-engagement messages to non-responsive candidates | 5% response rate |

Based on this data, which crons do you keep, kill, or improve? Show your reasoning. What's your framework for making this call?

### Part 4: Your Operating Edge

**AI Fluency:**
- What's one operational workflow you've personally automated or augmented with AI? Give us the before/after with real metrics.
- You're reviewing Oracle's output from last night: 12 "quick win" keywords for singlegrain.com. How do you evaluate whether these are actually good recommendations without being an SEO expert?
- What does a COO / GM look like in 2028 at a company where AI agents do 60% of the production work?

**Operational Experience:**
- Tell us about a time you inherited a broken or nonexistent operating rhythm and installed one. What did the cadence look like? How did you enforce it when people resisted?
- How do you ensure processes actually get followed — not just documented? Give a specific example of a process you enforced that people initially pushed back on.
- Describe a situation where you had to keep the trains running on time across multiple departments or workstreams with competing priorities. What was the mechanism?

**MMPI Self-Assessment:**
- Using your preferred LLM (ChatGPT, Claude, Gemini, etc.), run an MMPI-style personality assessment on yourself. Include the key findings in your submission. We're not looking for a perfect profile — we're looking for self-awareness and willingness to be transparent about how you're wired.

---

## What We're Evaluating

| Criterion | Weight | What We're Looking For |
|-----------|--------|----------------------|
| Operational judgment | 30% | Do your triage calls and prioritization reveal real experience? |
| AI fluency | 25% | Can you manage AI agents as a workforce, not just use AI as a tool? |
| Complexity reduction | 20% | Does your plan simplify or add complexity? Do you kill things? |
| Specificity | 15% | Could someone execute your plan tomorrow? |
| Communication | 10% | Clear, concise, structured like someone who respects other people's time |

## What Will Lose

- A 48-hour plan that starts with "schedule stakeholder meetings"
- A risk tiering system that's conceptual instead of concrete
- An Elon Algorithm audit that keeps everything running and adds more
- "I use ChatGPT for writing SOPs" as your AI edge
- Anything that could apply to any company's operations

## What Will Win

- Triage decisions that reveal pattern recognition from real experience
- A risk tiering system specific enough to implement Monday
- An audit that kills at least 2 crons with clear reasoning
- Evidence you've actually managed automated systems, not just read about it
- The instinct to close loops, not open new workstreams

---

## Format

**Maximum 2 pages.** Diagrams and decision trees don't count toward the limit. Estimated time: 1-2 hours.

Your submission is scored alongside Claude's baseline answer in a blind review. See [SCORING.md](../../SCORING.md) for the general rubric.

---

**Ready to submit?** Email to `beat-claude@singlegrain.com` with subject line `[ops-coo-009] - Your Name`

**Include with your submission:**
- Your LinkedIn profile URL (we're looking for long tenure and a track record of promotions — ideally at 2+ companies, because that means multiple organizations valued you enough to invest in your growth)
- Your MMPI self-assessment results (from Part 4)

**Questions?** Open an issue in this repo.
