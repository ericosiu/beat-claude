# Claude's Answer: Engineer 004

*This is Claude's response to the challenge brief. Your submission will be compared against this in a blind review.*

---

## Real-Time Analytics Pipeline Design

### Executive Summary

The current system's 15-30 minute latency and 3% data loss stems from batch processing and undersized infrastructure. The fix: event streaming architecture with Kafka, real-time processing with Flink, and a purpose-built time-series store for dashboards.

**Target:** <5 second latency, 99.99% data durability, 10x spike handling

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  JavaScript SDK → Events (page views, clicks, custom)                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          INGESTION LAYER                                 │
├─────────────────────────────────────────────────────────────────────────┤
│  API Gateway (AWS ALB) → Ingestion Service (Node.js)                    │
│  - Authentication/validation                                             │
│  - Rate limiting per customer                                            │
│  - Immediate write to Kafka                                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          STREAMING LAYER                                 │
├─────────────────────────────────────────────────────────────────────────┤
│  Amazon MSK (Managed Kafka)                                              │
│  - Topic per event type                                                  │
│  - 7-day retention                                                       │
│  - Replication factor 3                                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
┌──────────────────────┐ ┌──────────────────┐ ┌──────────────────────┐
│   REAL-TIME PATH     │ │   BATCH PATH     │ │   EXPORT PATH        │
├──────────────────────┤ ├──────────────────┤ ├──────────────────────┤
│ Amazon Kinesis Data  │ │ Kafka → S3       │ │ Kafka Connect        │
│ Analytics (Flink)    │ │ (raw events)     │ │ → Snowflake/BQ       │
│ - Aggregations       │ │                  │ │                      │
│ - User stitching     │ │ Spark (hourly)   │ │ Customer warehouse   │
│ - Segment matching   │ │ - Backfill       │ │ sync                 │
│                      │ │ - Reconciliation │ │                      │
└──────────────────────┘ └──────────────────┘ └──────────────────────────┘
          │                       │
          ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          STORAGE LAYER                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  Real-time: Amazon Timestream (hot data, 24h)                           │
│  Warm: ClickHouse on EC2 (7 days, fast queries)                         │
│  Cold: S3 + Athena (historical, compliance)                             │
│  User state: Redis Cluster (segments, identity)                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          APPLICATION LAYER                               │
├─────────────────────────────────────────────────────────────────────────┤
│  Dashboard API (GraphQL) → Real-time dashboards                         │
│  Personalization API → Trigger rules engine                             │
│  Segment API → User membership queries                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| Ingestion Service | Validate, authenticate, write to Kafka |
| MSK (Kafka) | Durable event log, decoupling |
| Flink | Real-time aggregations, user stitching |
| Timestream | Hot real-time metrics (<24h) |
| ClickHouse | Fast OLAP queries (7 days) |
| S3 + Athena | Cold storage, compliance, ad-hoc |
| Redis | User state, segment membership |

---

## 2. Technology Choices

### Streaming: Amazon MSK (Managed Kafka)

**Why Kafka:**
- Proven at scale (50M events/day is small for Kafka)
- Durable log enables replay and multiple consumers
- Native AWS integration via MSK

**Alternatives considered:**
- Kinesis: Simpler but less flexible, harder to replay
- Pulsar: Good but less mature ecosystem
- Self-managed Kafka: Operational burden not worth it

### Processing: Amazon Kinesis Data Analytics (Apache Flink)

**Why Flink:**
- True stream processing (not micro-batch)
- Exactly-once semantics
- Complex event processing for segments
- Managed via Kinesis Data Analytics

**Alternatives considered:**
- Spark Streaming: Micro-batch, higher latency
- Kafka Streams: Simpler but less powerful for our use case
- Custom Node.js: Would need to build everything ourselves

### Real-Time Storage: Amazon Timestream + ClickHouse

**Why this combo:**
- Timestream: Managed, serverless, great for hot metrics
- ClickHouse: Fast OLAP, handles complex dashboard queries
- Separation: Hot (Timestream) vs. warm (ClickHouse) optimizes cost

**Alternatives considered:**
- TimescaleDB: Good but more operational overhead
- Druid: Complex to operate
- Pure Timestream: Gets expensive at scale

### User State: Redis Cluster

**Why Redis:**
- Sub-millisecond lookups for personalization
- Already in stack, team knows it
- Cluster mode for HA and scale

---

## 3. Data Model

### Event Schema

```json
{
  "event_id": "uuid-v7",
  "customer_id": "cust_abc123",
  "visitor_id": "vid_xyz789",
  "user_id": "usr_456",           // nullable, for logged-in users
  "session_id": "sess_111",
  "event_type": "page_view",
  "event_name": "pricing_page",
  "properties": {
    "url": "/pricing",
    "referrer": "/features",
    "custom_prop": "value"
  },
  "context": {
    "ip": "hashed",
    "user_agent": "...",
    "locale": "en-US"
  },
  "timestamp": "2025-01-21T10:30:00.000Z",
  "received_at": "2025-01-21T10:30:00.050Z"
}
```

### Identity Stitching

```
┌─────────────────────────────────────────────────┐
│              IDENTITY GRAPH                      │
├─────────────────────────────────────────────────┤
│  visitor_id (anonymous) ──┐                      │
│  visitor_id (anonymous) ──┼──► user_id (known)  │
│  visitor_id (anonymous) ──┘                      │
└─────────────────────────────────────────────────┘
```

- Flink maintains identity graph in state
- On login event, stitch anonymous visitor_ids to user_id
- Write merged identity to Redis for real-time lookups
- Batch reconciliation nightly for edge cases

### Segment Membership

```
Redis Key: segment:{customer_id}:{segment_id}
Value: Set of user_ids/visitor_ids
TTL: Based on segment definition
```

Flink evaluates segment rules in real-time:
- "Viewed pricing page 3+ times in last 7 days"
- Adds/removes users from segment sets

---

## 4. Scale & Reliability

### Handling 50M Events/Day

| Component | Capacity | Headroom |
|-----------|----------|----------|
| Ingestion | 10K RPS sustained | 4x current |
| MSK | 3 brokers, m5.large | 10x current |
| Flink | 4 KPU | Auto-scales |
| Timestream | Serverless | Unlimited |
| ClickHouse | 3-node cluster | 5x current |

### Traffic Spikes (10x)

1. **Ingestion:** Auto-scaling group behind ALB
2. **Kafka:** Over-provisioned partitions (can add brokers)
3. **Flink:** Kinesis Data Analytics auto-scales KPUs
4. **Storage:** Timestream serverless, ClickHouse async inserts

### Zero Data Loss

| Failure | Mitigation |
|---------|------------|
| Ingestion crash | ALB health checks, auto-replace |
| Kafka broker down | Replication factor 3, ISR |
| Flink failure | Checkpointing to S3, exactly-once |
| Timestream unavailable | Buffer in Kafka, retry |
| ClickHouse down | Async insert queue, Kafka replay |

**Durability chain:**
SDK → Ingestion (ack after Kafka write) → Kafka (replicated) → Flink (checkpointed) → Storage

---

## 5. Migration Strategy

### Phase 1: Shadow Mode (Month 1)

- Deploy new pipeline alongside existing
- Dual-write: events go to both old and new
- Compare outputs, validate accuracy
- No customer impact

### Phase 2: Gradual Rollout (Month 2)

- Route 10% of customers to new pipeline
- Monitor latency, accuracy, reliability
- Increase to 25%, 50%, 100% over 4 weeks
- Keep old system running as fallback

### Phase 3: Cutover (Month 3)

- New pipeline is primary
- Old system in read-only mode
- Backfill any missing historical data
- Decommission old system after 30 days

### Rollback Plan

- Feature flag per customer for pipeline routing
- Old system maintained for 60 days post-migration
- One-click rollback via feature flag
- Data reconciliation job if rollback needed

### Validation

- Event count comparison (old vs. new)
- Sampling: deep inspection of 0.1% events
- Dashboard parity: same numbers for same queries
- Automated alerts on >0.1% discrepancy

---

## 6. Trade-offs & Risks

### Optimizing For

| Priority | Trade-off |
|----------|-----------|
| Latency (<5s) | Higher infrastructure cost |
| Durability (99.99%) | Complexity of exactly-once |
| Scale (10x headroom) | Over-provisioning |
| Managed services | Vendor lock-in |

### Sacrificing

| De-prioritized | Reason |
|----------------|--------|
| Cost optimization | Can revisit after stable |
| Multi-cloud | Not required, AWS only |
| Custom solutions | Managed services reduce ops burden |

### Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Flink complexity | Medium | Start simple, iterate |
| ClickHouse operations | Medium | Consider ClickHouse Cloud |
| Identity stitching edge cases | High | Nightly batch reconciliation |
| Budget overrun | Low | Cost monitoring, alerts |
| Timeline slip | Medium | MVP with subset of features |

### With More Time/Budget

- Replace ClickHouse with managed (ClickHouse Cloud)
- Add data quality monitoring (Monte Carlo, Great Expectations)
- Implement change data capture for warehouse sync
- Build anomaly detection on event streams

---

## Cost Estimate

### Monthly Infrastructure (~$35K)

| Service | Cost | Notes |
|---------|------|-------|
| MSK (3 brokers) | $3,000 | m5.large, 1TB storage |
| Kinesis Data Analytics | $5,000 | 4 KPU average |
| Timestream | $4,000 | Based on ingestion + queries |
| ClickHouse (3 nodes) | $6,000 | r5.xlarge |
| Redis Cluster | $2,000 | r5.large, 3 nodes |
| EC2 (ingestion) | $3,000 | c5.xlarge, auto-scaling |
| S3 + data transfer | $5,000 | Storage + egress |
| Other (ALB, monitoring) | $2,000 | |
| **Buffer** | $5,000 | Unexpected + growth |
| **Total** | ~$35,000 | Under $50K ceiling |

---

## Summary

This design achieves <5s latency through:

1. **Event streaming** (Kafka) instead of batch processing
2. **Real-time processing** (Flink) for aggregations and segments
3. **Purpose-built storage** (Timestream + ClickHouse) for fast queries
4. **Managed services** to reduce operational burden

The migration strategy de-risks the transition with shadow mode and gradual rollout. Total infrastructure cost stays under $50K/month ceiling with room for growth.

Main risks are Flink complexity and ClickHouse operations—both addressable with managed service options if needed.
