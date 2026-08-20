 # Requirements Analysis

## 1. Introduction

This document defines the business, functional, non-functional, technical, privacy, security, and integration requirements for the AdStream Revenue Optimization Platform.

AdStream Analytics serves approximately 500 digital publishers and processes nearly two billion advertisement impressions every month. Therefore, the platform must support high-throughput data processing while maintaining low response latency, reliable operation, and privacy compliance.

## 2. Business Problems

The platform must address the following business problems:

1. Publisher Revenue Per Mille has declined by approximately 25% during the last two years.
2. Cookie deprecation has reduced the effectiveness of traditional user-level advertisement targeting.
3. Privacy regulations restrict the collection and processing of personally identifiable information.
4. The current advertisement viewability rate is approximately 55%, while the industry benchmark is around 70%.
5. Advertisement positions are not sufficiently optimized according to user scrolling and engagement behaviour.
6. Header bidding introduces approximately 800 milliseconds of additional page-load latency.
7. Increased page-load time has contributed to a 12% increase in bounce rate.
8. Publishers require clearer explanations for advertisement placement recommendations.
9. The platform must analyse large volumes of impression, click, scroll, and viewability events.

## 3. Business Objectives

The primary business objectives are:

- Increase advertisement viewability from 55% toward or above 70%.
- Recover and improve publisher RPM.
- Reduce header-bidding and optimization latency.
- Reduce user bounce rate caused by slow advertisement delivery.
- Recommend suitable advertisement positions and formats.
- Support display, video, and native advertisement formats.
- Provide understandable explanations for optimization decisions.
- Replace third-party cookie dependence with contextual and cohort-based signals.
- Give publishers access to reliable revenue and performance analytics.

## 4. Stakeholders

The major stakeholders are:

- Publishers
- Website visitors
- Advertisers
- Ad operations teams
- Revenue managers
- Data analysts
- Machine-learning engineers
- Backend developers
- Platform administrators
- Privacy and compliance teams

## 5. Functional Requirements

### 5.1 Engagement Data Collection

The system shall collect privacy-compliant engagement signals, including:

- User or anonymous session identifier
- Page identifier
- Page category
- Scroll depth
- Time spent on the page
- Device type
- Advertisement position
- Advertisement format
- Impression event
- Click event
- Viewability event
- Estimated and actual RPM

### 5.2 Advertisement Optimization

The system shall:

- Analyse scrolling and engagement behaviour.
- Predict advertisement viewability.
- Estimate RPM for possible advertisement placements.
- Recommend an appropriate advertisement position.
- Recommend an appropriate advertisement format.
- Avoid intrusive or policy-violating placements.
- Return a fallback recommendation if an external service fails.

### 5.3 LLM Integration

The LLM integration shall:

- Generate a short explanation for the selected advertisement placement.
- Use only privacy-safe and approved contextual information.
- Avoid receiving directly identifiable user information.
- Return a structured, machine-readable response.
- Support timeout and fallback handling.
- Prevent unsafe or unrelated responses.

### 5.4 LangChain Agent Requirements

LangChain Agents shall:

- Coordinate calls to the optimization engine, Redis cache, analytics service, and LLM.
- Limit tool access to approved services.
- Apply clear tool descriptions and execution boundaries.
- Prevent unrestricted autonomous actions.
- Record tool execution results for auditing.
- Return a deterministic fallback result when an agent operation fails.

### 5.5 Redis Context Cache Requirements

Redis shall:
[8/20/26 3:32 AM] Cherwin N: - Store recent optimization results.
- Store reusable privacy-safe context.
- Reduce repeated LLM and optimization calls.
- Use a time-to-live value for cached records.
- Generate cache keys without exposing personal information.
- Return cached responses when a valid entry exists.
- Fall back to normal processing if Redis becomes unavailable.

### 5.6 Structured Output Requirements

Every optimization response shall follow a predefined schema containing:

- Recommended advertisement position
- Recommended advertisement format
- Predicted viewability
- Estimated RPM
- Explanation
- Response source
- Whether the LLM was used
- Processing latency

The system shall reject or repair responses that do not conform to the schema.

### 5.7 Guardrails AI Requirements

Guardrails AI shall:

- Validate the structure of the LLM response.
- Reject missing or invalid fields.
- Ensure numerical values remain within accepted ranges.
- Detect unsafe or irrelevant content.
- Prevent sensitive information from appearing in the output.
- Enforce approved advertisement formats and positions.
- Trigger fallback output if validation fails.

### 5.8 Temporal Workflow Requirements

Temporal shall:

- Manage long-running and multi-step workflows.
- Retry temporary service failures.
- Apply timeouts to LLM and external-service calls.
- Preserve workflow state during service restarts.
- Prevent duplicate event processing.
- Support failure recovery without restarting the entire operation.
- Maintain workflow history for debugging and auditing.

### 5.9 Event and Analytics Requirements

The system shall:

- Publish impression, click, scroll, viewability, and optimization events to Kafka.
- Store analytical events in ClickHouse.
- Support historical RPM and viewability analysis.
- Provide publisher-level performance information.
- Record optimization latency and LLM usage.
- Support dashboard filters based on publisher, date, position, format, and page category.

## 6. Non-Functional Requirements

### 6.1 Performance

- Cached optimization requests should normally complete in less than 100 milliseconds.
- Non-cached requests should minimise dependence on the LLM.
- LLM calls must use strict timeouts.
- Event publishing should not block the primary API response.
- The system should reduce the existing 800-millisecond latency overhead.

### 6.2 Scalability

- The architecture must support 500 publishers.
- It must be capable of processing traffic generated by approximately two billion monthly impressions.
- API services must support horizontal scaling.
- Kafka and ClickHouse must support high-volume event processing.
- Redis must support distributed caching when traffic increases.

### 6.3 Availability and Reliability

- Failure of the LLM must not stop advertisement optimization.
- Failure of Redis must not make the API unavailable.
- Failed workflows must be retried through Temporal.
- Duplicate event processing must be controlled.
- Health-check endpoints must be available for essential services.

### 6.4 Security

- All external communication must use HTTPS or TLS.
- API keys and passwords must be stored in environment variables or secret-management services.
- Secrets must never be committed to GitHub.
- API requests must be authenticated and authorized.
- Rate limiting must protect public endpoints.
- Input data must be validated before processing.
- Security-relevant actions must be recorded in audit logs.

### 6.5 Privacy and Compliance

- Personally identifiable information must not be sent to the LLM.
- The platform should use contextual and cohort-based targeting.
- User identifiers should be anonymized or pseudonymized.
- Data collection should follow consent requirements.
- Data retention periods must be documented.
- The architecture should support GDPR and CCPA requirements.
- Users must be able to exercise deletion and data-access rights when applicable.

### 6.6 Observability
[8/20/26 3:32 AM] Cherwin N: - OpenTelemetry shall collect distributed traces and metrics.
- Grafana shall display operational dashboards.
- The system shall monitor API latency, error rate, cache hit rate, LLM latency, LLM failure rate, Kafka publishing errors, and workflow retry count.
- Logs must include correlation identifiers.
- Logs must not expose secrets or personal information.

### 6.7 Maintainability

- Services should have clear responsibilities.
- API contracts should be documented.
- Components should be independently testable.
- Configuration should be separated from application code.
- Architecture and operational documentation should be maintained.

## 7. Technical Constraints

- Third-party cookies are being deprecated.
- Privacy regulations limit individual-level tracking.
- LLM responses can be slow, inconsistent, or unavailable.
- Advertisement decisions require low latency.
- The existing header-bidding wrapper and ad server must continue operating.
- The system must handle very high event volume.
- Recommendations must support existing advertisement formats.
- The design must provide deterministic fallback logic.

## 8. Acceptance Criteria

The task will be considered complete when:

- Business and technical requirements are documented.
- Functional and non-functional requirements are clearly separated.
- Privacy, security, performance, and scalability constraints are included.
- The initial architecture diagram is available.
- LangChain Agents, Redis context caching, Structured Output, Guardrails AI, and Temporal are included.
- Design decisions and assumptions are documented.
- The completed files are uploaded to the GitHub repository.