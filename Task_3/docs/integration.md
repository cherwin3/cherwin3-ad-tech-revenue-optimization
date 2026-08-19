# Integration and Data Flow Documentation

## 1. Introduction

This document explains the integration of FastAPI, Node.js, Redis, Gemini, Apache Kafka, and ClickHouse in the AdStream Revenue Optimization Platform.

The system analyzes user behaviour and recommends an advertisement position that can improve viewability and publisher RPM.

## 2. Integrated Components

| Component | Responsibility |
|---|---|
| Node.js | Receives ad-placement requests and forwards them to FastAPI |
| FastAPI | Validates requests and controls the optimization workflow |
| Pydantic | Validates user behaviour data |
| Redis | Caches optimization results |
| Optimizer | Selects ad position, format, viewability, and RPM |
| Gemini | Generates a contextual explanation |
| Kafka Producer | Publishes processed advertisement events |
| Kafka Consumer | Receives events from Kafka |
| ClickHouse | Stores events for analytics |
| Docker Compose | Runs Redis, Kafka, and ClickHouse |
| Pytest | Tests normal and edge-case behaviour |

## 3. Complete Architecture

```text
Client
  │
  ▼
Node.js Service
  │
  ▼
FastAPI
  │
  ├──► Pydantic Validation
  │
  ├──► Redis Cache Check
  │       │
  │       ├── Cache hit
  │       │      └──► Return cached recommendation
  │       │
  │       └── Cache miss
  │              └──► Run optimization
  │
  ├──► Advertisement Optimizer
  │
  ├──► Gemini LLM
  │
  ├──► Save result in Redis
  │
  └──► Kafka Producer
            │
            ▼
       Kafka: ad-events
            │
            ▼
       Kafka Consumer
            │
            ▼
        ClickHouse
```

## 4. Request Processing Flow

### Step 1: Node.js receives the request

The client sends behaviour data to:

```text
POST http://localhost:3000/ad-placement
```

Node.js forwards the request to:

```text
POST http://localhost:8000/optimize-placement
```

### Step 2: FastAPI validates the request

Pydantic validates:

- User ID
- Page ID
- Scroll depth between 0 and 100
- Time on page greater than or equal to zero
- Supported device type
- Supported page type

Invalid input returns:

```text
HTTP 422 Unprocessable Entity
```

### Step 3: Redis cache check

FastAPI generates a cache key from the request.

If the result exists:

```json
{
  "source": "redis_cache"
}
```

If the result does not exist, FastAPI runs the optimizer.

### Step 4: Advertisement optimization

The optimizer selects an advertisement placement using scroll depth:

| Scroll depth | Position | Format |
|---|---|---|
| Below 20% | `top_content` | Display |
| 20%–49% | `upper_middle` | Native |
| 50%–79% | `middle_content` | Native |
| 80%–100% | `bottom_content` | Display |

Time on page and device type are used to adjust predicted viewability.

Estimated RPM is calculated using the predicted viewability.

### Step 5: Gemini explanation

Gemini receives the recommendation and creates a short explanation.

If Gemini succeeds:

```json
{
  "llm_used": true
}
```

If Gemini is unavailable, the optimizer explanation is returned:

```json
{
  "llm_used": false
}
```

The API continues working even when Gemini fails.

### Step 6: Redis storage

The final response is saved in Redis with an expiry time.

When the same request is submitted again, Redis returns the cached result without repeating the optimization and Gemini call.

### Step 7: Kafka event publishing

FastAPI publishes the processed result to the Kafka topic:

```text
ad-events
```

The event contains:

```json
{
  "user_id": "U105",
  "page_id": "P505",
  "recommended_position": "middle_content",
  "ad_format": "native",
  "predicted_viewability": 0.94,
  "estimated_rpm": 5.76,
  "source": "optimization_engine",
  "llm_used": true,
  "latency_ms": 120.5,
  "timestamp": "2026-08-19T15:00:00+00:00"
}
```

### Step 8: Kafka consumption

The Kafka consumer listens to the `ad-events` topic.

After receiving an event, it converts the timestamp and prepares the data for ClickHouse.

### Step 9: ClickHouse storage

The consumer inserts the event into:

```text
adstream.ad_events
```

The table stores:

- User ID
- Page ID
- Recommended position
- Advertisement format
- Predicted viewability
- Estimated RPM
- Response source
- LLM usage
- Latency
- Event timestamp

## 5. Starting the Infrastructure

Start Redis, Kafka, and ClickHouse:

```bash
docker compose up -d
```

Verify:

```bash
docker compose ps
```

Expected containers:

```text
redis-adstream
kafka-adstream
clickhouse-adstream
```

## 6. Starting FastAPI

```bash
python -m uvicorn backend.app.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

Expected health result:

```json
{
  "api": "healthy",
  "redis": "connected"
}
```

## 7. Starting the Kafka Consumer

```bash
python -m backend.app.consumer.kafka_consumer
```

Expected:

```text
Connected to ClickHouse successfully
Connected to Kafka successfully
Kafka consumer started. Waiting for ad events...
```

## 8. Starting Node.js

```bash
cd node-service
npm install
npm start
```

Expected:

```text
Node.js service running at http://localhost:3000
```

## 9. API Validation

Example request:

```json
{
  "user_id": "U105",
  "page_id": "P505",
  "scroll_depth": 72,
  "time_on_page": 50,
  "device_type": "mobile",
  "page_type": "technology"
}
```

Example response:

```json
{
  "user_id": "U105",
  "page_id": "P505",
  "recommended_position": "middle_content",
  "ad_format": "native",
  "predicted_viewability": 0.94,
  "estimated_rpm": 5.76,
  "reason": "A native advertisement in the middle content aligns with the user's active reading behaviour.",
  "source": "optimization_engine",
  "llm_used": true,
  "latency_ms": 120.5
}
```

## 10. Redis Validation

Verify Redis:

```bash
docker exec -it redis-adstream redis-cli ping
```

Expected:

```text
PONG
```

The first API request should contain:

```json
{
  "source": "optimization_engine"
}
```

The second identical request should contain:

```json
{
  "source": "redis_cache"
}
```

## 11. Kafka Validation

Producer output:

```text
Kafka event published successfully:
topic=ad-events, partition=0, offset=0
```

Consumer output:

```text
Kafka event received
Event stored successfully in ClickHouse
```

## 12. ClickHouse Validation

Run:

```bash
docker exec -it clickhouse-adstream clickhouse-client \
--user adstream \
--password adstream123 \
--query "SELECT * FROM adstream.ad_events"
```

A stored event confirms:

```text
FastAPI → Kafka → Consumer → ClickHouse
```

## 13. Failure Handling

| Failure | System behaviour |
|---|---|
| Gemini unavailable | Uses optimizer explanation |
| Redis unavailable | Processes request without caching |
| Kafka unavailable | Returns API response and logs Kafka error |
| Invalid input | Returns HTTP 422 |
| ClickHouse unavailable | Consumer reports insertion error |
| Empty Gemini response | Uses optimizer explanation |

## 14. Integration Validation Result

The following data flow was validated:

```text
Node.js → FastAPI → Redis
FastAPI → Optimizer → Gemini
FastAPI → Kafka Producer
Kafka Producer → Kafka Consumer
Kafka Consumer → ClickHouse
```

The platform successfully integrates API processing, artificial intelligence, caching, event streaming, and analytical storage.