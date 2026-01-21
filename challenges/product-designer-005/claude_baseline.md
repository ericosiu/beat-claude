# Claude's Answer: Product Designer 005

*This is Claude's response to the challenge brief. Your submission will be compared against this in a blind review.*

---

## B2B Onboarding Redesign

### Executive Summary

The 43% drop-off at team invites reveals a fundamental UX mistake: forcing collaborative actions before showing individual value. The fix: let users experience the product solo first, then prompt team invites when they have context for why it matters.

**Goal:** Improve sign-up to first-value from 40% → 60%+ by removing friction and reordering steps.

---

## 1. Problem Analysis

### Root Cause: Premature Collaboration Ask

The current flow assumes users want to set up their whole team immediately. User research says otherwise:
> "I just wanted to try it myself first before inviting my team"

**The insight:** Users need to validate the tool personally before advocating for it internally.

### Step-by-Step Breakdown

| Step | Issue | Evidence |
|------|-------|----------|
| Team setup (43% drop-off) | Asks for commitment before value | User research: "try it myself first" |
| Integration setup (11% drop-off) | Too many options, overwhelming | User research: "felt overwhelming" |
| First project (3% drop-off) | Low friction, but why create empty project? | Unclear purpose |
| Tutorial (+2%!) | Actually helps—but 60% never see it | Comes too late |

### Assumptions in Current Flow

1. ❌ Users want to invite teammates immediately
2. ❌ More integrations upfront = better
3. ❌ Empty project creation is meaningful
4. ❌ Tutorial should come after setup

### The Real "First Value"

For a project management tool, first value is:
- Seeing how the UI works with real content
- Understanding how it would help their team
- Feeling "I could use this"

Current flow delays this by 10+ minutes of setup.

---

## 2. Redesigned Flow

### New Flow (3 core steps + progressive disclosure)

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Quick Account (30 seconds)                         │
│  - Email + password only                                     │
│  - Company name auto-detected from email domain              │
│  - Skip team invites entirely                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Role & Template (60 seconds)                        │
│  - "What's your role?" (PM, Designer, Account Manager)       │
│  - "Pick a template" (3 options based on role)               │
│  - Pre-populated project with sample content                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Interactive Sandbox (2-3 minutes)                   │
│  - Land directly in pre-populated project                    │
│  - Guided hotspots: "Try dragging this task"                 │
│  - Inline tutorial (not separate step)                       │
│  - "Aha moment" achieved                                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  POST-VALUE PROMPTS (Progressive)                            │
│  - After 2 minutes: "Connect Slack for notifications?"       │
│  - After creating 1 task: "Invite a teammate to assign this" │
│  - After 24 hours: "Set up your real project?"               │
└─────────────────────────────────────────────────────────────┘
```

### Wireframe Descriptions

#### Step 1: Quick Account
```
┌─────────────────────────────────────────┐
│  [Logo]                                 │
│                                         │
│  Get started in 30 seconds              │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ Work email                      │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ Password                        │   │
│  └─────────────────────────────────┘   │
│                                         │
│  [Continue →]                           │
│                                         │
│  or continue with [Google] [Microsoft] │
│                                         │
└─────────────────────────────────────────┘
```

- Removed: Company name (auto-detect from email)
- Removed: Team invites (moved to post-value)
- Added: SSO for faster signup

#### Step 2: Role & Template
```
┌─────────────────────────────────────────┐
│  What do you do?                        │
│                                         │
│  [Project Manager] [Designer] [Account] │
│                                         │
│  Start with a template:                 │
│                                         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │ Client  │ │ Sprint  │ │ Content │   │
│  │ Project │ │ Board   │ │ Calendar│   │
│  │         │ │         │ │         │   │
│  │ 12 tasks│ │ 8 tasks │ │ 15 tasks│   │
│  └─────────┘ └─────────┘ └─────────┘   │
│                                         │
│  [Let's go →]                           │
│                                         │
└─────────────────────────────────────────┘
```

- Templates pre-populated with realistic sample content
- Role selection personalizes the experience
- User immediately understands what they'll see

#### Step 3: Interactive Sandbox
```
┌─────────────────────────────────────────────────────────────┐
│  [Sidebar]  │  Client Website Redesign (Sample Project)     │
│             │                                                │
│  Projects   │  ┌─────────────────────────────────────────┐  │
│  > Sample   │  │ ◉ Design homepage mockup    [Due: Today]│  │
│             │  │   Assigned to: You                      │  │
│  Team       │  │   ┌──────────────────────────────┐      │  │
│  Settings   │  │   │ 💡 Try dragging this to      │      │  │
│             │  │   │    "In Progress"             │      │  │
│             │  │   └──────────────────────────────┘      │  │
│             │  └─────────────────────────────────────────┘  │
│             │                                                │
│             │  ┌─────────────────────────────────────────┐  │
│             │  │ ○ Review client feedback                │  │
│             │  └─────────────────────────────────────────┘  │
│             │                                                │
└─────────────┴────────────────────────────────────────────────┘
```

- User lands in a working project, not empty state
- Guided hotspots teach by doing
- Tutorial is embedded, not separate

---

## 3. Key Design Decisions

### What Changed

| Old | New | Why |
|-----|-----|-----|
| Team invite required | Team invite optional, post-value | Biggest drop-off point |
| 4+ integrations shown | 1 contextual integration prompt | Reduce overwhelm |
| Empty project creation | Pre-populated template | Show value immediately |
| Tutorial as final step | Tutorial embedded in experience | User is already engaged |
| 5-step wizard | 3-step wizard | Reduce perceived effort |

### Trade-offs

| Gain | Sacrifice |
|------|-----------|
| Higher completion rate | Fewer team invites on Day 1 |
| Faster time-to-value | Less data collected upfront |
| Lower cognitive load | Delayed integration setup |

### Why This Works

1. **Reduced commitment upfront:** Users only give email + password
2. **Show, don't tell:** Pre-populated templates demonstrate value
3. **Progressive disclosure:** Team invites come after "aha moment"
4. **Contextual prompts:** Integration asks happen when relevant

---

## 4. Progressive Disclosure Strategy

### Time-Based Prompts

| Trigger | Prompt | Rationale |
|---------|--------|-----------|
| After 2 min in sandbox | "Get notifications in Slack?" | User is engaged, low-friction add |
| After creating first task | "Assign to a teammate?" | Natural moment to invite |
| After 24 hours | Email: "Ready to set up your real project?" | Re-engage with progress |
| After 3 days (no team) | "Teams with 3+ people are 4x more productive" | Social proof nudge |

### Skipped Step Recovery

For users who skip team invites:
1. **Empty state prompts:** "This task has no assignee—invite someone?"
2. **Celebration moments:** "You've completed 10 tasks! Share the load?"
3. **Settings reminder:** Badge on team settings until first invite

For users who skip integrations:
1. **Contextual triggers:** When they mention Slack in a comment, prompt connection
2. **Weekly digest email:** "Connect Google Calendar to see deadlines here"

---

## 5. Success Metrics

### Primary Metric
- **Sign-up to first-value conversion:** 40% → 60%+
- Definition of "first-value": Completed 1 action in sandbox (drag task, create task, or similar)

### Secondary Metrics

| Metric | Current | Target | Why It Matters |
|--------|---------|--------|----------------|
| Time to first value | 12 min | <3 min | Speed = engagement |
| 7-day team invite rate | 45% | 50%+ | Preserve virality |
| 14-day integration rate | 30% | 35%+ | Preserve retention driver |
| Onboarding support tickets | 35% | <20% | Reduce support load |

### Leading Indicators (Week 1)

- Sandbox completion rate (target: 85%+)
- Template selection distribution (validate options)
- Hotspot interaction rate (are guides helpful?)
- Drop-off at each remaining step

### When We'll Know

- **1 week:** Sandbox engagement data
- **2 weeks:** Conversion rate trend
- **30 days:** Confidence in 60% target
- **60 days:** Team invite + integration rate impact

---

## 6. V1 Scope (2-Week Sprint)

### Must Have (Week 1-2)

1. Remove team invite from onboarding (move to post-value)
2. Add role + template selection step
3. Pre-populate 3 templates with sample content
4. Land users in project (not empty dashboard)

**Engineering effort:** ~8-10 days

### Nice to Have (Cut if needed)

- Embedded hotspot tutorial (can use existing modal tutorial)
- SSO buttons on signup (keep email/password only)
- Contextual integration prompts (use existing integrations page)

### Cut for V2

- Personalized templates based on company size
- AI-powered template suggestions
- Animated onboarding guide

### Rollout Plan

| Week | Action |
|------|--------|
| Week 1 | Build core flow changes |
| Week 2 | QA + polish |
| Week 3 | 10% rollout, monitor metrics |
| Week 4 | 50% rollout if metrics hold |
| Week 5 | 100% rollout |

---

## Summary

The current onboarding fails because it asks for collaboration before showing individual value. The fix:

1. **Get to value fast:** 3 steps, <3 minutes
2. **Show, don't explain:** Pre-populated templates
3. **Ask later:** Team invites after "aha moment"
4. **Recover gracefully:** Progressive prompts for skipped steps

Expected impact: 40% → 60%+ conversion, with preserved (or improved) team invite and integration rates over 14 days.
