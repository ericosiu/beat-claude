# Challenge: Ops COO 009

## Running the Operating System of an AI-Native Company

### The Situation

You're the new Head of Operations at a marketing agency that's mid-transition from traditional services to tech-enabled services (TES). The company has built an AI agent system that generates 50+ outputs per day. Nobody converts those outputs into outcomes. You're here to fix that.

**The Company: Single Grain**
- ~45-person digital marketing agency (SEO, Paid Media, Creative, CRO)
- Working with Amazon, Uber, Salesforce-class clients
- Average agency deal: $20K+ MRR
- SaaS product (ClickFlow): $11K MRR, targeting $25K MRR by end of year
- Second product (Karrot): LinkedIn ad platform, stable revenue
- Total revenue target: $7M this year, 50% TES revenue by 2028

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

You've been here 30 days. Time to audit the 48 crons. Here's a sample:

| Cron | Agent | Frequency | Output | Action Rate |
|------|-------|-----------|--------|-------------|
| GSC Quick Win Scan | Oracle | Daily | 8-12 keywords | 12% actioned |
| LinkedIn Prospect Sourcer | Cyborg | 2x daily | 10-15 profiles | 8% converted to meetings |
| Content Repurpose — YouTube | Flash | Daily per video | 5-8 social posts | 35% published |
| Deal Revival Scan | Alfred | Weekly | 3-5 stale deals | 60% followed up |
| Competitor Pricing Monitor | Oracle | Daily | Price change alerts | 3% led to action |
| Churn Signal Detector | Alfred | Daily | Risk flags | 20% investigated |
| Weekly Content Calendar | Flash | Weekly | 15-post calendar | 50% used |
| Candidate Outreach Follow-up | Cyborg | Daily | Re-engagement msgs | 5% response rate |

Based on this data, which crons do you keep, kill, or improve? Show your reasoning. What's your framework for making this call?

### Part 4: Your AI Operating Edge

- What's one operational workflow you've personally automated or augmented with AI? Give us the before/after with real metrics.
- You're reviewing Oracle's output from last night: 12 "quick win" keywords for singlegrain.com. How do you evaluate whether these are actually good recommendations without being an SEO expert?
- What does a Head of Operations look like in 2028 at a company where AI agents do 60% of the production work?

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

**Maximum 4 pages.** If you can make your case in 3, don't write 4. Diagrams and decision trees don't count toward the limit. Estimated time: 1-2 hours.

Your submission is scored alongside Claude's baseline answer in a blind review. See [SCORING.md](../../SCORING.md) for the general rubric.

---

**Ready to submit?** Email to `beat-claude@singlegrain.com` with subject line `[ops-coo-009] - Your Name`

**Questions?** Open an issue in this repo.
