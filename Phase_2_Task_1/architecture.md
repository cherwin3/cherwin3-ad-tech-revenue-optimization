# Initial Architecture Design

## 1. Architecture Objective

The architecture is designed to provide low-latency and privacy-compliant advertisement placement recommendations while improving publisher RPM and advertisement viewability.

The system separates real-time optimization from asynchronous analytics so that event processing and LLM failures do not delay advertisement delivery.

## 2. Main Components

### Publisher Website

The publisher website displays the article content and advertisement slots. It collects consent-approved engagement signals such as scroll depth, time spent on the page, page category, and device type.

### Header Bidding Wrapper

The header bidding wrapper requests bids from multiple advertising partners. It forwards eligible bids to the ad server while following strict latency limits.

### Ad Server and Targeting Rules Engine

The ad server selects the advertisement creative. The targeting rules engine applies publisher restrictions, format compatibility, privacy rules, campaign settings, and frequency limits.

### FastAPI Backend

FastAPI exposes the real-time optimization API. It validates incoming requests, checks the cache, calls the optimization workflow, and returns structured recommendations.

### LangChain Agents

LangChain Agents coordinate approved tools such as the prediction engine, Redis cache, analytics lookup, and LLM explanation service. Agent permissions are restricted so that they cannot call unauthorized systems or expose sensitive data.

### Optimization and Prediction Engine

The optimization engine analyses page context and engagement signals. It predicts viewability and estimated RPM before recommending an advertisement position and format.

The deterministic optimization result remains available even if the LLM fails.

### Redis Context Cache

Redis stores recent optimization results and reusable contextual information. Cached results reduce repeated model calls, improve response time, and control LLM cost.

All cache keys are generated from privacy-safe information and include a time-to-live value.

### LLM Explanation Service

The LLM generates a brief explanation for the optimization recommendation. It does not directly select or serve advertisements and does not receive personally identifiable information.

### Structured Output

The LLM response must follow a predefined JSON schema. Structured Output ensures that the response can be safely consumed by FastAPI and the publisher dashboard.

### Guardrails AI

Guardrails AI validates the LLM response. It checks required fields, approved values, numeric ranges, privacy restrictions, and content relevance. Invalid output activates a deterministic fallback explanation.

### Temporal

Temporal manages durable multi-step workflows. It handles retry policies, service timeouts, workflow state, error recovery, and duplicate prevention.

### Apache Kafka

Kafka transports impression, click, scroll, viewability, and optimization events. Event publishing is asynchronous and does not block the real-time API response.

### ClickHouse

ClickHouse stores large volumes of advertisement events and supports fast analytical queries for RPM, viewability, latency, formats, and positions.

### PostgreSQL

PostgreSQL stores transactional information such as publisher configuration, user roles, campaign metadata, targeting rules, and system settings.

### React Publisher Dashboard

The dashboard displays revenue, RPM, viewability, impression, click, cache, latency, and LLM performance metrics.

### OpenTelemetry and Grafana

OpenTelemetry collects logs, traces, and metrics across services. Grafana displays dashboards and alerts for API latency, errors, cache performance, workflow retries, Kafka health, and LLM failures.

## 3. Real-Time Request Flow
[8/20/26 3:32 AM] Cherwin N: 1. A user visits a publisher website.
2. The website collects privacy-approved contextual and engagement data.
3. The header bidding wrapper requests advertisement bids.
4. The publisher website sends an optimization request to FastAPI.
5. FastAPI validates the input.
6. The service checks Redis for a valid cached result.
7. If a cached result exists, it is returned immediately.
8. If no cached result exists, Temporal starts or resumes the optimization workflow.
9. LangChain Agents coordinate the prediction engine and approved contextual tools.
10. The optimization engine predicts viewability and estimated RPM.
11. The LLM generates a short explanation when available.
12. Structured Output converts the response into the required schema.
13. Guardrails AI validates the response.
14. The validated result is stored in Redis.
15. FastAPI returns the recommendation to the publisher website.
16. The ad server applies targeting rules and selects the advertisement.
17. Kafka receives the optimization and engagement events.
18. ClickHouse stores the events for analytics.
19. The React dashboard displays the processed information.

## 4. Failure-Handling Flow

- If Redis is unavailable, the request continues without caching.
- If the LLM times out, the deterministic explanation is returned.
- If Guardrails AI rejects the LLM output, a safe fallback response is used.
- If Kafka is temporarily unavailable, Temporal retries the event workflow.
- If ClickHouse is temporarily unavailable, events remain available for later processing.
- If a workflow service restarts, Temporal restores the workflow state.

## 5. Security and Privacy Flow

- Incoming API traffic uses HTTPS.
- API keys are stored in secure environment variables.
- Input data is validated through Pydantic models.
- Personal information is removed before LLM processing.
- Contextual and cohort-based signals replace third-party cookie dependence.
- Role-based access controls protect the dashboard.
- Audit logs record administrative and optimization actions.
- Guardrails prevent sensitive content from appearing in the response.

## 6. Architecture Diagram Flow

The architecture diagram should represent the following components:

```text
User
  |
Publisher Website
  |
Header Bidding Wrapper
  |
Ad Server and Targeting Rules
  |
FastAPI Backend
  |
Redis Context Cache
  |
Temporal Workflow
  |
LangChain Agents
  |
Optimization and Prediction Engine
  |
LLM Explanation Service
  |
Structured Output and Guardrails AI
  |
Validated Recommendation
  |
Ad Display

Engagement Events
  |
Apache Kafka
  |
ClickHouse Analytics
  |
React Publisher Dashboard

All services
  |
OpenTelemetry
  |
Grafana