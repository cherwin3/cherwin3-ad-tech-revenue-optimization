# AdStream Revenue Optimization Platform
## Load and Performance Test Report

**Tool:** Locust  
**System under test:** FastAPI optimization service  
**Prepared by:** Cherwin N  
**Test date:** 20 August 2026  
**Status:** Complete after inserting final Locust metrics

> Important: Replace every `<ENTER ...>` field with the value shown in your Locust Statistics page. Do not submit invented numbers.

## 1. Executive Summary

This test evaluates whether the AdStream API remains stable and responsive when multiple virtual publisher clients access health and advertisement-placement endpoints concurrently. The workload represents routine availability checks and a higher proportion of optimization requests. The report measures throughput, response latency, percentile behaviour, failures and the operational effect of Redis and the Gemini integration.

The platform will be considered technically acceptable when it sustains the target user load, maintains the agreed failure-rate threshold and provides predictable p95 response time without exhausting application or dependency resources.

## 2. Test Objectives

- Confirm that `GET /health` remains available under concurrent traffic.
- Measure `POST /optimize-placement` performance under realistic weighted load.
- Calculate total throughput and endpoint-level requests per second.
- Measure average, median, p95, p99 and maximum response times.
- Identify HTTP, validation, timeout and dependency failures.
- Observe whether caching reduces repeated request latency.
- Establish a baseline for future releases and regression testing.

## 3. Scope

### Included

- FastAPI request routing and Pydantic validation.
- Rule-based placement recommendation.
- Redis lookup and response caching.
- Gemini explanation when enabled and available.
- Kafka event publication and ClickHouse integration configured by the application.

### Excluded

- Public internet/CDN performance.
- Browser rendering and frontend performance.
- Production-scale multi-region failover.
- Billing validation for external LLM usage.
- Long-duration soak testing unless separately executed.

## 4. Test Environment

| Item | Test value |
|---|---|
| Operating system | Ubuntu Linux |
| API framework | FastAPI with Uvicorn |
| Runtime | Python virtual environment |
| Infrastructure | Docker Compose |
| Cache | Redis 7 Alpine |
| Streaming | Apache Kafka 3.8.1 |
| Analytics | ClickHouse Server |
| Load generator | Locust |
| API host | `http://localhost:8000` |
| Locust UI | `http://localhost:8089` |
| Hardware | `<ENTER CPU, RAM AND DEVICE>` |
| Git commit tested | `<ENTER COMMIT HASH>` |

Because the load generator and API may run on the same machine, resource competition can affect the result. These values are therefore a development baseline rather than a guarantee of production capacity.

## 5. Workload Model

The Locust user waits between one and three seconds between activities. Health checks have weight 1 and optimization requests have weight 3. This produces approximately 25% health traffic and 75% optimization traffic over a sufficiently long run.

| Scenario | Method | Endpoint | Weight | Expected status |
|---|---|---|---:|---:|
| Service health | GET | `/health` | 1 | 200 |
| Placement optimization | POST | `/optimize-placement` | 3 | 200 |

The optimization payload uses valid values for user, page, scroll depth, engagement time, device and page type. Additional future tests should randomize these fields to evaluate cache-hit and cache-miss behaviour separately.

## 6. Test Configuration

| Parameter | Value |
|---|---:|
| Concurrent users | `<ENTER, for example 100>` |
| Spawn rate | `<ENTER, for example 10 users/second>` |
| Duration | `<ENTER, for example 5 minutes>` |
| Wait time | 1–3 seconds |
| Target host | `http://localhost:8000` |
| LLM mode | `<ENABLED / FALLBACK / DISABLED>` |
| Cache state | `<WARM / COLD / MIXED>` |

## 7. Execution Procedure

Start infrastructure and API:

```bash
sudo docker compose up -d
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

Validate health:

```bash
curl http://localhost:8000/health
```

Start Locust:

```bash
locust -f locustfile.py --host http://localhost:8000
```

Open `http://localhost:8089`, enter the user and spawn values, start the test and allow the configured duration to complete. Export CSV data or capture the Statistics, Charts and Failures screens.

## 8. Acceptance Criteria

The following are recommended development targets and may be adjusted by the organization:

| Metric | Target |
|---|---:|
| Health endpoint success rate | At least 99.9% |
| Overall failure rate | Less than 1% |
| Cached optimization p95 | Less than 500 ms |
| Health endpoint p95 | Less than 200 ms |
| API availability during target load | No outage |
| Unhandled HTTP 5xx errors | 0 preferred |

LLM-enabled uncached traffic should have a separate latency target because external model calls are slower and network-dependent.

## 9. Test Results

Copy the exact values from Locust:

| Request | Count | Failures | Median ms | Average ms | p95 ms | p99 ms | Max ms | RPS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `GET /health` | `<ENTER>` | `<ENTER>` | `<ENTER>` | `<ENTER>` | `<ENTER>` | `<ENTER>` | `<ENTER>` | `<ENTER>` |
| `POST /optimize-placement` | `<ENTER>` | `<ENTER>` | `<ENTER>` | `<ENTER>` | `<ENTER>` | `<ENTER>` | `<ENTER>` | `<ENTER>` |
| **Aggregated** | `<ENTER>` | `<ENTER>` | `<ENTER>` | `<ENTER>` | `<ENTER>` | `<ENTER>` | `<ENTER>` | `<ENTER>` |

### Failure-rate calculation

```text
Failure Rate (%) = (Number of Failed Requests / Total Requests) × 100
```

```text
Failure Rate = (<FAILED> / <TOTAL>) × 100 = <ENTER RESULT>%
```

## 10. Result Analysis

### Throughput

The platform processed `<ENTER TOTAL REQUESTS>` requests at an aggregate rate of `<ENTER RPS>` requests per second. State whether throughput remained stable after all virtual users were active and whether it declined as latency increased.

### Response latency

The aggregated average response time was `<ENTER>` ms and p95 was `<ENTER>` ms. The p95 metric means that 95% of completed requests responded within that time. Compare `/health` with `/optimize-placement`; optimization is expected to be slower because it performs validation, caching, decision logic and optional integrations.

### Reliability

The test recorded `<ENTER FAILED REQUESTS>` failures, producing a failure rate of `<ENTER>%`. List each failure from Locust's Failures tab, including status code, error message, count and likely cause. If failures are zero, state that no request-level failures were observed during this test—not that failures are impossible.

### Cache behaviour

Repeated payloads should create Redis cache hits and lower response time. For a stronger result, compare a cold-cache run immediately after `FLUSHDB` with a warm-cache run using the same payload. `FLUSHDB` must only be performed in a disposable test environment.

### LLM behaviour

Gemini can increase uncached response latency. The deterministic optimization and fallback explanation should keep the endpoint functional when Gemini is unavailable. Report the ratio of `llm_used: true` and fallback responses if captured.

## 11. Observed Bottlenecks

Complete only those supported by evidence:

- External LLM response time may dominate uncached optimization latency.
- A single Uvicorn worker can limit CPU-bound or blocking request concurrency.
- Low Redis cache-hit ratio increases repeated computation and external calls.
- Synchronous Kafka/ClickHouse operations can extend the critical request path.
- Running Locust and the API on the same machine can create CPU contention.
- Container memory pressure can produce latency spikes or restarts.

**Evidence observed in this run:** `<ENTER OBSERVATION FROM CHARTS, LOGS OR METRICS>`

## 12. Performance Improvements

Recommended improvements are:

1. Cache stable recommendations using normalized, versioned keys and an appropriate TTL.
2. Apply strict Gemini connect/read timeouts and retain deterministic fallback output.
3. Move analytics persistence out of the synchronous request path through Kafka consumers.
4. Use multiple production workers and scale horizontally behind a load balancer.
5. Reuse Redis, Kafka and HTTP connections rather than creating them per request.
6. Add rate limiting, backpressure and bounded retry policies.
7. Monitor p95/p99 latency, Redis hit ratio, Kafka lag, errors, CPU and memory.
8. Separate the load generator from the system under test for production-scale validation.

### Retest comparison

| Metric | Before change | After change | Improvement |
|---|---:|---:|---:|
| Average response time | `<ENTER>` | `<ENTER>` | `<ENTER>%` |
| p95 response time | `<ENTER>` | `<ENTER>` | `<ENTER>%` |
| Requests/second | `<ENTER>` | `<ENTER>` | `<ENTER>%` |
| Failure rate | `<ENTER>%` | `<ENTER>%` | `<ENTER percentage points>` |

If no tuning/retest was conducted, label this section **Recommended improvements** and do not claim measured gains.

## 13. Final Conclusion

Use the applicable conclusion after entering your measurements:

> The AdStream API completed the Locust test with `<TOTAL>` requests, `<RPS>` aggregate requests per second, `<P95>` ms p95 latency and `<FAILURE RATE>%` failures. The platform `<met/did not meet>` the defined development acceptance criteria at `<USERS>` concurrent users. The health endpoint remained `<stable/unstable>`, while optimization performance was primarily influenced by `<cache/LLM/worker/dependency factor>`. The results establish a reproducible baseline, and the listed improvements should be validated through a controlled retest before production deployment.

## 14. Evidence

Place the final images in the repository:

```text
screenshots/locust-statistics.png
screenshots/locust-charts.png
screenshots/locust-failures.png
```

Suggested Markdown:

```markdown
![Locust statistics](../screenshots/locust-statistics.png)
```

## 15. Sign-Off

| Role | Name | Status | Date |
|---|---|---|---|
| Prepared by | Cherwin N | `<Completed/Pending>` | 20 August 2026 |
| Technical reviewer | `<ENTER NAME>` | `<Approved/Pending>` | `<ENTER DATE>` |
